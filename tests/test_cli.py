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
from articleone import common
from articleone import unitedstates as us
from tests import test_unitedstates as t_us


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


class WriteTermTestCase(unittest.TestCase):
    def test_valid(self):
        """cli.write_term: Given a title, string formating template, 
        and a report matrix, the function will write the report to 
        the terminal.
        """
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        tmp = '{} {} {}\n'
        lines = ['\n',]
        lines.append('TITLE\n')
        lines.append('-----\n')
        for line in [tmp.format(*args) for args in matrix]:
            lines.append(line)
        lines.append('-----\n')
        lines.append('\n')
        expected = ''.join(lines)
        
        title = 'Title'
        with capture() as (out, err):
            cli.write_term(title, tmp[:-1], matrix)
        actual = out.getvalue()
        
        self.assertEqual(expected, actual)


# @unittest.skip
class MembersTestCase(unittest.TestCase):
    @patch('articleone.common.build_member_matrix')
    @patch('articleone.unitedstates.members')
    def test_valid(self, mock__members, mock__build_matrix):
        """cli.members: The function should output a list of 
        the members of the U.S. Congress.
        """
        matrix = [
            [
                'Last Name',            # Member.last_name
                'First Name',           # Member.first_name
                'Party',                # Member.party
            ],
            ['Durbin', 'Dick', 'Democrat',],
            ['Duckworth', 'Tammy', 'Democrat',],
            ['Sanders', 'Benard', 'Independent',],
        ]
        tmp = '{:<20} {:<20} {}\n'
        lines = ['\n',]
        lines.append('LIST OF MEMBERS\n')
        lines.append('---------------\n')
        for line in [tmp.format(*args) for args in matrix]:
            lines.append(line)
        lines.append('---------------\n')
        lines.append('\n')
        expected = ''.join(lines)
        
        mock__members.return_value = [common.Member(*args) 
                                      for args in matrix[1:]]
        mock__build_matrix.return_value = matrix
        with capture() as (out, err):
            cli.members()
        actual = out.getvalue()
        
        self.assertEqual(expected, actual)


class RepresentativeTestCase(unittest.TestCase):
    @patch('articleone.common.build_member_matrix')
    @patch('articleone.unitedstates.representatives')
    def test_valid(self, mock__representatives, mock__build_matrix):
        """cli.senators: The function should output a list of 
        the members of the U.S. Senate.
        """
        matrix = [
            [
                'Last Name',            # Member.last_name
                'First Name',           # Member.first_name
                'Party',                # Member.party
            ],
            ['Durbin', 'Dick', 'Democrat',],
            ['Duckworth', 'Tammy', 'Democrat',],
            ['Sanders', 'Benard', 'Independent',],
        ]
        tmp = '{:<20} {:<20} {}\n'
        lines = ['\n',]
        lines.append('LIST OF REPRESENTATIVES\n')
        lines.append('-----------------------\n')
        for line in [tmp.format(*args) for args in matrix]:
            lines.append(line)
        lines.append('-----------------------\n')
        lines.append('\n')
        expected = ''.join(lines)
        
        args_list = []
        for args in matrix[1:]:
            args.append('House')
            args_list.append(args)
        mock__representatives.return_value = [common.Member(*args) 
                                              for args in args_list[1:]]
        mock__build_matrix.return_value = matrix
        with capture() as (out, err):
            cli.representatives()
        actual = out.getvalue()
        
        self.assertEqual(expected, actual)


class SenatorsTestCase(unittest.TestCase):
    @patch('articleone.common.build_member_matrix')
    @patch('articleone.unitedstates.senators')
    def test_valid(self, mock__senators, mock__build_matrix):
        """cli.senators: The function should output a list of 
        the members of the U.S. Senate.
        """
        args_list = [
            ['Spam', 'Eggs', 'Democrat', 'sen', 'IL',
             'senior', 3, 'http://eggs.senate.gov', 
             '309-555-5555',],
            ['Bacon', 'Baked Beans', 'Independent', 'sen', 'IL', 
             'junior', 1, 'http://bakedbeans.senate.gov', 
             '309-555-5555',],
        ]
        matrix = [
            [
                'Name',                 # sen.last_name, sen.first_name
                'State',                # sen.state
                'Rank',                 # sen.rank
                'Party',                # sen.party
            ],
        ]
        for args in args_list:
            row = [
                ', '.join((args[0], args[1])),
                args[4],
                args[5],
                args[2],
            ]
            matrix.append(row)
        tmp = '{:<30} {:<5} {:<8} {}\n'
        lines = ['\n',]
        lines.append('LIST OF SENATORS\n')
        lines.append('----------------\n')
        for line in [tmp.format(*args) for args in matrix]:
            lines.append(line)
        lines.append('----------------\n')
        lines.append('\n')
        expected = ''.join(lines)
        
        details = [t_us.build_senator_details(args) for args in args_list]
        mock__senators.return_value = [us.Senator(detail) 
                                       for detail in details] 
        mock__build_matrix.return_value = matrix
        with capture() as (out, err):
            cli.senators()
        actual = out.getvalue()
        
        self.assertEqual(expected, actual)
        