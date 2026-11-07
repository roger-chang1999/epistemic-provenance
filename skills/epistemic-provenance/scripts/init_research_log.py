"""在專案中建立 research_log/ 骨架。已存在的檔案不會被覆蓋。

用法：
    python init_research_log.py <專案根目錄> --project "<專案名稱>" [--dir research_log]
"""
import argparse
import datetime
import os
import sys

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
    ap.add_argument("root", help="專案根目錄")
    ap.add_argument("--project", required=True, help="專案名稱")
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
        "# {{一句話標題：這次思考轉折是什麼}}（主線 {{N}}）",
        f"# 研究起點：{a.project} 的原始研究動機（主線一）")
    write_new(os.path.join(base, "ideas", "001-origin.md"), origin, created, skipped)
    for sub in ["experiments", "papers"]:
        keep = os.path.join(base, sub, ".gitkeep")
        if not os.listdir(os.path.join(base, sub)):
            write_new(keep, "", created, skipped)

    print(f"research log：{os.path.abspath(base)}")
    for p in created:
        print("  建立", os.path.relpath(p, base))
    for p in skipped:
        print("  已存在，略過", os.path.relpath(p, base))
    print("下一步：填入 README.md 的因果線、methods.md 的第一個協定、hypotheses.md 的初始假設、ideas/001-origin.md。")


if __name__ == "__main__":
    sys.exit(main())
