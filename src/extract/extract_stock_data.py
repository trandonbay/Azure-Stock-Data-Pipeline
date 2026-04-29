from config.loader import load_config
import yfinance as yf
import pandas as pd

def extract_stock_data(tickers: list[str], start: str, end: str) -> pd.Dataframe:

    # Download stock data using Yahoo Finance API
    df = yf.download(tickers=tickers,
                     start=start,
                     end=end, 
                     group_by="ticker",
                     threads=True)

    return df

# if __name__ == "__main__":
#     stocks = load_config("stocks")["mag7"]
#     data = extract_stock_data(stocks, "2026-04-20", "2026-04-25")
#     print(data)
#     data = extract_stock_data().to_json()
#     for ticker in stocks:
#         data[ticker].head().to_csv(f"./data/raw/{ticker}_raw_data.csv")