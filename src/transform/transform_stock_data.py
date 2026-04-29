from config.loader import load_config
import pandas as pd

def transform_stock_data(df: pd.DataFrame, ticker: str, mapping: dict) -> pd.DataFrame:
    # Retrieve DataFrame for specific stock
    try:
        df_ticker = df.xs(ticker, axis=1, level=1).copy()
    except KeyError:
        df_ticker = df.xs(ticker, axis=1, level=0).copy()
    
    df_ticker.reset_index(inplace=True)
    df_ticker.columns = [col.lower() for col in df_ticker.columns]

    # Date handling
    df_ticker["date"] = pd.to_datetime(df_ticker["date"])
    df_ticker["date_id"] = df_ticker["date"].dt.strftime("%Y%m%d").astype(int)

    # Rename columns
    df_ticker.rename(columns={
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price"
    }, inplace=True)

    # Map stocks to ID
    df_ticker["stock_id"] = mapping[ticker]

    df_ticker = df_ticker[[
        "date_id",
        "stock_id",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume"
    ]]

    return df_ticker

# if __name__ == "__main__":
#     from src.extract.extract_stock_data import extract_stock_data
#     stocks = load_config("stocks")["mag7"]
#     raw_df = extract_stock_data(stocks, "2026-04-20", "2026-04-25")

#     stocks_mapping = {}
#     for i in range(len(stocks)):
#         stocks_mapping[stocks[i]] = i+1

#     processed_df = transform_stock_data(raw_df, "AAPL", stocks_mapping)
#     print(processed_df)

    # for ticker in stocks:
    #     processed_df = transform_stock_data(raw_df[ticker], ticker)
    #     processed_df.to_csv(f"./data/processed/{ticker}_processed_data.csv")