from abc import abstractclassmethod
import click
import json

class DB:
    @abstractclassmethod
    def get():
        raise NotImplementedError
    
    @abstractclassmethod
    def set():
        raise NotImplementedError

    @abstractclassmethod
    def delete():
        raise NotImplementedError

    @abstractclassmethod
    def reset():
        raise NotImplementedError


class JsonDB(DB):
    def __init__(self):
        with open('j.json') as f:
            self.data = json.load(f)
    
    def close(self, data):
        with open('j.json', 'w') as f:
            json.dump(data,f)

    def get(self,key):
        if key in self.data:
            click.echo(self.data[key]['value'])
        else: 
            print("This key is not exictit")
        
    def set(self,key,value):
        self.data[key] = {"value": value, "outdated": False}

        self.close(self.data)

    def delete(self,key):
        if key in self.data:
            del self.data[key]
        else:
            print("This is not a key!")

        self.close(self.data)

    def reset(self,key):
        if key not in self.data:
            print("This key is not exictit")
        
        self.data[key]['outdated'] = True
        print(key, 'is now outdated!')

        self.close(self.data)

@click.group()
def cli():
   pass

@cli.command()
@click.argument('key')
def get(key):
    db = JsonDB()
    db.get(key)

@cli.command()
@click.argument('key')
@click.argument('value')
def set(key,value):
    db = JsonDB()
    db.set(key,value)
   
@cli.command()
@click.argument('key')
def delete(key):
    db = JsonDB()
    db.delete(key)

@cli.command()
@click.argument('key')
def reset(key):
    db = JsonDB()
    db.reset(key)

if __name__ == '__main__':
   cli()