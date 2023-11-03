DROP TABLE IF EXISTS dim_air_quality;
CREATE TABLE IF NOT EXISTS dim_air_quality (
   n_id_aq serial primary key,
   n_id_kabko integer,
   d_date datetime,
   n_pm10 decimal(18,2),
   n_pm2_5 decimal(18,2)
);
