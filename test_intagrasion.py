from db_utils import JsonDB,sqlDB
import pytest

class test_json():

    @pytest.fixture
    def data():
        db=JsonDB()
        db.set(key,)
        yield db

    def test_get(data,key):
        data.get(key)

    def test_set():
        pass

    def test_reset():
        pass

    def test_delete():
        pass


class test_sql():
    def test_get():
        pass

    def test_set():
        pass

    def test_reset():
        pass

    def test_delete():
        pass