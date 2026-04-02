# CRIS-datasets
## Cryptocurrency Regulatory Intelligence System (CRIS): Dataset Repository

This repository contains the datasets used in the research study:

**A Transformer Based Statistical System for Regulatory Risk Index Estimation and Forecasting in Cryptocurrency Markets Using Financial Text Data**

The datasets support regulatory text analysis, semantic classification, severity modeling, and construction of the Regulatory Risk Impact Factor (R2IF).

---

# Repository Structure

CRIS-datasets/

│  
├── news/  
│   ├── cryptonews.csv  
│   ├── crypto_regulatory_news.csv  
│  
├── market/  
│   ├── BTC.csv  
│   ├── ETH.csv  
│   ├── BNB.csv  
│   ├── XRP.csv  
│   ├── ADA.csv  
│   ├── SOL.csv  
│   └── additional cryptocurrency price files  
│  
└── README.md  

---

# Dataset Description

This repository contains two primary categories of datasets used for regulatory risk modeling and statistical analysis.

---

## 1. Regulatory and Cryptocurrency News Dataset

**Location:**  
`news/`

**Files:**
- cryptonews.csv  
- crypto_regulatory_news.csv  

These datasets include:

- Cryptocurrency related news articles  
- Regulatory announcements  
- Policy changes and enforcement actions  
- Government and institutional statements  

**Typical columns:**
- Date  
- Title  
- Content  
- Source  
- URL  

**Usage in system:**

- Regulatory intent classification  
- Semantic feature extraction using transformer models  
- Regulatory signal detection  
- Severity score computation  

---

## 2. Cryptocurrency Market Dataset

**Location:**  
`market/`

**Files:**
- BTC.csv  
- ETH.csv  
- BNB.csv  
- XRP.csv  
- ADA.csv  
- SOL.csv  
- Additional cryptocurrency price files  

**Each file contains:**

- Date  
- Open  
- High  
- Low  
- Close  
- Volume  
- Market Capitalization  

**Usage in system:**

- Market behavior analysis  
- Validation of Regulatory Risk Impact Factor  
- Econometric modeling and correlation analysis  
- Forecasting and trend evaluation  

---

# Dataset Sources

The datasets are collected from publicly available sources, including:

- Kaggle datasets:
  - Cryptocurrency Price History  
  - Crypto News datasets  

- CoinMarketCap:
  - https://coinmarketcap.com/

- Cryptocurrency news platforms:
  - CoinDesk  
  - CoinTelegraph  
  - CryptoSlate  
  - Bitcoin Magazine  

These sources provide comprehensive coverage of regulatory developments and market activity.

---

# Purpose of Dataset in CRIS System

These datasets support the CRIS system for:

- Regulatory signal detection  
- Transformer based semantic classification  
- Severity score computation  
- Construction of Regulatory Risk Impact Factor (R2IF)  
- Econometric validation and statistical analysis  
- Time series forecasting of regulatory risk  

---

# Regulatory Risk Impact Factor (R2IF)

The system processes regulatory text and computes:

Regulatory Severity Score  
↓  
Temporal aggregation  
↓  
Regulatory Risk Impact Factor (R2IF)

This index represents the intensity of regulatory pressure in cryptocurrency markets over time.

Market data is used to validate the statistical relationship between regulatory risk and market behavior.

---

# Data Characteristics

- **Data Type:** Structured and semi structured  
- **Format:** CSV  
- **Time Span:** 2014 – 2023  
- **Domain:** Cryptocurrency regulation and financial markets  

No personal or sensitive data is included.  
All datasets are derived from publicly available sources.

---

# Reproducibility

This dataset supports reproducibility of the proposed system, including:

- Regulatory classification  
- Severity estimation  
- Risk index construction  
- Statistical validation  
- Forecasting experiments  

---

# Citation

If you use this dataset, please cite:

**A Transformer Based Statistical System for Regulatory Risk Index Estimation and Forecasting in Cryptocurrency Markets Using Financial Text Data**

---

# License

This dataset is provided for academic and research purposes only.  
All original data rights belong to their respective sources.

---

# Contact

**Veerababu Reddy**  
Department of IT  
Vignan's Lara Institute of Technology and Science  
Email: rveerababu_vlits@vignan.ac.in  

**Durga Prasad Pragada**  
Department of MCA  
Vignan's Lara Institute of Technology and Science  
Email: durgaprasadpragada90@gmail.com  

---

# End of README
