"""Visualisations for the FAERS signal analysis.

Produces the figures referenced in the README and the RWE memo:
  1. Top adverse events by report count (the "headline" chart).
  2. A PRR vs. report-count scatter that makes flagged signals pop out.
"""

import matplotlib.pyplot as plt
import pandas as pd

from .config import FIGURES, TARGET_DRUG_LABEL


def plot_top_events(signals: pd.DataFrame, top_n: int = 15, save: bool = True):
    """Horizontal bar chart of the most-reported adverse events."""
    top = signals.sort_values("a", ascending=False).head(top_n).iloc[::-1]
    colors = ["#c0392b" if s else "#7f8c8d" for s in top["is_signal"]]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(top["event_pt"].str.title(), top["a"], color=colors)
    ax.set_xlabel("Co-reported cases (a)")
    ax.set_title(f"Top reported adverse events — {TARGET_DRUG_LABEL}")
    ax.spines[["top", "right"]].set_visible(False)
    handles = [
        plt.Rectangle((0, 0), 1, 1, color="#c0392b"),
        plt.Rectangle((0, 0), 1, 1, color="#7f8c8d"),
    ]
    ax.legend(handles, ["Flagged signal", "Not flagged"], frameon=False)
    fig.tight_layout()
    if save:
        out = FIGURES / "top_adverse_events.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        print(f"saved {out}")
    return fig


def plot_signal_scatter(signals: pd.DataFrame, save: bool = True):
    """PRR vs. case count; flagged signals highlighted."""
    fig, ax = plt.subplots(figsize=(9, 6))
    sig = signals[signals["is_signal"]]
    non = signals[~signals["is_signal"]]
    ax.scatter(non["a"], non["prr"], s=20, c="#bdc3c7", label="Not flagged")
    ax.scatter(sig["a"], sig["prr"], s=35, c="#c0392b", label="Flagged signal")
    ax.axhline(2.0, ls="--", c="#34495e", lw=1)
    ax.set_xscale("log")
    ax.set_xlabel("Co-reported cases (a, log scale)")
    ax.set_ylabel("PRR")
    ax.set_title(f"Disproportionality signals — {TARGET_DRUG_LABEL}")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    if save:
        out = FIGURES / "signal_scatter.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        print(f"saved {out}")
    return fig


if __name__ == "__main__":
    from .disproportionality import compute_signals
    from .load_faers import build_report_event_table, load_all

    signals = compute_signals(build_report_event_table(load_all()))
    plot_top_events(signals)
    plot_signal_scatter(signals)
