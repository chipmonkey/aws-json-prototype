from parser import archiver

from click.testing import CliRunner
from unittest.mock import patch, MagicMock, mock_open
import json
import os

VALID_KEYS = ['first_name', 'middle_name', 'last_name', 'zip_code']

def test_generate_filename():
    result = archiver._generate_filename('.test')
    print(f"generated filename: {result}")
    assert len(result) > 13  # Basic timestamp plus suffix
    assert isinstance(result, str)

def test_archive_str():
    m = mock_open()
    with patch ('parser.archiver.open', m):
        archiver.archive_raw('hello world', '.test')
        m.assert_called_once()

