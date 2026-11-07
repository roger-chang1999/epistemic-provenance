# epistemic-provenance（知識來源追溯）

> **為研究中的每個主張，保留它從哪裡來、憑什麼成立、怎麼被改變的完整紀錄。**

研究紀錄系統，可在 Claude Code 和 claude.ai 使用。

**Provenance** 原指藝術品從創作到現在的完整經手紀錄：每一手都要記錄，而且紀錄不能被竄改。**Epistemic** 表示追溯的對象是知識主張。

設計動機來自心理學的「後設認知」（metacognition）：研究者很容易騙到自己。這套紀錄方式要防範研究中常見的認知偏誤：

- **來源混淆**：把看到結果之後才想到的解釋，誤記成原始設計
- **後見之明偏誤**：知道結果後，回頭改寫當初的推理
- **協定混用**：把不同方法量出來、名稱相同的數字放在同一張表比較

做法是在專案裡維護一個 `research_log/`：

```
research_log/
├── README.md                  使用說明與「因果線」定義
├── hypotheses.md              中樞索引：所有假設與狀態
├── methods.md                 評估協定登記表
├── research_tree_overview.md  研究樹：假設 → 設計 → 結果 → 推論 ⟹ 下一個假設
├── comparison_catalog.md      A vs B 比較總目錄
├── ideas/NNN-slug.md          想法演變（只追加、不改寫）
├── papers/slug.md             文獻筆記（含不可比之處、資訊來源）
└── experiments/exp-slug.md    實驗記錄（含完整指令、限制）
```

## 安裝：Claude Code

這是私人 repo，安裝時會用你本機的 git 登入（已執行過 `gh auth login` 和 `gh auth setup-git` 即可）。

```bash
claude plugin marketplace add roger-chang1999/epistemic-provenance
claude plugin install epistemic-provenance@epistemic-provenance
```

或在 Claude Code 對話中輸入 `/plugin marketplace add roger-chang1999/epistemic-provenance`，再用 `/plugin` 面板安裝。

更新：`claude plugin marketplace update epistemic-provenance`

## 安裝：claude.ai

```bash
python tools/package_for_claudeai.py
```

會產生 `dist/epistemic-provenance.zip`。到 claude.ai 的「設定 → Capabilities → Skills」上傳。

## 使用

安裝後直接用自然語言，例如：

- 「幫這個專案初始化 research log」
- 「把剛剛的實驗結果記錄下來」
- 「開一個新的 idea，記下我們剛剛的討論」
- 「整理這篇論文的筆記」
- 「我們現在研究進度到哪？」

也可以明確呼叫：`/epistemic-provenance:epistemic-provenance`

## 內容

```
.claude-plugin/
  plugin.json, marketplace.json
skills/epistemic-provenance/
  SKILL.md                      核心原則與工作流程
  assets/templates/             各類檔案的空白模板
  scripts/init_research_log.py  建立骨架（不覆蓋既有檔案）
  scripts/check_links.py        檢查相對連結、frontmatter、ideas 編號
tools/package_for_claudeai.py   打包成 claude.ai 可上傳的 zip
```
