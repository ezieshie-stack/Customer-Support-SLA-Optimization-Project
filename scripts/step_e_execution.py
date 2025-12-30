import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set display options
pd.set_option('display.max_columns', None)
sns.set_palette("crest")
plt.style.use('ggplot')

# Load Data
df = pd.read_csv('data/customer_support_tickets.csv')

# Preprocessing
date_cols = ['First Response Time', 'Time to Resolution']
for col in date_cols:
    df[col] = pd.to_datetime(df[col])

df['RPT_hours'] = abs((df['Time to Resolution'] - df['First Response Time']).dt.total_seconds() / 3600)
sla_rules = {'Critical': 4, 'High': 12, 'Medium': 24, 'Low': 48}
df['SLA_Target_Hours'] = df['Ticket Priority'].map(sla_rules)
df['Is_SLA_Breach'] = df['RPT_hours'] > df['SLA_Target_Hours']

baseline_breach_rate = df['Is_SLA_Breach'].mean()

# Scenario 1: Triage Optimization (20% reduction for Critical/High breaches)
df_sim1 = df.copy()
mask1 = (df_sim1['Ticket Priority'].isin(['Critical', 'High'])) & (df_sim1['Is_SLA_Breach'])
df_sim1.loc[mask1, 'RPT_hours'] = df_sim1.loc[mask1, 'RPT_hours'] * 0.8
df_sim1['Is_SLA_Breach_Sim'] = df_sim1['RPT_hours'] > df_sim1['SLA_Target_Hours']
sim1_breach_rate = df_sim1['Is_SLA_Breach_Sim'].mean()

# Scenario 2: Refund Focus (30% improvement in Refund processing)
df_sim2 = df.copy()
mask2 = (df_sim2['Ticket Type'] == 'Refund request')
df_sim2.loc[mask2, 'RPT_hours'] = df_sim2.loc[mask2, 'RPT_hours'] * 0.7
df_sim2['Is_SLA_Breach_Sim'] = df_sim2['RPT_hours'] > df_sim2['SLA_Target_Hours']
sim2_breach_rate = df_sim2['Is_SLA_Breach_Sim'].mean()

# Visualization
impact_data = pd.DataFrame({
    'Scenario': ['Baseline', 'Triage Optimization', 'Refund Focus'],
    'Breach Rate': [baseline_breach_rate, sim1_breach_rate, sim2_breach_rate]
})

plt.figure(figsize=(10, 6))
sns.barplot(data=impact_data, x='Scenario', y='Breach Rate', palette='crest', hue='Scenario', legend=False)
plt.title('Potential SLA Breach Rate Reduction')
plt.ylabel('Breach Rate')
plt.tight_layout()
plt.savefig('outputs/charts/phase_e_optimization_impact.png')

# Save Summary
impact_data.to_csv('outputs/summary_tables/phase_e_optimization_summary.csv', index=False)

print("Phase E Execution Complete. Simulation summary saved.")
