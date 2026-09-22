# 🧪 Autonomous Web QA & Self-Healing Testing Agent
### Production-Grade Zero-Scripting End-to-End Autonomous Test Suite

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-v1.40+-green.svg)
![Pytest](https://img.shields.io/badge/Pytest-Automation-orange.svg)
![LLM Reasoning](https://img.shields.io/badge/LLM-Gemini_SDK-red.svg)
![Architecture](https://img.shields.io/badge/Design-Self--Healing_AST-purple.svg)

---

## 📌 Executive Summary
Web test automation historically suffers from high test maintenance overhead, brittle CSS/XPath locators, and manual test authoring bottlenecks. 

**Autonomous Web QA Agent** solves these challenges by combining **Playwright** for headless/headed DOM exploration, **Pytest** for deterministic test execution, and **Google Gemini Reasoning Engine** for autonomous test generation and dynamic **Self-Healing Locator Repair**. The pipeline discovers web applications, generates robust assertions, executes tests, and autonomously patches broken selectors without human intervention.

---

## ⚙️ Core Architecture & Agentic Workflow

```text

[ Target URL ]
│
▼
[ Step 1: Headed/Headless Playwright Scanner ]
│  └── Inspects DOM Tree & Normalizes Interactive Selectors
▼
[ Step 2: Gemini Test Generation Engine ]
│  └── Synthesizes Deterministic Pytest Test Suites
▼
[ Step 3: Pytest Subprocess Runner ]
│  └── Executes Test Assertions & Captures Exit Trace
├───► (If Status == 0 / Passed) ──► Complete (100% Green)
│
└───► (If Status != 0 / Broken Locators)
│
▼
[ Step 4: Self-Healing Agent Pipeline ]
│  └── Inspects Error Stacktrace + Dynamic DOM State
│  └── Patches Corrupted Locators / AST Nodes
▼
[ Re-execution Suite ] ──► Verified Green Execution

```
---

## 🚀 Key Technical Features

* **Autonomous Dynamic Discovery:** Playwright dynamically scans client-side single-page applications (SPAs) and traditional DOM trees, filtering high-value interactable elements (buttons, inputs, dropdowns, forms).

* **Self-Healing AST & Locators:** When DOM changes break conventional automation, the Self-Healing mechanism analyzes stdout/stderr traces against the live DOM state, repairing selectors on the fly.

* **Deterministic Test Execution:** Generates clean, isolated Pytest scripts with explicit assertions rather than unreliable flaky simulations.

* **Configurable Execution Modes:** Supports full Headless CI/CD testing mode alongside Headed execution with calibrated `slow_mo` throttling for visual observability and live debugging.

* **Modular Streamlit Cockpit:** Centralized real-time monitoring console displaying live DOM extraction status, dynamic code generation, and low-level Pytest execution logs.

---

## 🛠️ Tech Stack & Dependencies

* **Language Engine:** Python 3.11+

* **Browser Automation:** Playwright (Chromium/WebKit/Firefox)

* **Testing Framework:** Pytest Runner

* **AI Cognitive Engine:** Google Gemini SDK (`google-genai`)

* **DOM Normalization:** BeautifulSoup4 (HTML Parsing)

* **Visualization Layer:** Streamlit Dashboard

---

## 📂 Project Structure

```bash
autonomous-web-qa-agent/
│
├── src/
│   ├── __init__.py
│   ├── scanner.py          # Playwright DOM inspection & dynamic element extraction
│   ├── ai_tester.py        # Gemini reasoning pipeline for test generation & self-healing
│   └── test_runner.py      # Subprocess Pytest harness & stdout/stderr parsers
│
├── tests/
│   └── generated_suite.py  # Runtime generated and healed test scripts
│
├── app.py                  # Streamlit enterprise cockpit
├── requirements.txt        # Pinned production dependencies
├── .env.example            # Environment variables configuration
└── README.md               # Architecture documentation

```

## 🚦 Getting Started

---

### 1. Clone Repository
```
git clone https://github.com/satyanarayana51115/autonomous-web-qa-agent.git
cd autonomous-web-qa-agent
```
### 2. Setup Virtual Environment
```
python -m venv .venv
```
**On Windows** 
```
.venv\Scripts\activate
```
**On macOS/Linux**
```
source .venv/bin/activate  
```
### 3. Install Dependencies & Playwright Browers
```
pip install -r requirements.txt
playwright install chromium
```
### 4. Configure API Credentials
Create a .env file in the root directory
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
### 5. Launch the Enterprise Cockpit
```
streamlit run app.py
```

---

## 🛡️ Engineering Highlights

* **Resilient Locator Fallbacks:**
    The scanner extracts multi-attribute locator footprints (id, name, aria-label, placeholder, text content) to prevent single-point selector failures.

* **Production Sandbox Isolation:** 
    All Pytest suites execute in encapsulated sub-processes with dedicated timeouts, mitigating script hangs and uncontrolled memory leaks.

* **​Token-Efficient Prompt Engineering:** 
    HTML DOM is pruned of heavy script/style payloads prior to model ingestion, reducing token consumption while preserving structural DOM intent.

---

## 👤 Author & Architecture Inquiries

* **Developer:** Satyanarayana

* **​Role:** AI & Workflow Automation Engineer

* **​GitHub:** @satyanarayana51115

* **​LinkedIn:** Connect on LinkedIn

