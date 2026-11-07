# Research Log — {{PROJECT}}

這個目錄記錄 {{PROJECT}} 的研究思考鏈路，讓「為什麼做這個實驗」和「這篇論文為什麼相關」不會隨時間遺忘。檔案之間用相對連結互相引用：

```
research_log/
├── README.md                  本檔：使用說明與因果線定義
├── hypotheses.md              中樞索引：所有假設的狀態
├── methods.md                 評估方法登記表：每個數字是用哪種協定量出來的
├── research_tree_overview.md  研究樹：假設 → 實驗設計 → 結果 → 推論 ⟹ 下一個假設
├── comparison_catalog.md      比較實驗總目錄
├── ideas/NNN-slug.md          想法演變：依時間序編號，每篇是一次思考轉折
├── papers/slug.md             文獻筆記：一篇論文一個檔案
└── experiments/exp-slug.md    實驗記錄：一組實驗一個檔案
```

引用或比較任何數字之前，先看 [methods.md](methods.md) 確認是用哪個協定量的。**不同協定的數字不能放進同一張表比較。**

## ⚠️ 因果線：寫新內容前先想清楚屬於哪一條

<!-- 填入本專案的因果線。至少要有「原始研究動機」這一條；看到結果後才出現的新方向，另開一條。 -->

- **主線一（原始研究動機）**：[ideas/001](ideas/001-origin.md)。{{一句話描述原始研究問題}}
- **主線二（{{例如：實驗結果出來後的貢獻定位／方法論問題}}）**：{{何時、因為什麼結果而出現}}

**不同的線不要混在一起寫進論文。** 如果把事後才出現的線包裝成一開始的設計目標，既不誠實，也容易被審稿人拆穿。

## 使用流程

1. **想法演變**（`ideas/`）：每次思考出現轉折就新增一篇，檔名遞增編號 `NNN-slug.md`。內容包含：從哪個假設或實驗而來、屬於哪條因果線、接下來想驗證什麼。
2. **文獻**（`papers/`）：記錄問題設定、可比性、關鍵數字、相關的線和假設。**務必記錄「不可比之處」和資訊來源。**
3. **實驗**（`experiments/`）：記錄對應的想法、完整指令與設定、結果、支持或推翻的假設、限制。
4. **假設索引**（`hypotheses.md`）：依因果線分開列出；最上面永遠是「當前最前沿的待分析問題」。
5. **總覽**：新的比較同步加進 `comparison_catalog.md`；假設狀態改變時同步更新 `research_tree_overview.md`。

## 連結與 frontmatter 慣例

使用相對 markdown 連結，每篇檔案開頭放 frontmatter：

```markdown
---
type: idea | paper | experiment
status: open | proposed | planned | supported | confirmed | refuted | superseded | done
date: YYYY-MM-DD
related: [相對路徑列表]
---
```

舊的想法即使被推翻也保留（append-only），標記 `status: refuted`，並在文末加「更新」段落。**不要回頭改寫舊內容。**
