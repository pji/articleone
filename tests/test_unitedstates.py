"""
test_unitedstates
~~~~~~~~~~~~~~~~~

This module contains the tests for the articleone.unitedstates module.
"""
import json
import unittest
from unittest.mock import patch

from articleone import common as com
from articleone import unitedstates as us


# Test data utilities.
def build_rep_details(details):
    """Build the test data for a representative."""
    data = build_us_details(details)
    data['terms'][-1]['district'] = details[5]
    data['terms'][-1]['url'] = details[6]
    data['terms'][-1]['phone'] = details[7]
    return data


def build_senator_details(details):
    """Build the test data for a senator."""
    data = build_us_details(details)
    data['terms'][-1]['state_rank'] = details[5]
    data['terms'][-1]['class'] = details[6]
    data['terms'][-1]['url'] = details[7]
    data['terms'][-1]['phone'] = details[8]
    return data


def build_us_details(details):
    """Build test data for a member of Congress."""
    return {
        'name': {
            'last': details[0],
            'first': details[1],
            'full name': f'{details[0]} {details[1]}',
        },
        'terms': [
            {
                'party': details[2],
                'type': details[3],
                'state': details[4],
            },
        ],
    }


class Descr:
    """A stub class for validator tests."""
    msg = '{}'


# Validator tests.
class ValClassTestCase(unittest.TestCase):
    def test_valid(self):
        """unitedstates.val_class: Given a valid Senate class, the 
        function should return the value.
        """
        expected = 2
        actual = us.val_class(None, expected)
        self.assertEqual(expected, actual)
    
    def test_invalid(self):
        """unitedstates.val_class: Given an invalid Senate class, the 
        function should raise a ValueError exception.
        """
        expected = ValueError
        class Spam:
            msg = '{}'
        value = 5
        
        with self.assertRaises(expected):
            _ = us.val_class(Spam(), value)
    
    def test_validStr(self):
        """unitedstates.val_class: Given a valid Senate class as a 
        string, normalize the value to an integer and return it.
        """
        expected_cls = int
        expected_val = 2
        value = str(expected_val)
        actual = us.val_class(None, value)
        self.assertTrue(isinstance(actual, expected_cls))
        self.assertEqual(expected_val, actual)


class ValDistrictTestCase(unittest.TestCase):
    def test_valid(self):
        """unitedstates.val_district: Given a value, if the value 
        is valid, return it.
        """
        expected = 10
        actual = us.val_district(Descr(), expected)
        self.assertEqual(expected, actual)
    
    def test_invalidMin(self):
        """unitedstates.val_district: Given a value, if the value 
        is below the minimum district number, the function should 
        raise a ValueError exception.
        """
        expected = ValueError
        value = -1
        with self.assertRaises(expected):
            _ = us.val_district(Descr(), value)
    
    def test_invalidMax(self):
        """unitedstates.val_district: Given a value, if the value 
        is above the maximum district number, the function should 
        raise a ValueError exception.
        """
        expected = ValueError
        value = 54
        with self.assertRaises(expected):
            _ = us.val_district(Descr(), value)
    
    def test_normalizeStr(self):
        """unitedstates.val_district: Given a value, if the value 
        cannot be coerced to a integer, it is invalid, and the 
        function should return a TypeError exception.
        """
        expected = TypeError
        value = 'two'
        with self.assertRaises(expected):
            _ = us.val_district(Descr(), value)


class ValRankTestCase(unittest.TestCase):
    def test__valid(self):
        """unitedstates.val_rank: Given a valid state rank for a 
        senator, the function should return it.
        """
        expected = 'junior'
        actual = us.val_rank(None, expected)
        self.assertEqual(expected, actual)
    
    def test__invalid(self):
        """unitedstates.val_rank: Given an invalid state rank for 
        a senator, the function should raise a ValueError exception.
        """
        expected = ValueError
        class Spam:
            msg = '{}'
        value = 1
        with self.assertRaises(expected):
            _ = us.val_rank(Spam(), value)


