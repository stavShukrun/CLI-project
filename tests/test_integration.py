from db_utils import JsonDB,sqlDB
import pytest
import os

@pytest.fixture(scope="class")
def json_init():
    json_test_path = 'test.json'
    JsonDB(path=json_test_path)
    yield 
    os.remove(json_test_path)

@pytest.mark.usefixtures("json_init")
class TestJson():

    def test_get(self):
        self.db=JsonDB()
        key='key1'
        import pdb;pdb.set_trace()
        assert self.db.get(key)=="KeyError: 'The DB not contain val1'"


    def test_set(self):
        pass

    def test_reset(self):
        pass

    def test_delete(self):
        pass


class TestSql():
    def test_get():
        pass

    def test_set():
        pass

    def test_reset():
        pass

    def test_delete():
        pass