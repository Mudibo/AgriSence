# Notebooks

This folder holds exploratory analysis and model-comparison notebooks for the crop price forecasting project. The notebooks are structured for use in VS Code with the local Jupyter extension, and they intentionally avoid any Colab-only authentication or mount steps.

## Files

- `01_eda.ipynb` — exploratory analysis covering data loading, missingness, market trends, and seasonality.
- `02_baseline_comparison.ipynb` — compares the statistical baseline models and the resulting validation scores.
- `03_climate_ablation.ipynb` — assesses the impact of climate features on model performance.

## Top of every notebook
```bash
REPO_URL = ""
!git clone {REPO_URL}
%cd <your-repo>/model
!pip install -r requirements.txt
```

## Notebook Push
```python
# ── Push updated model artifact back to GitHub ───────────────────────
# Colab Secrets (userdata.get) is not yet supported in the VS Code
# Colab extension — paste your token directly here, then clear this
# cell's output before saving the notebook.

import os
os.environ['GITHUB_TOKEN'] = ""  # paste, use, then clear output

GITHUB_USERNAME = "<your-username>"
REPO_NAME = "<your-repo>"

!git config --global user.email "<your-email>"
!git config --global user.name "<your-name>"
!git remote set-url origin https://{os.environ['GITHUB_TOKEN']}@[github.com/](https://github.com/){GITHUB_USERNAME}/{REPO_NAME}.git

!git add artifacts/models/*.pkl
!git commit -m "Update trained model artifact"
!git push
```