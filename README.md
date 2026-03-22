# 🏥 學習病歷產生器

將門診紀錄、急診紀錄或標準化病人腳本，轉換為結構化學習病歷，並提供臨床學習重點與 AI 問答功能。

## 安裝與執行

```bash
# 1. 安裝套件
pip install -r requirements.txt

# 2. 啟動網站
streamlit run app.py
```

瀏覽器會自動開啟 `http://localhost:8501`。

## 使用方式

1. 點開左側欄 (sidebar)，輸入你的 **Anthropic API Key**
2. 在主頁面左側文字框貼入病患資料
3. 按下「產生學習病歷」
4. 右側會出現三個分頁可切換：

| 分頁 | 功能說明 |
|------|---------|
| 📝 學習病歷 | 結構化病歷輸出，ROS / PE 中有更動的項目以**紅色字體**標示，可下載 .txt |
| 📚 學習重點 | 自動生成：診斷推理、鑑別診斷（表格）、治療原則（含劑量與 guideline 檢查）、進一步檢查建議、高 yield 學習重點 |
| 💬 AI 問答 | 根據病歷內容直接提問，支援多輪對話（如「病患有無發燒？」「為什麼選這個抗生素？」） |

## 功能特色

### 病歷生成
- Vital signs 以 `T:38.5 P:96 R:17 SBP:97 DBP:79 E:4 V:5 M:6 SPO2:97%` 精簡格式呈現
- 急診用藥只寫藥名，省略劑量
- Impression 中抗生素獨立換行、含起始日期
- Plan 保持 3–6 項精簡內容
- ROS 以編號列點輸出，確保複製貼上時編號保留
- PE 各項目之間無多餘空行，複製後不需手動刪除

### 紅色標示系統
- ROS 與 PE 中凡是根據病歷更動的項目，會以 🔴 **紅色粗體** 顯示
- 方便快速辨識哪些是 AI 根據病情調整的內容

### 學習重點（自動生成）
- 📌 主要診斷與臨床推理
- 🔍 鑑別診斷：以**表格**呈現（支持點 vs 不支持點）
- 💊 治療原則：含藥物劑量、途徑、頻率，引用相關 guideline
- ⚠️ Guideline 符合度檢查：自動審視病歷治療是否符合最新指引
- 🔬 建議進一步檢查
- ⚡ 學習重點摘要（若有適合表格呈現的比較會自動加入）

### AI 問答
- 根據生成的病歷內容進行多輪對話
- 支援中英文提問
- 可清除對話重新開始

## 部署到 Streamlit Cloud

1. 將 `app.py` 和 `requirements.txt` 上傳至 GitHub repo
2. 前往 [share.streamlit.io](https://share.streamlit.io) 連結你的 repo
3. 設定 Main file path 為 `app.py`
4. 啟動即可

## 輸出病歷格式

- 主訴 (Chief Complaint)
- 現在病症 (Present Illness)
- 過去病史 (Past History)
- 個人病史 (Personal History)
- 系統整理 (Review of System)
- 理學檢查 (Physical Examination)
- 臨床臆斷 (Impression)
- 處理計畫 (Plan)
