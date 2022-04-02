import logging as log

import pandas as pd
import psycopg2 as pg
from io import StringIO
from src.utils.db_connect import db_connect

log.basicConfig(level=log.INFO)

class SimilarTripPipeline():

    def __init__(self, file_path: str) -> None:
        self.conn = db_connect()
        self.file_path = file_path
        
    def read_table_from_db(self, table_name: str, conn) -> pd.DataFrame:
        """
        Read a csv file and return a pandas dataframe.
        """
        query = f"""
            SELECT * FROM {table_name}
        """

        return pd.read_sql_query(sql=query, con=conn)

    def get_latitude_longitue(self, data: pd.DataFrame) -> None:
        """
        Get latitude and longitude from the dataframe.
        """
        data["origin_coord_lat"] = data["origin_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[1])
        data["origin_coord_lng"] = data["origin_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[2])
        data["destination_coord_lat"] = data["destination_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[1])
        data["destination_coord_lng"] = data["destination_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[2])

        return data

    
    def create_table(self, conn) -> None:
        """
        Create a table in the database.
        """

        cur = conn.cursor()

        try:
            cur.execute("""
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
                );
            """)
            conn.commit()
            log.info("Table created.")
            cur.close()

        except (Exception, pg.DatabaseError) as error:
            log.error(error)
            conn.rollback()
            cur.close()


    def insert_data(self, data: pd.DataFrame, conn) -> None:
        """
        Insert data into the database.
        """
        buffer = StringIO()
        data.to_csv(buffer, sep=',', header=False)
        buffer.seek(0)

        cur = conn.cursor()

        try:
            cur.copy_from(buffer, 'similar_trips', sep=',')
            conn.commit()
            log.info("Data inserted into the database.")
            cur.close()

        except (Exception, pg.DatabaseError) as error:
            log.error(error)
            conn.rollback()
            cur.close()


    def run(self) -> None:
        """
        Run the pipeline.
        """
        data = self.read_table_from_db(self.file_path)
        self.create_table(self.conn)
        self.insert_data(data, self.conn)
        self.conn.close()