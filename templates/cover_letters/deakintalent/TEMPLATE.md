# Template: deakintalent

- **Type:** Cover letter
- **Source extension:** .txt
- **Engine/toolchain:** python-docx + Microsoft Word (PDF export via Word COM, `pywin32`)
- **Page limit:** 1 page(s)
- **Fonts:** Calibri 10pt (theme body font; system font, ships with Office)
- **Class/packages:** `template.docx` (DeakinTALENT Cover Letter Template, A4, 2.54 cm side / 2 cm top-bottom margins), filled by `build_cover.py`

Source: the official DeakinTALENT `Cover-Letter-Template.docx` (`documents/notes/templates/`), as Manit filled it for the Student Experience Assistant letter (13 Aug 2026). `template.docx` is that layout with every personal detail replaced by a placeholder. Made the default on 2026-10-20 at Manit's request.

## Compile command

    cd cover_letters && python ../templates/cover_letters/deakintalent/build_cover.py <file>.txt

Writes `<file>.docx` and `<file>.pdf` beside the draft and prints the Word page count; exits 1 if it is not exactly 1 page. Keep both the `.docx` and the `.pdf` (some portals want Word).

## Draft format (`<file>.txt`)

Sections headed `## Sender`, `## Date`, `## Recipient`, `## Greeting`, `## RE`, `## Body`, `## Sign-off`, `## Name` (see `template.txt`). One item per line, except Body, where blank lines separate paragraphs. `**text**` becomes bold. Leave `## RE` empty to drop the reference line. The last two Sender lines (phone, email) form the second right-aligned block. No LaTeX escaping: write `&`, `%`, `$` as plain characters.

## Style rules

- Layout is the template's, untouched: right-aligned sender block, date, recipient block, greeting, bold RE line, prose paragraphs separated by one blank line, sign-off, name. All 10pt Calibri, single spacing.
- Sender: name, street address, suburb/state/postcode, phone as `04XX XXX XXX`, email (DeakinTALENT asks for the street address here).
- Date written out: `Tuesday 20 October 2026`, never numeric.
- Recipient: name, position title (drop the line if unknown), organisation, street, suburb/state/postcode. Unknown contact: `Hiring Manager` / `Dear Hiring Manager,`.
- RE line: `RE: <full position title> position, REF: <number>`; drop `, REF: ...` when the ad gives none.
- Four prose paragraphs, no bullet list: introduction, body one (degree, 2028 completion, WAM, awards, two or three evidenced skills), body two (organisation research), closing (attachments, interview, thanks). See `documents/notes/guides/Cover-Letter-Guide.md` section 4a, which is normative.
- Sign-off `Kind regards,` then the full name. No e-signature.
- Final file to send: `Manit Khera Cover Letter.pdf` (and `.docx` if asked).

## Known pitfalls

- Word must be installed and closed on the output file; an open `.docx` makes the save fail ("close it in Word and re-run").
- The page count comes from Word itself, so trust it over `verify_layout.py`, whose thresholds are calibrated for cover.cls; run `verify_pdf.py --pages 1` and read the PDF, and treat `verify_layout.py` margin warnings as advisory.
- Word space budget: the original letter filled about 85% of the page with ~480 body words at 10pt. Stay under ~450 body words.
