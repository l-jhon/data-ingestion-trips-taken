-- Create table with partitions for trips table.
-- In this case was used the datetime column to partition the table by hour.

CREATE TABLE IF NOT EXISTS trips(
    id SERIAL PRIMARY KEY,
    region varchar(200),
    origin_coord text,
    destination_coord text,
    "datetime" timestamp default now(),
    datasource varchar(200)
);

CREATE INDEX IF NOT EXISTS trips_datetime_idx ON trips ("datetime");

CREATE SCHEMA trip_partition;

CREATE TABLE trip_partition.h0(
    check((extract(hour from "datetime")) >= 0 AND (extract(hour from "datetime")) < 1)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h0_datetime_idx ON trip_partition.h0 ("datetime");

CREATE TABLE trip_partition.h1(
    check((extract(hour from "datetime")) >= 1 AND (extract(hour from "datetime")) < 2)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h1_datetime_idx ON trip_partition.h1 ("datetime");

CREATE TABLE trip_partition.h2(
    check((extract(hour from "datetime")) >= 2 AND (extract(hour from "datetime")) < 3)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h2_datetime_idx ON trip_partition.h2 ("datetime");

CREATE TABLE trip_partition.h3(
    check((extract(hour from "datetime")) >= 3 AND (extract(hour from "datetime")) < 4)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h3_datetime_idx ON trip_partition.h3 ("datetime");

CREATE TABLE trip_partition.h4(
    check((extract(hour from "datetime")) >= 4 AND (extract(hour from "datetime")) < 5)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h4_datetime_idx ON trip_partition.h4 ("datetime");

CREATE TABLE trip_partition.h5(
    check((extract(hour from "datetime")) >= 5 AND (extract(hour from "datetime")) < 6)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h5_datetime_idx ON trip_partition.h5 ("datetime");

CREATE TABLE trip_partition.h6(
    check((extract(hour from "datetime")) >= 6 AND (extract(hour from "datetime")) < 7)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h6_datetime_idx ON trip_partition.h6 ("datetime");

CREATE TABLE trip_partition.h7(
    check((extract(hour from "datetime")) >= 7 AND (extract(hour from "datetime")) < 8)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h7_datetime_idx ON trip_partition.h7 ("datetime");

CREATE TABLE trip_partition.h8(
    check((extract(hour from "datetime")) >= 8 AND (extract(hour from "datetime")) < 9)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h8_datetime_idx ON trip_partition.h8 ("datetime");

CREATE TABLE trip_partition.h9(
    check((extract(hour from "datetime")) >= 9 AND (extract(hour from "datetime")) < 10)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h9_datetime_idx ON trip_partition.h9 ("datetime");

CREATE TABLE trip_partition.h10(
    check((extract(hour from "datetime")) >= 10 AND (extract(hour from "datetime")) < 11)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h10_datetime_idx ON trip_partition.h10 ("datetime");

CREATE TABLE trip_partition.h11(
    check((extract(hour from "datetime")) >= 11 AND (extract(hour from "datetime")) < 12)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h11_datetime_idx ON trip_partition.h11 ("datetime");

CREATE TABLE trip_partition.h12(
    check((extract(hour from "datetime")) >= 12 AND (extract(hour from "datetime")) < 13)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h12_datetime_idx ON trip_partition.h12 ("datetime");

CREATE TABLE trip_partition.h13(
    check((extract(hour from "datetime")) >= 13 AND (extract(hour from "datetime")) < 14)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h13_datetime_idx ON trip_partition.h13 ("datetime");

CREATE TABLE trip_partition.h14(
    check((extract(hour from "datetime")) >= 14 AND (extract(hour from "datetime")) < 15)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h14_datetime_idx ON trip_partition.h14 ("datetime");

CREATE TABLE trip_partition.h15(
    check((extract(hour from "datetime")) >= 15 AND (extract(hour from "datetime")) < 16)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h15_datetime_idx ON trip_partition.h15 ("datetime");

CREATE TABLE trip_partition.h16(
    check((extract(hour from "datetime")) >= 16 AND (extract(hour from "datetime")) < 17)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h16_datetime_idx ON trip_partition.h16 ("datetime");

CREATE TABLE trip_partition.h17(
    check((extract(hour from "datetime")) >= 17 AND (extract(hour from "datetime")) < 18)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h17_datetime_idx ON trip_partition.h17 ("datetime");

CREATE TABLE trip_partition.h18(
    check((extract(hour from "datetime")) >= 18 AND (extract(hour from "datetime")) < 19)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h18_datetime_idx ON trip_partition.h18 ("datetime");

CREATE TABLE trip_partition.h19(
    check((extract(hour from "datetime")) >= 19 AND (extract(hour from "datetime")) < 20)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h19_datetime_idx ON trip_partition.h19 ("datetime");

CREATE TABLE trip_partition.h20(
    check((extract(hour from "datetime")) >= 20 AND (extract(hour from "datetime")) < 21)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h20_datetime_idx ON trip_partition.h20 ("datetime");

CREATE TABLE trip_partition.h21(
    check((extract(hour from "datetime")) >= 21 AND (extract(hour from "datetime")) < 22)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h21_datetime_idx ON trip_partition.h21 ("datetime");

CREATE TABLE trip_partition.h22(
    check((extract(hour from "datetime")) >= 22 AND (extract(hour from "datetime")) < 23)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h22_datetime_idx ON trip_partition.h22 ("datetime");

CREATE TABLE trip_partition.h23(
    check((extract(hour from "datetime")) >= 23 AND (extract(hour from "datetime")) < 24)
) INHERITS (trips);
CREATE INDEX IF NOT EXISTS trips_h23_datetime_idx ON trip_partition.h23 ("datetime");

CREATE OR REPLACE FUNCTION trips_partition_trigger()
RETURNS trigger AS $$
DECLARE
    currentHour smallint;
begin
    CurrentHour := EXTRACT(HOUR FROM NEW.datetime);
    IF (CurrentHour = 0) THEN
        INSERT INTO trip_partition.h0 VALUES (NEW.*);
    ELSIF (CurrentHour = 1) THEN
        INSERT INTO trip_partition.h1 VALUES (NEW.*);
    ELSIF (CurrentHour = 2) THEN
        INSERT INTO trip_partition.h2 VALUES (NEW.*);
    ELSIF (CurrentHour = 3) THEN
        INSERT INTO trip_partition.h3 VALUES (NEW.*);
    ELSIF (CurrentHour = 4) THEN
        INSERT INTO trip_partition.h4 VALUES (NEW.*);
    ELSIF (CurrentHour = 5) THEN
        INSERT INTO trip_partition.h5 VALUES (NEW.*);
    ELSIF (CurrentHour = 6) THEN
        INSERT INTO trip_partition.h6 VALUES (NEW.*);
    ELSIF (CurrentHour = 7) THEN
        INSERT INTO trip_partition.h7 VALUES (NEW.*);
    ELSIF (CurrentHour = 8) THEN
        INSERT INTO trip_partition.h8 VALUES (NEW.*);
    ELSIF (CurrentHour = 9) THEN
        INSERT INTO trip_partition.h9 VALUES (NEW.*);
    ELSIF (CurrentHour = 10) THEN   
        INSERT INTO trip_partition.h10 VALUES (NEW.*);
    ELSIF (CurrentHour = 11) THEN
        INSERT INTO trip_partition.h11 VALUES (NEW.*);
    ELSIF (CurrentHour = 12) THEN
        INSERT INTO trip_partition.h12 VALUES (NEW.*);
    ELSIF (CurrentHour = 13) THEN
        INSERT INTO trip_partition.h13 VALUES (NEW.*);
    ELSIF (CurrentHour = 14) THEN
        INSERT INTO trip_partition.h14 VALUES (NEW.*);
    ELSIF (CurrentHour = 15) THEN
        INSERT INTO trip_partition.h15 VALUES (NEW.*);
    ELSIF (CurrentHour = 16) THEN
        INSERT INTO trip_partition.h16 VALUES (NEW.*);
    ELSIF (CurrentHour = 17) THEN  
        INSERT INTO trip_partition.h17 VALUES (NEW.*);
    ELSIF (CurrentHour = 18) THEN
        INSERT INTO trip_partition.h18 VALUES (NEW.*);
    ELSIF (CurrentHour = 19) THEN
        INSERT INTO trip_partition.h19 VALUES (NEW.*);
    ELSIF (CurrentHour = 20) THEN
        INSERT INTO trip_partition.h20 VALUES (NEW.*);
    ELSIF (CurrentHour = 21) THEN
        INSERT INTO trip_partition.h21 VALUES (NEW.*);
    ELSIF (CurrentHour = 22) THEN
        INSERT INTO trip_partition.h22 VALUES (NEW.*);
    ELSIF (CurrentHour = 23) THEN
        INSERT INTO trip_partition.h23 VALUES (NEW.*);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trips_partition_trigger
BEFORE INSERT ON trips FOR EACH ROW
EXECUTE PROCEDURE trips_partition_trigger();