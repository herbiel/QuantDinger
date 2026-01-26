<div align="center">
  <a href="https://github.com/brokermr810/QuantDinger">
    <img src="https://ai.quantdinger.com/img/logo.e0f510a8.png" alt="QuantDinger Logo" width="160" height="160">
  </a>

  <h1 align="center">QuantDinger</h1>

  <div align="center">
    <a href="README.md">🇺🇸 English</a> |
    <a href="README_CN.md">🇨🇳 简体中文</a> |
    <a href="README_TW.md">繁體中文</a> |
    <a href="README_JA.md">🇯🇵 日本語</a> |
    <a href="README_KO.md">🇰🇷 한국어</a>
  </div>
  <br/>
 
  <h3 align="center">
    Next-Gen AI Quantitative Trading Platform
  </h3>
  
  <p align="center">
    <strong>🤖 AI-Native · 🐍 Visual Python · 🌍 Multi-Market · 🔒 Privacy-First</strong>
  </p>
  <p align="center">
    <i>Build, Backtest, and Trade with an AI Co-Pilot. Better than PineScript, Smarter than SaaS.</i>
  </p>

  <p align="center">
  <a href="https://www.quantdinger.com"><strong>Official Community</strong></a> ·
  <a href="https://ai.quantdinger.com"><strong>Live Demo</strong></a> ·
  <a href="https://youtu.be/HPTVpqL7knM"><strong>📺 Video Demo</strong></a> ·
  <a href="CONTRIBUTORS.md"><strong>🌟 Join Us</strong></a>
  </p>

  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square&logo=apache" alt="License"></a>
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Vue.js-2.x-4FC08D?style=flat-square&logo=vue.js&logoColor=white" alt="Vue">
    <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/github/stars/brokermr810/QuantDinger?style=flat-square&logo=github" alt="Stars">
  </p>

  <p align="center">
    <a href="https://t.me/quantdinger"><img src="https://img.shields.io/badge/Telegram-QuantDinger%20Group-26A5E4?style=for-the-badge&logo=telegram" alt="Telegram Group"></a>
    <a href="https://discord.gg/vwJ8zxFh9Q"><img src="https://img.shields.io/badge/Discord-Join%20Server-5865F2?style=for-the-badge&logo=discord" alt="Discord"></a>
    <a href="https://x.com/HenryCryption"><img src="https://img.shields.io/badge/X-Follow%20Us-000000?style=for-the-badge&logo=x" alt="X"></a>
  </p>
</div>

---

## 📖 Introduction

**QuantDinger** is a local-first, privacy-first, self-hosted quantitative trading platform. It runs on your own infrastructure, providing multi-user accounts backed by PostgreSQL while keeping full control of your strategies, trading data, and API keys.

### Why QuantDinger?

| Feature | QuantDinger | Cloud SaaS |
|---------|-------------|------------|
| Data Ownership | ✅ Local storage | ❌ Vendor-controlled |
| Strategy Privacy | ✅ Never leaves your server | ❌ Uploaded to cloud |
| Subscription Fees | ✅ None | ❌ Monthly charges |
| Customization | ✅ Full source access | ❌ Limited |

### Core Capabilities

- **🐍 Python-Native Strategies** — Write indicators in standard Python with AI assistance
- **🤖 AI Multi-Agent Research** — LLM-powered analysis with web scraping and market intelligence
- **📊 Visual Backtesting** — TradingView-like charting with strategy visualization
- **⚡ Live Trading** — Direct API execution for 10+ crypto exchanges, IBKR, and MT5
- **🔒 Self-Hosted** — Your data stays on your infrastructure

---

## 📺 Video Demo

<div align="center">
  <a href="https://youtu.be/HPTVpqL7knM">
    <img src="docs/screenshots/video_demo.png" alt="QuantDinger Demo" width="100%" style="border-radius: 10px; max-width: 800px;">
  </a>
  <p><strong>Click to watch the project introduction</strong></p>
</div>

---

## 📸 Screenshots

