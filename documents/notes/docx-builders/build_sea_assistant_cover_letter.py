"""Student Experience Assistant cover letter, Melbourne Burwood Campus. One page.

BUILT ON THE OFFICIAL DEAKINTALENT TEMPLATE.
Base file: Templates/Cover-Letter-Template.docx

Guides/Cover-Letter-Guide.md and the checklist both require the template to be used as the
base rather than the layout being recreated. This script opens it, keeps its styles, page
setup and block structure, strips the placeholder text and writes the real letter back.

⚠️ FONT CONFLICT, RESOLVED DELIBERATELY. The cover letter template defaults to Calibri, but
the resume template (Resume-Template-3) is Verdana. The cover letter checklist is explicit:
"Font style and font size is the same as used in the resume" and the two "should look like
they belong together as one application package". That rule outranks the template's default,
so this letter is set in Verdana at the resume's body size. Do not "fix" it back to Calibri.

TWO DELIBERATE CHANGES FROM THE 12 AUG LETTER:

  1. NO BULLETED LIST. The 12 Aug letter set the four shift-running commitments as bullets.
     The checklist states lists SHOULD NOT BE INCLUDED in a cover letter. They are prose
     now, and all four ideas survive.
  2. ADDRESSED TO SARAH MIOCIC, named in the position description as Manager, Student
     Engagement and Orientation. The guide says address the named contact.

THE THREE QUESTIONS THE POSTING REQUIRES, answered in order:
  1. Which campus                  -> paragraph 1, named explicitly
  2. Enrolment through T1+T2 2027  -> paragraph 1
  3. Leadership experience, and how it would be used to lead, SUPPORT and MOTIVATE the
     Student Experience Ambassadors -> paragraphs 2 and 3.
     The question carries three verbs. Paragraph 2 evidences leading and supporting; the
     fourth commitment in paragraph 3 ("name what went well") answers motivate, on purpose.

⚠️ TENSE GUARD. "By the time this contract begins I will have worked that shift myself."
The Open Day ambassador role is SELECTED, not performed. Do not move to past tense.

House style: no em dashes, Australian spelling, numbers one to ten as words.

Run:  python Scripts/build_sea_assistant_cover_letter.py
"""

from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "Templates" / "Cover-Letter-Template.docx"
OUTDIR = ROOT / "Applications" / "Deakin-Student-Experience-Assistant"
OUT = OUTDIR / "Manit Khera Cover Letter.docx"

FONT = "Verdana"      # matched to the resume, per the checklist
BODY_SIZE = 9.5       # matched to the resume
BLACK = RGBColor(0, 0, 0)


# --------------------------------------------------------------------------- helpers

def clear_body(doc):
    body = doc.element.body
    for child in list(body):
        if child.tag == qn("w:sectPr"):
            continue
        body.remove(child)


def style_run(run, bold=False):
    run.font.name = FONT
    run.font.size = Pt(BODY_SIZE)
    run.font.bold = bold
    run.font.color.rgb = BLACK
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), FONT)
    return run


def para(doc, text="", bold=False, space_after=4, space_before=0):
    p = doc.add_paragraph(style="Normal")
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = 1.0
    if text:
        style_run(p.add_run(text), bold)
    return p


def block(doc, lines, space_after=4):
    """An address block: one paragraph, soft line breaks inside, as the template does."""
    p = doc.add_paragraph(style="Normal")
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.0
    for i, line in enumerate(lines):
        if i:
            style_run(p.add_run()).add_break()
        style_run(p.add_run(line))
    return p


# ------------------------------------------------------------------------------ body

SENDER = ["Manit Khera", "Blackburn South, VIC 3130",
          "0412 761 206", "manitkhera26@gmail.com"]

RECIPIENT = ["Sarah Miocic",
             "Manager, Student Engagement and Orientation",
             "Student Experience and Engagement Team, Student Services",
             "Deakin University",
             "221 Burwood Highway",
             "Burwood, VIC 3125"]

