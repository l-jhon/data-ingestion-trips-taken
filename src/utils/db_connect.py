import psycopg2 as pg
import os
import sys
import logging as log

log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=log.INFO,
    stream=sys.stdout
)

HOST = os.environ.get('POSTGRES_HOST')
DATABASE = os.environ.get('POSTGRES_DB')
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')

def db_connect():
    """
    Connect to the PostgreSQL database.
    Returns a database connection.
    """
    try:
        log.info('Connecting to the PostgreSQL database...')
        conn = pg.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        log.info("Connection established.")
        return conn
    except (Exception, pg.DatabaseError) as error:
        log.error(error)