"""Load FAERS ASCII tables into tidy pandas DataFrames.

The three tables we need for disproportionality analysis:
  DEMO  -- one row per report (demographics, used for de-duplication)
  DRUG  -- one or more rows per report (each drug mentioned, with a role code)
  REAC  -- one or more rows per report (each adverse-event MedDRA term)

All FAERS ASCII files are '$'-delimited. Column names vary slightly across
quarters, so we normalise to lowercase and select the fields we rely on.
"""

from pathlib import Path

import pandas as pd

from .config import DATA_RAW, QUARTERS, SUSPECT_ROLES


def _read_dollar(path: Path) -> pd.DataFrame:
    """Read one '$'-delimited FAERS table with forgiving settings."""
    df = pd.read_csv(
        path,
        sep="$",
        dtype=str,
        encoding="latin-1",
        on_bad_lines="skip",
        low_memory=False,
    )
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def _find(quarter_dir: Path, prefix: str) -> Path | None:
    """Find a table file by prefix (e.g. 'DEMO') regardless of the YYQQ suffix."""
    matches = sorted(quarter_dir.glob(f"{prefix}*.txt"))
    return matches[0] if matches else None


def load_quarter(year: int, q: int) -> dict[str, pd.DataFrame]:
    """Load DEMO/DRUG/REAC for a single quarter."""
    qdir = DATA_RAW / f"{year}q{q}"
    out: dict[str, pd.DataFrame] = {}
    for key, prefix in (("demo", "DEMO"), ("drug", "DRUG"), ("reac", "REAC")):
        path = _find(qdir, prefix)
        if path is None:
            raise FileNotFoundError(
                f"Missing {prefix} table for {year}Q{q} in {qdir}. "
                f"Run `python -m src.download_faers` first."
            )
        out[key] = _read_dollar(path)
    return out


def load_all() -> dict[str, pd.DataFrame]:
    """Load and concatenate every quarter listed in config.QUARTERS."""
    demo, drug, reac = [], [], []
    for year, q in QUARTERS:
        tables = load_quarter(year, q)
        demo.append(tables["demo"])
        drug.append(tables["drug"])
        reac.append(tables["reac"])
    return {
        "demo": pd.concat(demo, ignore_index=True),
        "drug": pd.concat(drug, ignore_index=True),
        "reac": pd.concat(reac, ignore_index=True),
    }


def deduplicate(demo: pd.DataFrame) -> pd.DataFrame:
    """Keep the latest report version per case.

    FAERS may contain several versions of the same case across quarters. The
    convention is to keep, for each `caseid`, the row with the highest
    `primaryid` (the most recent version).
    """
    d = demo.copy()
    d["primaryid_num"] = pd.to_numeric(d["primaryid"], errors="coerce")
    d = d.sort_values("primaryid_num").drop_duplicates("caseid", keep="last")
    return d.drop(columns="primaryid_num")


def build_report_event_table(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Return one tidy frame: (primaryid, drug_flag, event_pt).

    Each row is a unique (report, adverse-event) pair, with a boolean flag for
    whether the target drug was a suspect drug in that report. This is the
    input to the disproportionality calculation.
    """
    from .config import TARGET_DRUGS

    demo = deduplicate(tables["demo"])
    valid_ids = set(demo["primaryid"])

    # --- reactions: one preferred term (pt) per row ---
    reac = tables["reac"].copy()
    reac = reac[reac["primaryid"].isin(valid_ids)]
    reac = reac[["primaryid", "pt"]].dropna()
    reac["pt"] = reac["pt"].str.strip().str.lower()
    reac = reac.drop_duplicates()

    # --- drugs: flag reports where the target drug is a suspect ---
    drug = tables["drug"].copy()
    drug = drug[drug["primaryid"].isin(valid_ids)]
    if "role_cod" in drug.columns:
        drug = drug[drug["role_cod"].isin(SUSPECT_ROLES)]

    name_cols = [c for c in ("drugname", "prod_ai") if c in drug.columns]
    pattern = "|".join(TARGET_DRUGS)
    mask = pd.Series(False, index=drug.index)
    for col in name_cols:
        mask |= drug[col].fillna("").str.contains(pattern, case=False, regex=True)
    target_ids = set(drug.loc[mask, "primaryid"])

    reac["drug_flag"] = reac["primaryid"].isin(target_ids)
    return reac.rename(columns={"pt": "event_pt"})


if __name__ == "__main__":
    tabs = load_all()
    tidy = build_report_event_table(tabs)
    n_reports = tidy["primaryid"].nunique()
    n_target = tidy.loc[tidy["drug_flag"], "primaryid"].nunique()
    print(f"Unique reports: {n_reports:,}")
    print(f"Reports with target drug as suspect: {n_target:,}")
    print(f"Distinct adverse-event terms: {tidy['event_pt'].nunique():,}")
