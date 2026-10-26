---
name: cv-template-master-v7
description: "Default CV is the one-page master v7 Word layout, not 2-page LaTeX moderncv"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f501b398-3f78-43f2-807b-216f97410542
  modified: 2026-10-20T08:49:35.734Z
---

Resumes are one page, in the master v7 Word layout (set 2026-10-20). Registered at `templates/cv/master-v7/`: write `cv/main_<company>_<role>.txt` (start from `documents/cv/Manit_Khera_Resume_Rewrite.md`), run its `build_cv.py` from `cv/` to get `.docx` + `.pdf`; it fails unless Word reports exactly 1 page.

**Why:** Manit: "in aus we have 1 page resumes"; he wants the template he has been following (v7, used for Andromeda/Tekt/NxtGen) as the default.

**How to apply:** Cut copy to fit, never shrink the layout. Pairs with [[cover-letter-template-deakintalent]]. ATS text dumps go to `.ats.txt`, never `.txt` (that is the source).
