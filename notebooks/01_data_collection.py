# 01_data_collection.ipynb
# ========================
# collect earnings call transcripts and price data for project
# 2025-08-10

import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import requests
from pathlib import Path

# path check
Path("../data/raw/transcripts").mkdir(parents=True, exist_ok=True)
Path("../data/raw/market").mkdir(parents=True, exist_ok=True)

# collection
TRANSCRIPTS_PATH = Path("../data/raw/transcripts")

events_data = []
for file in TRANSCRIPTS_PATH.glob("*.txt"):
    try:
        ticker, date_str = file.stem.split("_")
        event_date = datetime.strptime(date_str, "%Y%m%d")
        events_data.append({
            "ticker": ticker,
            "event_date": event_date,
            "transcript_path": str(file)
        })
    except ValueError:
        print(f"Skipping file with unexpected name format: {file.name}")

df_events = pd.DataFrame(events_data).sort_values("event_date")
print(f"Found {len(df_events)} transcripts.")


Path("../data/interim").mkdir(parents=True, exist_ok=True)
df_events.to_csv("../data/interim/merged_events_sample.csv", index=False)
print("Saved merged events table.")
df_events.head()

#ticker data download
tickers = df_events["ticker"].unique().tolist()

min_event_date = df_events["event_date"].min()
start_date = (min_event_date - pd.Timedelta(days=365)).strftime("%Y-%m-%d")  # 1 year before earliest event
end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

print(f"Found {len(tickers)} tickers: {tickers}")
print(f"Downloading data from {start_date} to {end_date}")

# data download
for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)
    file_path = f"../data/raw/market/{ticker}.csv"
    df.to_csv(file_path)
    print(f"Saved: {file_path} ({len(df)} rows)")

# benchmark download (s&p 500 etf)
benchmark_ticker = "SPY"
df_bench = yf.download(benchmark_ticker, start=start_date, end=end_date)
df_bench.to_csv(f"../data/raw/market/{benchmark_ticker}.csv")
print(f"Saved benchmark: {benchmark_ticker}")


# end
"""
In Notebook 02:
---------------
- Clean transcript text
- Load matching price data
- Compute returns for t+1..t+5
- Merge with earnings surprise (if available)

Potential data sources for earnings surprise:
- Yahoo Finance 'Earnings' tab scraping
- Financial Modeling Prep API (free tier)
"""
