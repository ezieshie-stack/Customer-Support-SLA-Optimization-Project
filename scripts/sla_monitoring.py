import numpy as np
from datetime import datetime, timedelta
import os

def run_sla_watchdog():
    """
    Simulates a Daily SLA Watchdog process that identifies high-risk tickets
    and generates an operational alert report.
    """
    print("--- SLA Watchdog: Starting Daily Scan ---")
    
    # 1. Load Data
    data_path = 'data/customer_support_tickets.csv'
    if not os.path.exists(data_path):
        data_path = '../data/customer_support_tickets.csv'
    
    df = pd.read_csv(data_path)
    df['First Response Time'] = pd.to_datetime(df['First Response Time'])
    
    # 2. Apply Operational Business Rules (Calculated in Phase 3)
    sla_rules = {'Critical': 4, 'High': 12, 'Medium': 24, 'Low': 48}
    df['SLA_Target_Hours'] = df['Ticket Priority'].map(sla_rules)
    
    # 3. Simulate "Current Status" for Logic Demonstration
    # In a real system, we would compare 'Now' vs 'Created Date'
    # Here we identify tickets that are 'Open' or 'Pending' and have high exposure
    
    # Risk Factor 1: High Priority with no resolution yet
    # Risk Factor 2: Specific Categories identified by the model (Refunds)
    
    high_risk_mask = (
        (df['Ticket Status'].isin(['Open', 'Pending'])) & 
        ((df['Ticket Priority'].isin(['Critical', 'High'])) | (df['Ticket Type'] == 'Refund request'))
    )
    
    alert_report = df[high_risk_mask].copy()
    
    # 4. Quantify Financial Exposure for the Alert
    cost_map = {'Critical': 50, 'High': 50, 'Medium': 10, 'Low': 10}
    alert_report['Projected_Penalty'] = alert_report['Ticket Priority'].map(cost_map)
    
    # 5. Output Results
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"outputs/alerts/sla_alert_report_{timestamp}.csv"
    
    # Ensure directory exists
    os.makedirs('outputs/alerts', exist_ok=True)
    
    alert_report.to_csv(report_name, index=False)
    
    print(f"Daily Scan Complete.")
    print(f"Risk Tickets Identified: {len(alert_report)}")
    print(f"Total Financial Exposure in Queue: ${alert_report['Projected_Penalty'].sum():,.2f}")
    print(f"Report generated: {report_name}")
    
    return alert_report

if __name__ == "__main__":
    run_sla_watchdog()
