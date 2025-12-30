import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set display options
pd.set_option('display.max_columns', None)
sns.set_palette("viridis")
plt.style.use('ggplot')

# Load Data
df = pd.read_csv('data/customer_support_tickets.csv')

# Data Preprocessing
date_cols = ['Date of Purchase', 'First Response Time', 'Time to Resolution']
for col in date_cols:
    df[col] = pd.to_datetime(df[col])

df['Customer Satisfaction Rating'] = df['Customer Satisfaction Rating'].fillna(df['Customer Satisfaction Rating'].median())

# Derived columns for analysis
# TTR is Resolution - First Response (Processing Time)
df['TTR_hours'] = (df['Time to Resolution'] - df['First Response Time']).dt.total_seconds() / 3600
# FRT lag cannot be calculated accurately without creation date, so we focus on Processing Time.

# 1. Ticket Volume Breakdown
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

sns.countplot(data=df, x='Ticket Type', ax=axes[0,0], palette='viridis')
axes[0,0].set_title('Volume by Ticket Type')
axes[0,0].tick_params(axis='x', rotation=45)

sns.countplot(data=df, x='Ticket Priority', ax=axes[0,1], order=['Low', 'Medium', 'High', 'Critical'], palette='viridis')
axes[0,1].set_title('Volume by Priority')

sns.countplot(data=df, x='Ticket Channel', ax=axes[1,0], palette='viridis')
axes[1,0].set_title('Volume by Channel')

sns.countplot(data=df, x='Product Purchased', ax=axes[1,1], palette='viridis')
axes[1,1].set_title('Volume by Product')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('outputs/charts/phase_b_volume_breakdown.png')

# 2. Time Metrics (TTR)
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Ticket Type', y='TTR_hours', hue='Ticket Priority', palette='viridis')
plt.title('Time to Resolution (Hours) by Type and Priority')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/charts/phase_b_ttr_distribution.png')

# 3. CSAT vs TTR
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Customer Satisfaction Rating', y='TTR_hours', palette='viridis', errorbar=None)
plt.title('Average Resolution Time vs Customer Satisfaction')
plt.tight_layout()
plt.savefig('outputs/charts/phase_b_csat_vs_ttr.png')

# 4. Summary Table
ops_summary = df.groupby('Ticket Type').agg({
    'Ticket ID': 'count',
    'TTR_hours': 'mean',
    'Customer Satisfaction Rating': 'mean'
}).rename(columns={
    'Ticket ID': 'Ticket Volume', 
    'TTR_hours': 'Avg RPT (Hrs)', 
    'Customer Satisfaction Rating': 'Avg CSAT'
})
ops_summary.to_csv('outputs/summary_tables/phase_b_ops_summary.csv')

print("Phase B Execution Complete. Outputs saved to outputs/charts/ and outputs/summary_tables/.")
