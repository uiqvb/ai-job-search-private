"""The three Deakin Applied Artificial Intelligence Initiative research internship letters.

One script, three letters, because they share a spine and diverge only in paragraphs three
to five. Building them together is what keeps the shared paragraphs identical where they
should be and genuinely different where they must be.

BUILT ON THE OFFICIAL DEAKINTALENT TEMPLATE.
Base file: Templates/Cover-Letter-Template.docx, opened and edited, per CLAUDE.md.

FONT CONFLICT, RESOLVED THE STANDING WAY. The cover letter template defaults to Calibri
and the resume template is Verdana. The cover letter checklist requires the same font as
the resume and requires the two to look like one package, so these are Verdana at the
resume's body size. Do not "fix" this back to Calibri.

DECIDED 2026-09-18, MANIT'S CALL: ONLY THE BENCHMARKING LETTER SHIPS. He is applying to
that project alone, not to all three. Three applications into one institute read as
spraying, and benchmarking is both the one he actually wants and the one his evidence fits
best. So a plain run builds ONLY that letter; pass --all to rebuild the other two, whose
text is kept below in full in case he changes his mind. The two unsent letters were deleted
from Applications/ so the wrong file cannot be attached by accident.

WHY THREE LETTERS WERE DRAFTED AND NOT ONE. Barnett supervises two of the three projects,
so a single generic letter had a real chance of being read twice by the same person, and a
letter that could have gone to any of the three says nothing about which one the applicant
wants. That reasoning still holds if he ever applies to more than one.

⚠️ NOBODY KNOWS WHO READS THESE. The three briefs carry no submission instructions, no
contact address and no closing date. Do not assert anything about the selection process;
it is genuinely unrecorded.

THE SHARED SPINE, same in all three:
  P1  what is being applied for, the named supervisors, the academic record, and the
      availability their "other details" section asks about, answered before anyone has
      to ask.
  P2  why research at all. Stories/03, the short variant, keeping the honesty move that
      makes it work: he does not claim to know research is the career for him.
  P3  THE PROJECT-SPECIFIC HOOK. Different in every letter, mapped to one objective from
      that brief, quoted closely enough that the reader can see it was read.
  P4  the second hook, drawn from the Robot Controller or the clothesline.
  P5  the gap, run as the move in Stories/10-naming-the-ros-gap.md: name it plainly, say
      where it bites, offer the substrate underneath it, attach a date.
  P6  close.

THE HOOKS, one per letter:
  Benchmarking   -> seeded defects as benchmark-task design, plus run logs and the
                    "a log is not yet evidence" position. Stories 04 and 08.
  Datasets       -> ParkSense data-viability research, plus checkable ground truth.
                    Stories 13 and 04.
  Routing        -> the rain sensor cross-check as uncertainty-aware decision making,
                    plus defect calibration as ambiguity calibration. Stories 07 and 04.

GUARDS, all confirmed against CLAUDE.md and Stories/ on 2026-09-18:

  x NO claim of configuring coding agents. Manit uses Claude Code normally and has NOT
    written skills, hooks or worktree setups. The benchmarking letter names this as a gap
    rather than hiding it, because it is the one the reader is most likely to probe.
  x NO statistics, experimental-controls, conformal-prediction or research-methods claim.
    Each letter names the one that bites hardest for that project.
  x NO ML or modelling claim on ParkSense. The team lead's public write-up credits himself
    with the endpoints, the frontend, the pipeline and the model. Viability research and
    backend foundations only.
  x NO grade printed for the IB Psychology Extended Essay. Stories/03 flags the A as
    needing verification against the transcript. The essay itself is used; the grade is
    not.
  x NO "delivered" or "ran" the workshop. He built the application as part of the dev team
    and solely designed the defects. Someone else delivered the session.
  x NO industry or research experience implied anywhere.
  x No em dashes, Australian spelling, numbers one to ten as words, no bulleted lists
    (the checklist bans lists in a cover letter).

  ! AVAILABILITY IS A COMMITMENT MANIT IS MAKING, not a fact verified here. Every letter
    states two days per week on campus at Burwood for ten weeks. Confirm against his 2027
    timetable before sending.
  ! The institute is written exactly as the briefs write it, "Deakin Applied Artificial
    Intelligence Initiative". The PDFs say Initiative, not Institute, and the abbreviation
    is not used anywhere in them.

Run:  python Scripts/build_a2i2_cover_letters.py
"""

