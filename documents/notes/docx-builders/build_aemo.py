# -*- coding: utf-8 -*-
"""Derive the AEMO-targeted resume from 1_Manit_Khera_Resume.docx.

Edits run text in place so all styling, tabs and hyperlinks survive.
"""
import shutil, docx

SRC = r"C:\Users\Manit Khera\Documents\Resume\Resume_Versions\1_Manit_Khera_Resume.docx"
DST = r"C:\Users\Manit Khera\Documents\Resume\Resume_Versions\Manit_Khera_Resume_AEMO.docx"

shutil.copyfile(SRC, DST)
d = docx.Document(DST)
P = d.paragraphs


def set_para(i, text, expect):
    """Replace a single-run paragraph's text, asserting we hit the right one."""
    p = P[i]
    assert expect in p.text, "para %d changed: %r" % (i, p.text)
    assert len(p.runs) == 1, "para %d has %d runs" % (i, len(p.runs))
    p.runs[0].text = text


# --- 1. PROFILE -------------------------------------------------------------
# runs: r3 lead-in | r4 'a current ' | r5 'grade of High Distinction ' (bold)
# | r6 tail.  Keep the bold run so the emphasis survives.
prof = P[3]
assert "targeting backend and embedded" in prof.text
prof.runs[3].text = "Software Engineering (Honours) student at Deakin University with "
prof.runs[4].text = "a "
prof.runs[5].text = "High Distinction average"
prof.runs[6].text = (
    ", applying to AEMO's Internship Talent Pool. My work sits where software meets "
    "physical systems \u2014 autonomous control driven by live sensor telemetry and "
    "forecast data \u2014 with top results in Backend Development, Data Structures & "
    "Algorithms and Embedded Systems."
)

# --- 2. Robot Controller Platform: restore the grade ------------------------
set_para(
    21,
    "Built a REST platform coordinating autonomous robots across 18 controllers "
    "and 14 bounded contexts; awarded 100/100.",
    "hardware-neutral REST platform",
)

# --- 3. Smart Clothesline Robot: lead with sensing + forecast logic ---------
set_para(
    26,
    "Built an autonomous robot that shelters washing unaided, fusing line, light "
    "and rain sensor input in real time.",
    "autonomous clothesline robot using line",
)
set_para(
    27,
    "Developed a Flask dashboard and MQTT pipeline streaming live telemetry and "
    "dispatching remote commands.",
    "Flask dashboard and MQTT pipeline",
)
set_para(
    28,
    "Added a forecast fallback that cross-checks unreliable rain readings against "
    "Open-Meteo to act on predicted risk.",
    "forecast-based safety logic",
)

# --- 4. ParkSense: name the live sensor feed and the prediction horizon -----
set_para(
    31,
    "Originated ParkSense and validated live City of Melbourne sensor data for "
    "short-horizon occupancy prediction.",
    "validated Melbourne parking data",
)

# --- 5. DSEC: keep the defensible individual claim -------------------------
set_para(
    41,
    "Built the React app behind a 30-attendee debugging workshop and solely "
    "designed its seeded defects.",
    "React debugging workshop application",
)

d.save(DST)
print("saved", DST)
