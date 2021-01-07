""" Functions for archiving inbound data
"""

import datetime
import json
import logging
import os
import tempfile

import boto3

log = logging.getLogger('parser')

FILE_MODE = 'local'
if 'AWS_REGION' in os.environ:
    FILE_MODE = 'S3'

BUCKET_NAME = os.getenv('S3_BUCKET') or 'defaultbucket.json'

def _generate_filename(suffix, transaction_id, fullpath=True):
    """ Generate a temporary filename with no path
    Prefix with timestamp
    Suffix (str) as parameter
    """
    prefix = tempfile.gettempdir() + os.path.sep if fullpath else ''
    prefix = prefix + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    rvalue = prefix + '_' + transaction_id + suffix

    log.info('Generated filename: %s', rvalue)
    return rvalue


def _archive_s3(raw_object, transaction_id, suffix, prefix):
    """Archive a file to an s3 bucket
    """

    # Late import since this is only needed with AWS
    # import boto3  # pylint: disable=import-outside-toplevel

    body = json.dumps(raw_object)
    client = boto3.client('s3')
    filename = prefix + _generate_filename(suffix, transaction_id, False)
    client.put_object(Body=body, Bucket=BUCKET_NAME, Key=filename)


def _archive_local(raw_object, transaction_id, suffix):
    """Archive a file to the local filesystem
    """

    filename = _generate_filename(suffix, transaction_id)
    with open(filename, 'w') as file:
        if isinstance(raw_object, dict):
            json.dump(raw_object, file)
        else:
            file.write(raw_object)


def archive_raw(raw_object, transaction_id, suffix, prefix = ''):
    """ Archive raw_object input data to an archive file ending in suffix
    this is the public interface which chooses between filesystems
    """

    if FILE_MODE == 'S3':
        _archive_s3(raw_object, transaction_id, suffix, prefix)
    else:
        _archive_local(raw_object, transaction_id, suffix)
