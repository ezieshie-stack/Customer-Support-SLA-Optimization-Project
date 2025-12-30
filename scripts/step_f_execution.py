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
df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'])

# 1. Dashboard Data Preparation
daily_kpis = df.set_index('Date of Purchase').resample('D').agg({
    'Ticket ID': 'count'
}).rename(columns={'Ticket ID': 'Ticket_Volume'})

# Smooth and Detect
daily_kpis['Volume_7D_Avg'] = daily_kpis['Ticket_Volume'].rolling(window=7).mean()
mean_vol = daily_kpis['Ticket_Volume'].mean()
std_vol = daily_kpis['Ticket_Volume'].std()
threshold = mean_vol + (2 * std_vol)
daily_kpis['Is_Anomaly'] = daily_kpis['Ticket_Volume'] > threshold

# 2. Visualization
plt.figure(figsize=(12, 6))
plt.plot(daily_kpis.index, daily_kpis['Ticket_Volume'], alpha=0.3, label='Daily Volume', color='gray')
plt.plot(daily_kpis.index, daily_kpis['Volume_7D_Avg'], label='7-Day Rolling Avg', color='green', linewidth=2)
plt.axhline(y=threshold, color='red', linestyle='--', label='Alert Threshold (2STD)')
plt.fill_between(daily_kpis.index, threshold, daily_kpis['Ticket_Volume'], where=daily_kpis['Is_Anomaly'], color='red', alpha=0.3, label='Alert Zone')

plt.title('Automated Monitoring: Ticket Demand & Alert Zones')
plt.xlabel('Time')
plt.ylabel('Ticket Count')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/charts/phase_f_demand_monitoring.png')

# 3. Save Logic
daily_kpis.tail(10).to_csv('outputs/summary_tables/phase_f_monitoring_sample.csv')

print("Phase F Execution Complete. Monitoring charts and alert logic exported.")
