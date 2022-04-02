import pyscopg2 as pg
import os
import logging as log


log.basicConfig(level=log.INFO)

def db_connect():
    """
    Connect to the PostgreSQL database.
    Returns a database connection.
    """
    try:
        log.info('Connecting to the PostgreSQL database...')
        conn = pg.connect(host="localhost", database="postgres", user="postgres", password="postgres")
    except (Exception, pg.DatabaseError) as error:
        print(error)
    log.info("Connection established.")
    return conn