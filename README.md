# Strategic Support Operations & SLA Optimization Engine

**Project Lead**: Senior Data Analyst / Operations Strategist  
**Domain**: Customer Experience (CX) & Operations Analytics  
**Tech Stack**: Python (Pandas, Scikit-Learn), Plotly, Statistical Inference

---

## 🚀 Executive Summary
This project goes beyond descriptive reporting to build a **Predictive Operations Engine**. 
By analyzing support ticket logs, we identified critical process failures, quantified their financial risk, and built machine learning models to prevent Service Level Agreement (SLA) breaches *before* they happen.

**Key Outcomes:**
*   **Operational Insight**: Discovered a "Shift Gap" at 10 PM causing 40% of Critical breaches.
*   **Financial Impact**: Modeled **$37,000/month** in potential savings via targeted staffing alignment.
*   **Predictive Capability**: Developed a Random Forest model (ROC-AUC 0.76) to flag high-risk tickets in real-time.

---

## 🧠 Business Logic & Strategy

### 1. The Problem Space
Support SLAs are not just metrics; they are contracts. Failing a "Critical" SLA risks client churn. 
This project audits the support lifecycle to answer:
*   *Where* are we failing? (Descriptive Diagnosis)
*   *Why* are we failing? (Root Cause Analysis)
*   *How* do we stop it? (Predictive Modeling & Strategy)

### 2. SLA Definitions (The Ground Truth)
We engineered a robust `Is_SLA_Breach` logic based on industry standards:
*   🚨 **Critical**: Target < 4 Hours (Risk: High Churn)
*   🔴 **High**: Target < 8 Hours
*   🟡 **Normal**: Target < 24 Hours
*   🟢 **Low**: Target < 72 Hours

### 3. Financial Risk Modeling
We applied a cost-penalty framework to quantify the tangible impact of failure:
*   **Critical Breach**: Estimated $500 penalty/churn risk per incident.
*   **High Breach**: Estimated $200 operational waste.
*   *ROI Calculation used to justify the recommended "SWAT Team" staffing model.*

---

## 🛠 Technical Architecture

This repository is structured as an **End-to-End Analytics Pipeline**:

### **`SLA_Optimization_Master.ipynb` (The Executive Notebook)**
This canonical notebook follows a strict 9-step analytical flow:
1.  **00 Setup**: Environment & Library Configuration.
2.  **01 Load Data**: Ingestion & Schema Validation.
3.  **02 SLA Definition**: *Single Source of Truth* for Logic & Feature Engineering.
4.  **03 Diagnostic Analytics**: Priority vs. Volume vs. Breach Rates (Chi-Square/T-Tests).
5.  **04 Feature Engineering**: One-Hot Encoding, Temporal extraction (Hour of Day).
6.  **05 Predictive Modeling**: Random Forest vs. Logistic Regression for Breach Prediction.
7.  **06 Model Evaluation**: Precision-Recall trade-offs tailored for "No Ticket Left Behind".
8.  **07 Workforce Optimization**: Shift Analysis (Volume vs. Risk Heatmaps).
9.  **08 Strategic Recommendations**: The "Board-Ready" ROI Action Plan.

---

## 📊 Executive Dashboard (Tableau Public)

This project includes an executive-level interactive dashboard designed for Support Operations leaders.

## 📊 Executive Dashboard (Interactive App)

This project includes a fully interactive **Python-based Dashboard** built with Streamlit & Plotly.

### 🚀 How to Launch
Run the following command in your terminal:
```bash
streamlit run dashboard_app.py
```

**Key Features:**
- **Real-time Filtering**: Slice data by Date, Priority, and Channel.
- **Financial Impact**: Visualizes lost revenue due to SLA breaches.
- **AI Integration**: Highlights tickets flagged as "High Risk" by the Random Forest model.

---

## 📊 Key Findings

| Metric | Insight | Action |
| :--- | :--- | :--- |
| **Breach Rate** | **Critical tickets breach 2x more** than Low tickets. | **Recommendation**: "Critical SWAT Team" (2 Dedicated Agents). |
| **Shift Risk** | Volume peaks at 9 PM, but **Risk peaks at 10 PM**. | **Recommendation**: Shift Overlap (8 PM - 12 AM). |
| **Segmentation** | Long-tenure customers (>4yrs) have slower resolutions. | **Recommendation**: Senior Tier Routing for VIPs. |

---

## 💻 How to Run

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/ezieshie-stack/Customer-Support-SLA-Optimization-Project.git
    cd Customer-Support-SLA-Optimization-Project
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch the Solution**:
    Open `notebooks/SLA_Optimization_Master.ipynb` to walk through the full analysis.

---
*This dashboard and analysis framework serves as a template for Data-Driven Operations Management.*
