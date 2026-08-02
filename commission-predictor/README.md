# Commission Predictor

A machine learning pipeline that predicts the expected commission of a marketplace sales request, combining a conversion classifier with a fee regressor.

## Problem

Given a sales request (listing price, market estimate, seller/buyer info, etc.), estimate:
1. **Will it convert?** — probability the request results in a confirmed sale
2. **How much commission?** — expected fee (EUR) if it converts

The final output is the **expected commission per request**: `P(conversion) × predicted_fee`.

## Approach

1. **Data cleaning** — drop identifier/leakage columns, impute missing numeric values with the median, group rare brands into `Other`, one-hot encode categorical features
2. **Classification** — Logistic Regression, Random Forest, and XGBoost predict `SALE_CONFIRMED`
3. **Regression** — Linear Regression and Random Forest predict `SALE_FEE_EUR`, trained only on converted requests
4. **Combination** — multiply the classifier's conversion probability by the regressor's predicted fee to get the expected commission

## Results

| Stage | Best model | Key metric |
|---|---|---|
| Classification (conversion) | XGBoost | Accuracy 0.94, ROC AUC 0.97 |
| Regression (fee, EUR) | Random Forest | MAE 10.94, R² 0.98 |
| Combined (expected commission) | XGBoost + Random Forest | MAE 17.53 EUR |

## Data

`data/data.xlsx` — 37,672 sales requests, 21 columns, including:

`REQUEST_TYPE`, `LISTING_PRICE_EUR`, `MARKET_PRICE_EUR_ESTIMATE`, `MARKET_PRICE_DATA_STRENGTH_SCORE`, `USER_COUNTRY`, `LISTING_TYPE`, `SELLER_TYPE`, `STOCK_INFO`, `BRAND_NAME`, `CONDITION_CLASS`, `HANDLING_TIME_IN_DAYS`, `SALE_CONFIRMED`, `SALE_FEE_EUR`

The `data/` folder is not included in this repository.

## Project structure

```
src/
├── config.py           # paths
├── data_exploration.py # dataset overview
├── data_processing.py  # cleaning, encoding, train/test split
├── train_and_eval.py   # model training and evaluation
└── main.ipynb           # end-to-end pipeline
```

## Setup

```bash
pip install -r requirements.txt
```

Place `data.xlsx` in a `data/` folder, then run `src/main.ipynb`.

## Tech stack & Algorithms

- Tools & Libraries: Python, pandas, scikit-learn, matplotlib, numpy
- Classification Models: Logistic regression, Random forest, XGBoost classifier
- Regression Models: Linear regression,  Radom forest regressor

