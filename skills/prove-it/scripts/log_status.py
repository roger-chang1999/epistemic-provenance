"""Produce a status summary of a research_log, as the starting point for a review (workflow G).

Lists:
  1. Hypothesis overview: grouped by status (parsed from the tables in hypotheses.md)
  2. Nodes waiting on the user: hypotheses and experiments that are proposed / planned / analyzing
  3. Suspected status inconsistencies: a hypothesis is supported/confirmed but a linked experiment
     is not done; a hypothesis is confirmed but every linked experiment has a single seed
  4. Single-seed experiments
  5. Undiscussed decisions: table rows containing "undiscussed" (or the Chinese 未經討論)
  6. Papers with weak evidence: source is not "full text"
  7. Stale ideas: status open/proposed for more than --stale-days days

This is a heuristic summary that points at places worth a look, not a final judgment.
Logs written in English or Chinese are both recognized.

Usage:
    python log_status.py [research_log directory, default ./research_log] [--stale-days 30] [--out report.md]
"""
import argparse
import datetime
import glob
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STATUS = ["open", "proposed", "planned", "analyzing", "supported", "confirmed", "refuted", "superseded", "done"]

# Keywords recognized in both English and Chinese logs.
UNDISCUSSED = ("undiscussed", "未經討論")
DECIDER_HEADER = ("decided by", "決定者")
TYPED_CLAIM = ("implementation", "multi-seed", "multiple seeds", "multi-condition", "multiple conditions",
               "實作類", "多條件", "多 seed", "多seed")
NONSTANDARD = "(non-standard)"


def frontmatter(txt):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", txt, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def first_status(cell):
    """Return the first standard status word in a cell, or None."""
    for w in re.findall(r"[A-Za-z]+", cell):
        if w.lower() in STATUS:
            return w.lower()
    return None


def seed_count(fm):
    s = fm.get("seeds", "").strip().lstrip("[").rstrip("]")
    return len([x for x in s.split(",") if x.strip()]) if s else 0


