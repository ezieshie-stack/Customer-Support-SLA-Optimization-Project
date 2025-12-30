import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import os

# Set display options
pd.set_option('display.max_columns', None)
sns.set_palette("rocket")
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
df['Is_SLA_Breach'] = (df['RPT_hours'] > df['SLA_Target_Hours']).astype(int)

# Feature Engineering
features = ['Ticket Type', 'Ticket Priority', 'Ticket Channel']
X = pd.get_dummies(df[features], drop_first=True)
y = df['Is_SLA_Breach']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Model Training
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)

# Importance Visualization
importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_[0]
}).sort_values(by='Coefficient', ascending=False)

plt.figure(figsize=(10, 8))
sns.barplot(data=importance, x='Coefficient', y='Feature', palette='rocket')
plt.title('SLA Breach Risk Drivers (Log-Odds)')
plt.tight_layout()
plt.savefig('outputs/charts/phase_d_feature_importance.png')

# Save Model Summary
with open('outputs/summary_tables/phase_d_model_performance.txt', 'w') as f:
    f.write(f"ROC AUC Score: {roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]):.2f}\n")
    f.write("\nClassification Report:\n")
    f.write(classification_report(y_test, model.predict(X_test)))

print("Phase D Execution Complete. Risk drivers and performance metrics saved.")
