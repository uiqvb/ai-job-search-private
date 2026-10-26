"""Build the Suncorp Technology Vacation Program cover letter as a .docx, styled to match
Manit_Khera_Cover_Letter_Asta.docx (Calibri, navy letterhead, rule under header).

Regenerate with:  python Scripts/build_cover_letter_suncorp.py
Edit the BODY list below to change the letter body. A list entry may be a plain string, or
a list of (text, bold) pairs for a mixed-run paragraph.

Notes on content, for whoever edits this next:
  - First year was a DISTINCTION average with one Credit in a single unit. It was NOT a
    Credit average. The Asta letter's "After receiving a Credit" is wrong; do not copy it.
  - No natural-hazard / "why I love insurance" paragraph. Manit cut it deliberately as
    manufactured passion. The letter pitches transferable energy instead. Do not reinstate.
  - The sensor and rollback material stays framed as evidence of how he works, not as
    evidence that he belongs in insurance.
  - No em dashes anywhere. House style.
  - Two claims to verify before sending: the unit chair's "dream come true" quote (carried
    over from the Asta letter, and he is a named referee), and "people who had reasonable
    doubts", which is deliberately vague about who.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches

NAVY = RGBColor(0x2F, 0x54, 0x96)
BLACK = RGBColor(0x00, 0x00, 0x00)
FONT = "Calibri"

OUT = (r"C:\Users\Manit Khera\Documents\Resume\Cover_Letters"
       r"\Manit_Khera_Cover_Letter_Suncorp.docx")


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
    "My name is Manit Khera, and I am studying a Bachelor of Software Engineering (Honours) "
    "at Deakin University. I am writing to apply for Suncorp's Technology Vacation Program. "
    "Before I tell you what I have built, I want to tell you how I started caring about "
    "building anything at all.",

    "When I began my degree, I did not have much ownership over it. Software engineering was "
    "a path encouraged by my parents and my brother, and for my first year I approached it "
    "with one foot in and one foot out. I finished with a Distinction average, which sounds "
    "fine, and that was the problem. It was a decent result from someone who was not really "
    "trying. The single Credit on that transcript bothered me more than any of the rest of "
    "it, not because of the mark, but because I knew exactly how little I had put in to earn "
    "it.",

    "Second year began with a fairly ordinary motive. I wanted better marks, and part of me "
    "wanted to prove something to people who had reasonable doubts about how seriously I was "
    "taking this. That is not the most admirable reason to change, but it started me moving, "
    "and it took me somewhere I did not expect. I began staying ahead of deadlines instead of "
    "chasing them. I started talking to teaching staff about the reasoning behind what we "
    "were building rather than the requirements of the assignment. At some point the work "
    "stopped feeling like a queue of submissions and started feeling like a set of questions "
    "I wanted answers to. That is when I stopped waiting to be handed problems and started "
    "setting my own.",

    "The clearest example came in a single trimester, when I was completing two final "
    "projects that had nothing to do with each other.",

    "In my backend development unit, I was building a REST API designed to control robots. In "
    "my embedded systems unit, separately, I was building a two-wheel-drive line-tracking car "
    "with infrared, light and rain sensors. The two units were unrelated. The projects were "
    "never intended to interact, and nothing in either brief explained how they might.",

    "So naturally, I decided to connect them.",

    "I wanted to push the backend further than the unit required and make it drive the "
    "physical car. It was, honestly, a Frankenstein idea: two separate systems forced "
    "together because I could not stop wondering whether it was possible. When I described it "
    "to my backend unit chair, he told me that seeing it work would be a dream come true, "
    "while being understandably sceptical that it would. There was no guide for this. Both "
    "projects carried a significant share of my final results in their respective units.",

    "The sensible thing would have been to finish them separately. I risked both instead.",

    "I understood what failure looked like. If the integration did not come together, I would "
    "not have one broken project, I would have two unfinished ones, in two units, in the same "
    "trimester. I accepted that, because by then I could see what the two systems could become "
    "together and I was no longer satisfied with delivering only what had been asked of me.",

    "For about a month I built, broke and rebuilt it. Sometimes the backend behaved correctly "
    "and the car ignored it entirely. Sometimes fixing one fault created another somewhere I "
    "had already signed off. I changed approach repeatedly, went back to problems I thought "
    "were closed, and spent a fair amount of time being wrong in ways I had not anticipated.",

    "Eventually the backend spoke to the car, and the car listened.",

    "The project was awarded 100 out of 100, but the grade is not the part I think about. What "
    "mattered more was that my unit chair and teaching staff trusted the work enough to put it "
    "in front of the public, and it was selected from my cohort to be shown at Deakin "
    "University\u2019s Open Day. An idea that had started as a risk I probably should not have "
    "taken had turned into something other people thought was worth showing.",

    "That project changed how I work more than what I can do. What it left me with is a habit, "
    "not a passion. I now assume my inputs are lying to me. On the car, the rain sensor was "
    "the least trustworthy component in the whole system, and one bad reading could shelter "
    "the washing on a clear day or leave it out in a downpour, so I stopped letting it decide "
    "alone and made it agree with Open-Meteo forecast data before committing to move. In the "
    "backend, I wrote the rollback engine to refuse partial reversals, because a half-applied "
    "rollback would record the robot at a position it was never actually in. Neither of those "
    "was required by the brief. I built them because I could see exactly how the system would "
    "embarrass me if I did not.",

    "I am not going to tell you I have always wanted to work in insurance. You have read that "
    "sentence a hundred times this month and I doubt you believe it any more than I would. "
    "What I will tell you is that the difference between my first year and my second was not "
    "ability, it was how much of myself I decided to put in. I have now seen what I do when I "
    "go all the way in on something, and I am not interested in going back to the version of "
    "me that did the minimum and called it done.",

    "So my pitch is about energy rather than devotion. Give me a real system, a team that will "
    "tell me when I am wrong, and work that actually breaks if I get it wrong, and you get the "
    "person who spent a month rebuilding an integration nobody asked for. I will ask too many "
    "questions in my first fortnight. I will pick up the piece of work nobody else has "
    "volunteered for. And when I do not understand your domain, which will be often at the "
    "start, I will say so and go and learn it rather than guess in front of you.",

    "Outside coursework I have spent the past year maintaining the website of the Boroondara "
    "Stroke Support Group, a community not-for-profit, which is where I learned that the least "
    "glamorous work is usually the work someone is actually relying on. I also lead LinkedIn "
    "for Deakin\u2019s Data Science Club, and on the Software Engineering Club committee I "
    "built the application behind a debugging workshop and seeded the bugs the attendees had "
    "to find.",

    "I began this degree on a path chosen largely for me. I am continuing it because I found "
    "the kind of work that makes me lose track of time. I am available full time from 24 "
    "November 2026 to 12 February 2027, based in Melbourne, with full Australian working "
    "rights. Twelve weeks is long enough for you to find out whether the energy I am "
    "describing is real. I would like you to test it.",

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
    para(doc, "8 August 2026", size=10.5, space_before=6, space_after=10)

    # --- Addressee block ---
    for line in ["Suncorp Graduate Recruitment Team", "Suncorp Group"]:
        para(doc, line, size=10.5, space_after=0, spacing=1.05)

    # --- Subject line (no em dash, house style) ---
    para(doc, "Re: Application, 2026/27 Technology Vacation Program",
         size=10.5, bold=True, color=NAVY, space_before=12, space_after=10)

    # --- Salutation + body ---
    para(doc, "Dear Suncorp Graduate Recruitment Team,", size=10.5, space_after=8)
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
