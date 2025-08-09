# Earnings-Call Sentiment Alpha
Predict short-term abnormal returns following earnings calls using NLP and ML.

## Overview
This project builds an end-to-end pipeline that:
1. Collects earnings call transcripts and market data.
2. Extracts NLP features (VADER + FinBERT embeddings).
3. Trains ML models to predict abnormal returns 1–5 days after earnings calls.
4. Backtests an event-driven trading strategy with transaction costs and slippage.

## Repo structure
earnings-sentiment-alpha/
├── data/
│   ├── raw/
│   │   ├── transcripts/                 # raw transcripts: {TICKER}_{YYYYMMDD}.txt
│   │   └── market/                      # raw OHLCV CSVs {TICKER}.csv
│   ├── interim/                        # cleaned/merged files
│   │   └── merged_events.parquet
│   └── external/                        # earnings estimates, benchmarks (SPY.csv)
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_preprocessing_and_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training_evaluation.ipynb
│   └── 05_backtesting_and_reporting.ipynb
├── src/
│   ├── data_collection.py               # scrapers / downloaders
│   ├── preprocess.py                    # text cleaning + merging
│   ├── features.py                      # feature engineering functions
│   ├── models.py                        # training/predict wrappers
│   ├── backtest.py                      # simple backtester (custom)
│   └── utils.py                         # helpers, I/O
├── reports/
│   └── figures/                         # png/svg plots for README
├── tests/                               
│   └── test_preprocess.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── environment.yml                        # optional conda spec


## Quickstart
1. Create Python environment:
   
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Populate `data/raw/` with transcripts and `data/raw/market/` with price CSVs (scripts in `src/` help with this).
3. Run notebooks in order:
- `notebooks/01_data_collection.ipynb`
- `notebooks/02_preprocessing_and_eda.ipynb`
- `notebooks/03_feature_engineering.ipynb`
- `notebooks/04_model_training_evaluation.ipynb`
- `notebooks/05_backtesting_and_reporting.ipynb`

## Results (summary)
- Best model: LightGBM with VADER + FinBERT embeddings
- 1-day event-driven strategy (sample): Sharpe = X.XX, Hit rate = YY%
- Full report: `reports/figures/` (equity curve, feature importance, SHAP)

## Files of interest
- `src/preprocess.py` — transcript cleaning + return calculation
- `src/features.py` — sentiment & embedding extraction
- `src/models.py` — model training & saving
- `src/backtest.py` — backtest logic

## Reproducibility & Limitations
- Data sources and scraping scripts are provided, but transcript completeness varies by provider.
- Results are sensitive to transaction costs, selection bias, and survivorship bias. See notebook 05 for stress tests.

## License
MIT
