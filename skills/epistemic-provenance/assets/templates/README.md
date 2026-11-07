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

## 給審查者的指引（人或 agent 都適用）

這份紀錄遵循「知識來源追溯（epistemic provenance）」的原則：每個主張都要能追溯它從哪裡來、憑什麼成立、怎麼被改變。審查時，不需要任何額外工具，照下列順序進行即可。

**從哪裡開始讀**：`hypotheses.md`（現況）→ `research_tree_overview.md`（推論鏈）→ 個別 `experiments/` 與 `ideas/`。引用數字前先查 `methods.md`。

**核心原則**（審查時逐項對照）：
1. **因果線分離**：每篇 idea 標明屬於哪條線；事後的發現不能寫成原始動機。
2. **只追加**：被推翻的 idea 保留並標 `refuted`，新證據寫在文末「更新」段落，不改原文。
3. **先寫預測**：實驗記錄的預測要在執行前寫下，並經研究者確認。
4. **協定登記**：每個數字都能對應到 `methods.md` 的某個協定與版本；不同協定的數字不放在同一張表比較。
5. **來源強度**：文獻的 `source` 標明讀過全文、摘要或憑記憶；被引用、比較或依其實作之前必須讀完全文。實驗寫明限制。
6. **可重現**：實驗記錄有完整指令、程式版本、結果路徑、seed。
7. **狀態詞彙**：open → proposed → planned → analyzing → supported / confirmed / refuted / superseded。confirmed 的條件：實作類需通過有已知答案的驗證測試；實驗類需多 seed 或多條件；依賴文獻者維持 supported，除非我們自己也獨立驗證。
8. **決策來源**：設計決策記錄決定者；「未經討論」的預設值要標明。

**審查檢查清單**：
- [ ] 假設狀態和實驗結果一致（confirmed 是否名副其實、supported 的限制是否寫清楚）
- [ ] hypotheses.md 與 comparison_catalog.md 的結論沒有比實驗記錄更強
- [ ] 沒有因果線混淆
- [ ] 比較表中的數字協定一致
- [ ] 被推翻的想法有保留，沒有被改寫（可用 `git log -p` 查看）
- [ ] 未經討論的決策中，有哪些會影響目前的結論
- [ ] 被引用、比較或依其實作的文獻，都已讀過全文

如果有安裝 epistemic-provenance skill，可以用 `scripts/log_status.py` 產生狀態總表作為起點。
