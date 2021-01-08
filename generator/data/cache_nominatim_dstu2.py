import json
import os
import time

from geopy.geocoders import Nominatim

import sqlite3
from sqlite3 import Error



def enhance_fhir_dtsu2(conn):
    """ Call Nominatim API
    :param conn:  SQLite DB with table dstu2 for cache/memoization
    """

    cur = conn.cursor()

    insert_sql = """INSERT INTO dstu2(full_addr, filename, location)
                    VALUES (?, ?, ?)"""

    select_sql = """SELECT full_addr, filename, location from dstu2
                    WHERE filename = ?"""

    geolocator = Nominatim(user_agent="Python3.8 GeoPy aws_json_prototype; email=chip@chiplynch.com")
    # location = geolocator.geocode("175 5th Avenue NYC")
    
    patients = []
    
    directory = './fhir_dstu2/'
    for filename in os.listdir(directory):
        cur.execute(select_sql, (filename,))
        rows = cur.fetchall()
        if rows:
            print(f"row found for filename: {filename}")
            continue
        elif filename.endswith('.json'):
            time.sleep(3)  # Nominatim has a 1 query per second limit, so.  This.
            print(f"opening: {filename}")
            with open(directory + filename) as json_file:
                data=json.load(json_file)
                entry = data['entry']
                resources = [ x['resource'] for x in entry ]
                patient = [ x['resource'] for x in entry if x['resource']['resourceType'] == 'Patient' ][0]
    
                # Get name
                official_name = [ x for x in patient['name'] if x['use'] == 'official' ][0]
                first_name = official_name['given']
                last_name = official_name['family']
                print(f'first_name: {first_name}, last_name: {last_name}')
    
                # Geocode to get zip
                address = patient['address'][0]
                line = ' '.join(address['line'])
                full_addr = ', '.join([line, address['city'], address['state'], address['country']])
                print(f'geocoding: {full_addr}')
                location = geolocator.geocode(line)
                print(f'location {type(location)}: {location}')
    
                patients.append(patient)
                print(f"Writing to the lovely database")
                if location:
                    cur.execute(insert_sql, (full_addr, filename, json.dumps(location.raw)))
                else:
                    cur.execute(insert_sql, (full_addr, filename, str(location)))
                conn.commit()


def create_connection(db_file):
    """ create a datakbase connection to a SQLite database
    thanks: https://www.sqlitetutorial.net/sqlite-python/creating-database/
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_cache_tables(conn):
    """ create a cache / memoization table for openstreetmap results
    """
    try:
        c = conn.cursor()
        create_table_sql = """CREATE TABLE IF NOT EXISTS dstu2 (
                                  full_addr TEXT PRIMARY KEY,
                                  filename TEXT NOT NULL,
                                  location TEXT
                              );
                           """

        c.execute(create_table_sql)
    except Error as e:
        print(e)


if __name__ == '__main__':
    conn = create_connection(r"./dstu2_cache.db")
    create_cache_tables(conn)
    enhance_fhir_dtsu2(conn)

