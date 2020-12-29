""" Pull out the following fields from anywhere in a JSON file:
first_name, middle_name, last_name, and zip_code
Note: properties are individually optional.  At least one makes a valid sample.
Note: Gracefully handle bad data.

Usage: python generate.py --help
"""

import datetime
import json
import os
import sys
import tempfile
import uuid

import click

search_keys = ['first_name', 'middle_name', 'last_name', 'zip_code']

def generate_filename(suffix):
    """ Generate a temporary filename
    For the moment, where is not important.
    Prefix with timestamp
    Suffix (str) as parameter
    """
    prefix = tempfile.gettempdir() + os.path.sep + datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    rvalue = prefix + '_' + str(uuid.uuid4()) + suffix

    print(f'Generated filename: {rvalue}')
    return rvalue

def _generate_magic_keys(my_dict):

    for my_key, my_value in my_dict.items():
        if my_key in search_keys and isinstance(my_value, str):
            yield {my_key: my_value}
        elif my_key in search_keys and not isinstance(my_value, str):
            print(f"""{my_key} was found, but value was {type(my_value)}"""
                    """(not str) - excluding without error""")
        elif isinstance(my_value, list):
            for listitem in my_value:
                for rvalue in _generate_magic_keys(listitem):
                    yield rvalue

def _process_values(my_dict):
    print("Processing values")
    print(my_dict)

def _archive_raw(raw_object, suffix):
    filename = generate_filename(suffix)
    with open(filename, 'w') as file:
        file.write(raw_object)

def lambda_handler(event, _context):
    """ Main handler for AWS Lambda
    Takes an input event as JSON
    Parses the JSON to search for the required fields (handling those separately)
    Archives the raw JSON
    """


    for record in event['Records']:
        # Leaving this commented for future reference if we use Kinesis:
        # Kinesis example
        # via https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-create-package.html
        # import base64
        # Kinesis data is base64 encoded so decode here
        # if 'kinesis' in record:
        #     my_json = base64.b64decode(record["kinesis"]["data"])
        #     print("Decoded payload: " + str(payload))
        # else:
        #     my_json = record
        my_json = record

        status_code = 200

        try:
            payload = list(_generate_magic_keys(json.loads(my_json)))
            print(f'payload: {payload}')
            _process_values(payload)
            _archive_raw(my_json, '.json')
        except Exception as error:  # pylint: disable=W0703
            print(f"JSON load failed with error: {str(error)}")
            try:
                _archive_raw(my_json, '.error')
            except Exception as archive_error:  # pylint: disable=W0703
                print(f"Failed to archive file: {str(archive_error)}")
            status_code = 500

        response = {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps(payload)
        }

        print(f"response: {response}")

        return response


@click.command()
@click.option('-f', '--filename', default=None,
              help='Filename (optional otherwise read from stdin)')
def parse(filename):
    """ Handles JSON input
    Archives raw JSON
    Processes parsed JSON to find and handle magic fields
    """

    if filename:
        with open(filename) as my_file:
            data = my_file.readlines()
    else:
        data = sys.stdin.readlines()

    event = {}  # Simulate AWS Lambda Payload
    event['Records'] = data

    lambda_handler(event, None)

    return 0


if __name__ == '__main__':
# pylint: disable=no-value-for-parameter
    parse()
# pylint: enable=no-value-for-parameter
