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


def _generate_valid_json():
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
        # Incomplete coverage; generates false zips
        zip_code = random.randint(10000, 99999)
        rdict['zip_code'] = zip_code

    return rdict


def _generate_invalid_json():
    return {'nonsense': True}  # This suffices, but we can do better someday


@click.command()
@click.option('-c', '--count', default=10,
              help='Number of records to generate')
@click.option('-p', '--pinvalid', default=0.1, required=False, type=float,
              help='Percent of BAD records to target')
def generate(count, pinvalid):
    """ Generates {count} JSON results with {pinvalid} percent invalid fields
    """

    valid_count = int((1.0 - pinvalid) * count)
    invalid_count = count - valid_count

    result = [_generate_valid_json() for i in range(valid_count)]
    invalid = [_generate_invalid_json() for i in range(invalid_count)]

    if result and invalid:
        result.extend(invalid)
    elif invalid:
        # result = json.dumps(invalid)
        result = invalid

    rvalue = json.dumps(result)
    print(rvalue)
    return rvalue


if __name__ == '__main__':
# pylint: disable=no-value-for-parameter
    generate()
# pylint: enable=no-value-for-parameter
