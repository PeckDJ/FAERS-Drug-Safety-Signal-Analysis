"""Disproportionality analysis for FAERS signal detection.

For each adverse-event term reported alongside the target drug, we build the
classic 2x2 contingency table:

                          event e      not event e
    target drug      |       a       |      b      |
    all other drugs  |       c       |      d      |

and compute the two measures pharmacovigilance teams use to flag a potential
safety signal:

  PRR (Proportional Reporting Ratio) = [a/(a+b)] / [c/(c+d)]
  ROR (Reporting Odds Ratio)         = (a*d) / (b*c)

A pair is flagged as a signal using the widely cited Evans et al. (2001)
criteria: PRR >= 2, chi-squared (Yates) >= 4, and a >= 3.

References:
  Evans SJW, Waller PC, Davis S. Use of proportional reporting ratios (PRRs)
  for signal generation from spontaneous adverse drug reaction reports.
  Pharmacoepidemiol Drug Saf. 2001;10(6):483-486.
"""

import numpy as np
import pandas as pd

from .config import CHI2_THRESHOLD, MIN_CASES, PRR_THRESHOLD


def compute_signals(report_event: pd.DataFrame) -> pd.DataFrame:
    """Compute PRR/ROR and signal flags for every event seen with the drug.

    Parameters
    ----------
    report_event : DataFrame with columns [primaryid, event_pt, drug_flag]
        One row per unique (report, adverse-event) pair.

    Returns
    -------
    DataFrame ranked by PRR, one row per adverse-event term.
    """
    df = report_event.drop_duplicates(["primaryid", "event_pt"])

    total_reports = df["primaryid"].nunique()
    drug_reports = df.loc[df["drug_flag"], "primaryid"].nunique()

    # Counts per event term, split by whether the target drug was present.
    grp = (
        df.groupby("event_pt")["drug_flag"]
        .agg(a="sum", n_event="count")
        .reset_index()
    )
    grp["a"] = grp["a"].astype(int)          # drug AND event
    grp["c"] = grp["n_event"] - grp["a"]     # not drug AND event
    grp["b"] = drug_reports - grp["a"]       # drug AND not event
    grp["d"] = total_reports - grp["a"] - grp["b"] - grp["c"]  # neither

    # Only analyse events with at least MIN_CASES co-reports.
    grp = grp[grp["a"] >= MIN_CASES].copy()

    a, b, c, d = (grp["a"].astype("float64"), grp["b"].astype("float64"), grp["c"].astype("float64"), grp["d"].astype("float64"))

    # --- PRR with 95% CI ---
    prr = (a / (a + b)) / (c / (c + d))
    se_ln_prr = np.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
    grp["prr"] = prr
    grp["prr_ci_low"] = np.exp(np.log(prr) - 1.96 * se_ln_prr)
    grp["prr_ci_high"] = np.exp(np.log(prr) + 1.96 * se_ln_prr)

    # --- ROR with 95% CI ---
    ror = (a * d) / (b * c)
    se_ln_ror = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    grp["ror"] = ror
    grp["ror_ci_low"] = np.exp(np.log(ror) - 1.96 * se_ln_ror)
    grp["ror_ci_high"] = np.exp(np.log(ror) + 1.96 * se_ln_ror)

    # --- Chi-squared with Yates continuity correction ---
    n = a + b + c + d
    expected_a = (a + b) * (a + c) / n
    grp["chi2"] = (
        n * (np.abs(a * d - b * c) - n / 2) ** 2
        / ((a + b) * (c + d) * (a + c) * (b + d))
    )
    # Guard against the negative-corrected case for tiny cells.
    grp.loc[(np.abs(a * d - b * c) - n / 2) < 0, "chi2"] = 0.0

    # --- Signal flag (Evans 2001) ---
    grp["is_signal"] = (
        (grp["prr"] >= PRR_THRESHOLD)
        & (grp["chi2"] >= CHI2_THRESHOLD)
        & (grp["a"] >= MIN_CASES)
    )

    cols = [
        "event_pt", "a", "b", "c", "d",
        "prr", "prr_ci_low", "prr_ci_high",
        "ror", "ror_ci_low", "ror_ci_high",
        "chi2", "is_signal",
    ]
    return grp[cols].sort_values("prr", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    from .load_faers import build_report_event_table, load_all

    tidy = build_report_event_table(load_all())
    signals = compute_signals(tidy)
    print(signals.head(20).to_string(index=False))
    print(f"\nFlagged signals: {int(signals['is_signal'].sum())} "
          f"of {len(signals)} event terms")
