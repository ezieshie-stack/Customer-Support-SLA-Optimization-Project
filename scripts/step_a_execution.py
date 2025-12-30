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
print(f"Dataset shape: {df.shape}")

# Data Preprocessing
date_cols = ['Date of Purchase', 'First Response Time', 'Time to Resolution']
for col in date_cols:
    df[col] = pd.to_datetime(df[col])

# Simple handle for missing values
df['Customer Satisfaction Rating'] = df['Customer Satisfaction Rating'].fillna(df['Customer Satisfaction Rating'].median())
df['Resolution'] = df['Resolution'].fillna("No resolution recorded")

# Initial Business Overview Chart
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Ticket Type', hue='Ticket Priority', palette='viridis')
plt.title('Ticket Volume by Type and Priority')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/charts/ticket_volume_overview.png')

# Summary Statistics
summary = df.describe(include='all')
summary.to_csv('outputs/summary_tables/initial_data_profile.csv')

print("Step A Execution Complete. Outputs saved to outputs/charts/ and outputs/summary_tables/.")
