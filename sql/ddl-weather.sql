DROP TABLE IF EXISTS dim_weather;
CREATE TABLE IF NOT EXISTS dim_weather (
   n_id_weather serial primary key,
   n_id_kabko integer REFERENCES fact_kabko(n_id_kabko),
   d_date timestamp,
   n_temperature_2m decimal(18,2),
   n_relativehumidity_2m integer,
   n_visibility decimal(18,2),
   n_uv_index decimal(18,2)
);
