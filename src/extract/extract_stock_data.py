import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()

stocks = os.getenv("MAG_SEVEN")

def extract_stock_data():
    df = yf.download(tickers=stocks, group_by="ticker")
    return df

# if __name__ == "__main__":
#     data = extract_stock_data().to_json()
#     for ticker in stocks:
#         data[ticker].head().to_csv(f"./data/raw/{ticker}_raw_data.csv")