""" Pull out the following fields from anywhere in a JSON file:
first_name, middle_name, last_name, and zip_code
Note: properties are individually optional.  At least one makes a valid sample.
Note: Gracefully handle bad data.

Usage: python generate.py --help
"""

import datetime
import json
import logging
import os
import sys
import tempfile
import uuid
import click

log = logging.getLogger('parser')
search_keys = ['first_name', 'middle_name', 'last_name', 'zip_code']

def generate_filename(suffix):
    """ Generate a temporary filename
    For the moment, where is not important.
    Prefix with timestamp
    Suffix (str) as parameter
    """
    prefix = tempfile.gettempdir() + os.path.sep + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    rvalue = prefix + '_' + str(uuid.uuid4()) + suffix

    log.info('Generated filename: %s', rvalue)
    return rvalue

def _generate_magic_keys(my_dict):

    log.info("generating from: %s: %s", type(my_dict), my_dict)

    for my_key, my_value in my_dict.items():
        if my_key in search_keys and isinstance(my_value, str):
            yield {my_key: my_value}
        elif my_key in search_keys and not isinstance(my_value, str):
            log.warning("""%s was found, but value was (%s)"""
                    """(not str) - excluding without error""", my_key, type(my_value))
        elif isinstance(my_value, list):
            for listitem in my_value:
                for rvalue in _generate_magic_keys(listitem):
                    yield rvalue

def _process_values(my_dict):
    """Placeholder for doing things like writing to a database
    """
    log.info("Processing values")
    log.info(my_dict)

def _archive_raw(raw_object, suffix):
    filename = generate_filename(suffix)
    with open(filename, 'w') as file:
        if isinstance(raw_object, dict):
            json.dump(raw_object, file)
        else:
            file.write(raw_object)

def _aws_unpack(inthing):
    """ AWS Does some weirdness like escaping quotes in the payload which confuses json.
    Make uniform all AWS specific pre-processing here.
    If we wanted to make this cross platform, we could implement a google or azure version as well.
    """
    return inthing


def lambda_handler(event, _context):
    """ Main handler for AWS Lambda
    Takes an input event as JSON
    Parses the JSON to search for the required fields (handling those separately)
    Processes whatever needs processing
    Archives the raw JSON
    """

    if isinstance(event, dict):
        if 'body' in event:
            my_json = _aws_unpack(event['body'])
        else:
            my_json = event
    else:
        my_json = json.loads(event)

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

    status_code = 200

    try:
        payload = list(_generate_magic_keys(my_json))
        _process_values(payload)
        _archive_raw(my_json, '.json')
    except Exception as error:  # pylint: disable=broad-except
        log.error("JSON load failed with error: %s", str(error))
        try:
            _archive_raw(my_json, '.error')
        except Exception as archive_error:  # pylint: disable=broad-except
            log.error("Failed to archive file: %s", str(archive_error))
        status_code = 500

    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(payload)
    }

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
            data = json.load(my_file)
    else:
        data = json.load(sys.stdin)

    event = {}  # Simulate AWS Lambda Payload
    event['body'] = data

    lambda_handler(event, None)

    return 0


if __name__ == '__main__':
# pylint: disable=no-value-for-parameter
    parse()
# pylint: enable=no-value-for-parameter
