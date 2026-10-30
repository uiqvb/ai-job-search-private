"""Build a one-page resume in the master v7 layout from a markdown-style text file.

Layout comes from base.docx beside this script (Calibri, navy headings with thin rules,
right-aligned dates and links, A4). Its body is empty; this script writes the content
back with fixed run properties, then exports <file>.pdf through a private Word instance
and checks the page count.

Adapted from documents/notes/docx-builders/build_master_resume_rewrite.py (v7). The
differences: the input path is an argument, project links and referees come from the
text file instead of being hard-coded, and the links QR is an option (--qr) instead of a
second output.

Source format (see template.txt):

    # NAME
    Suburb, VIC | phone | email
    linkedin | github

    ## PROFILE
    One paragraph.

    ## EDUCATION
    **Degree — University, Campus** | 2025–2028 (expected)
    - bullet

    ## TECHNICAL SKILLS
    **Label:** values

    ## PROJECTS
    **Project name** | tech, tech | [Demo video](url) · [Source code](url)
    - bullet

    ## EXPERIENCE            (any other heading is laid out the same way)
    **Role — Organisation** | Jul 2025–Present
    - bullet

    ## LEADERSHIP            (whole title line bold)

    ## REFERENCES
    **Name** — Role, Organisation | email  |  phone
    (or a plain line such as "Available upon request.")

**text** is bold anywhere in a bullet.

Run from the source's folder:
    python ../templates/cv/master-v7/build_cv.py main_<company>_<role>.txt [--pages N]
    --qr  float links_qr.png (beacons.ai/manit.k, "Scan for links") in the top right corner
Writes main_<company>_<role>.docx and .pdf beside it. Exits 1 unless the page count is N (default 1).
"""

import json
import os
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches

HERE = Path(__file__).resolve().parent
BASE_DOCX = HERE / "base.docx"
# QR to the projects and LinkedIn (beacons.ai/manit.k). Caption is baked into the image.
QR_IMAGE = HERE / "links_qr.png"
QR_WIDTH_IN = 0.68
QR_RAISE_IN = 0.14  # how far it sits up into the top margin, so it clears the PROFILE rule

GREY = "555555"
NAVY = "1F3A5F"

# All in twips (20 = 1pt), from the v7 master. RESUME_LAYOUT='{"line": 220}' overrides any
# value for a one-off squeeze; record it in the application notes if you use it.
LAYOUT = {
    "page_w": 11906, "page_h": 16838,       # A4
    "margin_x": 697, "margin_y": 640,
    "line": 227,                            # exact line pitch for 10pt body
    "bullet_after": 30,
    "entry_before": 80,
    "title_after": 30,
    "section_before": 130,
    "head_after": 40,
    "header_after": 60,
    "rule_sz": 6,
}
LAYOUT.update(json.loads(os.environ.get("RESUME_LAYOUT", "{}")))
L = LAYOUT
TEXT_W = L["page_w"] - 2 * L["margin_x"]

HEAD = '<w:b/><w:sz w:val="21"/>'
DATE = f'<w:i/><w:color w:val="{GREY}"/><w:sz w:val="19"/>'
TECH = f'<w:i/><w:color w:val="{GREY}"/><w:sz w:val="18"/>'
CONTACT = f'<w:color w:val="{GREY}"/><w:sz w:val="19"/>'
BR = "<w:r><w:br/></w:r>"
TAB = "<w:r><w:tab/></w:r>"
LINK = re.compile(r"\[(.+?)\]\((.+?)\)")


def ppr(before=0, after=0, body=True, bullet=False, rule=False):
    out = "<w:pPr>"
    if body:
        out += '<w:pStyle w:val="BodyText"/>'
    if bullet:
        out += '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
    if rule:
        out += (f'<w:pBdr><w:bottom w:val="single" w:sz="{L["rule_sz"]}" w:space="1" '
                f'w:color="{NAVY}"/></w:pBdr>')
    out += f'<w:tabs><w:tab w:val="right" w:pos="{TEXT_W}"/></w:tabs>'
    out += f'<w:spacing w:before="{before}" w:after="{after}" w:line="{L["line"]}" w:lineRule="exact"/>'
    if bullet:
        out += '<w:ind w:left="317" w:hanging="202"/>'
    return out + "</w:pPr>"


def run(text, rpr=""):
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def rich(text, base=""):
    out = []
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            out.append(run(part, base + ("<w:b/><w:bCs/>" if i % 2 else "")))
    return "".join(out)


def para(props, inner):
    return parse_xml(f'<w:p {nsdecls("w", "r")}>{props}{inner}</w:p>')


