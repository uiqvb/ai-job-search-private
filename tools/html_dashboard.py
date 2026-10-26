import csv, html, math, re, sys, datetime
from pathlib import Path
from collections import Counter

REPO = Path.home() / "Documents" / "ai-job-search"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "reports" / "application-dashboard.html"
FIELDS = "date,company,sector,role,role_type,channel,status,contact_person,fit_rating,notes,cv_file,cover_letter_file,source,deadline".split(",")
COL = {"Drafted": "#64748b", "Active": "#3b82f6", "Interview": "#f59e0b", "Offer": "#8b5cf6", "Hired": "#22c55e", "Rejected/Closed": "#ef4444"}
ORDER = list(COL)
e = lambda s: html.escape(str(s or ""), quote=True)
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower())

rows = []
with open(REPO / "job_search_tracker.csv", encoding="utf-8", newline="") as fh:
    for raw in csv.reader(fh):
        if raw and raw[0] == "date":
            continue
        raw += [""] * (len(FIELDS) - len(raw))
        rows.append(dict(zip(FIELDS, raw)))

unknown = set()
def bucket(s):
    s = (s or "").strip().lower()
    m = {"drafted": "Drafted", "applied": "Active", "interview": "Interview", "offer": "Offer", "hired": "Hired"}
    if s in m: return m[s]
    if s in {"rejected", "no_response", "no response", "offer_declined", "offer declined", "withdrawn"}: return "Rejected/Closed"
    unknown.add(s); return "Rejected/Closed"

# outcome.md merge
outcomes = {}
for om in (REPO / "documents" / "applications").glob("*/outcome.md"):
    t = om.read_text(encoding="utf-8")
    m = re.search(r"# Outcome:\s*(.+?)\s+—\s+(.+)", t)
    key = norm(m.group(1) + m.group(2)) if m else norm(om.parent.name)
    ticked = {s.strip().lower() for s in re.findall(r"- \[x\]\s*([^\n(]+)", t, re.I)}
    outcomes[key] = ticked
for r in rows:
    r["bucket"] = bucket(r["status"])
    r["stages"] = outcomes.get(norm(r["company"] + r["role"]), set())

sent = [r for r in rows if r["bucket"] != "Drafted"]
drafted = len(rows) - len(sent)
bc = Counter(r["bucket"] for r in rows)
def reached(r, stage):
    b, st = r["bucket"], r["stages"]
    interview_ticked = any(k in st for k in ("phone screen", "technical interview", "case interview", "final round"))
    if stage == "Applied": return True
    if stage == "Interview": return b in {"Interview", "Offer", "Hired"} or interview_ticked or "offer received" in st
    if stage == "Offer": return b in {"Offer", "Hired"} or "offer received" in st or r["status"].lower().replace(" ", "_") == "offer_declined"
    if stage == "Hired": return b == "Hired"
funnel = [(s, sum(reached(r, s) for r in sent)) for s in ("Applied", "Interview", "Offer", "Hired")]
past_screen = round(100 * funnel[1][1] / len(sent)) if sent else 0
final = [r for r in sent if r["status"].lower().replace(" ", "_") in {"rejected", "no_response", "offer_declined", "withdrawn", "hired"}]
rej = sum(r["status"].lower().replace(" ", "_") in {"rejected", "no_response"} for r in final)
rej_rate = f"{round(100*rej/len(final))}% ({rej} of {len(final)} resolved)" if final else "—"
sectors = Counter(r["sector"] or "—" for r in sent).most_common()
channels = Counter(r["channel"] or "other" for r in sent).most_common()
months = Counter(r["date"][:7] for r in sent if r["date"])