from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "Templates" / "Cover-Letter-Template.docx"
OUTDIR = ROOT / "Applications" / "Deakin-A2I2-Research-Internships"

FONT = "Verdana"      # matched to the resume, per the checklist
BODY_SIZE = 9.5       # matched to the resume
BLACK = RGBColor(0, 0, 0)

DATE = "Friday 18 September 2026"

SENDER = ["Manit Khera", "Blackburn South, VIC 3130",
          "0412 761 206", "manitkhera26@gmail.com"]

INSTITUTE = ["Deakin Applied Artificial Intelligence Initiative",
             "Deakin University",
             "221 Burwood Highway",
             "Burwood, VIC 3125"]


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


def para(doc, text="", bold=False, space_after=3, space_before=0):
    p = doc.add_paragraph(style="Normal")
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = 1.0
    if text:
        style_run(p.add_run(text), bold)
    return p


def block(doc, lines, space_after=3):
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


# ------------------------------------------------------------- shared paragraphs

def p1(project, supervisors):
    return (
        "I am writing to apply for the " + project + " research internship with the "
        "Deakin Applied Artificial Intelligence Initiative, supervised by " + supervisors
        + ". I am a Bachelor of Software Engineering (Honours) student at Deakin, "
        "Burwood, with a Weighted Average Mark of 81.33 and 100 in both Backend "
        "Development and Data Structures and Algorithms. I am available on campus at "
        "Burwood two days per week for the full ten weeks, and I understand the position "
        "is unpaid."
    )


# Stories/03, short variant. The final two sentences are the honesty move that makes the
# story work. Removing them turns it into a claim about himself he cannot support.
P2 = (
    "As a child I wanted to be a scientist, which in practice meant finding experiments "
    "on YouTube, gathering whatever was in the house and trying them to see what "
    "changed. I found the same thing again in Year 12, in an "
    "IB Psychology Extended Essay I spent months on: one question, a body of literature "
    "to read and understand, and a conclusion I had to be willing to defend. I will not "
    "pretend I already know that research is the career for me. I do not. Being "
    "completely invested in one problem is one of the few things that makes me lose "
    "track of time, and ten weeks on a real question is how I would find out."
)

CLOSE = (
    "My resume is attached, and every project in it links to public code and a working "
    "demonstration, so the claims can be checked rather than taken on trust. I would "
    "welcome the chance to discuss the project, and thank you for your consideration."
)


# ------------------------------------------------------------------------ letter one
# BENCHMARKING AGENT WORKFLOWS FOR SOFTWARE DEVELOPMENT
# Dr Wannita Takerngsaksiri, A/Prof Scott Barnett. Manit's stated first preference.

BENCH_P3 = (
    "The objective I keep returning to is the second, identifying the coding tasks the "
    "benchmark runs on. On the Deakin Software Engineering Club committee I solely "
    "designed the defects seeded into a React application built as the teaching "
    "artefact for a debugging workshop, for around thirty attendees to find. Choosing "
    "the faults was harder and more interesting than building the application. A "
    "defect that is too obvious measures "
    "nothing. One that is too subtle measures only patience. The ones worth planting are "
    "those a reviewer will confidently declare fixed without having fixed them. A "
    "benchmark task set has that problem from the other direction: if every workflow "
    "passes every task the benchmark has told you nothing, and the tasks that earn their "
    "place are the ones where an agent can report a success it has not earned."
)

BENCH_P4 = (
    "Your first expected outcome is a working harness with run logs for every workflow, "
    "and I have already had to take a position on what a log may be used for. The "
    "backend I built for my backend development unit records every dispatched and "
    "completed action to a queryable execution history, and the rollback engine "
    "reconstructs the robot's state from that record rather than from what the robot "
    "reports, because a half-applied reversal would otherwise log the robot at a "
    "position it was never at. Every reported action is replayed through simulation "
    "before anything is committed. A log is not yet evidence, and the work is deciding "
    "what the record must guarantee before anyone draws a conclusion from it. A "
    "comparison across workflows stands or falls on that."
)

