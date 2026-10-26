"""Build the CSIRO 2026/27 Undergraduate Vacation Studentship cover letter (2 pages).

Companion script: build_resume_csiro.py. CSIRO's posting asks for the resume and cover
letter as one combined document, but Manit wants them as separate files (instruction
2026-08-10). Merge at upload time if the form only accepts one file.

  Preference 1 - Technology 11, Human-in-the-Loop Planning for Heterogeneous Robot Teams
                 (Kavindie Katuwandeniya, CSIRO Robotics, Clayton VIC)
  Preference 2 - Technology 14, Learning Engine and Fleet Knowledge for HART OS
                 (Kartik Yellapantula, CSIRO Robotics, Clayton VIC)

Notes on content, for whoever edits this next:

  - THE LETTER CITES A PAPER MANIT MUST ACTUALLY READ. Katuwandeniya, Tian and Kulic,
    "What did the Robot do in my Absence? Video Foundation Models to Enhance Intermittent
    Supervision", IEEE RA-L 2025, arxiv.org/html/2411.10016. It compared storyboard, video
    and text summaries of robot activity across 30 participants; storyboards won on the
    accuracy/effort trade-off and users preferred visual over text. It is the direct
    precursor to Technology 11. If he has not read it, cut paragraphs 5 and 6.

  - The seeded-defects paragraph is the strongest thing in the application. Tech 11's user
    study has participants review plans containing deliberately introduced errors, and he
    has built that instrument. Do not trim it for space.

  - NO ROS OR ROS2 CLAIM. He confirmed zero exposure 2026-08-10. The gap is named outright
    in the letter, which is the right call in front of a robotics panel, and paired with
    the MQTT/telemetry substrate that genuinely transfers. Do not soften this.

  - The trimester narrative is compressed to two short paragraphs. The Suncorp letter runs
    that story at length; a research panel wants the technical reasoning first and the
    motivation story second, so the proportions are deliberately inverted here.

  - Honesty constraints from README.md, verified against the repo 2026-08-08: no "Saga",
    no "autonomous robots" for the Robot Controller, no PID on the clothesline, and
    ParkSense stays "originated the concept and ran data-viability research", never
    "built the model" or "designed the pipeline".

House style: no em dashes, Australian spelling.

Run:  python Scripts/build_cover_letter_csiro.py
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches, Cm

NAVY = RGBColor(0x2F, 0x54, 0x96)
BLACK = RGBColor(0x00, 0x00, 0x00)
GREY = RGBColor(0x59, 0x59, 0x59)
FONT = "Calibri"

BODY_SIZE = 10.5

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Cover_Letters" / "Manit_Khera_Cover_Letter_CSIRO.docx"


# --------------------------------------------------------------------------- helpers

def bottom_rule(paragraph, color="2F5496", size=6):
    """Draw a horizontal rule beneath a paragraph."""
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), color)
    borders.append(bottom)
    p_pr.append(borders)


def para(doc, text="", size=BODY_SIZE, bold=False, italic=False, color=BLACK, align=None,
         space_after=6, space_before=0, spacing=1.05, letter_spacing=None):
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
        run.font.italic = italic
        run.font.color.rgb = color
        if letter_spacing is not None:
            rpr = run._element.get_or_add_rPr()
            spc = OxmlElement("w:spacing")
            spc.set(qn("w:val"), str(int(letter_spacing * 20)))
            rpr.append(spc)
    return p


# ---------------------------------------------------------------------------- content

SUBJECT = "Re: Application, 2026/27 Undergraduate Vacation Studentship (Technology)"

PREFERENCES = [
    "Preference 1:   Technology 11, Human-in-the-Loop Planning for Heterogeneous Robot "
    "Teams (Clayton, VIC)",
    "Preference 2:   Technology 14, Learning Engine and Fleet Knowledge from Robot "
    "Experience, HART OS (Clayton, VIC)",
]

LETTER = [
    # --- 1. who, what, eligibility ---------------------------------------------
    "I am completing the second year of a Bachelor of Software Engineering (Honours) at "
    "Deakin University, and I am applying for the two Clayton robotics projects listed "
    "above. I will have completed two full years of full-time study before the placement "
    "begins, and I carry a High Distinction average, including perfect scores in Backend "
    "Development and in Data Structures and Algorithms.",

    # --- 2. the common thread ---------------------------------------------------
    "I have chosen these two projects because they are the same question asked at "
    "different ends of a mission. Technology 11 asks how a person can meaningfully review "
    "what a robot team is about to do. Technology 14 asks how what a robot team has "
    "already done becomes knowledge somebody can query later. Both assume the intelligence "
    "sits with the operator and the server rather than inside the robot, and both live or "
    "die on whether the record and the representation are trustworthy. That is the "
    "assumption I have spent the past year building software against.",

    # --- 3. Tech 11: the architecture -------------------------------------------
    "Technology 11 is my first preference because I have already built a student-scale "
    "version of the architecture RobotLinq is testing against. For my backend unit I built "
    "a hardware-neutral REST control plane for a robot fleet, spanning 18 controllers and "
    "16 bounded contexts, in which all planning is held server-side. The robot "
    "deliberately holds no plan of its own; it executes what the operator dispatches to "
    "it. The project was awarded 100 out of 100 and was selected from my cohort for "
    "showcase at Deakin Open Day.",

    "What that project taught me is not in the mark. Separately, in an embedded systems "
    "unit in the same trimester, I had built a two-wheel-drive robot with infrared, light "
    "and rain sensors. The two units were unrelated and nothing in either brief suggested "
    "they should meet, so I spent about a month making the backend drive the physical "
    "robot, at the risk of finishing neither. Watching a plan that looked entirely "
    "reasonable on a dashboard turn into the wrong movement on a floor is the reason the "
    "premise of Technology 11 reads as obviously true to me. The representation an "
    "operator approves and the behaviour they actually get are two different objects.",

    # --- 4. Tech 11: the seeded defects -----------------------------------------
    "The part of the brief I keep returning to is the user study, where participants "
    "review plans containing deliberately introduced errors. I have designed that "
    "instrument before. On the Deakin Software Engineering Club committee, the development "
    "team built a React application for a debugging workshop, and I solely designed the "
    "defects seeded into it for thirty attendees to find. Choosing those faults was harder "
    "and more interesting than building the application: a defect that is too obvious "
    "measures nothing, a defect that is too subtle measures only patience, and the ones "
    "worth planting are the ones a reviewer will confidently declare fixed without having "
    "fixed them. Which faults people caught immediately, which they walked straight past, "
    "and which they believed they had resolved is the closest thing I have to your "
    "experimental question, and it is the reason I do not think error injection is a "
    "detail you can leave to the end of the project.",

    # --- 5. Tech 11: the paper ---------------------------------------------------
    "In preparing this application I read “What did the Robot do in my Absence?”. The "
    "result I found most useful was not that storyboards came out ahead overall, but that "
    "they were weaker on event-related questions than on object-related ones, and that "
    "query-driven summaries bought accuracy at the cost of time. That is a warning that "
    "there may be no single winning representation, only representations matched to the "
    "kind of error an operator is being asked to catch. Extending that from “what did the "
    "robot do” to “what is the robot about to do” seems to me to make it harder rather "
    "than easier, because a proposed plan has no ground truth yet for the operator to "
    "check against, and a heterogeneous team means the reviewer also has to hold each "
    "robot's differing skills and limits in their head while they read it. Those are the "
    "questions I would like to spend twelve weeks on.",

    # --- 6. Tech 14 --------------------------------------------------------------
    "Technology 14 draws me for a connected reason. The same backend records every "
    "dispatched and completed action to a queryable job and workflow execution history, "
    "and its rollback engine reconstructs robot state from that record rather than from "
    "whatever the robot reports, because a half-applied reversal would otherwise log the "
    "robot at a position it was never in. Every reported action is replayed through "
    "simulation before anything is committed. Building that taught me the distinction the "
    "Learning Engine rests on: a log is not yet evidence, and the work is in deciding what "
    "the record has to guarantee before anyone is allowed to draw a conclusion from it.",

    "The grass traversability case study also rhymes with something I built. On the "
    "clothesline robot, the rain sensor was the least reliable component in the system, "
    "and one bad reading could shelter the washing on a clear day or leave it out in a "
    "downpour. Rather than let a single reading decide, I made it agree with Open-Meteo "
    "forecast data before the robot committed to moving. Treating a signal as "
    "conditionally reliable rather than absolutely is the same posture as treating grass "
    "as conditionally traversable rather than always fatal. Separately, on a hackathon "
    "project I originated, my main contribution was the unglamorous half of exactly this "
    "problem: establishing whether the public sensor feed we wanted to use carried enough "
    "signal to support prediction at all, before the team committed to building on it. "
    "Asking whether the evidence can bear the weight of the capability is work I have "
    "already found I enjoy.",

    # --- 7. the honest gap -------------------------------------------------------
    "I should be straightforward about one gap, because it matters more for Technology 14 "
    "than for Technology 11. I have not used ROS or ROS2, and I am not going to dress that "
    "up. What I do have is the substrate underneath them: MQTT publish and subscribe "
    "topics carrying JSON telemetry on a fixed interval between a microcontroller and a "
    "Python supervisor, that telemetry logged, and the system then debugged from the "
    "record rather than from the hardware. I once traced an intermittent brownout to a "
    "failing buck converter using boot identifiers and reset causes in the telemetry "
    "rather than a multimeter, which is the same instinct a bag file rewards. I work in "
    "both C++ and Python. I would rather name this now and arrive in November having "
    "worked through the ROS2 basics in my own time than overstate it here and have you "
    "find out in week one.",

    # --- 8. why research ---------------------------------------------------------
    "I am applying because I want to find out whether research is the direction I take "
    "after this degree, and I do not think I can answer that from inside coursework. In a "
    "unit, the question is set for you and somebody already knows the answer. What "
    "attracted me to both of these projects is that they end in design guidance and "
    "evidence rather than a working demo, and I would like to know whether I am any good "
    "at that, including the parts that are unglamorous: recruiting participants, running "
    "sessions carefully enough that the results mean something, and reporting a result "
    "that does not go the way I expected.",

    # --- 9. logistics and close --------------------------------------------------
    "I am Melbourne based and able to be on site at Clayton daily, including for lab work "
    "with the physical testbed and for participant sessions, and I am available full time "
    "from November 2026 to February 2027. I would be glad to talk through the rollback "
    "engine or the clothesline robot in more detail, and demonstration videos and source "
    "code for both are linked on my resume.",

    "Thank you for considering my application.",
]


def build():
    doc = Document()

    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(BODY_SIZE)

    # --- letterhead (mirrors the resume header) ---
    para(doc, "MANIT KHERA", size=22, bold=True, color=NAVY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2, letter_spacing=2.0)
    para(doc, "0412 761 206  |  manitkhera26@gmail.com", size=9,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    rule_p = para(doc, "Blackburn South, VIC  |  linkedin.com/in/manit-khera-603957252",
                  size=9, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=9)
    bottom_rule(rule_p)

    # --- date ---
    para(doc, "10 August 2026", space_before=4, space_after=9)

    # --- addressee ---
    para(doc, "Undergraduate Vacation Studentships Selection Panel", space_after=0)
    para(doc, "CSIRO Technology", space_after=0)

    # --- subject and preferences ---
    para(doc, SUBJECT, bold=True, color=NAVY, space_before=11, space_after=3)
    for line in PREFERENCES:
        para(doc, line, size=9.5, color=GREY, space_after=1, spacing=1.0)

    # --- salutation and body ---
    para(doc, "Dear Selection Panel,", space_before=9, space_after=7)
    for block in LETTER:
        para(doc, block, space_after=7, spacing=1.05)

    # --- sign-off ---
    para(doc, "Yours sincerely,", space_before=4, space_after=14)
    para(doc, "Manit Khera", size=11, bold=True, color=NAVY, space_after=0)

    doc.save(OUT)
    print("Written:", OUT)


if __name__ == "__main__":
    build()
