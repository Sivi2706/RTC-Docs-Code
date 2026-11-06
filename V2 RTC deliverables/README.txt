RTC 2027 Student 3K Electronics MDR - Styled Figures + Vibration Payload Flow

Files:
- RTC_2027_3K_Pico_Electronics_MDR_Styled_PayloadFlow.tex (main document)
- RTC_2027_Pico_MDR_refs.bib (IEEE sources, also embedded in .tex via filecontents*)
- RTC_2027_3K_Pico_Electronics_MDR_Styled_PayloadFlow.pdf (compiled preview)

Compile with pdfLaTeX -> Biber -> pdfLaTeX -> pdfLaTeX.
The .tex has an embedded bibliography: it can recreate the .bib itself, or use the included .bib file.
Changes applied from the uploaded figure upgrade patch:
1. Dark Navy terminal/process styling; Teal signals, Amber power/fault emphasis.
2. Replaced mission profile illustration, power-domain architecture, vibration fixture, and Gantt figure.
3. Added full payload process flowchart (fig:payloadflow) and a text cross-reference.
4. Added the required TikZ decorations.pathmorphing library for zigzag and snake cable symbols.
5. Preserved scoped row colour handling to avoid MiKTeX input-stack errors.
6. Placed architecture diagram on a separate page from the interfaces table to remove a page overflow.

MDR status: this is an extended engineering annex, not the single final competition MDR. Flight parameters and recovery hardware remain preliminary.
