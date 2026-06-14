"""Run the full FAERS signal-analysis pipeline end to end.

    python run_analysis.py

Steps:
  1. Load the quarters listed in src/config.py (download them first).
  2. De-duplicate and build the report-event table.
  3. Compute PRR/ROR disproportionality and flag signals.
  4. Save a ranked results table + the two README figures.
"""

import sys

from src.config import DATA_PROCESSED, TARGET_DRUG_LABEL
from src.disproportionality import compute_signals
from src.load_faers import build_report_event_table, load_all
from src.visualize import plot_signal_scatter, plot_top_events


def main() -> int:
    print(f"Target: {TARGET_DRUG_LABEL}")
    print("Loading FAERS quarters ...")
    tidy = build_report_event_table(load_all())

    n_reports = tidy["primaryid"].nunique()
    n_target = tidy.loc[tidy["drug_flag"], "primaryid"].nunique()
    print(f"  unique reports: {n_reports:,}")
    print(f"  reports with target drug (suspect): {n_target:,}")

    print("Computing disproportionality signals ...")
    signals = compute_signals(tidy)

    out_csv = DATA_PROCESSED / "signals.csv"
    signals.to_csv(out_csv, index=False)
    print(f"  wrote {out_csv}")

    n_sig = int(signals["is_signal"].sum())
    print(f"  flagged {n_sig} signals across {len(signals)} event terms\n")
    print("Top 10 by PRR:")
    print(
        signals.head(10)[
            ["event_pt", "a", "prr", "prr_ci_low", "ror", "chi2", "is_signal"]
        ].to_string(index=False)
    )

    print("\nMaking figures ...")
    plot_top_events(signals)
    plot_signal_scatter(signals)
    print("\nDone. See data/processed/signals.csv and figures/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
