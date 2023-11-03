DROP TABLE IF EXISTS fact_kabko;
CREATE TABLE IF NOT EXISTS fact_kabko (
   n_id_kabko serial primary key,
   v_name varchar,
   n_lat decimal(18,6),
   n_long decimal(18,6),

);
