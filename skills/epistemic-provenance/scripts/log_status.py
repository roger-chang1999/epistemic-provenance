"""產生 research_log 的狀態總表，作為審查（工作流程 G）的起點。

列出：
  1. 假設總覽：依狀態分組（從 hypotheses.md 的表格解析）
  2. 等待使用者的 node：proposed / planned 的假設與實驗
  3. 疑似狀態不一致：假設是 supported/confirmed，但連到的實驗尚未完成；
     假設是 confirmed，但連到的實驗都只有單一 seed
  4. 單一 seed 的實驗
  5. 未經討論的決策：檔案中「未經討論」出現的位置
  6. 證據強度較弱的文獻：source 不是「全文」
  7. 停留過久的 idea：status 為 open/proposed 且超過 --stale-days 天

這是啟發式的總表，用來找出「值得看一眼」的地方，不是最終判斷。

用法：
    python log_status.py [research_log 目錄，預設 ./research_log] [--stale-days 30] [--out report.md]
"""
import argparse
import datetime
import glob
import os
import re
import sys

STATUS = ["open", "proposed", "planned", "supported", "confirmed", "refuted", "superseded", "done"]


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
    """從狀態欄位取出第一個標準狀態詞；找不到時回傳原文摘要。"""
    for w in re.findall(r"[A-Za-z]+", cell):
        if w.lower() in STATUS:
            return w.lower()
    return None


def seed_count(fm):
    s = fm.get("seeds", "").strip().lstrip("[").rstrip("]")
    return len([x for x in s.split(",") if x.strip()]) if s else 0


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
        print(f"找不到目錄 {base}")
        return 1
    today = datetime.date.today()
    out = []
    P = out.append

    # ---- 實驗 ----
    exps = {}
    for f in sorted(glob.glob(os.path.join(base, "experiments", "*.md"))):
        fm = frontmatter(read(f))
        exps[os.path.basename(f)] = {"status": fm.get("status", "?"), "seeds": seed_count(fm),
                                     "date": fm.get("date", "")}

    # ---- 假設 ----
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
                         "status_raw": re.sub(r"\*", "", status_cell)[:80], "section": section,
                         "linked": linked})

    P(f"# Research log 狀態總表（{today.isoformat()}）\n")
    P(f"來源：`{os.path.abspath(base)}`。這是啟發式總表，標出值得檢查的地方，不是最終判斷。\n")

    P("## 1. 假設總覽\n")
    if hyps:
        P("| 狀態 | 數量 | 假設 |")
        P("|---|---|---|")
        groups = {}
        for h in hyps:
            groups.setdefault(h["status"] or "（非標準）", []).append(h["id"])
        for st in STATUS + ["（非標準）"]:
            if st in groups:
                P(f"| {st} | {len(groups[st])} | {', '.join(groups[st])} |")
    else:
        P("（hypotheses.md 中沒有找到 `| H# |` 開頭的表格列）")
    P("")

    P("## 2. 等待使用者的 node（proposed / planned）\n")
    waiting = [h for h in hyps if h["status"] in ("proposed", "planned")]
    waiting_exp = [k for k, v in exps.items() if v["status"] in ("proposed", "planned")]
    if waiting or waiting_exp:
        for h in waiting:
            P(f"- {h['id']}（{h['status']}）：{h['text'][:70]}")
        for k in waiting_exp:
            P(f"- experiments/{k}（{exps[k]['status']}）")
    else:
        P("- 無")
    P("")

    P("## 3. 疑似狀態不一致\n")
    issues = []
    for h in hyps:
        for e in h["linked"]:
            if e not in exps:
                issues.append(f"- {h['id']} 連到不存在的實驗 experiments/{e}")
                continue
            if h["status"] in ("supported", "confirmed") and exps[e]["status"] not in ("done",):
                issues.append(f"- {h['id']} 為 {h['status']}，但連到的 experiments/{e} 狀態是 {exps[e]['status']}")
        if h["status"] == "confirmed" and h["linked"] and all(exps.get(e, {}).get("seeds", 0) <= 1 for e in h["linked"]):
            issues.append(f"- {h['id']} 為 confirmed，但連到的實驗都只有 ≤1 個 seed：確認主張類型（實作類需有已知答案的驗證測試；實驗類需多 seed 或多條件；依賴文獻者應維持 supported）")
        if h["status"] in ("supported", "confirmed", "refuted") and not h["linked"]:
            issues.append(f"- {h['id']} 為 {h['status']}，但證據欄沒有連到任何實驗記錄")
    P("\n".join(issues) if issues else "- 無")
    P("")

    P("## 4. 單一 seed 的實驗\n")
    single = [k for k, v in exps.items() if v["seeds"] <= 1 and v["status"] == "done"]
    P("\n".join(f"- experiments/{k}（seeds: {exps[k]['seeds']}）" for k in single) if single else "- 無")
    P("")

    P("## 5. 未經討論的決策\n")
    hits = []
    for f in sorted(glob.glob(os.path.join(base, "**", "*.md"), recursive=True)):
        for i, line in enumerate(read(f).splitlines(), 1):
            if "未經討論" in line and line.lstrip().startswith("|") and "決定者" not in line:
                hits.append(f"- {os.path.relpath(f, base)}:{i}：{line.strip()[:100]}")
    P("\n".join(hits) if hits else "- 無")
    P("")

    P("## 6. 證據強度較弱的文獻（source 不是全文）\n")
    weak = []
    for f in sorted(glob.glob(os.path.join(base, "papers", "*.md"))):
        src = frontmatter(read(f)).get("source", "")
        if not src or "全文" not in src or "未" in src:
            weak.append(f"- papers/{os.path.basename(f)}：{src or '（未標示 source）'}")
    P("\n".join(weak) if weak else "- 無")
    P("")

    P(f"## 7. 停留超過 {a.stale_days} 天的 idea（open / proposed）\n")
    stale = []
    for f in sorted(glob.glob(os.path.join(base, "ideas", "*.md"))):
        fm = frontmatter(read(f))
        st = first_status(fm.get("status", ""))
        try:
            d = datetime.date.fromisoformat(fm.get("date", "")[:10])
        except ValueError:
            continue
        if st in ("open", "proposed") and (today - d).days > a.stale_days:
            stale.append(f"- ideas/{os.path.basename(f)}（{st}，{(today - d).days} 天）")
    P("\n".join(stale) if stale else "- 無")
    P("")

    report = "\n".join(out)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(report)
        print("已寫入", a.out)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