def doughnut():
    data = [(b, bc[b]) for b in ORDER if bc[b]]
    total = sum(n for _, n in data); cx = cy = 90; R, r0 = 80, 50; a = -math.pi / 2; parts = []
    for b, n in data:
        frac = n / total
        if frac >= 0.9999:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{(R+r0)/2}" fill="none" stroke="{COL[b]}" stroke-width="{R-r0}"><title>{e(b)}: {n}</title></circle>'); continue
        a2 = a + frac * 2 * math.pi; lg = 1 if frac > 0.5 else 0
        p = lambda rad, ang: (cx + rad * math.cos(ang), cy + rad * math.sin(ang))
        x1, y1 = p(R, a); x2, y2 = p(R, a2); x3, y3 = p(r0, a2); x4, y4 = p(r0, a)
        parts.append(f'<path d="M{x1:.2f},{y1:.2f} A{R},{R} 0 {lg} 1 {x2:.2f},{y2:.2f} L{x3:.2f},{y3:.2f} A{r0},{r0} 0 {lg} 0 {x4:.2f},{y4:.2f} Z" fill="{COL[b]}"><title>{e(b)}: {n}</title></path>')
        a = a2
    legend = "".join(f'<rect x="200" y="{20+i*24}" width="14" height="14" rx="3" fill="{COL[b]}"/><text x="222" y="{32+i*24}" class="lbl">{e(b)} · {n}</text>' for i, (b, n) in enumerate(data))
    label = "Status breakdown: " + ", ".join(f"{n} {b}" for b, n in data)
    return f'<svg viewBox="0 0 380 180" role="img" aria-label="{e(label)}">{"".join(parts)}<text x="{cx}" y="{cy+6}" text-anchor="middle" class="big">{total}</text>{legend}</svg>'

def hbar(items, title, color="var(--active)"):
    mx = max([n for _, n in items] or [1]); h = 26; w = 200; lw = 150
    out = []
    for i, (k, n) in enumerate(items):
        y = 6 + i * h; bw = max(2, w * n / mx) if n else 0
        out.append(f'<text x="{lw-8}" y="{y+15}" text-anchor="end" class="lbl">{e(k)}</text><rect x="{lw}" y="{y+2}" width="{bw:.1f}" height="18" rx="4" fill="{color}"><title>{e(k)}: {n}</title></rect><text x="{lw+bw+6:.1f}" y="{y+15}" class="lbl">{n}</text>')
    label = f"{title}: " + ", ".join(f"{k} {n}" for k, n in items)
    return f'<svg viewBox="0 0 400 {12+len(items)*h}" role="img" aria-label="{e(label)}">{"".join(out)}</svg>'

def card(label, n, color):
    return f'<div class="card" style="border-left-color:{color}"><div class="num">{n}</div><div class="cl">{e(label)}</div></div>'

def cell(v): return e(v) if v else "—"
def src(v): return f'<a href="{e(v)}" target="_blank" rel="noopener">link</a>' if v.startswith("http") else "—"
def note(v):
    if not v: return "—"
    short = v if len(v) <= 80 else v[:79] + "…"
    return f'<span title="{e(v)}">{e(short)}</span>'

rows_sorted = sorted(rows, key=lambda r: r["company"].lower())
rows_sorted = sorted(rows_sorted, key=lambda r: r["date"], reverse=True)
trs = "".join(
    f'<tr data-status="{e(r["bucket"])}" data-sector="{e(r["sector"] or "—")}" data-text="{e((r["company"]+" "+r["role"]+" "+r["sector"]).lower())}">'
    f'<td>{cell(r["date"])}</td><td>{cell(r["deadline"])}</td><td><b>{cell(r["company"])}</b></td><td>{cell(r["role"])}</td><td>{cell(r["sector"])}</td>'
    f'<td>{cell(r["channel"])}</td><td><span class="pill" style="background:{COL[r["bucket"]]}">{e(r["bucket"])}</span></td><td class="notes">{note(r["notes"])}</td><td>{src(r["source"])}</td></tr>'
    for r in rows_sorted)
# Planned (not yet sent) opportunities: separate file, never counted in the stats above
planned = []
pf = REPO / "planned_applications.csv"
if pf.exists():
    with open(pf, encoding="utf-8", newline="") as fh:
        planned = list(csv.DictReader(fh))
