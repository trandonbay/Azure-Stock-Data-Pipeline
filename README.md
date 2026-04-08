# Azure-Stock-Data-Pipeline

This project builds an end-to-end data pipeline on Microsoft Azure to ingest, store, transform, and analyze stock market data. The pipeline automates daily data ingestion and loads structured data into a cloud-based data warehouse for analytics.

1. Extract stock data using Python (yfinance)
2. Upload raw data to Azure Blob Storage
3. Transform and clean data
4. Load into Azure SQL using a star schema
5. Schedule daily pipeline runs using Data Factory
