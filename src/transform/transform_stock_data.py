from config.loader import load_config
import pandas as pd

def transform_stock_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.stack(level=0).reset_index()
    df.columns = [col.lower() for col in df.columns]
    df["date"] = pd.to_datetime(df["date"])

    df.rename(columns={
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price"
    }, inplace=True)

    return df

# if __name__ == "__main__":
#     from src.extract.extract_stock_data import extract_stock_data
#     stocks = load_config("stocks")["mag7"]
#     raw_df = extract_stock_data(stocks, "2026-04-20", "2026-04-25")

#     clean_df = transform_stock_data(raw_df)
#     print(clean_df)