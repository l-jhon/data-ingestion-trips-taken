import logging as log
import json
import sys

import pandas as pd
import psycopg2 as pg
from io import StringIO
from src.utils.db_connect import db_connect
from src.utils.redis_connect import redis_connect

log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=log.INFO,
    stream=sys.stdout
)

class TripPipeline():

    def __init__(self, data: str) -> None:
        self.postgresql_conn = db_connect()
        self.redis_conn = redis_connect()
        self.data = data
    
    def put_redis(self) -> None:
        """
        Put data into redis.
        """
        try:
            self.redis_conn.rpush("trip_data", self.data)
            log.info("Data inserted into redis.")
        except Exception as error:
            log.error(error)


    def get_redis(self) -> dict:
        """
        Read a csv file and return a pandas dataframe.
        """
        data = self.redis_conn.lpop("trip_data")
        data = dict(json.loads(data))

        return data


    def create_table(self) -> None:
        """
        Create a table in the database.
        """

        cur = self.postgresql_conn.cursor()

        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trips(
                    id SERIAL PRIMARY KEY,
                    region varchar(200),
                    origin_coord text,
                    destination_coord text,
                    datetime timestamp,
                    datasource varchar(200)
                );
            """)
            self.postgresql_conn.commit()
            log.info("Table created.")
            cur.close()

        except (Exception, pg.DatabaseError) as error:
            log.error(error)
            self.postgresql_conn.rollback()
            cur.close()


    def insert_data(self) -> None:
        """
        Insert data into the database.
        """

        data = self.get_redis()

        cur = self.postgresql_conn.cursor()

        try:
            values = ",".join(["%({})s".format(keys) for keys in data.keys()])

            sql_insert = f"""
                INSERT INTO trips
                (region, origin_coord, destination_coord, datetime, datasource)
                VALUES ({values});
            """

            cur.execute(sql_insert, data)
            self.postgresql_conn.commit()
            log.info("Data inserted into the database.")
            cur.close()

        except (Exception, pg.DatabaseError) as error:
            log.error(error)
            self.postgresql_conn.rollback()
            cur.close()

    def run(self) -> None:
        """
        Run the pipeline.
        """
        self.put_redis()
        self.create_table()
        self.insert_data()
        self.postgresql_conn.close()
        self.redis_conn.close()
        
        log.info("PostgreSQL Connection closed.")
        log.info("Redis Connection closed.")