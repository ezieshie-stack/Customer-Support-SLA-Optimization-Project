# 🎯 Customer Support SLA Optimization — $30K Monthly Savings via Predictive Escalation

[![Project Status: Complete](https://img.shields.io/badge/Project%20Status-Complete-green.svg)](https://github.com/ezieshie-stack/Customer-Support-SLA-Optimization-Project)
[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/dashboard-Streamlit-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)

---

## 📌 Problem Statement

The customer support operations team is **hemorrhaging money through SLA breaches**. Historically, **$213K in operational losses** can be traced to tickets that exceeded their resolution deadline — and the team's escalation process is entirely **reactive**. Managers only discover a breach *after* it's already happened.

The core challenges:
- **No early warning system** — There's no way to identify which tickets will breach *before* they do
- **Manual escalation is slow** — By the time a manager spots a problem, the SLA has already been missed
- **No visibility into cost** — Leadership knows breaches are bad, but can't quantify the financial impact per ticket, per channel, or per priority level
- **Limited agent capacity** — The team can't review every ticket. Any intervention strategy must respect real-world agent workload constraints

**The question**: Can we build a system that predicts which tickets will breach their SLA, ranks them by financial risk, and tells managers exactly which ones to escalate — all while staying within a realistic daily capacity?

---

## 🎯 Objectives

1. **Diagnose the root cause** — Identify which ticket types, channels, and priorities are structurally failing SLAs
2. **Quantify the cost** — Translate breaches from "missed deadlines" into actual dollars lost
3. **Build a predictive model** — Create a machine learning system that flags at-risk tickets before they breach
4. **Simulate real-world deployment** — Test the model under capacity constraints (can't review all 500+ daily tickets)
5. **Deliver an operational tool** — Build an interactive command center that managers can use to make daily escalation decisions

---

## 📊 Methodology & Approach

### Phase 1: Data Understanding & Diagnosis

The raw support ticket dataset was loaded and profiled to understand the landscape:
- **Ticket volume**: Thousands of support tickets across multiple channels (Email, Chat, Phone, Social Media)
- **Priority tiers**: Critical, High, Medium, Low — each with different SLA thresholds
- **Timestamp data**: Created, first response, and resolution timestamps for calculating actual SLA performance

### Phase 2A: Exploratory Analysis

Deep EDA was performed to understand *where* the failures were happening:
- **Breach rate by priority**: Critical tickets had disproportionate breach rates
- **Breach rate by channel**: Certain channels consistently underperformed
- **Time-based patterns**: Breaches were not random — they followed patterns based on time of day, day of week, and ticket age

### Phase 2B: Statistical Root Cause Analysis

Before jumping to solutions, we needed to validate whether the patterns were real:
- **Cramer's V analysis** confirmed that Critical priority tickets fail structurally after **8 hours** — this isn't a team performance issue; it's an SLA design problem
- Debunked the myth that specific channel teams were to blame — the failure is systemic, not team-specific

### Phase 2C: Predictive Modeling — "The Sniper"

A **cost-sensitive Random Forest** classifier was built — not optimized for generic accuracy, but specifically for **minimizing financial loss**:

| Model Decision | Approach |
|---------------|----------|
| **Objective function** | Minimize total dollar loss, not just prediction error |
| **Algorithm** | Random Forest with cost-sensitive class weights |
| **Feature engineering** | Ticket age, priority encoding, channel risk scores, time features |
| **Evaluation** | ROC-AUC (discrimination power) + financial impact simulation |

**Result**: The model achieves **89% ROC-AUC**, meaning it can reliably distinguish between tickets that will breach and those that won't.

### Phase 3A: Strategy Comparison — "The Nuke" vs. "The Sniper"

Two escalation strategies were tested:

| Strategy | Description | Result |
|----------|-------------|--------|
| **"The Nuke"** | Escalate ALL tickets flagged as any risk | Catches everything but overwhelms agents — not scalable |
| **"The Sniper"** | Escalate only the **Top 50** highest-risk tickets per day | Captures **68% of total possible savings** with a fixed, manageable workload |

The Sniper approach was chosen because it respects real-world agent capacity while still capturing the majority of preventable losses.

### Phase 3B: Financial Simulation

A capacity-aware simulation was run to quantify the actual dollar impact:

| Metric | Baseline (No AI) | With "The Sniper" | Impact |
|--------|-------------------|-------------------|--------|
| **Financial Loss** | $44,200 (Test Set) | $14,200 | **$30,000 Saved** (2-day test window) |
| **ROI** | — | 150× | **Massive return** on agent time investment |
| **Breach Rate** | High | Low | **68% reduction** in SLA breaches |
| **Agent Load** | Reactive firefighting | Fixed 50 tickets/day | **Predictable, manageable workload** |

**Projected Annual Impact**: ~$450,000 to ~$700,000 in prevented SLA penalties and churn-related losses.

### Phase 4: Operational Deployment

#### Streamlit Command Center
An interactive **SLA Risk Command Center** was built with Streamlit, allowing managers to:
- View the day's **Top 50 highest-risk tickets** (the "Kill List")
- Adjust escalation capacity dynamically with a sidebar slider
- Watch net savings update in real-time as capacity changes
- Visualize financial exposure by priority and channel

#### Tableau Dashboards
Two Tableau dashboards were published for broader organizational visibility:
- **[Operational Monitoring Dashboard](https://public.tableau.com/views/OperationalMonitoring/Dashboard2)** — Risk heatmaps, breach trends, cost analysis
- **[SLA Risk Intelligence Dashboard](https://public.tableau.com/views/SLARiskIntelligence/Dashboard1)** — ML prediction distribution, model validation, the "Kill List"

---

## 🔑 Key Findings

1. **SLA breaches are systemic, not individual** — Cramer's V analysis proves that Channel team "blame" is unfounded; the issue is structural
2. **Critical tickets have a hard 8-hour cliff** — After 8 hours without resolution, breach probability spikes dramatically
3. **Cost-sensitive ML outperforms accuracy-optimized ML** — A model trained to minimize financial loss makes fundamentally different (and better) decisions than one trained for generic accuracy
4. **Capacity constraints matter** — The "best" model is useless if agents can't act on its predictions. The Sniper strategy (Top 50/day) balances precision with real-world feasibility
5. **$30K savings in a 2-day test period** — Extrapolated, this represents a 6–7 figure annual impact

---

## 💡 Recommended Solutions

### 1. Deploy the Sniper Model in Production
- Integrate the Random Forest model into the ticketing system's API
- Each incoming ticket gets a **risk score** (0–100%) at creation time
- Sort the daily queue by risk score and present the Top 50 to the escalation team

### 2. Restructure Critical SLA Thresholds
- Current SLA for Critical tickets is too aggressive — consider a **10-hour window** instead of 8
- Alternatively, create an **"Ultra-Critical" tier** for the top 5% of risk-scored tickets with a dedicated response team

### 3. Automate First Response for Low-Risk Tickets
- Use the model's confidence scores to auto-send templated first responses for tickets with <10% breach probability
- Frees up agent capacity for legitimately high-risk tickets

---

## 🏗️ Project Structure

```
Customer-Support-SLA-Optimization/
│
├── data/                    # Processed datasets (CSV)
├── notebooks/               # Analysis & Modeling notebooks
│   └── SLA_Optimization_Master.ipynb
├── outputs/                 # Generated reports & executive slides
│   └── executive_slides.md
├── docs/                    # Documentation
├── dashboard_app.py         # Streamlit "Sniper" Command Center
├── requirements.txt         # Python dependencies
├── README.md
└── .gitignore
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.x** | Core analysis and modeling |
| **Pandas / NumPy** | Data manipulation and feature engineering |
| **Scikit-Learn** | Random Forest, cost-sensitive classification, ROC-AUC evaluation |
| **SciPy** | Cramer's V statistical testing |
| **Streamlit** | Interactive SLA Risk Command Center |
| **Tableau Public** | Organizational dashboards for monitoring and intelligence |
| **Matplotlib / Seaborn** | Exploratory visualizations |

---

## ⚙️ Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the Sniper Command Center
streamlit run dashboard_app.py
```
Use the sidebar to adjust "Escalation Capacity" and watch the Net Savings update in real-time.

---

## 🧠 Skills Demonstrated

| Skill | Application |
|-------|-------------|
| **Operational Analytics** | Translating "breach rates" into "financial exposure" |
| **Cost-Sensitive ML** | Optimizing for business value ($), not just prediction accuracy |
| **Statistical Validation** | Cramer's V to disprove incorrect narratives about team blame |
| **Simulation & Optimization** | Capacity-constrained strategy comparison (Nuke vs. Sniper) |
| **Data Product Design** | Building an interactive tool that non-technical managers can use daily |
| **Executive Communication** | Packaging complex stats into a board-ready narrative |

---

## 👤 Author

> *"Every dataset has a story. My job is to find it, prove it, and make it actionable."*

**David Ezieshi** — Business Analyst & Data Analytics  
[LinkedIn](https://www.linkedin.com/in/david-ezieshi/) | [GitHub](https://github.com/ezieshie-stack)
