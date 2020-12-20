""" Generate random JSON data with the following properties:
first_name, middle_name, last_name, and zip_code
Note: properties are individually optional.  At least one makes a valid sample.
Note: This generator can optionally generate bad data (without one of the required fields)

Usage: python generate.py --help
"""

import json
import random

import click
import names


def _generateValidJSON():
    fieldmask = 0
    while fieldmask == 0:
        fieldmask = random.getrandbits(4)

    rdict = {}

    if fieldmask & 1:
        first_name = names.get_first_name()
        rdict['first_name'] = first_name
    if fieldmask & 2:
        middle_name = names.get_first_name()  # No middle name specific generator
        rdict['middle_name'] = middle_name
    if fieldmask & 4:
        last_name = names.get_last_name()
        rdict['last_name'] = last_name
    if fieldmask & 8:
        zip_code = random.randint(10000, 99999)  # Incomplete coverage; generates false zips
        rdict['zip_code'] = zip_code

    print(rdict)
    
    return rdict


def _generateInvalidJSON():
    return {}  # This suffices, but we can do better someday

@click.command()
@click.option('--count', default=1, help='Number of records to generate')
@click.option('--pinvalid', default=0, required=False, type=float,
              help='Percent of BAD records to target')
def generate(count, pinvalid):
    """ Generates {count} JSON results with {pinvalid} percent invalid fields
    """

    validCount = int((1.0-pinvalid) * count)
    invalidCount = count - validCount

    valid = [_generateValidJSON() for i in range(validCount)]
    invalid = [_generateInvalidJSON() for i in range(invalidCount)]

    valid.extend(invalid)

    return json.dumps(valid.extend(invalid))
    

if __name__ == '__main__':
    result = generate()
    print(result)
