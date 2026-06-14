# Real-World Evidence Memo — Safety Signal Review

**To:** Drug Safety / Pharmacovigilance review committee
**From:** [Your name]
**Re:** Potential safety signal for [DRUG / DRUG CLASS] — [ADVERSE EVENT]
**Data source:** FDA FAERS, quarters [e.g. 2024 Q1–Q4]
**Date:** [date]

---

## Summary (read this if nothing else)

A disproportionality screen of FAERS spontaneous reports flagged
**[adverse event]** as reported more often than expected in association with
**[drug]**. The signal met all three standard screening criteria
(PRR ≥ 2, chi² ≥ 4, ≥ 3 cases). This memo summarises the finding and
recommends [a next step — e.g. a focused review of the cases / no action
because the event is already on the label].

> Keep this section to 3–4 sentences. A reviewer should understand the
> takeaway without reading further.

## The signal in numbers

| Metric | Value | Screening threshold |
|---|---|---|
| Co-reported cases (a) | [a] | ≥ 3 |
| PRR (95% CI) | [PRR] ([low]–[high]) | ≥ 2 |
| ROR (95% CI) | [ROR] ([low]–[high]) | CI lower bound > 1 |
| Chi-squared (Yates) | [chi²] | ≥ 4 |

## What this means

In plain terms: among all FAERS reports in this period, [adverse event] was
reported [PRR]× more frequently for [drug] than for the rest of the database.
That is a **statistical signal**, not proof that the drug causes the event.

## Context that matters

- **Is it already known?** [Is this event on the current label / in the
  prescribing information? If so, the signal is expected and reassuring that
  the method works. If not, it's more interesting.]
- **Biological plausibility:** [One or two sentences on mechanism, if any.]
- **Confounding / bias:** [Indication bias? Notoriety/stimulated reporting?
  Channelling? Note the most likely alternative explanation.]

## Limitations

FAERS captures spontaneous reports only — there is no denominator of treated
patients, reporting is voluntary and incomplete, and duplicate or low-quality
reports occur. Disproportionality cannot establish causation or incidence. The
appropriate output of this analysis is a prioritised hypothesis.

## Recommendation

- [ ] [e.g. Pull and clinically review the underlying case narratives]
- [ ] [e.g. Cross-check against the current label and recent literature]
- [ ] [e.g. No further action — known, labelled, expected]

---

*Prepared from publicly available FDA FAERS data using PRR/ROR
disproportionality analysis (Evans et al., 2001). Code and full ranked results
in this repository.*
