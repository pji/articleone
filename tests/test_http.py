"""
test_http
~~~~~~~~~

Tests for the articleone.http module.
"""
from threading import Thread
from time import sleep
import unittest

from requests import get, Session

from articleone import http
from tests import stub_http


# Tests.
class BuildSessionTestCase(unittest.TestCase):
    def test__valid(self):
        """http.build_session: The function should return an 
        http.Session object.
        """
        expected = Session
        actual = http.build_session()
        self.assertTrue(isinstance(actual, expected))


class GetTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Stand up the test server."""
        cls.fqdn = 'http://127.0.0.1'
        cls.port = 5001
        
        print('\nSTANDING UP STUB_HTTP')
        kwargs = {'port': cls.port,}
        T = Thread(target=stub_http.app.run, kwargs=kwargs)
        T.start()
        sleep(.01)             # Give server time to stand up.
    
    @classmethod
    def tearDownClass(cls):
        """Tear down the test server."""
        url = f'{cls.fqdn}:{cls.port}/shutdown'
        get(url)
        print('\nSHUT DOWN STUB_HTTP')
    
    def test_200(self):
        """http.get: The function should make an HTTP GET request 
        to the given URL, and return the text in the body of the 
        HTTP response.
        """
        expected = 'success'
        
        url = f'{self.fqdn}:{self.port}/get'
        actual = http.get(url)
        
        self.assertEqual(expected, actual)
    
    def test_401(self):
        """http_get: The function raises an http.AuthenticationError 
        exception if the status code from the server was 401.
        """
        expected = http.AuthenticationError
        url = f'{self.fqdn}:{self.port}/401'
        with self.assertRaises(expected):
            resp = http.get(url)
            
    def test_404(self):
        """http_get: The function raises an http.NotFoundError 
        exception if the status code from the server was 404.
        """
        expected = http.NotFoundError
        url = f'{self.fqdn}:{self.port}/404'
        with self.assertRaises(expected):
            resp = http.get(url)
            
    def test_500(self):
        """http.get: The function raises an http.ServerError 
        exception if the status code from the server was in the 
        5xx range.
        """
        expected = http.ServerError
        url = f'{self.fqdn}:{self.port}/500'
        with self.assertRaises(expected):
            resp = http.get(url)
    
    def test_session(self):
        """http.get: The function should accept a requests.Session 
        object used to manage the http session and use it when 
        sending requests.
        """
        expected = 'success'
        
        session = Session()
        url1 = f'{self.fqdn}:{self.port}/cookie_set'
        url2 = f'{self.fqdn}:{self.port}/cookie_check'
        _ = http.get(url1, session)
        actual = http.get(url2, session)
        
        self.assertEqual(expected, actual)