BENCH_P5 = (
    "Two gaps, named rather than left for week one. I use Claude Code daily in my own "
    "development, so I am a user of the thing this project studies, but I have not "
    "configured agents beyond ordinary use: no custom skills, no hooks, no worktree "
    "setups. I have also designed a measurement instrument without ever running a "
    "controlled experiment with formal controls and statistics. Your brief lists both as "
    "skills this internship develops, so I will not dress either up. Underneath them "
    "sits Python and C#, code review on a team repository as well as my own, and the "
    "habit of instrumenting a system so the record can answer questions "
    "afterwards. I would arrive having worked through the agent configuration surface in "
    "my own time."
)


# ------------------------------------------------------------------------ letter two
# CURATING REAL-WORLD MANUFACTURING EVALUATION DATASETS, OVERSEER
# A/Prof Scott Barnett, Stefanus Kurniawan.

DATA_P3 = (
    "Your first objective is analysing, cleaning and structuring real partner data into "
    "task-specific evaluation datasets with checkable ground truth. The closest work I "
    "have done to that is the unglamorous half of a project I originated. ParkSense was "
    "a Melbourne parking-availability predictor built for a Deakin Data Science Club "
    "hackathon and it won first place, but my main contribution was not the build. It "
    "was establishing whether the public sensor feed carried enough signal to support "
    "prediction at all, before the team committed to building on it: finding the usable "
    "sources, working out what the feed actually measured rather than what it appeared "
    "to, and separating signal from noise. I would rather be the person who asks whether "
    "the evidence can bear the weight of the capability."
)

DATA_P4 = (
    "The objective I find most interesting is the second, favouring deterministic and "
    "checkable success criteria over subjective judgement. On the Deakin Software "
    "Engineering Club committee I solely designed the defects seeded into a React "
    "application for a debugging workshop of around thirty attendees, which is the same "
    "problem in miniature: a fault is only a usable test if whether it was found is "
    "decidable. In my backend development unit I built a control plane that records "
    "every dispatched and completed action to a queryable execution history and "
    "reconstructs state from that record rather than from what the robot reports, "
    "replaying every reported action through simulation before committing it, because a "
    "half-applied reversal would otherwise log a position the robot was never at. A log "
    "is not yet evidence, and deciding what the record must guarantee before anyone "
    "draws a conclusion from it is the part I want to do more of."
)

DATA_P5 = (
    "Two gaps, named rather than hidden. I have never worked with manufacturing or "
    "industrial data, and I have not built or extended a model evaluation harness or "
    "benchmarked open-weight models. That matters more here than on a pure software "
    "project, so I will not dress it up. What I bring is Python, SQL and PostgreSQL used "
    "on real messy data rather than teaching sets, and the habit of asking what a "
    "dataset can honestly support before it is used to "
    "justify a claim. I would rather spend the first fortnight inside the partner data "
    "than arrive claiming a factory background I do not have."
)


# ---------------------------------------------------------------------- letter three
# SMARTER AI AGENT ROUTING THROUGH TASK UNDERSTANDING
# Dr Aleksandar Pasquini, Prof Rajesh Vasa.

ROUTE_P3 = (
    "The idea in your brief I recognise from my own work is that a system has to know "
    "when the information in front of it is not sufficient to make a reliable choice. On "
    "the smart clothesline robot I built for my embedded systems unit, the rain sensor "
    "was the least reliable component, and one bad reading had real consequences in both "
    "directions: shelter the washing on a clear day, or leave it out in a downpour. "
    "Rather than let a single reading decide, I made it agree with Open-Meteo forecast "
    "data before the robot would commit to moving. The habit that came out of it is "
    "treating a signal as conditionally rather than absolutely reliable, and deciding in "
    "advance what a system should do when its own confidence is the thing in question. "
    "That is a far smaller system than uncertainty-aware routing, but it is the same "
    "instinct, and I arrived at it because the naive version failed."
)

