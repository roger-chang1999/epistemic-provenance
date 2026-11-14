"""Create a research_log/ skeleton in a project. Existing files are never overwritten.

Usage:
    python init_research_log.py <project root> --project "<project name>" [--dir research_log]
"""
import argparse
import datetime
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "..", "assets", "templates")

HUB_FILES = ["README.md", "hypotheses.md", "methods.md",
             "research_tree_overview.md", "comparison_catalog.md"]


def render(name, project, today):
    with open(os.path.join(TPL, name), encoding="utf-8") as f:
        txt = f.read()
    return txt.replace("{{PROJECT}}", project).replace("{{YYYY-MM-DD}}", today)


def write_new(path, content, created, skipped):
    if os.path.exists(path):
        skipped.append(path)
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    created.append(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="project root directory")
    ap.add_argument("--project", required=True, help="project name")
    ap.add_argument("--dir", default="research_log")
    a = ap.parse_args()

    today = datetime.date.today().isoformat()
    base = os.path.join(a.root, a.dir)
    for sub in ["", "ideas", "experiments", "papers"]:
        os.makedirs(os.path.join(base, sub), exist_ok=True)

    created, skipped = [], []
    for name in HUB_FILES:
        write_new(os.path.join(base, name), render(name, a.project, today), created, skipped)
    origin = render("idea.md", a.project, today).replace(
        "# {{One-line title: what this turn in thinking is}} (line {{N}})",
        f"# Starting point: the original research motivation of {a.project} (line 1)")
    write_new(os.path.join(base, "ideas", "001-origin.md"), origin, created, skipped)
    for sub in ["experiments", "papers"]:
        keep = os.path.join(base, sub, ".gitkeep")
        if not os.listdir(os.path.join(base, sub)):
            write_new(keep, "", created, skipped)

    print(f"research log: {os.path.abspath(base)}")
    for p in created:
        print("  created", os.path.relpath(p, base))
    for p in skipped:
        print("  exists, skipped", os.path.relpath(p, base))
    print("Next: fill in the log language and causal lines in README.md, the first protocol in methods.md, "
          "the initial hypotheses in hypotheses.md, and ideas/001-origin.md. "
          "Templates are in English; translate headings when the log language differs.")


if __name__ == "__main__":
    sys.exit(main())
