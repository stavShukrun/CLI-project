from abc import abstractmethod,ABC
from os import PathLike, path
import json
import sqlite3
import click


class DB(ABC):
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
    def __exit__ (self,exc_type, exc_value, exc_traceback):
        pass

    @abstractmethod
    def __enter__(self):
        pass

class JsonDB(DB):
    def __init__(self,path='db_Json.json'):
        self.path = path
        try:
            with open(self.path,'r+') as f:
                self.data = json.load(f)
        except FileNotFoundError as e:
                print('file is empty',e)
                self.data={}
    
    def close(self, data):
        with open(self.path,'w') as f:
            json.dump(self.data,f)

    def get(self,key):
        if key in self.data:
            click.echo(self.data[key]['value'])
        else: 
            raise KeyError(f'The DB not contain {key}')
        
    def set(self,key,value):
        self.data[key] = {"value": value, "outdated": False}

    def delete(self,key):
        if key in self.data:
            del self.data[key]
        else:
            raise KeyError(f'The DB not contain {key}')

    def reset(self,key):
        if key not in self.data:
            raise KeyError(f'The DB not contain {key}')
        
        self.data[key]['outdated'] = True

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.close(self.data)
    
    def __enter__(self):
        return self

class sqlDB(DB):

    def __init__(self,path='sqlite_db.sqlite'):
            self.conn = sqlite3.connect(path)
            self.cur=self.conn.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS hash (key TEXT PRIMARY KEY, value TEXT, outdated INTEGER );")

    def get(self,key):
        item = self.cur.execute(f'SELECT value FROM hash WHERE key = "{key}";').fetchall()
        if not item:
            raise KeyError(f'The DB not contain {key}')
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
            raise KeyError(f'The DB not contain {key}')

    def reset(self, key):
        keys = self.cur.execute(f"SELECT key FROM hash WHERE key='{key}'").fetchall()
        if keys:
            self.cur.execute(f'UPDATE hash SET outdated = 1 WHERE key="{key}";')

    def __enter__(self):
         return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.conn.close()