# 工作流程 A：初始化新專案的 research log

使用者要為專案建立 research log 時讀這份文件。

1. 先問使用者，或從對話與計畫書整理出：專案名稱、目前的因果線（至少一條「原始研究動機」）、主要評估指標。
2. 執行：
   ```bash
   python <skill 目錄>/scripts/init_research_log.py <專案根目錄> --project "<專案名稱>"
   ```
   這會建立目錄和所有中樞檔案的骨架（含「給審查者的指引」）；已存在的檔案不會被覆蓋。
3. 填入：
   - `README.md` 的因果線定義
   - `methods.md` 的第一個評估協定
   - `hypotheses.md` 的初始假設
   - `ideas/001-origin.md`：原始研究動機。有計畫書時，從計畫書整理研究問題、應驗證的假設，以及**不應先行宣稱的結論**。
4. 如果專案已經有討論或實驗歷史，依時間順序補寫成 ideas 和 experiments，**明確標註是事後補記**，並在設計決策紀錄中標明哪些決策當時未經討論。
5. 執行 `scripts/check_links.py`。
