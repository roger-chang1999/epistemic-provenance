"""Check the relative links and frontmatter in a research_log and list problems.

Checks:
  1. Whether files targeted by markdown relative links [x](path.md) and frontmatter related: [...] exist
  2. Whether files in ideas/experiments/papers have frontmatter with type and status fields
  3. Whether idea numbers are duplicated

Usage:
    python check_links.py [research_log directory, default ./research_log]
Exit code: 1 when problems are found.
"""
import glob
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STATUS = {"open", "proposed", "planned", "analyzing", "supported", "confirmed", "refuted", "superseded", "done"}


def frontmatter(txt):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", txt, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "research_log"
    if not os.path.isdir(base):
        print(f"Directory not found: {base}")
        return 1
    problems = []
    files = glob.glob(os.path.join(base, "**", "*.md"), recursive=True)
    for f in files:
        txt = open(f, encoding="utf-8").read()
        # Skip links inside code blocks (e.g. format examples)
        body = re.sub(r"```.*?```", "", txt, flags=re.S)
        body = re.sub(r"`[^`\n]*`", "", body)  # inline code (format examples)
        links = re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", body)
        fm = frontmatter(txt)
        rel = os.path.relpath(f, base)
        top = rel.split(os.sep)[0]
        if top in ("ideas", "experiments", "papers"):
            if fm is None:
                problems.append(f"{rel}: missing frontmatter")
            else:
                if "type" not in fm:
                    problems.append(f"{rel}: frontmatter missing type")
                st = fm.get("status", "")
                if top != "papers" and st and st.split()[0].strip(",") not in STATUS:
                    problems.append(f"{rel}: status '{st}' is not in the standard vocabulary {sorted(STATUS)} "
                                    "(acceptable, but consistency is recommended)")
                if "related" in fm:
                    inner = fm["related"].strip().lstrip("[").rstrip("]")
                    links += [x.strip() for x in inner.split(",") if x.strip()]
        for link in links:
            if link.startswith(("http://", "https://")):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(f), link))
            if not os.path.exists(target):
                problems.append(f"{rel}: broken link → {link}")

    nums = {}
    for f in glob.glob(os.path.join(base, "ideas", "*.md")):
        m = re.match(r"(\d+)-", os.path.basename(f))
        if m:
            nums.setdefault(m.group(1), []).append(os.path.basename(f))
    for n, fs in nums.items():
        if len(fs) > 1:
            problems.append(f"duplicate idea number {n}: {fs}")

    print(f"Checked {len(files)} files")
    for p in problems:
        print("  ✗", p)
    if not problems:
        print("  ✓ No problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