def full_text_read(src):
    """True when a paper's source says the full text was read (English or Chinese)."""
    low = src.lower()
    if "全文" in src and "未" not in src:
        return True
    return "full text" in low and not re.search(r"\bnot\b|\bunread\b|\bno\b", low)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", nargs="?", default="research_log")
    ap.add_argument("--stale-days", type=int, default=30)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    base = a.base
    if not os.path.isdir(base):
        print(f"Directory not found: {base}")
        return 1
    today = datetime.date.today()
    out = []
    P = out.append

    # ---- experiments ----
    exps = {}
    for f in sorted(glob.glob(os.path.join(base, "experiments", "*.md"))):
        fm = frontmatter(read(f))
        exps[os.path.basename(f)] = {"status": fm.get("status", "?"), "seeds": seed_count(fm),
                                     "date": fm.get("date", "")}

    # ---- hypotheses ----
    hyps = []
    hpath = os.path.join(base, "hypotheses.md")
    if os.path.exists(hpath):
        section = ""
        for line in read(hpath).splitlines():
            if line.startswith("## "):
                section = line[3:].strip()
            m = re.match(r"^\|\s*(H\d+)\s*\|(.*)$", line)
            if not m:
                continue
            cells = [c.strip() for c in m.group(2).split("|")]
            text = cells[0] if cells else ""
            status_cell = cells[1] if len(cells) > 1 else ""
            evidence = " ".join(cells[2:])
            linked = re.findall(r"experiments/([^)\s]+\.md)", evidence)
            hyps.append({"id": m.group(1), "text": text, "status": first_status(status_cell),
                         "status_raw": re.sub(r"\*", "", status_cell), "section": section,
                         "linked": linked})

    P(f"# Research log status summary ({today.isoformat()})\n")
    P(f"Source: `{os.path.abspath(base)}`. A heuristic summary that flags places worth checking, not a final judgment.\n")

    P("## 1. Hypothesis overview\n")
    if hyps:
        P("| Status | Count | Hypotheses |")
        P("|---|---|---|")
        groups = {}
        for h in hyps:
            groups.setdefault(h["status"] or NONSTANDARD, []).append(h["id"])
        for st in STATUS + [NONSTANDARD]:
            if st in groups:
                P(f"| {st} | {len(groups[st])} | {', '.join(groups[st])} |")
    else:
        P("(No table rows starting with `| H# |` found in hypotheses.md)")
    P("")

    P("## 2. Nodes waiting on the user (proposed / planned / analyzing)\n")
    waiting = [h for h in hyps if h["status"] in ("proposed", "planned", "analyzing")]
    waiting_exp = [k for k, v in exps.items() if v["status"] in ("proposed", "planned", "analyzing")]
    if waiting or waiting_exp:
        for h in waiting:
            P(f"- {h['id']} ({h['status']}): {h['text'][:70]}")
        for k in waiting_exp:
            P(f"- experiments/{k} ({exps[k]['status']})")
    else:
        P("- None")
    P("")

    P("## 3. Suspected status inconsistencies\n")
    issues = []
    for h in hyps:
        for e in h["linked"]:
            if e not in exps:
                issues.append(f"- {h['id']} links to a nonexistent experiment experiments/{e}")
                continue
            if h["status"] in ("supported", "confirmed") and exps[e]["status"] not in ("done",):
                issues.append(f"- {h['id']} is {h['status']}, but the linked experiments/{e} has status {exps[e]['status']}")
        raw = h["status_raw"].lower()
        typed = any(k in raw for k in TYPED_CLAIM)
        if (h["status"] == "confirmed" and not typed and h["linked"]
                and all(exps.get(e, {}).get("seeds", 0) <= 1 for e in h["linked"])):
            issues.append(f"- {h['id']} is confirmed, but every linked experiment has ≤1 seed: check the claim type "
                          "(implementation claims need a validation test with a known answer; experimental claims need "
                          "multiple seeds or conditions; literature-dependent claims should stay supported)")
        if h["status"] in ("supported", "confirmed", "refuted") and not h["linked"]:
            issues.append(f"- {h['id']} is {h['status']}, but its evidence cell links to no experiment record")
    P("\n".join(issues) if issues else "- None")
    P("")

    P("## 4. Single-seed experiments\n")
    single = [k for k, v in exps.items() if v["seeds"] <= 1 and v["status"] == "done"]
    P("\n".join(f"- experiments/{k} (seeds: {exps[k]['seeds']})" for k in single) if single else "- None")
    P("")

    P("## 5. Undiscussed decisions\n")
    hits = []
    for f in sorted(glob.glob(os.path.join(base, "**", "*.md"), recursive=True)):
        for i, line in enumerate(read(f).splitlines(), 1):
            low = line.lower()
            if (any(k in low for k in UNDISCUSSED) and line.lstrip().startswith("|")
                    and not any(k in low for k in DECIDER_HEADER)):
                hits.append(f"- {os.path.relpath(f, base)}:{i}: {line.strip()[:100]}")
    P("\n".join(hits) if hits else "- None")
    P("")

    P("## 6. Papers with weak evidence (source is not full text)\n")
    weak = []
    for f in sorted(glob.glob(os.path.join(base, "papers", "*.md"))):
        src = frontmatter(read(f)).get("source", "")
        if not src or not full_text_read(src):
            weak.append(f"- papers/{os.path.basename(f)}: {src or '(no source given)'}")
    P("\n".join(weak) if weak else "- None")
    P("")

    P(f"## 7. Ideas open / proposed for more than {a.stale_days} days\n")
    stale = []
    for f in sorted(glob.glob(os.path.join(base, "ideas", "*.md"))):
        fm = frontmatter(read(f))
        st = first_status(fm.get("status", ""))
        try:
            d = datetime.date.fromisoformat(fm.get("date", "")[:10])
        except ValueError:
            continue
        if st in ("open", "proposed") and (today - d).days > a.stale_days:
            stale.append(f"- ideas/{os.path.basename(f)} ({st}, {(today - d).days} days)")
    P("\n".join(stale) if stale else "- None")
    P("")

    report = "\n".join(out)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(report)
        print("Written to", a.out)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
