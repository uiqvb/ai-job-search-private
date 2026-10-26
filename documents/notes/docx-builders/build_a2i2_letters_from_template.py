"""Fill the A2I2 cover letters into Templates/Cover-Letter-Template.docx in place.

Manit's instruction, 2026-09-24: copy the template .docx and fill it in exactly, keeping its
own layout (right-aligned sender block, its fonts, sizes, spacing and paragraph structure).
So this script does NOT clear the body and rebuild it. It opens a copy of the template and
replaces the text of the existing runs, copying each run's own formatting for any new runs.

Text source: the reviewed .md drafts in Applications/Deakin-A2I2-Research-Internships/.
Edit the .md, then re-run. Expected .md shape, blocks separated by blank lines:
  sender (5 lines), date, recipient (5 lines), greeting, **RE line**,
  intro, body 1, body 2, body 3, closing, sign-off, name.
**text** in a body paragraph becomes bold.

Note: Templates/Cover-Letter-Template.docx is not the blank DeakinTALENT original. It holds
the 13 August Student Experience Assistant letter, and it is what his Benchmarking letter
was built from. This script fills that file's structure, as instructed.

Run:  python Scripts/build_a2i2_letters_from_template.py
Then: python Scripts/verify_docs.py "<output>.docx" ...
"""

import copy
import re
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "Templates" / "Cover-Letter-Template.docx"
FOLDER = ROOT / "Applications" / "Deakin-A2I2-Research-Internships"

LETTERS = {
    "Draft - Overseer Datasets.md":
        "Manit Khera Cover Letter - Manufacturing Evaluation Datasets.docx",
    "Draft - AI Agent Routing.md":
        "Manit Khera Cover Letter - AI Agent Routing.docx",
}

BOLD = re.compile(r"(\*\*[^*]+\*\*)")


def segments(text):
    out = []
    for part in BOLD.split(text):
        if part:
            bold = part.startswith("**") and part.endswith("**")
            out.append((part[2:-2] if bold else part, bold))
    return out


def set_segments(p, segs):
    """Replace a single-run paragraph's text with formatted segments, keeping its rPr."""
    proto = p.runs[0]
    for r in p.runs[1:]:
        r._element.getparent().remove(r._element)
    anchor = proto._element
    for _ in segs[1:]:
        new = copy.deepcopy(proto._element)
        anchor.addnext(new)
        anchor = new
    for run, (text, bold) in zip(p.runs, segs):
        run.text = text
        run.bold = True if bold else None


def parse(md_path):
    text = md_path.read_text(encoding="utf-8")
    blocks = [b.strip().splitlines() for b in re.split(r"\n\s*\n", text) if b.strip()]
    sender, (date,), recipient, (greeting,), (re_line,) = blocks[:5]
    body = [" ".join(b) for b in blocks[5:-2]]
    (signoff,), (name,) = blocks[-2:]
    assert len(sender) == 5 and len(recipient) == 5 and len(body) == 5, md_path.name
    return dict(sender=sender, date=date, recipient=recipient, greeting=greeting,
                re_line=re_line.strip("*"), body=body, signoff=signoff, name=name)


def build(md_name, docx_name):
    L = parse(FOLDER / md_name)
    doc = Document(str(TEMPLATE))
    P = doc.paragraphs

    # sender block, right aligned: name / street / suburb, then phone / email
    P[0].runs[4].text = L["sender"][1]
    P[0].runs[6].text = L["sender"][2]
    P[1].runs[0].text = L["sender"][3]
    P[1].runs[2].text = L["sender"][4]

    P[2].runs[0].text = L["date"]

    # the template has six recipient lines, these letters need five, so the
    # contact's position title line is removed rather than left blank
    P[4].runs[0].text = L["recipient"][0]
    P[5]._element.getparent().remove(P[5]._element)
    P[6].runs[0].text = L["recipient"][1]
    P[7].runs[0].text = L["recipient"][2]
    P[8].runs[0].text = L["recipient"][3]

    # last address line, greeting and RE line share one paragraph in the template
    runs = P[9].runs
    runs[0].text = L["recipient"][4]
    runs[3].text = L["greeting"]
    runs[6].text = L["re_line"]

    intro, body1, body2, body3, close = L["body"]
    set_segments(P[11], segments(intro))

    # the template's middle paragraph holds two paragraphs separated by line breaks
    P[13].runs[0].text = body1
    P[13].runs[3].text = body2

    set_segments(P[15], segments(body3))
    # closing goes in its own paragraph, cloned from the one above to keep formatting
    close_el = copy.deepcopy(P[15]._element)
    blank = copy.deepcopy(P[16]._element)
    P[15]._element.addnext(blank)
    blank.addnext(close_el)
    set_segments([p for p in doc.paragraphs if p._element is close_el][0], segments(close))

    P[17].runs[0].text = L["signoff"]
    P[18].runs[0].text = L["name"]

    out = FOLDER / docx_name
    doc.save(out)
    print("Written:", out.name)


if __name__ == "__main__":
    for md, dx in LETTERS.items():
        build(md, dx)
