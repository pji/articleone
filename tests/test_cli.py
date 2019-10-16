"""
test_cli
~~~~~~~~

This module contains the tests for the articleone.cli module.
"""
from contextlib import contextmanager
from io import StringIO
import sys
import unittest
from unittest.mock import patch

from articleone import cli


# Utility functions.
@contextmanager
def capture():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


# Tests.
class StatusTestCase(unittest.TestCase):
    def test__init(self):
        """cli.Status: The cli.Status class should populate its 
        attributes when instantiated.
        """
        expected = [
            'Spam',
            '{:>7.2} ',
        ]
        
        status = cli.Status(*expected)
        actual = [
            status.title,
            status.prefix,
        ]
        
        self.assertEqual(expected, actual)
    
    def test__start(self):
        """cli.Status.start: The method should announce the 
        start of the activity.
        """
        expected = ('SPAM\n'
                    '----\n')
        expected_prefix = '{:>7.2} '
        
        status = cli.Status('spam', '{:>7.2} ')
        with capture() as (out, err):
            status.start()
        actual = out.getvalue()
        
        self.assertEqual(expected, actual)
    
    @patch('time.time')
    def test__end(self, mock__time):
        """cli.Status.end: The method should announce the end 
        of the activity.
        """
        expected = '\n{:7.2f} End\n----\n'.format(0.00)
        
        mock__time.return_value = 0.00
        status = cli.Status('spam', '{:>7.2f} ')
        with capture() as (out, err):
            status.end()
        actual = out.getvalue()
        
        self.assertEqual(expected, actual)
    
    @patch('time.time')
    def test__set(self, mock__time):
        """cli.Status.set: Given a message template and initial 
        values, the method should set the new message, and 
        print an initial update.
        """
        expected = '\n{:7.2f} Eggs 0'.format(0.00)
        
        mock__time.return_value = 0.00
        tmp = 'Eggs {}'
        status = cli.Status('spam', '{:>7.2f} ')
        with capture() as (out, err):
            status.set(tmp, 0)
        actual_out = out.getvalue()
        actual_msg = status.msg
        
        self.assertEqual(expected, actual_out)
        self.assertEqual(expected[1:], actual_msg)
    
    @patch('time.time')
    def test__update(self, mock__time):
        """cli.Status.update: Given an update to the status, 
        the method should remove the initial status and write 
        an updated status.
        """
        expected_msg = '{:7.2f} Eggs 2'.format(1.00)
        clear = '\x08' * len(expected_msg)
        expected_out = clear + expected_msg
        
        mock__time.return_value = 1.00
        status = cli.Status('spam', '{:>7.2f} ')
        status.tmp = '{:7.2f} Eggs {}'
        status.msg = '{:7.2f} Eggs 1'.format(1.00)
        mock__time.return_value = 2.00
        with capture() as (out, err):
            status.update(2)
        actual_out = out.getvalue()
        actual_msg = status.msg
        
        self.assertEqual(expected_out, actual_out)
        self.assertEqual(expected_msg, actual_msg)


@unittest.skip
class SenatorsTestCase(unittest.TestCase):
    def test_valid(self):
        """cli.senators: The function should output a list of 
        U.S. senators.
        """
        raise NotImplementedError