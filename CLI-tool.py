from abc import abstractmethod
import click
import json
import sqlite3

class DB:
    @abstractmethod
    def get(self,key):
        pass
    
    @abstractmethod
    def set(self,key,value):
        pass

    @abstractmethod
    def delete(self,key):
        pass

    @abstractmethod
    def reset(self,key):
        pass
    
    @abstractmethod
    def close(self, data):
        pass
    
    @abstractmethod
    def __exit__ (self,exc_type, exc_value, exc_traceback):
        pass

    @abstractmethod
    def __enter__(self):
        pass

class JsonDB(DB):
    def __init__(self):
        with open('db.json','r+') as f:
            try:
                self.data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print('file is empty',e)
                self.data = {}
    
    def close(self, data):
        with open('db.json', 'w') as f:
            json.dump(data,f)

    def get(self,key):
        if key in self.data:
            click.echo(self.data[key]['value'])
        else: 
            raise KeyError(key)
        
    def set(self,key,value):
        self.data[key] = {"value": value, "outdated": False}

    def delete(self,key):
        if key in self.data:
            del self.data[key]
        else:
            raise KeyError(key)

    def reset(self,key):
        if key not in self.data:
            raise KeyError(key)
        
        self.data[key]['outdated'] = True
        print(key, 'is now outdated!')

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.close(self.data)
    
    def __enter__(self):
        return self

class sqlDB(DB):

    def __init__(self):
            self.conn = sqlite3.connect('sqlite_db.sqlite')
            self.cur=self.conn.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS hash (key TEXT PRIMARY KEY, value TEXT, outdated INTEGER );")

    def get(self,key):
        item = self.cur.execute(f'SELECT value FROM hash WHERE key = "{key}";').fetchall()
        if not item:
            raise KeyError(key)
        return print(item)

    def set(self,key,value):
        keys = self.cur.execute(f"SELECT key FROM hash WHERE key='{key}'").fetchall()
        if keys:
            self.cur.execute(f'UPDATE hash SET value = "{value}", outdated = 0  WHERE key="{key}";')
        else:
            self.cur.execute(f'INSERT INTO hash (key, value, outdated) VALUES ("{key}", "{value}", 0);')

    def delete(self, key):
        keys = self.cur.execute(f"SELECT key FROM hash WHERE key='{key}'").fetchall()
        if keys:
            self.cur.execute(f"DELETE FROM hash WHERE key = '{key}';")
        else:
            raise KeyError(key)

    def reset(self, key):
        keys = self.cur.execute(f"SELECT key FROM hash WHERE key='{key}'").fetchall()
        if keys:
            self.cur.execute(f'UPDATE hash SET outdated = 1 WHERE key="{key}";')
            print(key, 'is now outdated!')

    def __enter__(self):
         return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.conn.close()

@click.group()
def cli():
   pass

@cli.command()
@click.argument('key')
def get(key):
    with sqlDB() as db:
    # with JsonDB() as db:
        db.get(key)

@cli.command()
@click.argument('key')
@click.argument('value')
def set(key,value):
    with sqlDB() as db:
    # with JsonDB() as db:
        db.set(key,value)
   
@cli.command()
@click.argument('key')
def delete(key):
    with sqlDB() as db:
    # with JsonDB() as db:
        db.delete(key)

@cli.command()
@click.argument('key')
def reset(key):
    with sqlDB() as db:
    # with JsonDB() as db:
        db.reset(key)

if __name__ == '__main__':
   cli()