# coding: utf-8
# Your code here!
import unittest
from unittest import mock
from unittest.mock import MagicMock,Mock

# This is a test for @mock.patch()
# Summary:
# In order to reflect the mock configuration to the instances of the patch target class,
# We have to use (1) spec arg, and (2) pass parameters to kwargs on @mock.patch() decorator.

class App:
    def run(self):
        db = DB()
        ret = DB.query("select * from TESTTABLE")
        print("QUERY RESULT=",ret)
        
class DB:
    def __init__(self):
        self.conn = "mydbserver"
        
    def query(sql):
        return 123456789
    
class MockDB:
    def __init__(self):
        self.conn = "mydbserver"
        
    def query(sql):
        return 1000
            

class TestMockPach(unittest.TestCase):

    # OK works fine. query() in all the instances of DB class return 1000
    @mock.patch("__main__.DB",spec=DB,**{"query.return_value":1000})
    def test1(self,mock):        
        app = App()
        ret = app.run()

    # NG: this patch only DB class object, but the instances. This test print out MagicMock.
    @mock.patch("__main__.DB",**{"query.return_value":1000})
    def test2(self,mock):        
        app = App()
        ret = app.run()
        
    # NG: this patch only the instances of DB class that passed in the 2nd argument of test3(). This test prints out MagicMock.
    @mock.patch("__main__.DB")
    def test3(self,mock):        
        att = {"query.return_value": 1000}
        mock.configure_mock(**att)
        app = App()
        ret = app.run()

    # NG: this will raise error to fail. 
    @mock.patch("__main__.DB",new=AnotherMockDB,**{"query.return_value":1000})
    def test4(self,mock):
        app = App()
        ret = app.run()

    # OK: this is another way to implement query() method. But it takes time to write MockDB if DB class is complicated. 
    @mock.patch("__main__.DB",new=MockDB)
    def test5(self):
        app = App()
        ret = app.run()


unittest.main()