<div align="center">
  <img src="docs/screenshots/tuopu.png" alt="System Architecture" width="100%" style="max-width: 800px;">
  <p><em>System Architecture Overview</em></p>
</div>

<table align="center">
  <tr>
    <td align="center"><img src="docs/screenshots/dashboard.png" alt="Dashboard"><br/><em>Dashboard</em></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/screenshots/ai_analysis1.png" alt="AI Analysis"><br/><em>AI Multi-Agent Analysis</em></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/screenshots/indicator_analysis.png" alt="Indicator Analysis"><br/><em>Indicator Analysis</em></td>
  </tr>
</table>

---

## 🔌 Supported Exchanges & Brokers

### Cryptocurrency (Direct API Trading)

| Exchange | Spot | Futures | Features |
|:--------:|:----:|:-------:|:---------|
| **Binance** | ✅ | ✅ | Margin, COIN-M, USDⓈ-M |
| **OKX** | ✅ | ✅ | Options, Copy Trading |
| **Bitget** | ✅ | ✅ | Copy Trading |
| **Bybit** | ✅ | ✅ | Linear, Inverse |
| **KuCoin** | ✅ | ✅ | — |
| **Gate.io** | ✅ | ✅ | — |
| **Kraken** | ✅ | ✅ | — |
| **Coinbase** | ✅ | — | Spot Only |
| **Bitfinex** | ✅ | ✅ | Derivatives |
| **Deepcoin** | ✅ | ✅ | — |

### Traditional Brokers

| Broker | Markets | Platform |
|:------:|:--------|:---------|
| **Interactive Brokers** | US/HK Stocks, Options | TWS / IB Gateway |
| **MetaTrader 5** | Forex, CFDs | MT5 Terminal |

### Market Data Sources

| Market | Sources |
|--------|---------|
| Crypto | 100+ exchanges via CCXT |
| US Stocks | Yahoo Finance, Finnhub, Tiingo |
| CN/HK Stocks | AkShare, East Money |
| Forex | Finnhub, OANDA |

---

## ✨ Key Features

### 1. Visual Python Strategy Workbench

Write strategies in Python with full ecosystem access (Pandas, NumPy, TA-Lib). AI assists with code generation, and signals visualize directly on interactive charts.

### 2. Complete Trading Lifecycle

```
Indicator → Strategy Config → Backtest → AI Optimization → Live Execution
```

### 3. AI Multi-Agent Research

A team of specialized agents analyzes markets:
- **Research Agents** — Web scraping for news and events
- **Analysis Agents** — Technical indicators and capital flows
- **Risk Assessment** — Market filter based on AI sentiment

### 4. Multi-LLM Support

| Provider | Models |
|----------|--------|
| OpenRouter | 100+ models |
| OpenAI | GPT-4o, GPT-4o-mini |
| Google | Gemini 1.5 Flash/Pro |
| DeepSeek | DeepSeek Chat |
| xAI | Grok Beta |

### 5. Enterprise Features

- **Multi-User Support** — PostgreSQL-backed accounts with role-based permissions
- **OAuth Integration** — Google and GitHub login
- **Security** — Cloudflare Turnstile, rate limiting, email verification

---

## 🚀 Quick Start

### Docker Deployment (Recommended)

```bash
# Clone and configure
git clone https://github.com/brokermr810/QuantDinger.git
cd QuantDinger
cp backend_api_python/env.example backend_api_python/.env

# Start services
docker-compose up -d --build
```

**Access:**
- Frontend: http://localhost:8888
- API: http://localhost:5000
- Default login: `quantdinger` / `123456`

### Docker Commands

```bash
docker-compose ps              # Status
docker-compose logs -f         # Logs
docker-compose down            # Stop
docker-compose up -d --build   # Rebuild
```

### Local Development

```bash
# Backend
cd backend_api_python
pip install -r requirements.txt
cp env.example .env
python run.py

# Frontend
cd quantdinger_vue
npm install && npm run serve
```

---

## 📚 Documentation

