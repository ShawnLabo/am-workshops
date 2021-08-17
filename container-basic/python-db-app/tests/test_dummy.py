class Test_MyDB:
    import pytest

    def test_methods(self):
        import mydb
        obj = mydb.DB("dummy")
        assert hasattr(obj, 'get')
        assert hasattr(obj, 'put')
    
    