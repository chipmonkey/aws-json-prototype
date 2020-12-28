""" Pull out the following fields from anywhere in a JSON file:
first_name, middle_name, last_name, and zip_code
Note: properties are individually optional.  At least one makes a valid sample.
Note: Gracefully handle bad data.

Usage: python generate.py --help
"""

import datetime
import tempfile
import json
import sys

import click

search_keys = ['first_name', 'middle_name', 'last_name', 'zip_code']

def generate_filename(suffix):
    """ Generate a temporary filename
    For the moment, where is not important.
    Prefix with timestamp
    Suffix (str) as parameter
    """
    prefix = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    tfile = tempfile.NamedTemporaryFile(prefix=prefix)

    rvalue = tfile.name + suffix
    print(f'Generated filename: {rvalue}')
    return rvalue


def lambda_handler(event, _context):
    """ Main handler for AWS Lambda
    Takes an input event as JSON
    Parses the JSON to search for the required fields (handling those separately)
    Archives the raw JSON
    """

    def _get_magic_key(my_dict):
        # Thanks https://stackoverflow.com/a/14059645/1786204
        results = {}
        for my_key in search_keys:
            if my_key in my_dict:
                results[my_key] = my_dict[my_key]

        return results

    def _process_values(my_dict):
        print("Processing values")
        print(my_dict)

    def _archive_raw(raw_object, suffix):
        filename = generate_filename(suffix)
        with open(filename, 'w') as file:
            file.write(raw_object)


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

        try:
            payload = json.loads(my_json, object_hook=_get_magic_key)
            _process_values(payload)
            _archive_raw(my_json, '.json')
        except Exception as error:  # pylint: disable=W0703
            print(f"JSON load failed with error: {str(error)}")
            _archive_raw(my_json, '.error')



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
