from config.loader import load_config
from azure.storage.blob import BlobServiceClient
from src.extract.extract_stock_data import extract_stock_data
from src.transform.transform_stock_data import transform_stock_data
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Step 1: Create client to Azure Blob Storage
connection_string = os.getenv("CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Step 2: Extract stock data
stocks = load_config("stocks")["mag7"]
before = (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d")
now = datetime.now().strftime("%Y-%m-%d")
stocks_df = extract_stock_data(stocks, before, now)

# Step 3: Transform stock data
stocks_df = transform_stock_data(stocks_df)

# Step 4: Load stock data
container_name = "stock-data"
blob_name = f"bronze/stock_data_{now}.csv"
blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)
if blob_client.exists():
    print(f"Stock data already exists: {blob_name}")
else:
    blob_client.upload_blob(stocks_df.to_csv(index=False))

logger.info("Upload successful!")