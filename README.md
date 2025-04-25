# End-to-End Data Pipeline Development 🛠️📊

This project is an end-to-end data pipeline workflow that automates data extraction, cleaning, SQL integration, and visualization using Power BI. The target dataset is extracted from Amazon's product listings using web scraping and follows through multiple stages for clean analysis and insights.

## 📌 Project Phases

The project is organized into **four major phases**:

---

### 🔍 Phase 1: Web Scraping

- **File**: `amazon.py`  
  Uses **Selenium** to scrape product data from the Amazon website.

- **File**: `chromedriver.exe`  
  Required for running Selenium web scraping in a local environment.

---

### 🧹 Phase 2: Data Cleaning

- **File**: `AMAZON DATASET CLEAN.ipynb`  
  Jupyter notebook that performs step-by-step cleaning of the extracted data.

- **File**: `cean1.py`  
  Combines all cleaning operations into a single executable script for running in VS Code.

- **File**: `clean2.py`  
  A continuation of `cean1.py` to complete the full data cleaning process.

- **Folder**: `data/`  
  - `amazon_products.csv` — raw, uncleaned data.
  - `cleannew.csv` — final cleaned data.

---

### 📈 Phase 3: Data Visualization (Graphing)

- **File**: `AMAZON DATASET GRAPHS.ipynb`  
  Generates insightful graphs and visualizations based on the cleaned dataset.

---

### 🗃️ Phase 4: SQL Integration

- **File**: `sql1.ipynb`  
  SQL queries and analysis using the cleaned data in Mysql or sqlite.

---

### 📊 Bonus Phase: Power BI Dashboard

- **File**: `Amazondashboard.pbix`  
  Power BI file with a dashboard built on the cleaned dataset for interactive visualizations and insights.

---

## 🚀 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sushmithaloknath/Endtoend-data-pipeline-development.git
