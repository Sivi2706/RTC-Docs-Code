RTC 2027 Student 3K — corrected avionics MDR and focused scoping review (4 November 2026)

Source files:
- RTC_2027_3K_Pico_Electronics_MDR_Corrected.tex (embedded BibTeX via filecontents*)
- RTC_2027_Pico_MDR_refs.bib (extracted bibliography, optional separate copy)
- RTC_2027_3km_Avionics_SLR_Corrected.tex
- RTC_2027_3km_Avionics_SLR_Corrected.bib

Build each LaTeX document: pdfLaTeX → Biber → pdfLaTeX twice.
The main MDR .tex embeds its own .bib. The SLR requires the separately named .bib.

Changes to MDR: three recovery/flight IMUs; provisional baseline high-g channel; 44-byte logging records / 47.52 MB per 90 min; 32-byte FRAM checkpoint; sea-ingress and Li-ion protections; 15 FMEA items; mission-to-requirement link; explicit outcome tiers; illustrative unvalidated altitude/time graphic; proposed Gantt; GPS mounting and demo plan; revised partial budget and mass.

Changes to scoping review: broadened 3 km to include the adjacent 10,000-foot IREC design stratum; documented scoring weights; separate competition-grey-literature examples; architecture comparison PGFPlots; reconciled storage figure with corrected MDR.

No actual Pioneer-10K trajectory was available. The mission graph is illustrative and is NOT a simulation outcome. No verification tests are claimed as completed. The battery, BOM and mass figures are preliminary. Recovery release mechanism, GPS integration and final sensor qualification are pending team review.

This is an engineering annex plus a rapid scoping evidence review, NOT the competition's final 21-page master MDR nor a completed PRISMA systematic review.
