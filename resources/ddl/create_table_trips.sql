CREATE TABLE IF NOT EXISTS trips(
    id SERIAL PRIMARY KEY,
    region varchar(200),
    origin_coord text,
    destination_coord text,
    datetime timestamp,
    datasource varchar(200)
)