PRI = {"High": "#16a34a", "Medium": "#d97706", "Low": "#64748b"}
porder = {"High": 0, "Medium": 1, "Low": 2}
planned.sort(key=lambda p: (porder.get(p["priority"], 3), p["type"], p["company"].lower()))
ptrs = "".join(
    f'<tr data-pri="{e(p["priority"])}" data-type="{e(p["type"])}" data-text="{e((p["company"]+" "+p["opportunity"]+" "+p["why"]+" "+p["location"]).lower())}">'
    f'<td><span class="pill" style="background:{PRI.get(p["priority"], "#64748b")}">{e(p["priority"])}</span></td><td><b>{cell(p["company"])}</b></td><td>{cell(p["opportunity"])}</td>'
    f'<td>{cell(p["type"])}</td><td>{cell(p["send_as"])}</td><td>{cell(p["location"])}</td><td>{cell(p["deadline"])}</td><td class="notes">{note(p["why"])}</td>'
    f'<td class="notes">{note(p["contact"])}</td><td class="notes">{note(p["next_step"])}</td><td>{src(p["source"])}</td></tr>'
    for p in planned)
pcount = Counter(p["priority"] for p in planned)
opt = lambda vals: "".join(f'<option value="{e(v)}">{e(v)}</option>' for v in vals)
today = datetime.date.today().isoformat()
unk = f'<p class="muted">Unrecognised status values counted as Rejected/Closed: {e(", ".join(sorted(unknown)))}</p>' if unknown else ""
season = " · ".join(f"{e(k)}: {v}" for k, v in sorted(months.items()))

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Job Search Dashboard</title><style>
:root{{--drafted:#64748b;--active:#3b82f6;--interview:#f59e0b;--offer:#8b5cf6;--hired:#22c55e;--rejected:#ef4444;--bg:#f1f5f9;--card:#fff;--text:#0f172a;--muted:#64748b;--line:#e2e8f0}}
*{{box-sizing:border-box}}body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text)}}
.wrap{{max-width:1200px;margin:0 auto;padding:24px 16px}}header{{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px}}
h1{{margin:0;font-size:24px}}.muted{{color:var(--muted);font-size:13px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:20px 0}}
.card{{background:var(--card);border-radius:10px;padding:14px 16px;box-shadow:0 1px 3px rgba(0,0,0,.08);border-left:5px solid}}
.num{{font-size:30px;font-weight:700}}.cl{{color:var(--muted);font-size:13px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.chart-card{{background:var(--card);border-radius:10px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}.chart-card h3{{margin:0 0 10px;font-size:15px}}
svg{{width:100%;height:auto}}.lbl{{font-size:12px;fill:var(--text)}}.big{{font-size:28px;font-weight:700;fill:var(--text)}}
.stats{{background:var(--card);border-radius:10px;padding:12px 16px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:16px;font-size:14px;line-height:1.7}}
.tablecard{{background:var(--card);border-radius:10px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.08);overflow-x:auto}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 12px}}select,input{{padding:7px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;font-size:14px}}input{{flex:1;min-width:180px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}th{{text-align:left;padding:8px;border-bottom:2px solid var(--line);white-space:nowrap}}td{{padding:8px;border-bottom:1px solid var(--line);vertical-align:top}}
tbody tr:nth-child(even){{background:#f8fafc}}.pill{{color:#fff;border-radius:999px;padding:2px 9px;font-size:12px;white-space:nowrap}}.notes{{max-width:320px;color:#334155}}
a{{color:var(--active)}}footer{{text-align:center;color:var(--muted);font-size:12px;margin:24px 0}}
</style></head><body><div class="wrap">
<header><h1>🔍 Job Search Dashboard</h1><span class="muted">Generated: {today}</span></header>
<div class="cards">{card("Sent", len(sent), "#0f172a")}{card("Drafted", drafted, COL["Drafted"])}{card("Active", bc["Active"], COL["Active"])}{card("Interview", bc["Interview"], COL["Interview"])}{card("Offer", bc["Offer"], COL["Offer"])}{card("Hired", bc["Hired"], COL["Hired"])}{card("Rejected/Closed", bc["Rejected/Closed"], COL["Rejected/Closed"])}{card("Planned (not sent)", len(planned), "#16a34a") if planned else ""}</div>
<div class="stats"><b>Past resume screen:</b> {past_screen}% · <b>Rejection rate:</b> {e(rej_rate)} · <b>By month sent:</b> {season}{unk}<br><span class="muted">Drafted applications are left out of every number except the Drafted card and the status chart.</span></div>
<div class="grid"><div class="chart-card"><h3>Status breakdown</h3>{doughnut()}</div><div class="chart-card"><h3>By sector</h3>{hbar(sectors, "By sector")}</div></div>
<div class="grid"><div class="chart-card"><h3>By channel</h3>{hbar(channels, "By channel", "#0ea5e9")}</div><div class="chart-card"><h3>Application funnel</h3>{hbar(funnel, "Funnel", "#f59e0b")}</div></div>
<div class="tablecard"><h3 style="margin:0">Applications ({len(rows)})</h3>
<div class="filters"><select id="fs"><option value="">All statuses</option>{opt([b for b in ORDER if bc[b]])}</select>
<select id="fc"><option value="">All sectors</option>{opt(sorted({r["sector"] or "—" for r in rows}))}</select><input id="fq" type="search" placeholder="🔍 Search company, role, sector"></div>
<table><thead><tr><th>Date</th><th>Deadline</th><th>Company</th><th>Role</th><th>Sector</th><th>Channel</th><th>Status</th><th>Notes</th><th>Source</th></tr></thead><tbody id="tb">{trs}</tbody></table></div>
{f'''<div class="tablecard" style="margin-top:16px"><h3 style="margin:0">Planned: to send ({len(planned)})</h3>
<p class="muted" style="margin:4px 0 0">Not sent yet, so not counted in any number above. High {pcount["High"]} · Medium {pcount["Medium"]} · Low {pcount["Low"]}. Source: planned_applications.csv</p>
<div class="filters"><select id="pp"><option value="">All priorities</option>{opt([k for k in ("High","Medium","Low") if pcount[k]])}</select>
<select id="pt"><option value="">All types</option>{opt(sorted({p["type"] for p in planned}))}</select><input id="pq" type="search" placeholder="🔍 Search company, opportunity, location"></div>
<table><thead><tr><th>Priority</th><th>Company</th><th>Opportunity</th><th>Type</th><th>Send as</th><th>Location</th><th>Deadline</th><th>Why</th><th>Contact</th><th>Next step</th><th>Source</th></tr></thead><tbody id="ptb">{ptrs}</tbody></table></div>''' if planned else ""}
<footer>Generated by Claude Code · ai-job-search · {today}</footer></div>
<script>
const fs=document.getElementById('fs'),fc=document.getElementById('fc'),fq=document.getElementById('fq');
function f(){{const s=fs.value,c=fc.value,q=fq.value.trim().toLowerCase();
for(const tr of document.querySelectorAll('#tb tr')){{const ok=(!s||tr.dataset.status===s)&&(!c||tr.dataset.sector===c)&&(!q||tr.dataset.text.includes(q));tr.style.display=ok?'':'none';}}}}
[fs,fc].forEach(x=>x.addEventListener('change',f));fq.addEventListener('input',f);
const pp=document.getElementById('pp'),pt=document.getElementById('pt'),pq=document.getElementById('pq');
function g(){{const p=pp.value,t=pt.value,q=pq.value.trim().toLowerCase();
for(const tr of document.querySelectorAll('#ptb tr')){{const ok=(!p||tr.dataset.pri===p)&&(!t||tr.dataset.type===t)&&(!q||tr.dataset.text.includes(q));tr.style.display=ok?'':'none';}}}}
if(pp){{[pp,pt].forEach(x=>x.addEventListener('change',g));pq.addEventListener('input',g);}}
</script></body></html>"""
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print(f"OUT={OUT}\nsent={len(sent)} drafted={drafted} buckets={dict(bc)} funnel={funnel} past_screen={past_screen}% rejection={rej_rate} unknown={unknown} outcomes_matched={sum(1 for r in rows if (norm(r['company']+r['role']) in outcomes))}")
