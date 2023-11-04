COPY fact_kabko FROM '/data/lat-long-data/lat_long_data.csv' DELIMITER AS ',' CSV HEADER;
SELECT * FROM fact_kabko LIMIT 5;