P1 = (
    "I am writing to apply for the Student Experience Assistant position with Deakin "
    "University, advertised through DeakinTALENT. I am applying for the Melbourne Burwood "
    "Campus. I am currently enrolled in a Bachelor of Software Engineering (Honours) at "
    "Deakin, expected to complete in 2028, and will remain enrolled through Trimesters 1 "
    "and 2 of 2027, so I am available for the full six-month contract and any extension. "
    "I am applying because I have spent the past year doing this work through two Deakin "
    "clubs, and leading a team who do it is the part I want next."
)

P2 = (
    "I am maintaining a High Distinction average, and a unit project of mine was selected "
    "from my cohort for showcase at Deakin Open Day. On leadership, I will give you the "
    "honest version rather than the impressive one. I have not been a club president. What I can show you is that in every role I have "
    "held, the work ended with someone else able to do it without me. At 7-Eleven I "
    "trained new starters on the POS, food safety and shift routines while running shifts "
    "solo and opening and closing the store unsupervised. Training someone on a till "
    "during peak trade teaches you that people learn by doing one part of it while you "
    "stand close enough to catch it and far enough back that the customer is still "
    "theirs. At the Boroondara Stroke Support Group I ran the monthly activity calendar publication "
    "to deadline for twelve months, then trained new volunteers to run it themselves. On "
    "the Deakin Software Engineering Club committee I designed the defects seeded into a "
    "debugging workshop for thirty attendees, then floated the room getting people "
    "unstuck without reaching over and taking the keyboard."
)

P3 = (
    "I would use that with the Student Experience Ambassadors in four ways. I would brief "
    "the team before the shift rather than during it, because most nerves on a stall are "
    "not about confidence but about not knowing what you will be asked. I would take the "
    "first hard question and hand the second one back, because answering everything for "
    "someone keeps them dependent on you all day. I would watch for the third hour, since "
    "Orientation shifts are long and there is a predictable point where people go quiet. "
    "And I would name what went well out loud at the "
    "end, because casual staff on roughly a hundred hours a year rarely hear specifically "
    "what they did well, and it is the thing most likely to bring someone back for the "
    "next intake."
)

P4 = (
    "I know Deakin from inside these programs rather than only as a student. Over the past "
    "year I have served on the Software Engineering and Data Science "
    "Club committees at Burwood, fronted Market Day stalls, hosted and anchored networking "
    "sessions, and used DeakinTALENT's own services while preparing this application. I "
    "have been selected as a Student Ambassador with Deakin Future Students for Open Day, "
    "which is the role this position leads, so by the time this contract begins I will "
    "have worked that shift myself. I am also interested in the partnership half of the "
    "role rather than only the rostered shifts. Designing those workshop defects taught me "
    "that the design of an activity decides what you learn from it, and that is what I "
    "would bring to focus groups, design workshops and evaluation as a Student Partner."
)

P5 = (
    "I hold a current Working with Children Check and am available for evening and weekend "
    "events and across the key intake periods. I have held that average while volunteering "
    "weekly and holding two committee roles, which is the clearest evidence I can give of "
    "managing my time. My resume is attached. I would "
    "welcome the opportunity to discuss the role with you at interview, and thank you for "
    "your consideration."
)

BODY = [P1, P2, P3, P4, P5]


def build():
    doc = Document(str(TEMPLATE))
    clear_body(doc)

    block(doc, SENDER)
    # Template date format: "Wednesday 1 April 2026".
    para(doc, "Thursday 13 August 2026")
    block(doc, RECIPIENT)

    para(doc, "Dear Sarah Miocic,")
    para(doc, "RE: Application for Student Experience Assistant, Melbourne Burwood Campus",
         bold=True)

    for b in BODY:
        para(doc, b)

    para(doc, "Yours sincerely,", space_before=0, space_after=7)
    para(doc, "Manit Khera", space_after=0)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("Written:", OUT)
    print("Base template:", TEMPLATE.name)
    print("Body word count:", sum(len(b.split()) for b in BODY))


if __name__ == "__main__":
    build()
