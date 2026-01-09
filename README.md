# Customer Support SLA Optimization — $30K Monthly Savings via Predictive Escalation

## Executive Summary
This project identifies structural SLA failures in customer support operations and deploys a predictive decision system (“The Sniper”) that reduces breach-related financial loss by **68%** under realistic capacity constraints. Using statistical validation, machine learning, and cost-based simulation, the solution converts analytics into an operational command center suitable for executive deployment.

## The Business Problem
Support operations currently manage tickets using detailed priority queues but lack real-time visibility into breach risk.
*   **Critical SLA breaches are expensive**, driving $213k in historical operational waste.
*   **Manual escalation is reactive**, often catching issues only after they have failed.
*   **Leadership lacks a lever** to balance intervention capacity against financial risk.

## The Solution
This operational intelligence suite moves the organization from "Firefighting" to "Sniper-Like Precision":

*   **Diagnosis (Phase 2B)**: Statistical proofs (Cramer's V) confirmed that "Critical" priority tickets fail structurally after 8 hours, debunking the myth that specific channel teams were to blame.
*   **Prediction (Phase 2C)**: A cost-optimized Random Forest model flags incoming tickets with **89% ROC-AUC** accuracy, trained specifically to minimize financial loss rather than just prediction error.
*   **Simulation (Phase 3B)**: A capacity-aware simulation proved that reviewing just the **Top 50** riskiest tickets/day yields 68% of the total possible benefit, optimizing for team workload.
*   **Product (Phase 4B)**: An interactive **SLA Risk Command Center** (Streamlit) allows managers to visualize live risks and adjust escalation capacity dynamically.

## Key Results
| Metric | Baseline (No AI) | With "The Sniper" | Impact |
| :--- | :--- | :--- | :--- |
| **Financial Loss** | $44,200 (Test Set) | $14,200 | **$30,000 Saved** (2 Days) |
| **ROI** | — | 150x | **High Return** on Agent Time |
| **Breach Risk** | High | Low | **68% Reduction** |
| **Operational Impact** | Reactive | Proactive | **Fixed 50 Tickets/Day** Load |

**Projected Annual Impact:** ~$450,000 to ~$700,000 in prevented SLA penalties and churn risk.

## Visual Analytics Dashboards

Interactive Tableau dashboards provide **stats at a click** for operational monitoring and ML-powered intervention planning:

### 📊 [Operational Monitoring Dashboard](https://public.tableau.com/views/OperationalMonitoring/Dashboard2?:language=en-US&:display_count=n&:origin=viz_share_link)
- Risk Heatmap (Priority × Channel)
- SLA Breach Trends
- Cost by Channel Analysis
- Interactive filters for real-time exploration

### 🤖 [SLA Risk Intelligence Dashboard](https://public.tableau.com/views/SLARiskIntelligence/Dashboard1?:language=en-US&:display_count=n&:origin=viz_share_link)
- ML Model Risk Distribution (Prediction Histogram)
- Model Accuracy Validation (Risk Bucket vs Actual Breaches)
- **Top 50 Kill List** — Highest-risk tickets for immediate intervention
- Breach Rate by Priority with ML insights

> **Architecture**: `Raw Data → Python ML Pipeline (89% ROC-AUC) → Predictions CSV → Tableau Visualization`

## Repository Structure
```
Customer-Support-SLA-Optimization/
│
├── data/                  # Processed datasets (CSV)
├── notebooks/             # Analysis & Modeling Logic
│   └── SLA_Optimization_Master.ipynb
├── outputs/               # Generated Artifacts
│   └── executive_slides.md
├── dashboard_app.py       # The "Sniper" Command Center (Streamlit)
├── requirements.txt       # Project Dependencies
├── README.md              # Executive Overview
└── .gitignore
```

## How to Run

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Launch the Command Center**
    ```bash
    streamlit run dashboard_app.py
    ```
    *Use the sidebar to adjust the "Escalation Capacity" and watch the Net Savings update in real-time.*

## Skills Demonstrated
*   **Operational Analytics**: Translating "breach rates" into "financial exposure".
*   **Predictive Modeling**: Cost-sensitive Machine Learning (Random Forest) optimizing for business value ($), not just accuracy.
*   **Data Visualization**: Interactive Tableau dashboards for operational monitoring and ML insights.
*   **Simulation & Optimization**: Designing capacity-constrained strategies (The Nuke vs The Sniper) for real-world deployment.
*   **Executive Science**: Packaging complex stats into a board-ready narrative and interaction model.

---
*Built by David Ezieshi — Senior Operations Analyst Portfolio*