ROUTE_P4 = (
    "Your third objective is a dataset spanning simple to complex tasks with "
    "instructions ranging from clear to genuinely ambiguous, and that is calibration "
    "work I have done at a smaller scale. On the Deakin Software Engineering Club "
    "committee I solely designed the defects seeded into a React application for a "
    "debugging workshop of around thirty attendees. Too obvious and the task measures "
    "nothing, too subtle and it measures only patience, and the ones worth planting are "
    "those someone will confidently declare fixed without having fixed them. Building a "
    "task set graded from clear to ambiguous is the same craft: the difficulty has to be "
    "deliberate, or the results cannot distinguish a router that handles ambiguity from "
    "one that got lucky."
)

ROUTE_P5 = (
    "I should name the gap plainly, because it bites harder here than on the other two "
    "internships the Initiative is offering. I have not used conformal prediction and I "
    "have no formal statistics background beyond my degree. I will not dress that up. "
    "Underneath it sits Python, daily use of language models as a user rather than a "
    "builder, and real comfort with the underlying question, which is when a system "
    "should decline to act on its own answer. I would rather tell you now and arrive "
    "having worked through the conformal prediction basics in my own time than overstate "
    "it here and have you find out in week one."
)


# ---------------------------------------------------------------------------- letters

LETTERS = [
    {
        "file": "Manit Khera Cover Letter - Benchmarking Agent Workflows.docx",
        "recipient": ["Dr Wannita Takerngsaksiri"] + INSTITUTE,
        "salutation": "Dear Dr Takerngsaksiri,",
        "subject": "RE: Application for the Benchmarking Agent Workflows for Software "
                   "Development research internship",
        "body": [
            p1("Benchmarking Agent Workflows for Software Development",
               "yourself and Associate Professor Scott Barnett"),
            P2, BENCH_P3, BENCH_P4, BENCH_P5, CLOSE,
        ],
    },
    {
        "file": "Manit Khera Cover Letter - Manufacturing Evaluation Datasets.docx",
        "recipient": ["Associate Professor Scott Barnett"] + INSTITUTE,
        "salutation": "Dear Associate Professor Barnett,",
        "subject": "RE: Application for the Curating Real-World Manufacturing Evaluation "
                   "Datasets research internship",
        "body": [
            p1("Curating Real-World Manufacturing Evaluation Datasets to Assess the AI "
               "Models and Agentic Harnesses behind Overseer",
               "yourself and Stefanus Kurniawan"),
            P2, DATA_P3, DATA_P4, DATA_P5, CLOSE,
        ],
    },
    {
        "file": "Manit Khera Cover Letter - AI Agent Routing.docx",
        "recipient": ["Dr Aleksandar Pasquini"] + INSTITUTE,
        "salutation": "Dear Dr Pasquini,",
        "subject": "RE: Application for the Smarter AI Agent Routing Through Task "
                   "Understanding research internship",
        "body": [
            p1("Smarter AI Agent Routing Through Task Understanding",
               "yourself and Professor Rajesh Vasa"),
            P2, ROUTE_P3, ROUTE_P4, ROUTE_P5, CLOSE,
        ],
    },
]


def build_letter(spec):
    doc = Document(str(TEMPLATE))
    clear_body(doc)

    block(doc, SENDER)
    para(doc, DATE)
    block(doc, spec["recipient"])

    para(doc, spec["salutation"])
    para(doc, spec["subject"], bold=True)

    for b in spec["body"]:
        para(doc, b)

    para(doc, "Yours sincerely,", space_after=7)
    para(doc, "Manit Khera", space_after=0)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / spec["file"]
    doc.save(out)
    words = sum(len(b.split()) for b in spec["body"])
    print(f"Written: {out.name}  ({words} body words)")
    return out


# Only this one is live. See the decision at the top of this file.
LIVE = "Manit Khera Cover Letter - Benchmarking Agent Workflows.docx"


def build(build_all=False):
    for spec in LETTERS:
        if not build_all and spec["file"] != LIVE:
            continue
        build_letter(spec)
    print("Base template:", TEMPLATE.name)
    if not build_all:
        print("Only the live benchmarking letter was built. Use --all for the other two.")


if __name__ == "__main__":
    import sys
    build(build_all="--all" in sys.argv)
