import subprocess, json, concurrent.futures as cf
LI = ["bun", "run", ".agents/skills/linkedin-search/cli/src/cli.ts", "search", "--jobage", "14", "--limit", "20", "--format", "json"]
FH = ["bun", "run", ".agents/skills/freehire-search/cli/src/cli.ts", "search", "--jobage", "14", "--limit", "20", "--no-description", "--format", "json"]
M = "Melbourne, Victoria, Australia"
jobs = []
for q in ["robotics intern", "embedded software", "firmware", "software engineer intern", "backend developer junior", ".NET C# junior", "AI intern", "STEM instructor casual", "coding tutor"]:
    jobs.append(("linkedin-search", LI + ["-q", q, "-l", M]))
jobs.append(("linkedin-search", LI + ["-q", "software engineer intern", "-l", "Remote"]))
jobs.append(("linkedin-search", LI + ["-q", "junior developer C#", "-l", "Remote"]))
jobs.append(("freehire-search", FH + ["-q", "robotics OR embedded OR firmware", "--country", "AU"]))
jobs.append(("freehire-search", FH + ["-q", "intern OR junior OR graduate", "--country", "AU"]))
jobs.append(("freehire-search", FH + ["-q", "intern OR junior", "--remote", "remote", "--region", "apac"]))

def run(j):
    p, cmd = j
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    try:
        d = json.loads(r.stdout)
        return p, cmd, d.get("results", []), r.stderr[:200]
    except Exception:
        return p, cmd, None, (r.stderr or r.stdout)[:200]

seen = json.load(open("job_scraper/seen_jobs.json", encoding="utf-8"))["seen"]
seen_urls = {v.get("url", "").split("?")[0] for v in seen.values()}
seen_ct = {(v.get("company", "").lower(), v.get("title", "").lower()) for v in seen.values()}
out = {}
with cf.ThreadPoolExecutor(6) as ex:
    for p, cmd, res, err in ex.map(run, jobs):
        q = cmd[cmd.index("-q") + 1]
        print("##", p, q, "->", None if res is None else len(res), err if res is None else "")
        for x in res or []:
            u = (x.get("url") or "").split("?")[0]
            key = x.get("id") or u
            if u in seen_urls or ((x.get("company") or "").lower(), (x.get("title") or "").lower()) in seen_ct:
                continue
            out[key] = (p, x)
print("NEW", len(out))
for k, (p, x) in out.items():
    print(p[:2], k, "|", x.get("title"), "|", x.get("company"), "|", x.get("location"), "|", x.get("date"))
json.dump({k: {"portal": p, **x} for k, (p, x) in out.items()}, open("job_scraper/_tmp_new.json", "w", encoding="utf-8"))
