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
            },
        ],
    }


# Tests.
class MembersTestCase(unittest.TestCase):
    @patch('articleone.common.parse_json')
    @patch('articleone.http.get')
    def test_valid(self, mock__get, mock__parse_json):
        """unitedstates.members: The function should return a list 
        of common.Member objects representin the members of U.S. 
        Congress.
        """
        data = [
            ['Spam', 'Eggs', 'Democrat',],
            ['Bacon', 'Baked Beans', 'Independent',],
        ]
        us_json = [build_us_details(item) for item in data]
        expected = [com.Member(*args) for args in data]
        
        mock__get.return_value = json.dumps(us_json)
        mock__parse_json.return_value = us_json
        actual = us.members()
        
        self.assertEqual(expected, actual)
        mock__parse_json.assert_called_with(json.dumps(us_json))
        