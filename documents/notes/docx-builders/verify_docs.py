"""Open .docx files in Word, report page and word counts, and export a PDF beside each.

CLAUDE.md rule: check the page count with Word COM rather than guessing, especially in
Verdana. This is the shared checker rather than another copy inside each build script.

Run:  python Scripts/verify_docs.py "<path>.docx" ["<path>.docx" ...]
"""

import sys
from pathlib import Path

import win32com.client as win32

WD_STATISTIC_PAGES = 2
WD_STATISTIC_WORDS = 0
WD_FORMAT_PDF = 17


def main(paths):
    word = win32.gencache.EnsureDispatch("Word.Application")
    word.Visible = False
    try:
        for raw in paths:
            p = Path(raw).resolve()
            doc = word.Documents.Open(str(p), ReadOnly=False)
            try:
                pages = doc.ComputeStatistics(WD_STATISTIC_PAGES)
                words = doc.ComputeStatistics(WD_STATISTIC_WORDS)
                links = doc.Hyperlinks.Count
                pdf = p.with_suffix(".pdf")
                doc.SaveAs(str(pdf), FileFormat=WD_FORMAT_PDF)
                print(f"{p.name}: {pages} page(s), {words} words, {links} hyperlink(s)")
                print(f"  PDF: {pdf}")
            finally:
                doc.Close(SaveChanges=False)
    finally:
        word.Quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python Scripts/verify_docs.py <file.docx> [...]")
    main(sys.argv[1:])
