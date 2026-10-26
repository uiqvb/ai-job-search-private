"""Build the Deloitte "Me at Deloitte" cover letter as a .docx styled to match
1_Manit_Khera_Resume_final.pdf (Calibri, navy letterhead, rule under header).

Regenerate with:  python build_cover_letter_deloitte.py
Edit the BODY list below to change the letter body. A tuple entry is a
mixed-run paragraph: (text, bold) pairs.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches

NAVY = RGBColor(0x2F, 0x54, 0x96)
BLACK = RGBColor(0x00, 0x00, 0x00)
FONT = "Calibri"

OUT = r"C:\Users\Manit Khera\Documents\Resume\Cover_Letters\Manit_Khera_Cover_Letter_Deloitte.docx"


def bottom_rule(paragraph, color="2F5496", size=6):
    """Draw a horizontal rule beneath a paragraph."""
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    p_pr.append(borders)


def para(doc, text="", size=10.5, bold=False, color=BLACK, align=None,
         space_after=6, space_before=0, spacing=1.0, caps=False, letter_spacing=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = spacing
    if text:
        run = p.add_run(text)
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.all_caps = caps
        if letter_spacing is not None:
            rpr = run._element.get_or_add_rPr()
            spc = OxmlElement("w:spacing")
            spc.set(qn("w:val"), str(int(letter_spacing * 20)))
            rpr.append(spc)
    return p


def rich_para(doc, parts, size=10.5, space_after=8, spacing=1.06):
    """parts: list of (text, bold) tuples."""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing = spacing
    for text, bold in parts:
        run = p.add_run(text)
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = BLACK
    return p


BODY = [
    "My name is Manit Khera, and I am currently studying a Bachelor of Software Engineering "
    "at Deakin University. I am writing to express my interest in the Me at Deloitte program, "
    "as advertised on the Deloitte careers page. But first, let me tell you a story about "
    "who I am.",

    "When I began my degree, I did not have a strong sense of ownership over my studies. "
    "Software engineering was a path encouraged by my parents and brother, and during my "
    "first year, I approached it with one foot in and one foot out. After receiving a Credit, "
    "I entered my second year determined to prove that I was capable of more.",

    "At first, that motivation came from pride. I wanted higher grades and wanted to prove "
    "people wrong. It may not have been the most mature reason to change, but it led me "
    "somewhere unexpected: I began to genuinely enjoy technology.",

    "I started staying ahead of deadlines, engaging with my teaching staff and putting real "
    "effort into understanding what I was building. Assignments stopped feeling like tasks I "
    "had to submit. They became opportunities to test ideas and see how far I could take them.",

    "That change led to the boldest idea I had attempted at university.",

    "During the trimester, I was completing two unrelated final projects. In my backend "
    "programming unit, I was working with an API designed to control a robot. In my embedded "
    "systems unit, I was building a two-wheel-drive robotic car. The projects belonged to "
    "separate units and were never intended to interact.",

    "Naturally, I decided to connect them.",

    "I wanted to develop the backend API further and make it communicate with the physical "
    "car. It was essentially a Frankenstein project: two separate systems forced together "
    "because I could not stop wondering whether it was possible.",

    "When I shared the idea with my backend professor, he told me that seeing it work would "
    "be a dream come true, although he was understandably sceptical. There was no guide "
    "showing me how to combine the systems, and both projects were worth a significant part "
    "of my final results.",

    "The sensible option would have been to complete them separately.",

    "Instead, I risked both.",

    "If the integration failed, I could have been left with two incomplete final projects. I "
    "understood that risk, but by that point, I was obsessed with making the idea work. I had "
    "seen what the two systems could become together, and I was no longer satisfied with "
    "completing only what had been asked of me.",

    "For the next month, I built, tested, broke and rebuilt the system. Sometimes the backend "
    "worked but the car would not respond. At other times, fixing one issue created another. "
    "I repeatedly changed my approach, tested new solutions and returned to problems I "
    "thought I had already solved.",

    "Eventually, the backend communicated with the car.",

    "It worked.",

    "That moment changed my relationship with technology. Before then, I had mainly "
    "experienced engineering through structured assignments: a problem was provided, "
    "requirements were defined and I produced a solution. This project was different. I had "
    "created the challenge myself and accepted the possibility that it might fail.",

    "The project received 100 out of 100, but the grade was not the result that mattered "
    "most. I earned the trust of my professor and unit chair and was given the opportunity to "
    "present the project at Deakin University\u2019s Open Day. What began as a risky idea had "
    "become something other people believed was worth seeing.",

    "I am now exploring whether the project could evolve into a miniature warehouse robotics "
    "system, potentially with university funding or as the basis of my capstone project.",

    "This experience clarified the kind of engineer I want to become. I want to build systems "
    "that are technically reliable but also imaginative. I want to recognise connections that "
    "others may overlook and have the discipline to turn uncertain ideas into practical "
    "solutions.",

    "This is why the Me at Deloitte program stands out to me. University has shown me that I "
    "enjoy solving technical problems, but I now want to understand how this mindset is "
    "applied to real organisational challenges. I want to learn how technology professionals "
    "balance creativity with business needs and how multidisciplinary teams turn ambitious "
    "ideas into measurable outcomes.",

    [("My experience closely reflects Deloitte\u2019s value of ", False),
     ("Lead the way", True),
     (". Connecting the projects meant moving beyond the defined requirements, pursuing an "
      "idea with no guaranteed outcome and accepting the risk that came with it. I learned "
      "that leading the way is not simply about having bold ideas. It is about taking "
      "responsibility for them, remaining committed when they become difficult and doing the "
      "work required to make them real.", False)],

    "I began my degree following a path that had largely been chosen for me. I am now "
    "continuing because I have discovered the kind of work that makes me lose track of time: "
    "imagining what a system could become and refusing to leave the idea unexplored.",

    "Through Me at Deloitte, I hope to continue that journey and learn how bold technical "
    "thinking can create an impact that matters.",

    "Thank you for considering my application.",
]


def build():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10.5)

    # --- Letterhead (mirrors the resume header) ---
    para(doc, "MANIT KHERA", size=24, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, letter_spacing=2.0)
    para(doc, "0412 761 206  |  manitkhera26@gmail.com", size=9.5,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    rule_p = para(doc, "Blackburn South, VIC  |  linkedin.com/in/manit-khera-603957252",
                  size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    bottom_rule(rule_p)

    # --- Date ---
    para(doc, "26 July 2026", size=10.5, space_before=6, space_after=10)

    # --- Addressee block ---
    for line in ["Deloitte Recruitment Team", "Deloitte Australia"]:
        para(doc, line, size=10.5, space_after=0, spacing=1.05)

    # --- Subject line ---
    para(doc, "Re: Application \u2014 Me at Deloitte Program",
         size=10.5, bold=True, color=NAVY, space_before=12, space_after=10)

    # --- Salutation + body ---
    para(doc, "Dear Deloitte Recruitment Team,", size=10.5, space_after=8)
    for block in BODY:
        if isinstance(block, list):
            rich_para(doc, block)
        else:
            para(doc, block, size=10.5, space_after=8, spacing=1.06)

    # --- Sign-off ---
    para(doc, "Yours sincerely,", size=10.5, space_before=4, space_after=16)
    para(doc, "Manit Khera", size=11, bold=True, color=NAVY, space_after=0)

    doc.save(OUT)
    print("Written:", OUT)


if __name__ == "__main__":
    build()
