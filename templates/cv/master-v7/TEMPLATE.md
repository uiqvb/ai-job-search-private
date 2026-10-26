# Template: master-v7

- **Type:** CV
- **Source extension:** .txt
- **Engine/toolchain:** python-docx + Microsoft Word (PDF export via Word COM, `pywin32`)
- **Page limit:** 1 page(s)
- **Fonts:** Calibri (system font, ships with Office); name 21pt navy, headings 10.5pt navy with thin rule, body 10pt on an exact 11.35pt line
- **Class/packages:** `base.docx` (styles, numbering and page setup of Manit's master resume, body empty), filled by `build_cv.py`

Source: Manit's master resume v7 (`documents/cv/Manit_Khera_Resume_Rewrite_v7.*`), built by `documents/notes/docx-builders/build_master_resume_rewrite.py`. Every technical application since 13 Oct 2026 (Andromeda, Tekt, NxtGen, ReSource, cold outreach) used it. `build_cv.py` is that builder with the input as an argument; its output was checked pixel-identical to the original builder's on the v7 content. Made the default on 2026-10-20 at Manit's request: Australian resumes are one page.

## Compile command

    cd cv && python ../templates/cv/master-v7/build_cv.py <file>.txt

Writes `<file>.docx` and `<file>.pdf` beside the source and prints page count, words, links and the spare room at the foot (pt). Exits 1 unless exactly 1 page. Keep both outputs.

## Source format (`<file>.txt`)

Markdown-like, see `template.txt`. `# NAME`, contact lines, then `## SECTION` blocks. Entry lines are `**Title — Organisation** | dates`; projects are `**Name** | tech | [Demo video](url) · [Source code](url)`; bullets start `- `; `**bold**` inside bullets. Sections: PROFILE, EDUCATION, TECHNICAL SKILLS, PROJECTS, EXPERIENCE, LEADERSHIP (title line all bold), REFERENCES. Any other heading is laid out like EXPERIENCE. Start from `documents/cv/Manit_Khera_Resume_Rewrite.md` (the master) and tailor; project links are in `build_master_resume_rewrite.py` `PROJECT_LINKS`, referees in its `REFEREES`.

## Style rules

- One A4 page, always. Section order may change to suit the ad (projects before experience for technical roles).
- Keep the layout values; do not shrink fonts to fit. Cut copy instead. The v7 master fills the page with 2.3pt spare, so any line added must be paid for by one removed.
- Dates right-aligned, italic grey, as **ASCII ranges**: `Jul 2025 - Present`, `Mar 2025 - 2028 (expected)`. Never an en dash next to a year: ATS imports (Workday) drop it, and `/apply` runs `verify_pdf.py --ascii-dates`.
- Third-year (penultimate) student, finishing 2028. Never "second-year".
- References: the two referees (Slavnenko, Bhatia) on one line each, or "Available upon request." when space is short or the ad asks only for a resume.
- No LaTeX escaping: write `#`, `&`, `%` as plain characters.

## Known pitfalls

- Word must be installed; close the output `.docx` in Word before rebuilding.
- `verify_layout.py` thresholds are calibrated for moderncv; trust the builder's Word page count and the visual read, treat its margin warnings as advisory.
- The spare-room figure is the honest measure of fit. Under ~3pt means the next added word may break the page.
- `RESUME_LAYOUT='{"line": 220}'` overrides spacing for one build. Use only as a last resort and say so.
