from abc import abstractclassmethod, abstractmethod
import click
import json

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
            print("This key is not exictit")
        
    def set(self,key,value):
        self.data[key] = {"value": value, "outdated": False}

    def delete(self,key):
        if key in self.data:
            del self.data[key]
        else:
            print("This is not a key!")

    def reset(self,key):
        if key not in self.data:
            print("This key is not exictit")
        
        self.data[key]['outdated'] = True
        print(key, 'is now outdated!')

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.close(self.data)
    
    def __enter__(self):
        return self

@click.group()
def cli():
   pass

@cli.command()
@click.argument('key')
def get(key):
    with JsonDB() as db:
        db.get(key)

@cli.command()
@click.argument('key')
@click.argument('value')
def set(key,value):
    with JsonDB() as db:
        db.set(key,value)
   
@cli.command()
@click.argument('key')
def delete(key):
    with JsonDB() as db:
        db.delete(key)

@cli.command()
@click.argument('key')
def reset(key):
    with JsonDB() as db:
        db.reset(key)

if __name__ == '__main__':
   cli()