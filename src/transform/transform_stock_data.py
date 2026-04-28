from src.extract.extract_stock_data import extract_stock_data
import os
from dotenv import load_dotenv

stocks = os.getenv("MAG_SEVEN")
stocks = stocks.split(", ")

stocks_mapping = {}
for i in range(len(stocks)):
    stocks_mapping[stocks[i]] = i+1

def transform_stock_data(df, ticker):
    df.reset_index(inplace=True)
    df.columns = [col.lower() for col in df.columns]

    df["date"] = df["date"].astype(str)
    df["date_id"] = df["date"].str.replace("-", "").astype(int)

    df["stock_id"] = stocks_mapping[ticker]

    df = df[[
        "date_id",
        "stock_id",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]]

    return df

# if __name__ == "__main__":
#     raw_df = extract_stock_data()
    # print(transform_stock_data(raw_df["NVDA"], "NVDA"))
    # print(stocks)

    # for ticker in stocks:
    #     processed_df = transform_stock_data(raw_df[ticker], ticker)
    #     processed_df.to_csv(f"./data/processed/{ticker}_processed_data.csv")