class DescriptorsTestCase(unittest.TestCase):
    def test__ValidClass(self):
        """unitedstates.ValidClass: If given a valid Senate class, 
        the descriptor should set it as the protected value.
        """
        expected = 2
        
        class Spam:
            senate_class = us.ValidClass()
        obj = Spam()
        obj.senate_class = expected
        actual = obj.senate_class
        
        self.assertEqual(expected, actual)

    def test__ValidDistrict(self):
        """unitedstates.ValidDistrict: Given a value, if the value 
        is a valid possible House of Representatives district, the 
        descriptor should set it as the value of the protected 
        attribute.
        """
        expected = 4
        
        class Spam:
            district = us.ValidDistrict()
        obj = Spam()
        obj.district = expected
        actual = obj.district
        
        self.assertEqual(expected, actual)
    
    
    def test__ValidRank(self):
        """unitedstates.ValidRank: If given a valid senator's state 
        rank, the descriptor should set it as the protected value.
        """
        expected = 'senior'
        
        class Spam:
            rank = us.ValidRank()
        obj = Spam()
        obj.rank = expected
        actual = obj.rank
        
        self.assertEqual(expected, actual)
    

# Trusted object tests.
class RepresentativeTestCase(unittest.TestCase):
    def test__subclass(self):
        """unitedstates.Representative: The class should be a 
        subclass of common.Member.
        """
        expected = com.Member
        actual = us.Representative
        self.assertTrue(issubclass(actual, expected))
    
    def test__init(self):
        """unitedstates.Representative: Given a dictionary of 
        details, the class should populate its attributes as 
        expected when instantiated.
        """
        expected = [
            'Eggs', 
            'Spam', 
            'Democrat',
            'House',
            'IL',
            13,
            'http://eggs.house.gov',
            '309-555-5555',
        ]
        
        details = build_rep_details(expected)
        rep = us.Representative(details)
        actual = [
            rep.last_name,
            rep.first_name,
            rep.party,
            rep.chamber,
            rep.state,
            rep.district,
            rep.url,
            rep.phone,
        ]
        
        self.assertEqual(expected, actual)


class SenatorTestCase(unittest.TestCase):
    def test__subclass(self):
        """common.Senator: The class should be a subclass of 
        common.Member.
        """
        expected = com.Member
        actual = us.Senator
        self.assertTrue(issubclass(actual, expected))
    
    def test__init(self):
        """common.Senator.__init__: The class should populate 
        its attributes as expected when instantiated.
        """
        expected = [
            'Spam',
            'Eggs',
            'Democrat',
            'Senate',
            'IL',
            'junior',
            2,
            'https://test.local/index.html',
            '309-555-5555',
        ]
        
        data = build_senator_details(expected)
        sen = us.Senator(data)
        actual = [
            sen.last_name,
            sen.first_name,
            sen.party,
            sen.chamber,
            sen.state,
            sen.rank,
            sen.senate_class,
            sen.url,
            sen.phone,
        ]
        
        self.assertEqual(expected, actual)


# Data gathering function tests.
class MembersTestCase(unittest.TestCase):
    @patch('articleone.common.parse_json')
    @patch('articleone.http.get')
    def test_valid(self, mock__get, mock__parse_json):
        """unitedstates.members: The function should return a list 
        of common.Member objects representing the members of U.S. 
        Congress.
        """
        data = [
            ['Spam', 'Eggs', 'Democrat', 'Senate', 'IL',],
            ['Bacon', 'Baked Beans', 'Independent', 'Senate', 'IL',],
        ]
        us_json = [build_us_details(item) for item in data]
        expected = [com.Member(*args) for args in data]
        
        mock__get.return_value = json.dumps(us_json)
        mock__parse_json.return_value = us_json
        actual = us.members()
        
        self.assertEqual(expected, actual)
        mock__parse_json.assert_called_with(json.dumps(us_json))


