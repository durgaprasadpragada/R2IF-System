# R2IF System

## Regulatory Risk Index Estimation and Forecasting in Cryptocurrency Markets

This repository contains a complete implementation of a data-driven system for analyzing regulatory risk in cryptocurrency markets using financial text data and time-series modeling.

The system processes regulatory news, computes severity scores, constructs a risk index, and performs statistical forecasting.

---

# Overview

The system follows a structured analytical pipeline:

User Input → Text Processing → NLP Classification → Severity Scoring → Risk Index (R2IF) → Statistical Analysis → Forecasting

All outputs are dynamically generated based on the input data provided by the user.

---

# Project Structure

```
R2IF-System/

app/            → Core application logic  
datasets/       → Input datasets (user-provided or sample)  
outputs/        → Generated results  
```

---

# Core Modules

### main.py

Controls the full pipeline:

* Accepts input data
* Executes preprocessing, NLP, severity scoring
* Computes risk index
* Runs statistical models

---

### ui.py

Streamlit-based interactive dashboard:

* Accepts user input (file upload or manual)
* Displays metrics and results
* Triggers analysis and prediction
* Shows interactive visualizations

---

### data_loader.py

Handles:

* File uploads
* Column detection and mapping
* Data validation

---

### preprocessing.py

Performs:

* Text normalization
* Cleaning and formatting

---

### nlp_model.py

Implements:

* Financial sentiment analysis using FinBERT
* Outputs:

  * Sentiment label
  * Confidence score

---

### severity_model.py

Computes regulatory severity using:

S = (W + P + C + L) / 4

Where:

* W = country/regional signals
* P = policy/regulation keywords
* C = coverage/impact scope
* L = NLP model confidence

---

### risk_index.py

Constructs the Regulatory Risk Index (R2IF):

* Aggregates severity scores by date
* Produces time-series representation

---

### econometrics.py

Performs statistical analysis:

* ADF Test
* Linear Regression
* Granger Causality
* ARIMA Forecasting

---

### visualization.py

Generates interactive plots:

* Risk index trends
* Price vs severity relationship
* Forecast visualization

---

# Input Data Format

## News Dataset

Required columns:

* content (or text/title)
* date

Example:

```
content,date
government imposes crypto ban,2023-01-01
```

---

## Market Dataset

Required columns:

* date
* price (or close)

Example:

```
date,price
2023-01-01,42000
```

---

# How to Run the Project

## Step 1: Install dependencies

```
pip install -r requirements.txt
```

---

## Step 2: Run the application

```
streamlit run app/ui.py
```

---

## Step 3: Use the interface

1. Upload:

   * News dataset
   * Price dataset
     OR
     Enter manual input

2. Click:

   * Run Analysis

3. View:

   * Metrics
   * Severity scores
   * Risk index

4. Click:

   * Run Prediction

5. View:

   * Forecast graphs

---

# Outputs

Generated files are stored in:

```
outputs/
```

Includes:

* classified_news.csv
* severity_scores.csv
* r2if_timeseries.csv

---

# Features

* Fully dynamic input-driven system
* Transformer-based NLP classification
* Regulatory severity modeling
* Time-series risk index construction
* Econometric validation
* Forecasting using ARIMA
* Interactive visualization dashboard

---

# Notes

* The system works for both single input and batch datasets
* Results vary based on input data
* Larger datasets improve statistical accuracy

---

# License

This project is intended for academic and research purposes.

---

# Authors

Durga Prasad Pragada
Department of MCA

Veerababu Reddy
Department of IT

---

# End
