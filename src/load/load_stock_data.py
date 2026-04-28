from azure.storage.blob import BlobServiceClient
import pandas as pd
from src.extract.extract_stock_data import *
from src.transform.transform_stock_data import transform_stock_data
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

connection_string = os.getenv("CONNECTION_STRING")
stocks = os.getenv("MAG_SEVEN")
stocks = stocks.split(", ")

# Create client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Container name
container_name = "stock-data"

date_str = datetime.now().strftime("%Y-%m-%d")

# Load raw data
raw_stock_data = extract_stock_data().to_json()
blob_name = f"raw/stock_data_{date_str}.json"
blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)
if blob_client.exists():
    pass
else:
    blob_client.upload_blob(raw_stock_data)

# Load processed data
raw_stock_data = extract_stock_data()
for ticker in stocks:
    processed_stock_data = transform_stock_data(raw_stock_data[ticker], ticker).to_csv(index=False)
    blob_name = f"processed/symbol={ticker}/date={date_str}/data.csv"
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )
    blob_client.upload_blob(processed_stock_data, overwrite=True)

print("Upload successful!")