""" Pull out the following fields from anywhere in a JSON file:
first_name, middle_name, last_name, and zip_code
Note: properties are individually optional.  At least one makes a valid sample.
Note: Gracefully handle bad data.

Usage: python parser.py --help
"""

import json
import logging
import sys
import uuid

import click

# This import has to work in pytest, when using the cli, and in AWS
# if 'AWS_REGION' in os.environ:
try:
    from archiver import archive_raw  # pylint: disable=import-error
except Exception:  # pylint: disable=broad-except
    from .archiver import archive_raw


log = logging.getLogger('parser')
log.setLevel(logging.INFO)
search_keys = ['first_name', 'middle_name', 'last_name', 'zip_code']


def _generate_magic_keys(my_dict):

    print("generating from: %s: %s", type(my_dict), my_dict)

    if isinstance(my_dict, str):
        my_dict = json.loads(my_dict)
    if isinstance(my_dict, float):
        return

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

def _process_values(my_list, transaction_id):
    """Placeholder for doing things like writing to a database
    For now, just place parsed values in an s3 bucket
    """
    log.info("Processing values")

    my_dict = {}
    for item in my_list:
        my_dict.update(item)

    archive_raw(my_dict, transaction_id, '.json', 'parsed/')

def _aws_unpack(inthing):
    """ Since the API already encodes the payload, the JSON string is double escaped.
    Fix that weirdness and do any other AWS pre-processing here.
    If we wanted to make this cross platform, we could implement a google or azure version as well.
    """
    try:
        rvalue = json.loads(inthing)
    except Exception:  # pylint: disable=broad-except
        rvalue = inthing

    return rvalue


def lambda_handler(event, _context):
    """ Main handler for AWS Lambda
    Takes an input event as JSON
    Parses the JSON to search for the required fields (handling those separately)
    Processes whatever needs processing
    Archives the raw JSON
    """

    transaction_id = str(uuid.uuid4())

    if isinstance(event, dict):
        if 'body' in event:
            my_json = _aws_unpack(event['body'])
        else:
            my_json = event
    else:
        my_json = json.loads(event)

    log.info("processing: %s (of type: %s)", my_json, type(my_json))

    status_code = 200

    try:
        payload = list(_generate_magic_keys(my_json))
        _process_values(payload, transaction_id)
        archive_raw(my_json, transaction_id, '.json', 'raw/')
    except Exception as error:  # pylint: disable=broad-except
        log.error("JSON load failed with error: %s", str(error))
        try:
            archive_raw(my_json, transaction_id, '.error', 'error/')
        except Exception as archive_error:  # pylint: disable=broad-except
            log.error("Failed to archive file: %s", str(archive_error))
        status_code = 500

    body = json.dumps(payload) if isinstance(payload, dict) else payload
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(body)
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

    parse_result = lambda_handler(event, None)

    print(parse_result)

    return parse_result


if __name__ == '__main__':
# pylint: disable=no-value-for-parameter
    parse()
# pylint: enable=no-value-for-parameter
