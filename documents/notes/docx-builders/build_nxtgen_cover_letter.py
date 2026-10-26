"""Fill the NxtGen Intern Challenge cover letter into Templates/Cover-Letter-Template.docx in place.

Same method as build_a2i2_letters_from_template.py (copy the template, replace the text
of its existing runs, keep its layout), pointed at the NxtGen folder.

Text source: Applications/NxtGen-Intern-Challenge/Manit Khera Cover Letter.md.
Edit the .md, then re-run. Same block shape as the A2I2 drafts.

Run:  python Scripts/build_rosterfy_cover_letter.py
Then: python Scripts/verify_docs.py "<output>.docx"
"""

import build_a2i2_letters_from_template as letters

if __name__ == "__main__":
    letters.FOLDER = letters.ROOT / "Applications" / "NxtGen-Intern-Challenge"
    letters.build("Manit Khera Cover Letter.md", "Manit Khera Cover Letter.docx")
