import os
import pandas as pd
import yfinance as yf

TICKERS = ["ABEV3"]
INICIO = "2010-01-01"

os.makedirs("data", exist_ok=True)

for ticker in TICKERS:
    df = yf.download(f"{ticker}.SA", start=INICIO, auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    saida = df[["Close"]].dropna().rename(columns={"Close": "fechamento"})
    saida.index = saida.index.strftime("%Y-%m-%d")
    saida.index.name = "data"
    saida.to_csv(f"data/{ticker}.csv")
    print(ticker, len(saida), "linhas")