def split_entry(line, first_bar=False):
    """'**Title** | right' -> (title, right), bold markers dropped. Dates split at the last
    ' | ' (titles never hold one); projects at the first, since their right side holds links."""
    plain = line.strip().replace("**", "")
    if " | " not in plain:
        return plain, ""
    left, _, right = plain.partition(" | ") if first_bar else plain.rpartition(" | ")
    return left.strip(), right.strip()


def role_runs(title, all_bold):
    if all_bold or " — " not in title:
        return run(title, HEAD)
    role, org = title.split(" — ", 1)
    return run(role + " ", HEAD) + run("— " + org, '<w:sz w:val="21"/>')


def parse(path):
    header, sections, current = [], [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            header.append(line[2:].strip())
        elif line.startswith("## "):
            current = (line[3:].strip(), [])
            sections.append(current)
        elif current is None:
            header.append(line.strip())
        else:
            current[1].append(line.strip())
    return header, sections


def build(src, out, with_qr=False):
    header, sections = parse(src)
    doc = Document(str(BASE_DOCX))
    body = doc.element.body
    sect = body.find(qn("w:sectPr"))
    size, margins = sect.find(qn("w:pgSz")), sect.find(qn("w:pgMar"))
    size.set(qn("w:w"), str(L["page_w"]))
    size.set(qn("w:h"), str(L["page_h"]))
    for side in ("left", "right"):
        margins.set(qn(f"w:{side}"), str(L["margin_x"]))
    for side in ("top", "bottom"):
        margins.set(qn(f"w:{side}"), str(L["margin_y"]))

    def add(p):
        sect.addprevious(p)

    def link(text, url):
        rid = doc.part.relate_to(
            url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
            is_external=True)
        return (f'<w:hyperlink r:id="{rid}">'
                + run(text, f'<w:color w:val="{NAVY}"/><w:sz w:val="18"/><w:u w:val="single"/>')
                + "</w:hyperlink>")

    def heading(title, first=False):
        add(para(ppr(before=L["header_after"] if first else L["section_before"],
                     after=L["head_after"], rule=True),
                 run(title, f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="21"/>')))

    def bullet(text):
        add(para(ppr(after=L["bullet_after"], bullet=True), rich(text)))

    def entry(inner, first):
        add(para(ppr(before=0 if first else L["entry_before"], after=L["title_after"]), inner))

    add(para('<w:pPr><w:jc w:val="center"/></w:pPr>',
             run(header[0], f'<w:b/><w:color w:val="{NAVY}"/><w:spacing w:val="50"/><w:sz w:val="42"/>')))
    for line in header[1:]:
        add(para('<w:pPr><w:jc w:val="center"/></w:pPr>', run(line.replace(" | ", "  |  "), CONTACT)))

    if with_qr:
        # Float the QR in the top right corner, anchored to the name line, out of the text flow.
        inline = doc.part.new_pic_inline(str(QR_IMAGE), width=Inches(QR_WIDTH_IN))
        graphic = inline.find(qn("a:graphic"))
        anchor = parse_xml(
            f'<wp:anchor {nsdecls("wp", "a")} distT="0" distB="0" distL="0" distR="0" simplePos="0" '
            'relativeHeight="20" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1">'
            '<wp:simplePos x="0" y="0"/>'
            '<wp:positionH relativeFrom="margin"><wp:align>right</wp:align></wp:positionH>'
            f'<wp:positionV relativeFrom="margin"><wp:posOffset>{-int(Inches(QR_RAISE_IN))}</wp:posOffset></wp:positionV>'
            f'<wp:extent cx="{inline.extent.cx}" cy="{inline.extent.cy}"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>'
            '<wp:docPr id="900" name="Links QR" descr="QR code linking to project demos, source code and LinkedIn"/>'
            '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            '</wp:anchor>')
        anchor.append(graphic)
        qr_run = parse_xml(f'<w:r {nsdecls("w")}><w:drawing/></w:r>')
        qr_run[0].append(anchor)
        body.find(qn("w:p")).append(qr_run)  # the name paragraph
        # stop Word resampling the QR when it saves, so a printed copy still scans
        settings = doc.settings.element
        if settings.find(qn("w:doNotAutoCompressPictures")) is None:
            settings.append(parse_xml(f'<w:doNotAutoCompressPictures {nsdecls("w")}/>'))

    for n, (title, lines) in enumerate(sections):
        heading(title, first=n == 0)
        key = title.upper()

        if key in ("PROFILE", "CAREER PROFILE", "SUMMARY"):
            add(para(ppr(body=False), rich(" ".join(lines))))

        elif key in ("TECHNICAL SKILLS", "SKILLS"):
            rows = []
            for line in lines:
                m = re.match(r"\*\*(.+?)\*\*\s*(.+)$", line)
                rows.append(run(f"{m.group(1)}  {m.group(2)}") if m else rich(line))
            add(para(ppr(body=False), BR.join(rows)))

        elif key == "REFERENCES":
            for line in lines:
                if line.startswith("**"):
                    left, _, right = line.partition(" | ")
                    m = re.match(r"\*\*(.+?)\*\*\s*(.*)$", left)
                    inner = run(m.group(1) + " ", "<w:b/>") + run(m.group(2))
                    if right:
                        inner += TAB + run(right.strip(), CONTACT)
                    add(para(ppr(after=L["bullet_after"]), inner))
                else:
                    add(para(ppr(after=L["bullet_after"]), rich(line)))

        elif key == "EDUCATION":
            first = True
            for line in lines:
                if line.startswith("- "):
                    bullet(line[2:])
                    continue
                degree, dates = split_entry(line)
                it = '<w:i/><w:iCs/><w:sz w:val="21"/>'
                if " — " in degree:
                    course, uni = degree.split(" — ", 1)
                    inner = run(course + " ", it) + run("— ", '<w:sz w:val="21"/>') + run(uni, it)
                else:
                    inner = run(degree, it)
                entry(inner + TAB + run(dates, DATE), first)
                first = False

        elif "PROJECTS" in key:
            first = True
            for line in lines:
                if line.startswith("- "):
                    bullet(line[2:])
                    continue
                name, right = split_entry(line, first_bar=True)
                tech, _, link_part = right.partition(" | ")
                inner = run(name, HEAD)
                if tech:
                    inner += run("  —  ", '<w:sz w:val="21"/>') + run(tech.strip(), TECH)
                links = LINK.findall(link_part)
                if links:
                    sep = run("   ·   ", f'<w:color w:val="{GREY}"/><w:sz w:val="18"/>')
                    inner += TAB + sep.join(link(t, u) for t, u in links)
                entry(inner, first)
                first = False

        else:  # EXPERIENCE, LEADERSHIP, VOLUNTEERING, ...
            first = True
            for line in lines:
                if line.startswith("- "):
                    bullet(line[2:])
                    continue
                name, dates = split_entry(line)
                entry(role_runs(name, key == "LEADERSHIP") + TAB + run(dates, DATE), first)
                first = False

    cp = doc.core_properties
    cp.author = header[0].title()
    cp.title = "Resume"
    try:
        doc.save(str(out))
    except PermissionError:
        sys.exit(f"Cannot write {out.name}: close it in Word and re-run")


def export(path):
    import win32com.client as win32
    pdf = path.with_suffix(".pdf")
    pdf.unlink(missing_ok=True)  # never leave a stale PDF behind a failed export
    word = win32.DispatchEx("Word.Application")  # private instance, never the user's own Word
    word.Visible = False
    try:
        doc = word.Documents.Open(str(path), ReadOnly=True)
        try:
            last = doc.Paragraphs.Last.Range
            bottom = last.Information(6) + L["line"] / 20  # wdVerticalPositionRelativeToPage
            spare = (L["page_h"] - L["margin_y"]) / 20 - bottom
            pages, words, links = doc.ComputeStatistics(2), doc.ComputeStatistics(0), doc.Hyperlinks.Count
            doc.ExportAsFixedFormat(str(pdf), 17, False, 0)
        finally:
            doc.Close(SaveChanges=False)
    finally:
        word.Quit()
    return pages, words, links, spare


def sharpen_qr(pdf):
    """Word exports images at about 200 dpi, which softens the QR. Put the original back."""
    import pymupdf

    doc = pymupdf.open(str(pdf))
    page = doc[0]
    xref = page.get_images(full=True)[0][0]
    rect = page.get_image_rects(xref)[0]
    page.delete_image(xref)
    page.insert_image(rect, filename=str(QR_IMAGE))
    tmp = pdf.with_suffix(".pdf.tmp")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()
    os.replace(tmp, pdf)


def main(argv):
    pages_wanted = 1
    with_qr = "--qr" in argv
    if with_qr:
        argv.remove("--qr")
    if "--pages" in argv:
        i = argv.index("--pages")
        pages_wanted = int(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) != 1:
        sys.exit("usage: build_cv.py <source>.txt [--pages N] [--qr]")
    src = Path(argv[0]).resolve()
    out = src.with_suffix(".docx")
    build(src, out, with_qr)
    pages, words, links, spare = export(out)
    if with_qr:
        sharpen_qr(out.with_suffix(".pdf"))
    print(f"Written: {out.name}, {out.with_suffix('.pdf').name} "
          f"({pages} page(s), {words} words, {links} links, {spare:.1f}pt spare at the foot)")
    if pages != pages_wanted:
        sys.exit(f"FAIL: resume is {pages} page(s), must be exactly {pages_wanted}")


if __name__ == "__main__":
    main(sys.argv[1:])
