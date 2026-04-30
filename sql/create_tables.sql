CREATE TABLE stg_stock_prices (
    date DATE,
    ticker VARCHAR(10),
    open_price DECIMAL(18,4),
    high_price DECIMAL(18,4),
    low_price DECIMAL(18,4),
    close_price DECIMAL(18,4),
    volume BIGINT
);

CREATE TABLE dim_stock (
    stock_id INT IDENTITY(1, 1) PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE,
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
    open_price DECIMAL(18,4),
    high_price DECIMAL(18,4),
    low_price DECIMAL(18,4),
    close_price DECIMAL(18,4),
    volume BIGINT

--     -- FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
--     -- FOREIGN KEY (stock_id) REFERENCES dim_stock(stock_id)
);

-- Step 1a - Upsert dimensions (stock)
MERGE dim_stock AS t
USING (SELECT DISTINCT ticker FROM stg_stock_prices) s
ON t.ticker = s.ticker
WHEN NOT MATCHED THEN
INSERT (ticker) VALUES (s.ticker);

-- Step 1b - Upsert dimensions (date)
INSERT INTO dim_date (date_id, date, year, month, day)
SELECT DISTINCT
    CAST(FORMAT(date, 'yyyyMMdd') AS INT) AS date_id,
    date,
    YEAR(date),
    MONTH(date),
    DAY(date)
FROM stg_stock_prices st
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_date d
    WHERE d.date = st.date
);

-- Step 2 - Build fact
INSERT INTO fact_stock_prices
(date_id, stock_id, open_price, high_price, low_price, close_price, volume)

SELECT
    d.date_id,
    s.stock_id,
    st.open_price,
    st.high_price,
    st.low_price,
    st.close_price,
    st.volume
FROM stg_stock_prices st
JOIN dim_stock s ON st.ticker = s.ticker
JOIN dim_date d ON st.date = d.date;

SELECT * FROM fact_stock_prices;
SELECT * FROM dim_date;
SELECT * FROM dim_stock;
SELECT * FROM stg_stock_prices;