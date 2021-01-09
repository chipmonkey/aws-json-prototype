from parser import parser

from click.testing import CliRunner
from unittest.mock import patch, Mock
import json
import os

VALID_KEYS = ['first_name', 'middle_name', 'last_name', 'zip_code']

def test_handler_direct_str():
    result = parser.lambda_handler('{"first_name": "chip"}', None)
    assert isinstance(result, dict)

def test_handler_direct_nobody():
    result = parser.lambda_handler({"first_name": "chip"}, None)
    assert isinstance(result, dict)

def test_generate_magic_keys_str():
    result = list(parser._generate_magic_keys(str('{"first_name": "chip"}')))
    assert result == [{'first_name': 'chip'}]

def test_aws_unpack_good():
    result = parser._aws_unpack('{"first_name": "chip"}')
    assert result == {'first_name': 'chip'}

def test_aws_unpack_bad():
    result = parser._aws_unpack('babbadook')
    assert result == 'babbadook'

@patch('parser.parser.archive_raw')
def test_process_values(mock_archive):
    parser._process_values([{"first_name": "chip"}], '1234')
    print("huh: ", mock_archive.call_args)
    mock_archive.assert_called_once_with({'first_name': 'chip'}, '1234', '.json', 'parsed/')

def test_cli_parse_success():
    runner = CliRunner()
    test_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = test_folder + '/good_sample.json'
    print(f"testing with test file: {test_file}")
    result = runner.invoke(parser.parse, ['-f', test_file])
    assert result.exit_code == 0

def test_cli_parse_success_complex():
    runner = CliRunner()
    test_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = test_folder + '/complex_sample.json'
    print(f"testing with test file: {test_file}")
    result = runner.invoke(parser.parse, ['-f', test_file])
    assert result.exit_code == 0

def test_cli_parse_failure():
    runner = CliRunner()
    test_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = test_folder + '/fail_sample.json'
    print(f"testing with test file: {test_file}")
    result = runner.invoke(parser.parse, ['-f', test_file])
    assert result.exit_code != 0

def test_cli_parse_warn_weird():
    runner = CliRunner()
    test_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = test_folder + '/weird_sample.json'
    print(f"testing with test file: {test_file}")
    result = runner.invoke(parser.parse, ['-f', test_file])
    assert result.exit_code == 0

def test_cli_parse_aws_format():
    runner = CliRunner()
    test_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = test_folder + '/aws_payload_sample.json'
    print(f"testing with test file: {test_file}")
    result = runner.invoke(parser.parse, ['-f', test_file])
    assert result.exit_code == 0

def test_cli_parse_float_field():
    runner = CliRunner()
    test_folder = os.path.dirname(os.path.abspath(__file__))
    test_file = test_folder + '/float_sample.json'
    print(f"testing with test file: {test_file}")
    result = runner.invoke(parser.parse, ['-f', test_file])
    assert result.exit_code == 0

def test_cli_parse_stdin():
    runner = CliRunner()
    result = runner.invoke(parser.parse, input='{"middle_name": "happy"}')
    assert result.exit_code == 0

@patch('parser.parser._process_values', side_effect=Exception('fake parser error'))
@patch('parser.parser.archive_raw', side_effect=Exception('fake archive error'))
def test_json_archive_failures(mockprocess, mockarchive):
    runner = CliRunner()
    result = runner.invoke(parser.parse, input='{"middle_name": "happy"}')
    mockprocess.assert_called_once()
    mockarchive.assert_called_once()
    assert result.exit_code == 0


def test_main():
    """Not testing __main__ for cli
    the proper way is to mock generate() and assert it was called
    """
    assert(True)
