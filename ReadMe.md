# Sample Jupyter Project

Going through the motions of creating a project.

---

## 📂 Project Structure

```
your-project/
│
├── .vscode/               # VS Code workspace settings
├── notebooks/             # Jupyter notebooks
├── src/                   # Python source code
├── data/
│   ├── raw/               # Original, immutable data
│   ├── processed/         # Cleaned / transformed data
│   └── external/          # Third‑party datasets
│
├── environment.yml        # Reproducible conda environment
└── README.md              # Project documentation
```

---

## 🧪 Environment Setup

This project uses a reproducible conda environment defined in `environment.yml`.

### Create the environment

```bash
conda env create -f environment.yml
conda activate test01-env
```

### Update the environment (if dependencies change)

```bash
conda env update -f environment.yml --prune
```

---

## 🧠 Development Workflow

### 1. Open the VS Code workspace

Use the `.code-workspace` file located one level above the project folder:

```
your-project.code-workspace
```

This ensures VS Code automatically:

- selects the correct Python interpreter  
- activates the `ds` environment  
- configures Jupyter kernels  
- applies formatting and linting rules  

### 2. Working with notebooks

All notebooks live in:

```
notebooks/
```

VS Code will prompt you to select the `ds` kernel when you open a notebook.

---

## 📊 Data

Data is organised using the standard *cookiecutter‑data‑science* layout:

- `data/raw/` — untouched source data  
- `data/processed/` — cleaned datasets ready for analysis  
- `data/external/` — third‑party or reference datasets  

Raw data should **not** be committed to Git.

---

## 🧩 Code Organisation

Place reusable Python modules in:

```text
src/
```

Example structure:

```text
src/
├── __init__.py
├── data_loader.py
├── preprocessing.py
└── analysis.py
```

Import modules in notebooks using:

```python
from src.preprocessing import clean_data
```

---

## 📝 Formatting & Standards

This project uses:

- **Black** for Python formatting  
- **jupyterlab-code-formatter** for notebook formatting  
- **VS Code settings** stored in `.vscode/settings.json`  

Formatting runs automatically on save.

---

## 📈 Reproducibility

To reproduce results:

1. Clone the repository  
2. Create the conda environment  
3. Open the VS Code workspace  
4. Run notebooks in order (if applicable)  

---

## 📚 References

Add academic references here if the project is part of coursework or your dissertation.

---

## ✔️ Status

- [ ] Initial setup  
- [ ] Data ingestion  
- [ ] Exploratory analysis  
- [ ] Modelling  
- [ ] Evaluation  
- [ ] Report writing  

---

## 📬 Contact

Author: **Tushar Karsan**  
GitHub: https://github.com/TusharKarsan  
LinkedIn: https://www.linkedin.com/in/tusharkarsan/

