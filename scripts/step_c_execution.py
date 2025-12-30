import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set display options
pd.set_option('display.max_columns', None)
sns.set_palette("magma")
plt.style.use('ggplot')

# Load Data
df = pd.read_csv('data/customer_support_tickets.csv')

# Data Preprocessing
date_cols = ['First Response Time', 'Time to Resolution']
for col in date_cols:
    df[col] = pd.to_datetime(df[col])

# Calculating Resolution Processing Time (RPT) using absolute values
df['RPT_hours'] = abs((df['Time to Resolution'] - df['First Response Time']).dt.total_seconds() / 3600)

# Define SLA Thresholds (Synthetic Business Rules)
sla_rules = {'Critical': 4, 'High': 12, 'Medium': 24, 'Low': 48}
df['SLA_Target_Hours'] = df['Ticket Priority'].map(sla_rules)
df['Is_SLA_Breach'] = df['RPT_hours'] > df['SLA_Target_Hours']

# 1. SLA Breach Analysis Charts
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.barplot(data=df, x='Ticket Type', y='Is_SLA_Breach', ax=axes[0], palette='magma', errorbar=None)
axes[0].set_title('SLA Breach Rate by Ticket Type')
axes[0].tick_params(axis='x', rotation=45)

sns.barplot(data=df, x='Ticket Priority', y='Is_SLA_Breach', order=['Low', 'Medium', 'High', 'Critical'], ax=axes[1], palette='magma', errorbar=None)
axes[1].set_title('SLA Breach Rate by Priority')

plt.tight_layout()
plt.savefig('outputs/charts/phase_c_sla_breach_analysis.png')

# 2. Bottleneck Detection
p90_threshold = df['RPT_hours'].quantile(0.9)
df['Is_Bottleneck'] = df['RPT_hours'] > p90_threshold

bottleneck_drivers = df[df['Is_Bottleneck']].groupby(['Ticket Type', 'Ticket Channel']).size().unstack().fillna(0)

plt.figure(figsize=(12, 8))
sns.heatmap(bottleneck_drivers, annot=True, fmt='.0f', cmap='magma')
plt.title('Extreme Bottlenecks (P90) by Type and Channel')
plt.tight_layout()
plt.savefig('outputs/charts/phase_c_bottleneck_heatmap.png')

# 3. Diagnostic Summary
diagnostic_summary = df.groupby('Ticket Type').agg({
    'Is_SLA_Breach': 'mean',
    'RPT_hours': ['mean', 'max', 'std'],
    'Is_Bottleneck': 'sum'
})
diagnostic_summary.to_csv('outputs/summary_tables/phase_c_diagnostic_summary.csv')

print("Phase C Execution Complete. Outputs saved to outputs/charts/ and outputs/summary_tables/.")
