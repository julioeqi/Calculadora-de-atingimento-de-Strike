import os
import pandas as pd
import yfinance as yf

TICKERS = ["ABEV3"]
INICIO = "2010-01-01"

os.makedirs("data", exist_ok=True)

for ticker in TICKERS:
    df = yf.download(f"{ticker}.SA", start=INICIO, auto_adjust=False, progress=False)

    if df.empty:
        print(f"Sem dados para {ticker}")
        continue

    # Achata MultiIndex colocando o nível que contém 'Close' como coluna principal
    if isinstance(df.columns, pd.MultiIndex):
        if "Close" in df.columns.get_level_values(0):
            df.columns = df.columns.get_level_values(0)
        elif "Close" in df.columns.get_level_values(1):
            df.columns = df.columns.get_level_values(1)

    # Mostra uma amostra para você conferir High vs Close no terminal
    print(df[["High", "Close"]].tail(3))

    saida = df[["Close"]].dropna().rename(columns={"Close": "fechamento"})
    saida.index = pd.to_datetime(saida.index).strftime("%Y-%m-%d")
    saida.index.name = "data"
    saida.to_csv(f"data/{ticker}.csv")
    print(f"Salvo {ticker}: {len(saida)} linhas")
