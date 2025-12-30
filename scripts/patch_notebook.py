import json
import os

notebook_path = '/Users/davidezieshi/Downloads/ba-projects/Customer Support Ticket Dataset/notebooks/customer_support_analytics_master.ipynb'

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Find the first code cell that has "import pandas"
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and any('import pandas' in line for line in cell['source']):
        # Found it. Let's update the source.
        # Ensure we have all the required imports
        new_imports = [
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import os\n",
            "from sklearn.model_selection import train_test_split\n",
            "from sklearn.linear_model import LogisticRegression\n",
            "from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score\n"
        ]
        
        # Preserve existing set_option and style lines
        for line in cell['source']:
            if any(x in line for x in ['pd.set_option', 'sns.set_palette', 'plt.style.use']):
                if line not in new_imports:
                    new_imports.append(line)
        
        cell['source'] = new_imports
        break

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)

print("Successfully updated notebook imports.")
