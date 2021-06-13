import click
from db_utils import JsonDB,sqlDB

@click.group()
def cli():
    """ A simple CLI tool"""

DB_Proxy = {
   'json':  JsonDB,
   'sqlite': sqlDB
}

@cli.command('get', short_help='return value for your key')
@click.argument('db_type')
@click.argument('key')
def get(db_type,key):
    with DB_Proxy[db_type]() as db:
        db.get(key)

@cli.command('set', short_help='create new key and value or change for old key is value')
@click.argument('db_type')
@click.argument('key')
@click.argument('value')
def set(db_type,key,value):
    with DB_Proxy[db_type]() as db:
        db.set(key,value)
   
@cli.command('delete', short_help='delete key')
@click.argument('db_type')
@click.argument('key')
def delete(db_type,key):
    with DB_Proxy[db_type]() as db:
        db.delete(key)

@cli.command('reset', short_help='outseted key')
@click.argument('db_type')
@click.argument('key')
def reset(db_type,key):
    with DB_Proxy[db_type]() as db:
        db.reset(key)
        print(key, 'is now outdated!')

if __name__ == '__main__':
   cli()