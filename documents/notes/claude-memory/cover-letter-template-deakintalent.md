---
name: cover-letter-template-deakintalent
description: "Default cover letter template is the DeakinTALENT Word template, not LaTeX cover.cls"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f501b398-3f78-43f2-807b-216f97410542
  modified: 2026-10-20T08:23:32.919Z
---

Cover letters use the DeakinTALENT Word template by default (set 2026-10-20). Registered at `templates/cover_letters/deakintalent/`: write `cover_letters/cover_<company>_<role>.txt`, run its `build_cover.py` from `cover_letters/` to get `.docx` + `.pdf` (Word does the export and page count). CVs stay LaTeX moderncv.

**Why:** Manit asked to switch the CL template to "the one from DT" and keep it as the default from now on.

**How to apply:** Never draft a cover letter in cover.cls unless Manit asks; the `ACTIVE-TEMPLATE` block in `06-cover-letter-templates.md` is the source of truth. Prose only, "Kind regards,", guide section 4a rules.
