COPY fact_kabko FROM '/data/lat-long-data/lat-long-data.csv' DELIMITER AS ',' CSV HEADER;
SELECT * FROM fact_kabko LIMIT 5;