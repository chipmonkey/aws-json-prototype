from generate import generate

from click.testing import CliRunner
import json

VALID_KEYS = ['first_name', 'middle_name', 'last_name', 'zip_code']

def test_generate_valid_json():
    result = generate._generate_valid_json()
    isValid = any(x in VALID_KEYS for x in result.keys())
    assert(isValid)

def test_generate_invalid_json():
    result = generate._generate_invalid_json()
    isValid = any(x in VALID_KEYS for x in result.keys())
    assert(not isValid)

def test_generate():
    runner = CliRunner()
    result = runner.invoke(generate.generate, ['--count', 10, '-p', '0.5'])
    assert result.exit_code == 0
    assert json.loads(result.output)

def test_cli_invalid_only():
    runner = CliRunner()
    result = runner.invoke(generate.generate, ['--count', 10, '-p', '1'])
    assert result.exit_code == 0
    assert json.loads(result.output)

def test_main():
    """Not testing __main__ for cli
    the proper way is to mock generate() and assert it was called
    """
    assert(True)
