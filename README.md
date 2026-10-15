# 📈 AI Stock Advisor & Taiwan Broker Tracker
### AI 股票投資顧問與臺股主力籌碼分析系統

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![TWSE/TPEx](https://img.shields.io/badge/TWSE%2FTPEx-Market%20Chips-green)](https://www.twse.com.tw/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 一套整合 **LangGraph 多代理人 AI 股票交易顧問系統** 與 **臺灣證券交易所 (TWSE/TPEx) 11 大主力與外資券商分點籌碼追蹤引擎** 的全方位智慧金融決策專案。

---

## 🌟 兩大核心子系統 (Core Subsystems)

### 1. 🤖 OpenTrade.ai：多代理人 AI 股票交易顧問 (LangGraph Pipeline)
採用 LangGraph `StateGraph` 架構，由 8 位專門職責的 AI Agent 分工協同辯論與風控審查，產出嚴謹的投資決策：

```
行情與新聞數據 ──> [基本面分析師, 市場情緒分析師, 新聞分析師, 技術面分析師] (平行運算)
                                      │
                              多空正反辯論 (Bull vs Bear)
                                      │
                                交易員決策產出
                                      │
                                風險管理員審查 (核准 / 修正 / 否決)
                                      │
                                  最終交易決策
```

- **八大專業代理人陣容**：
  1. `Fundamental Analyst`：公司財報、估值、本益比與成長動能分析。
  2. `Sentiment Analyst`：社群討論聲量與市場情緒分析。
  3. `News Analyst`：即時重大財經新聞與總經事件解讀。
  4. `Technical Analyst`：RSI、MACD、布林通道、均線 (SMA/EMA) 與 ATR 指標計算。
  5. `Bull Researcher`：提出最具說服力的看多論點與催化劑。
  6. `Bear Researcher`：提出最嚴苛的看空論點與下行風險。
  7. `Trader Agent`：綜合上述所有資訊，產出明確交易方向與策略。
  8. `Risk Manager`：進行最終風控審查，嚴格控管最大虧損與槓桿風險。
- **雙前端介面**：提供互動式 **Streamlit Web 儀表板** 與高效率 **CLI 終端機指令介面**。
- **支援本機離線與雲端 LLM**：可無縫串接 [Ollama](https://ollama.com) (Llama 3 / Mistral)、[LM Studio](https://lmstudio.ai) 或 OpenAI API。

---

### 2. 🏛️ TW Broker Tracker：臺股 11 大主力與外資分點籌碼追蹤引擎
專門針對台股特有的「券商分點進出明細」所開發的高速清算與報告產出引擎：

- **11 大核心監控主力分點**：
  - 國票-敦北法人 (5527)
  - 凱基-城中 (9208)
  - 統一-城中
  - 國票-安和
  - 元大證券總分公司
  - 富邦證券總分公司
  - 統一證券總分公司
  - 群益金鼎證券
  - 美商高盛 (Goldman Sachs)
  - 美林證券 (Merrill Lynch)
  - 摩根大通 (JPMorgan / 小摩)
- **嚴格遵循全市場成交量守恆**：真實撮合數據取自證交所與櫃買中心官方結算盤後清單，拒絕模擬數值。
- **高質感雙格式日報生成 (Format A & B)**：
  - **Format A (當日實盤)**：左右並排 Markdown 表格，一眼對照該主力「買超前 10 檔 vs 賣超前 10 檔」之淨金額與均價。
  - **Format B (週波段波長)**：追蹤主力連續加碼或調節天數與 5 日累計總金額。

---

## 📂 專案目錄結構 (Project Structure)

```text
ai-stock-advisor/
├── opentrade/                   # 🤖 LangGraph 多代理人交易顧問系統
│   ├── app/                     # Streamlit 視覺化儀表板
│   ├── cli/                     # CLI 命令行介面
│   ├── src/                     # 核心代理人邏輯、工具與 StateGraph 定義
│   ├── tests/                   # 單元測試集
│   ├── .env.example             # LLM 與 API 環境變數範本
│   ├── pyproject.toml           # 專案相依性規格
│   └── requirements.txt
├── tw_tracker/                  # 📊 臺股主力分點籌碼追蹤模組
│   ├── engine.py                # 分點清算與過濾核心引擎
│   ├── real_data.py             # 盤後真實搓合數據獲取模組
│   ├── render_format_a.py       # 雙向對照報表渲染器
│   ├── cross_reference.py       # 交叉對比分析邏輯
│   ├── check_*.py               # 關鍵個股籌碼專項檢驗工具
│   └── reports/                 # 每日實盤清算日報歸檔 (Format A)
├── skills/                      # 🧠 AI Agent 擴充技能
│   └── tw-broker-tracker/
│       └── SKILL.md             # 專供 AI Agent 調用之分點追蹤規格書
├── .gitignore                   # Git 排除清單
└── README.md                    # 本專案技術文件
```

---

## 🚀 快速上手 (Quick Start)

### 1. 複製專案庫

```bash
git clone https://github.com/Thomas412570510/ai-stock-advisor.git
cd ai-stock-advisor
```

### 2. 安裝環境需求

推薦使用 Python 3.10 或以上版本：

```bash
pip install -r opentrade/requirements.txt
```

---

## 💻 執行指南 (Usage)

### 模式 A：啟動 OpenTrade.ai 互動式 Streamlit 儀表板

```bash
cd opentrade
cp .env.example .env

# 啟動 Streamlit 視覺化儀表板
streamlit run app/main.py
```
*(在瀏覽器打開 `http://localhost:8501`，輸入美股代號如 `AAPL`、`NVDA` 或 `TSLA` 即可啟動多代理人辯論！)*

---

### 模式 B：執行 OpenTrade.ai 終端機分析 (CLI)

```bash
cd opentrade
python cli/main.py analyze AAPL --llm ollama --model llama3.2
```

---

### 模式 C：產出臺股 11 大主力分點今日實盤籌碼日報

```bash
# 執行籌碼追蹤引擎產出今日 Format A 雙向對照表
python tw_tracker/render_format_a.py
```
報告將自動輸出至 `tw_tracker/reports/` 目錄，格式呈現清晰的多空並排雙向 Markdown 表格。

---

## 🛡️ 安全性與隱私規範 (Security)

1. 本專案嚴格排除任何敏感 API Key，所有憑證請妥善存放在 `.env`，**請勿簽入 Git 版本控制**。
2. 預設推薦使用本地 Ollama / LM Studio 執行推論，保護您的個人交易策略與數據不外洩。

---

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 授權。
