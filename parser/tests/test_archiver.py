from parser import archiver

from click.testing import CliRunner
from unittest.mock import patch, MagicMock, mock_open
import json
import os

VALID_KEYS = ['first_name', 'middle_name', 'last_name', 'zip_code']

def test_generate_filename():
    result = archiver._generate_filename('.test', '1234')
    print(f"generated filename: {result}")
    assert len(result) > 13  # Basic timestamp plus suffix
    assert isinstance(result, str)

def test_archive_str():
    m = mock_open()
    with patch ('parser.archiver.open', m):
        archiver.archive_raw('hello world', '1234', '.test')
        m.assert_called_once()

@patch('parser.archiver.FILE_MODE', 'S3')
@patch('boto3.client')
def test_archive_s3(put_object):
    with patch.dict('os.environ', {"AWS_REGION": "localtest"}, clear=True):
        archiver.archive_raw('boto3 test', '1234', '.test')
        put_object.assert_called_once()
