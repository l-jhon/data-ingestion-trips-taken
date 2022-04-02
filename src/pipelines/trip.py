import logging as log

import pandas as pd
from io import StringIO
from utils import db_connect

log.basicConfig(level=log.INFO)

class TripPipeline():

    def __init__(self) -> None:
        self.db_connection = db_connect()
        
    def _read_csv(self, file_path: str) -> pd.DataFrame:
        """
        Read a csv file and return a pandas dataframe.
        """
        return pd.read_csv(file_path)

    def get_latitude_longitue(self, data: pd.DataFrame) -> None:
        """
        Get latitude and longitude from the dataframe.
        """
        data["origin_coord_lat"] = data["origin_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[1])
        data["origin_coord_lng"] = data["origin_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[2])
        data["destination_coord_lat"] = data["destination_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[1])
        data["destination_coord_lng"] = data["destination_coord"].str.replace("POINT|[()]", "", regex=True).str.split(" ").apply(lambda x: x[2])

        return data

    def copy_from_stringio(self, data: pd.DataFrame, conn: pg.Connection) -> None:
        """
        Insert data into the database.
        """
        buffer = StringIO()
        data.to_csv(buffer, sep=',', header=True)
        buffer.seek(0)

        cur = conn.cursor()

        try:
            cur.copy_from(buffer, 'trips', columns=data.columns, null="")
            conn.commit()
        except (Exception, pg.DatabaseError) as error:
            log.error(error)
            conn.rollback()
            cur.close()

        log.info("Data inserted into the database.")
        cur.close()