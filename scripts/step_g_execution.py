import pandas as pd
import os

# Load Data
df = pd.read_csv('data/customer_support_tickets.csv')
df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'])
df['First Response Time'] = pd.to_datetime(df['First Response Time'])
df['Time to Resolution'] = pd.to_datetime(df['Time to Resolution'])
df['RPT_hours'] = abs((df['Time to Resolution'] - df['First Response Time']).dt.total_seconds() / 3600)
sla_rules = {'Critical': 4, 'High': 12, 'Medium': 24, 'Low': 48}
df['SLA_Target_Hours'] = df['Ticket Priority'].map(sla_rules)
df['Is_SLA_Breach'] = df['RPT_hours'] > df['SLA_Target_Hours']

# Create Executive Summary
summary = pd.DataFrame({
    'Metric': [
        'Total Tickets Analyzed',
        'Average Resolution Time (Hrs)',
        'Overall SLA Breach Rate',
        'Average Customer Satisfaction'
    ],
    'Value': [
        len(df),
        round(df['RPT_hours'].mean(), 2),
        f"{df['Is_SLA_Breach'].mean():.2%}",
        round(df['Customer Satisfaction Rating'].mean(), 2)
    ]
})

# Save Summary
summary.to_csv('outputs/summary_tables/final_executive_summary.csv', index=False)

# Recommendations
recommendations = pd.DataFrame({
    'Focus Area': [
        'Category Optimization',
        'Predictive Triage',
        'Channel Strategy',
        'Monitoring Sustenance'
    ],
    'Action': [
        'Assign specialized agents to Refund Requests.',
        'Prioritize tickets flagged by the SLA Breach model.',
        'Integrate Chat/Web teams to smooth demand volatility.',
        'Deploy the 7-day rolling demand dashboard.'
    ],
    'Estimated Impact': [
        '~2.5% reduction in SLA breaches.',
        '~1.5% reduction in high-priority breaches.',
        'Reduced FRT variance.',
        'Prevents staffing-related bottlenecks.'
    ]
})
recommendations.to_csv('outputs/summary_tables/final_executive_recommendations.csv', index=False)

print("Phase G Execution Complete. Executive summary and recommendations exported.")