class RepresentativesTestCase(unittest.TestCase):
    @patch('articleone.unitedstates._get_members_details')
    def test_valid(self, mock__gmd):
        """unitedstates.representatives: The function should 
        return a list of common.Member objects representing the 
        members of the U.S. House of Representatives.
        """
        args_list = [
            ['Spam', 'Eggs', 'Democrat', 'Senate', 'IL',],
            ['Bacon', 'Baked Beans', 'Independent', 'rep', 'IL',
             3, 'http://bakedbeans.house.gov', '309-555-5555',],
            ['Ham', 'Tomato', 'Democrat', 'rep', 'IL', 
             4, 'http://ham.house.gov', '309-555-5555',],
        ]
        details = [
            build_us_details(args_list[0]),
            build_rep_details(args_list[1]), 
            build_rep_details(args_list[2]),
        ]
        expected = [
            us.Representative(details[1]),
            us.Representative(details[2]),
        ]
        
        mock__gmd.return_value = details
        actual = us.representatives()
        
        self.assertEqual(expected, actual)


class SenatorsTestCase(unittest.TestCase):
    @patch('articleone.unitedstates._get_members_details')
    def test_valid(self, mock__gmd):
        """unitedstates.senators: The function should return a 
        list of common.Member objects representing the members 
        of the U.S. Senate.
        """
        args_list = [
            ['Spam', 'Eggs', 'Democrat', 'sen', 'IL',
             'senior', 3, 'http://eggs.senate.gov', 
             '309-555-5555',],
            ['Bacon', 'Baked Beans', 'Independent', 'sen', 'IL', 
             'junior', 1, 'http://bakedbeans.senate.gov', 
             '309-555-5555',],
            ['Ham', 'Tomato', 'Democrat', 'rep', 'IN',],
        ]
        details = [
            build_senator_details(args_list[0]), 
            build_senator_details(args_list[1]), 
            build_us_details(args_list[2]),
        ]
        expected = [
            us.Senator(details[0]),
            us.Senator(details[1]),
        ]
        
        mock__gmd.return_value = details
        actual = us.senators()
        
        self.assertEqual(expected, actual)


# Matrix building functions.
class BuildSenMatrixTestCase(unittest.TestCase):
    def test_valid(self):
        """unitedstates.build_sen_matrix: Given a list of 
        unitedstates.Senator objects, return a list of rows 
        suitable for a report on the Senator orbjects.
        """
        args_list = [
            ['Spam', 'Eggs', 'Democrat', 'sen', 'IL',
             'senior', 3, 'http://eggs.senate.gov', 
             '309-555-5555',],
            ['Bacon', 'Baked Beans', 'Independent', 'sen', 'IL', 
             'junior', 1, 'http://bakedbeans.senate.gov', 
             '309-555-5555',],
        ]
        expected = [[
            'Name',                 # sen.last_name, sen.first_name
            'State',                # sen.state
            'Rank',                 # sen.rank
            'Party',                # sen.party
        ],]
        for args in args_list:
            row = [
                ', '.join((args[0], args[1])),
                args[4],
                args[5],
                args[2],
            ]
            expected.append(row)
        
        details = [build_senator_details(args) for args in args_list]
        sen_list = [us.Senator(detail) for detail in details]
        actual = us.build_sen_matrix(sen_list)
        
        self.assertEqual(expected, actual)


# Internal function tests.
class GetMembersDetailsTestCase(unittest.TestCase):
    @patch('articleone.common.parse_json')
    @patch('articleone.http.get')
    def test_valid(self, mock__get, mock__parse_json):
        """unitedstates._get_members_details: The function should 
        return a list of dictionaries representing the members of 
        the U.S. Congress.
        """
        data = [
            ['Spam', 'Eggs', 'Democrat', 'Senate', 'IL',],
            ['Bacon', 'Baked Beans', 'Independent', 'Senate', 'IL',],
        ]
        expected = [build_us_details(item) for item in data]
        
        mock__get.return_value = json.dumps(expected)
        mock__parse_json.return_value = expected
        actual = us._get_members_details()
        
        self.assertEqual(expected, actual)


