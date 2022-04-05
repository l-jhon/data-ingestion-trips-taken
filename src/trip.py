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

class Trip(object):

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
            
            cur.execute("select exists(select * from information_schema.tables where table_name='trips')")

            if cur.fetchone()[0] == False:
                cur.execute(open("resources/ddl/create_table_trips.sql", "r").read())
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

    def get_average_trips_per_week(self) -> None:
        """
        Get average number of trips per week.
        """
        
        cur = self.postgresql_conn.cursor()
        cur.execute(open("resources/sql/weekly_average_trips.sql", "r").read())
        data = cur.fetchall()

        print("\nAverage number of trips per week for each region:\n")
        
        for row in data:
            print("Region:", row[0])
            print("Average:", float(row[1]))
            print("\n")

        cur.close()


    def get_latest_datasource(self) -> None:
        """
        Get the latest datasource of two commonly region.
        """

        cur = self.postgresql_conn.cursor()
        cur.execute(open("resources/sql/latest_datasource_commonly_region.sql", "r").read())
        data = cur.fetchall()

        print("\nThe latest datasource of two commonly region:\n")
        
        for row in data:
            print("Region:", row[0])
            print("Datasource:", row[1])
            print("\n")

        cur.close()


    def get_number_of_appearance(self) -> None:
        """
        Get the number of appearance for data source "cheap_mobile" in each region.
        """

        cur = self.postgresql_conn.cursor()
        cur.execute(open("resources/sql/number_of_appearances.sql", "r").read())
        data = cur.fetchall()

        print("\nNumber of appearance of each region:\n")
        
        for row in data:
            print("Region:", row[0])
            print("Data source:", row[1])
            print("Number of appearance:", row[2])
            print("\n")

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