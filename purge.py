#!/usr/bin/python3.6
import os
import logging
import time
import datetime
import mysql.connector

from mysql.connector import errorcode
from datetime import datetime, timedelta

logging.basicConfig(filename='purge.log', level=logging.DEBUG)

rows_completed = False
rows_affected = 0
rows_purged = 0

# Take the current date, take current time and subtract by arg
# convert result to UNIX timestamp and return
def get_timestamp(daysBack):
    date = datetime.today() - timedelta(days=daysBack)
    return date.timestamp()

logging.info('## PURGE START! ##')
# Put in table tables that we want to iterate through during the purge
logging.info('Loading table list...')
tables = ["co_block", "co_chat", "co_command", "co_container", "co_entity", "co_item", "co_session", "co_sign", "co_skull"]
logging.info('Tables loaded')
try:
    # Connect to the database and create a cursor object
    logging.info('Attempting to connect to database')
    con = mysql.connector.connect(user='admin_cp', password='', host='127.0.0.1', database='admin_cp')
    logging.info('Connection established.')
    cursor = con.cursor()
    # Iterate through each table and delete records 10,000 at a time
    for table in tables:
        rows_completed = False
        rows_purged = 0
        logging.info('Purging %s table...', table)
        sql = 'DELETE FROM %s WHERE time < %d LIMIT 10000' % (table, get_timestamp(60))
        while not(rows_completed):
            cursor.execute(sql)
            rows_affected = cursor.rowcount
            rows_purged += rows_affected
            logging.info('%s rows purged...', rows_purged)
            if(rows_affected == 0):
                rows_completed = True
                logging.info('## TABLE PURGED: %d rows purged from %s table ##', rows_purged, table)
            con.commit()
except mysql.connector.Error as err:
    # We got issues, figure out what
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.error('Check username and password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logging.error('Database does not exist')
    else:
        logging.error(err)
else:
    con.close()
con.close()
logging.info('## PURGE COMPLETE! ##')