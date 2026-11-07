"""檢查 research_log 內的相對連結與 frontmatter，並列出缺漏。

檢查項目：
  1. markdown 相對連結 [x](path.md) 與 frontmatter related: [...] 指向的檔案是否存在
  2. ideas/experiments/papers 的檔案是否有 frontmatter，以及 type、status 欄位
  3. ideas 編號是否重複

用法：
    python check_links.py [research_log 目錄，預設 ./research_log]
回傳碼：有問題時為 1。
"""
import glob
import os
import re
import sys

STATUS = {"open", "planned", "supported", "confirmed", "refuted", "superseded", "done"}


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
        print(f"找不到目錄 {base}")
        return 1
    problems = []
    files = glob.glob(os.path.join(base, "**", "*.md"), recursive=True)
    for f in files:
        txt = open(f, encoding="utf-8").read()
        # 略過程式碼區塊內的連結（例如格式範例）
        body = re.sub(r"```.*?```", "", txt, flags=re.S)
        body = re.sub(r"`[^`\n]*`", "", body)  # 行內程式碼（格式範例）
        links = re.findall(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", body)
        fm = frontmatter(txt)
        rel = os.path.relpath(f, base)
        top = rel.split(os.sep)[0]
        if top in ("ideas", "experiments", "papers"):
            if fm is None:
                problems.append(f"{rel}：缺少 frontmatter")
            else:
                if "type" not in fm:
                    problems.append(f"{rel}：frontmatter 缺少 type")
                st = fm.get("status", "")
                if top != "papers" and st and st.split()[0].strip(",") not in STATUS:
                    problems.append(f"{rel}：status「{st}」不在標準詞彙 {sorted(STATUS)}（可接受，但建議統一）")
                if "related" in fm:
                    inner = fm["related"].strip().lstrip("[").rstrip("]")
                    links += [x.strip() for x in inner.split(",") if x.strip()]
        for link in links:
            if link.startswith(("http://", "https://")):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(f), link))
            if not os.path.exists(target):
                problems.append(f"{rel}：連結斷掉 → {link}")

    nums = {}
    for f in glob.glob(os.path.join(base, "ideas", "*.md")):
        m = re.match(r"(\d+)-", os.path.basename(f))
        if m:
            nums.setdefault(m.group(1), []).append(os.path.basename(f))
    for n, fs in nums.items():
        if len(fs) > 1:
            problems.append(f"ideas 編號重複 {n}：{fs}")

    print(f"檢查 {len(files)} 個檔案")
    for p in problems:
        print("  ✗", p)
    if not problems:
        print("  ✓ 沒有問題")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
