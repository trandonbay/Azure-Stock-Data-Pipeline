CREATE TABLE dim_stock (
    stock_id INT PRIMARY KEY,
    ticker VARCHAR(10),
    company_name VARCHAR(100)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    date DATE,
    year INT,
    month INT,
    day INT
);

CREATE TABLE fact_stock_prices (
    date_id INT,
    stock_id INT,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,

    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (stock_id) REFERENCES dim_stock(stock_id)
);