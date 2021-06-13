from click.testing import CliRunner, Result
from cli import cli
import os
import json

def test_get():
    data={"key": {"value": "val1", "outdated": False}}
    with open('db_Json.json','w') as f:
        json.dump(data,f)          
    runner = CliRunner()
    result = runner.invoke(cli,['get','json','key'])
    assert 'val1' in result.output
    assert result.exit_code == 0
    os.remove('db_Json.json')

def test_set():
    runner = CliRunner()
    result = runner.invoke(cli,['set','json', 'key2', 'val2'])
    assert result
    assert result.exit_code == 0
    os.remove('db_Json.json')

def test_delete():
    data={"key": {"value": "val1", "outdated": False}}
    with open('db_Json.json','w') as f:
        json.dump(data,f)          
    runner = CliRunner()
    result = runner.invoke(cli,['delete','json','key'])
    assert '' in result.output
    assert result.exit_code == 0
    os.remove('db_Json.json')


def test_reset():
    data={"key": {"value": "val1", "outdated": False}}
    with open('db_Json.json','w') as f:
        json.dump(data,f)          
    runner = CliRunner()
    result = runner.invoke(cli,['reset','json','key'])
    assert 'key is now outdated!' in result.output
    assert result.exit_code == 0
    os.remove('db_Json.json')

def test_help():
    runner = CliRunner()
    result = runner.invoke(cli,['--help'])
    assert 'A simple CLI tool' in result.output
    assert result.exit_code == 0