- [Python Strategy Development Guide](docs/STRATEGY_DEV_GUIDE.md)
- [Interactive Brokers (IBKR) Trading Guide](docs/IBKR_TRADING_GUIDE_EN.md)
- [MetaTrader 5 (MT5) Trading Guide](docs/MT5_TRADING_GUIDE_EN.md)
- [Telegram Notification Setup](docs/NOTIFICATION_TELEGRAM_CONFIG_EN.md)
- [Email Notification Setup](docs/NOTIFICATION_EMAIL_CONFIG_EN.md)

---

## 🏗️ Architecture

```
┌─────────────────────────────┐
│      quantdinger_vue        │
│   (Vue 2 + Ant Design Vue)  │
└──────────────┬──────────────┘
               │ HTTP (/api/*)
               ▼
┌─────────────────────────────┐
│     backend_api_python      │
│  (Flask + Strategy Runtime) │
└──────────────┬──────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
PostgreSQL   Redis    Exchanges
             (opt)     & LLMs
```

---

## 🌍 Multi-Language Support

<p>
  <img src="https://img.shields.io/badge/🇺🇸_English-Supported-2563EB?style=flat-square" alt="English" />
  <img src="https://img.shields.io/badge/🇨🇳_简体中文-Supported-2563EB?style=flat-square" alt="Chinese" />
  <img src="https://img.shields.io/badge/🇹🇼_繁體中文-Supported-2563EB?style=flat-square" alt="Traditional Chinese" />
  <img src="https://img.shields.io/badge/🇯🇵_日本語-Supported-2563EB?style=flat-square" alt="Japanese" />
  <img src="https://img.shields.io/badge/🇰🇷_한국어-Supported-2563EB?style=flat-square" alt="Korean" />
  <img src="https://img.shields.io/badge/🇩🇪_Deutsch-Supported-2563EB?style=flat-square" alt="German" />
  <img src="https://img.shields.io/badge/🇫🇷_Français-Supported-2563EB?style=flat-square" alt="French" />
</p>

---

## 📜 License

Licensed under **Apache License 2.0**. See [LICENSE](LICENSE).

**Trademark Notice:** Apache 2.0 does not grant trademark rights. QuantDinger branding (name/logo) is protected. See [TRADEMARKS.md](TRADEMARKS.md) for usage guidelines.

---

## 🤝 Community & Support

- **Telegram**: [QuantDinger Group](https://t.me/quantdinger)
- **Discord**: [Join Server](https://discord.gg/vwJ8zxFh9Q)
- **GitHub Issues**: [Report bugs / Request features](https://github.com/brokermr810/QuantDinger/issues)
- **Email**: [brokermr810@gmail.com](mailto:brokermr810@gmail.com)

---

## 💝 Support the Project

**Crypto Donations (ERC-20 / BEP-20 / Polygon / Arbitrum)**

```
0x96fa4962181bea077f8c7240efe46afbe73641a7
```

<p>
  <img src="https://img.shields.io/badge/USDT-Accepted-26A17B?style=for-the-badge&logo=tether&logoColor=white" alt="USDT">
  <img src="https://img.shields.io/badge/ETH-Accepted-3C3C3D?style=for-the-badge&logo=ethereum&logoColor=white" alt="ETH">
</p>

---

## 🎓 Supporting Partners

<div align="center">
  <a href="https://beinvolved.indiana.edu/organization/quantfiniu" target="_blank">
    <img src="docs/screenshots/qfs_logo.png" alt="QFS" width="200">
  </a>
  <br/>
  <strong>Quantitative Finance Society</strong><br/>
  <small>Indiana University Bloomington</small>
</div>

---

## 🙏 Acknowledgements

Built with [Flask](https://flask.palletsprojects.com/) · [Vue.js](https://vuejs.org/) · [CCXT](https://github.com/ccxt/ccxt) · [Pandas](https://pandas.pydata.org/) · [KlineCharts](https://github.com/klinecharts/KLineChart) · [Ant Design Vue](https://antdv.com/)
