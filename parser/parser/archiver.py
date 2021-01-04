""" Functions for archiving inbound data
"""
import datetime
import json
import logging
import os
import tempfile
import uuid

log = logging.getLogger('parser')

def _generate_filename(suffix):
    """ Generate a temporary filename
    For the moment, where is not important.
    Prefix with timestamp
    Suffix (str) as parameter
    """
    prefix = tempfile.gettempdir() + os.path.sep + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    rvalue = prefix + '_' + str(uuid.uuid4()) + suffix

    log.info('Generated filename: %s', rvalue)
    return rvalue

def archive_raw(raw_object, suffix):
    """ Archive raw_object input data to an archive file ending in suffix
    """
    filename = _generate_filename(suffix)
    with open(filename, 'w') as file:
        if isinstance(raw_object, dict):
            json.dump(raw_object, file)
        else:
            file.write(raw_object)
