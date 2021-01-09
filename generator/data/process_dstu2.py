""" Manual file to combine original JSON files
    with downloaded OSM data to create files ready
    to upload to AWS Lambda API for analysis
"""
import json
import os

import sqlite3
from sqlite3 import Error


def enhance_json(directory, filename, osm_data):
    """ Function which actually combines the data and writes output file
    """
    with open(directory + filename) as json_file:
        data = json.load(json_file)

    entry = data['entry']
    # resources = [x['resource'] for x in entry]
    patient = [x['resource']
               for x in entry if x['resource']['resourceType'] == 'Patient'][0]

    # Get name
    official_name = [x for x in patient['name'] if x['use'] == 'official'][0]
    first_name = official_name['given'][0]
    last_name = official_name['family'][0]
    # print(f'first_name: {first_name}, last_name: {last_name}')

    # Parse Address
    address = patient['address'][0]
    latitude = [x['valueDecimal'] for x in address['extension'][0]['extension'] if x['url'] == 'latitude'][0]
    longitude = [x['valueDecimal'] for x in address['extension'][0]['extension'] if x['url'] == 'longitude'][0]

    print(f"osm_data: {osm_data}")
    location = osm_data[0][2]  # location
    if location is not None:
        print(f"location: {location}")

    result = data
    result['first_name'] = first_name
    result['last_name'] = last_name
    result['latitude'] = latitude
    result['longitude'] = longitude

    out_dir = './processed/'
    with open(out_dir + 'api_' + filename, 'w') as out_file:
        json.dump(result, out_file)

    return result


def get_fhir_dtsu2(my_conn):
    """ Call Nominatim API
    :param conn:  SQLite DB with table dstu2 for cache/memoization
    """

    cur = my_conn.cursor()

    select_sql = """SELECT full_addr, filename, location from dstu2
                    WHERE filename = ?"""

    directory = './fhir_dstu2/'
    for filename in os.listdir(directory):
        print(f"Searching cache for {filename}")
        cur.execute(select_sql, (filename,))
        rows = cur.fetchall()
        if rows:
            print(f"row found for filename: {filename}")
            processed = enhance_json(directory, filename, rows)
            if not processed:
                print("not processed")


def create_connection(db_file):
    """ create a datakbase connection to a SQLite database
    thanks: https://www.sqlitetutorial.net/sqlite-python/creating-database/
    """
    new_conn = None
    try:
        new_conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as sqlite_error:
        print(sqlite_error)

    return new_conn


if __name__ == '__main__':
    conn = create_connection(r"./dstu2_cache.db")
    get_fhir_dtsu2(conn)
