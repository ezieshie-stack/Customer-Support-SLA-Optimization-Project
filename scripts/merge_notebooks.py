import json
import os

notebook_files = [
    'notebooks/01_data_quality_and_overview.ipynb',
    'notebooks/02_descriptive_ops_analytics.ipynb',
    'notebooks/03_diagnostic_root_cause.ipynb',
    'notebooks/04_predictive_risk_modeling.ipynb',
    'notebooks/05_optimization_simulation.ipynb',
    'notebooks/06_automation_monitoring.ipynb',
    'notebooks/07_executive_storytelling.ipynb'
]

# Essential imports to inject if a cell uses specific libraries
import_map = {
    'pd.': 'import pandas as pd',
    'np.': 'import numpy as np',
    'plt.': 'import matplotlib.pyplot as plt',
    'sns.': 'import seaborn as sns',
    'train_test_split': 'from sklearn.model_selection import train_test_split',
    'LogisticRegression': 'from sklearn.linear_model import LogisticRegression',
    'classification_report': 'from sklearn.metrics import classification_report',
    'roc_auc_score': 'from sklearn.metrics import roc_auc_score'
}

master_cells = []

# 1. Global Project Header
master_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🚀 Project 2: Customer Support Ticket Analytics (MASTER)\n",
        "---\n",
        "💡 **Pro-Tip**: Every cell in this notebook is self-contained. You can run any analytical phase independently!"
    ]
})

for nb_file in notebook_files:
    if not os.path.exists(nb_file):
        continue
        
    with open(nb_file, 'r') as f:
        nb_data = json.load(f)
        
    nb_name = os.path.basename(nb_file).replace('.ipynb', '').replace('_', ' ').title().split(' ', 1)[-1]
    master_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [f"\n\n# Phase: {nb_name}\n", "---\n"]
    })
    
    for cell in nb_data['cells']:
        if cell['cell_type'] == 'code':
            source_text = "".join(cell['source'])
            needed_imports = []
            for token, imp in import_map.items():
                if token in source_text and imp not in source_text:
                    needed_imports.append(imp + "\n")
            
            if needed_imports:
                cell['source'] = needed_imports + ["\n"] + cell['source']
                
        master_cells.append(cell)

# Structure and Save
master_nb = {
    "cells": master_cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.8.10"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open('notebooks/customer_support_analytics_master.ipynb', 'w') as f:
    json.dump(master_nb, f, indent=1)

print("Master notebook finalized with ATOMIC imports per cell.")
