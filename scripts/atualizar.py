import os
import pandas as pd
import yfinance as yf

TICKERS = [ "ABEV3", "ALOS3", "ASAI3", "AURE3", "AXIA3", "AZZA3",
    "B3SA3", "BBAS3", "BBDC3", "BBDC4", "BBSE3", "BPAC11",
    "BRAP4", "BRAV3", "CEAB3", "CMIG4", "COGN3", "CPLE3",
    "CSMG3", "CXSE3", "ELET3", "ELET6", "EMBR3", "ENEV3",
    "EGIE3", "EQTL3", "FLRY3", "GGBR4", "GOAU4", "HAPV3",
    "HYPE3", "ITSA4", "ITUB4", "JBSS3", "KLBN11", "LREN3",
    "MGLU3", "MRFG3", "MULT3", "PETR3", "PETR4", "PRIO3",
    "RADL3", "RAIL3", "RAIZ4", "RDOR3", "RENT3", "SANB11",
    "SBSP3", "SLCE3", "SUZB3", "TAEE11", "TIMS3", "TOTS3",
    "UGPA3", "USIM5", "VALE3", "VBBR3", "VIVA3", "WEGE3",
    "YDUQ3"]
INICIO = "2000-01-01"

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
