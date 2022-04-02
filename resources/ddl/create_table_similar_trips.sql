CREATE TABLE IF NOT EXISTS trips(
    id SERIAL PRIMARY KEY,
    region varchar(200),
    origin_coord text,
    destination_coord text,
    datetime timestamp,
    datasource varchar(200),
    origin_coord_lat text,
    origin_coord_lng text,
    destination_coord_lat text,
    destination_coord_lng text
)