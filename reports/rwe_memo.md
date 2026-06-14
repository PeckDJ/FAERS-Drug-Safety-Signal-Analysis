# Real-World Evidence Memo — Safety Signal Review

**To:** Drug Safety / Pharmacovigilance review committee
**From:** R. Peck Mingpatumkij
**Re:** Disproportionality signal for rosuvastatin — rhabdomyolysis
**Data source:** FDA FAERS, 2024 Q1–Q4 (1,484,347 unique reports; 4,984 with rosuvastatin as a suspect drug)
**Date:** 14 June 2026

---

## Summary (read this if nothing else)

A disproportionality screen of FAERS spontaneous reports flagged **rhabdomyolysis** as reported markedly more often than expected in association with **rosuvastatin** (PRR 48.3; ROR 51.8; 341 co-reported cases). The signal clears all three standard screening criteria. This is an *expected, label-recognised* statin-class effect rather than a novel safety concern — its strong appearance here primarily confirms that the method surfaces genuine signals. No new regulatory action is indicated; routine monitoring of reporting trends is sufficient.

## The signal in numbers

| Metric | Value | Screening threshold |
|---|---|---|
| Co-reported cases (a) | 341 | >= 3 |
| PRR (95% CI) | 48.3 (43.2–54.0) | >= 2 |
| ROR (95% CI) | 51.8 (46.0–58.2) | CI lower bound > 1 |
| Chi-squared (Yates) | 13,564 | >= 4 |

## What this means

In plain terms: among all FAERS reports in this period, rhabdomyolysis was reported roughly 48 times more frequently in rosuvastatin reports than across the rest of the database. That is a strong **statistical** signal — but it reflects *reporting patterns*, not the rate of rhabdomyolysis in treated patients, and on its own it does not establish that rosuvastatin causes the event.

## Context that matters

- **Is it already known?** Yes. Rhabdomyolysis is a well-characterised, labelled adverse effect of statins, including rosuvastatin. A strong signal here is therefore *expected and reassuring* — it indicates the screen is behaving correctly, and the same analysis flagged the related muscle-toxicity terms (myalgia, myopathy, raised creatine phosphokinase) as well as hepatic enzyme elevations.
- **Biological plausibility:** Statins can cause dose-related skeletal-muscle injury; rhabdomyolysis is the severe end of that spectrum and is mechanistically consistent with the drug class.
- **Confounding / reporting bias:** Rhabdomyolysis is a serious, medically significant event, and serious events are preferentially reported to FAERS. Some inflation of the disproportionality measure relative to milder events is expected for that reason alone. Co-reporting with interacting medications (e.g. certain fibrates or CYP3A4 inhibitors) may also contribute.

## Limitations

FAERS captures spontaneous reports only: there is no denominator of treated patients, reporting is voluntary and incomplete, duplicate and low-quality reports occur, and serious outcomes are over-represented. Disproportionality analysis cannot establish causation or incidence; its appropriate output is a prioritised hypothesis.

## Recommendation

- No new action warranted — the signal is a known, labelled, mechanistically plausible effect and is already managed through existing prescribing guidance.
- Optionally, monitor quarter-over-quarter reporting trends for any unexpected increase that could indicate a shift in product, formulation, or reporting behaviour.
- Optionally, review a sample of the underlying case narratives to characterise co-suspect drugs and contributing factors.

---

*Prepared from publicly available FDA FAERS data using PRR/ROR disproportionality analysis (Evans et al., 2001). Code and full ranked results in this repository.*
