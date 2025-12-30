# Customer Support Ticket Analytics & Process Optimization

## Project Overview
This project focuses on analyzing customer support ticket data to identify bottlenecks, improve SLA compliance, and optimize support workflows. We aim to translate raw data into actionable business insights that drive operational excellence.

## Business Objectives
- **Reduce Resolution Time:** Identify factors contributing to delays and recommend improvements.
- **Improve SLA Compliance:** Analyze breach rates and patterns to ensure service standards are met.
- **Optimize Workflows:** Detect queue congestion and agent workload imbalances.
- **Identify Automation Opportunities:** Surface ticket types suitable for auto-routing or self-service.

## Core KPIs
- **Average First Response Time (FRT):** Time from ticket creation to the first agent response.
- **Average Time to Resolution (TTR):** Total duration from ticket creation to resolution.
- **SLA Breach Rate:** Percentage of tickets that exceed predefined response or resolution thresholds.
- **Customer Satisfaction (CSAT):** Average rating provided by customers after ticket resolution.

## Project Structure
- `data/`: Contains the raw customer support ticket dataset.
- `notebooks/`: 
  - `customer_support_analytics_master.ipynb`: The primary end-to-end analytical pipeline.
  - `01_...` to `07_...`: Modular phase-specific notebooks.
- `scripts/`: Utility scripts for data patching and notebook management.
- `requirements.txt`: Project dependencies for environment setup.

## Getting Started

### 1. Environment Setup
It is recommended to use a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Running the Analysis
The primary analysis is contained in `notebooks/customer_support_analytics_master.ipynb`. 
1. Open the notebook in VS Code or Jupyter.
2. Ensure the kernel is set to your `.venv`.
3. **Run the first cell (Setup)** to load libraries and configurations.
4. Execute the cells sequentially to follow the Data Analyst's journey from Quality Assessment to Executive Storytelling.

## Core KPIs & SLA Definitions
We define SLA breaches based on **Resolution Processing Time (RPT)** vs **Priority-based Targets**:
- **Critical**: 4 Hours
- **High**: 12 Hours
- **Medium**: 24 Hours
- **Low**: 48 Hours

Breach impacts are quantified using business cost proxies to provide actionable optimization roadmaps.
