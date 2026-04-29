from config.loader import load_config
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from src.extract.extract_stock_data import extract_stock_data
from src.transform.transform_stock_data import transform_stock_data
import logging

load_dotenv()

connection_string = os.getenv("CONNECTION_STRING")

# Create client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Container name
container_name = "stock-data"

date_str = datetime.now().strftime("%Y-%m-%d")

stocks = load_config("stocks")["mag7"]
stock_df = extract_stock_data(stocks, "2026-04-20", "2026-04-25")

# Load raw data
raw_stock_data = stock_df.to_json()
blob_name = f"raw/stock_data_{date_str}.json"
blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)
if blob_client.exists():
    print(f"Raw data already exists: {blob_name}")
else:
    blob_client.upload_blob(raw_stock_data)

# Load processed data - FUTURE: load as parquet
stocks_mapping = {}
for i in range(len(stocks)):
    stocks_mapping[stocks[i]] = i+1
for ticker in stocks:
    processed_stock_data = transform_stock_data(stock_df, ticker, stocks_mapping).to_csv(index=False)
    blob_name = f"processed/symbol={ticker}/date={date_str}/data.csv"
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    try:
        blob_client.upload_blob(processed_stock_data, overwrite=True)
    except Exception as e:
        print(f"Failed to upload {ticker}: {e}")

logging.basicConfig(level=logging.INFO)
logging.info("Upload successful!")