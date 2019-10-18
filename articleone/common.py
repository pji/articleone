"""
common
~~~~~~

The module contains the basic classes used in articleone.
"""
from json import loads

from lxml import etree

from articleone import model as model
from articleone import validators as valid


# Common configuration.
PARTIES = ['D', 'I', 'R', 'Democrat', 'Republican', 'Independent']


# Common object validator functions.
def val_party(self, value):
    if value not in PARTIES:
        reason = 'value not in list'
        raise ValueError(self.msg.format(reason))
    return value


# Common object validating descriptors.
ValidParty = valid.valfactory('ValidParty', val_party, 'Invalid party ({}).')


# Common objects.
@model.trusted
class Member:
    """A member of Congress."""
    last_name = valid.Text()
    first_name = valid.Text()
    party = ValidParty()
    
    def __init__(self, last_name:str, first_name:str, party:str):
        """Initialize an instance."""
        self.last_name = last_name
        self.first_name = first_name
        self.party = party
    
    def __eq__(self, other):
        """Evaluate equality of two common.Member objects."""
        if not isinstance(other, Member):
            return NotImplemented
        return (self.last_name == other.last_name 
                and self.first_name == other.first_name 
                and self.party == other.party)
    
    def __ne__(self, other):
        """Evaluate non-equality of two common.Member objects."""
        return not self == other
    
    def __repr__(self):
        """Provide a string representation for troubleshooting."""
        name = self.__class__.__name__
        return (f'{name}({self.last_name!r}, {self.first_name!r}, '
                f'{self.party!r})')
    
    @classmethod
    def from_json(cls, details):
        """Build a member from @unitedstates JSON."""
        args = [
            details['name']['last'],
            details['name']['first'],
            details['terms'][-1]['party'],
        ]
        return cls(*args)


# Common utilities.
def build_member_matrix(mbr_list):
    """Return a matrix of information on the given members list."""
    headers = [
        'Last Name',            # Member.last_name
        'First Name',           # Member.first_name
        'Party',                # Member.party
    ]
    matrix = [headers,]
    for mbr in mbr_list:
        row = [
            mbr.last_name,
            mbr.first_name,
            mbr.party,
        ]
        matrix.append(row)
    return matrix


def parse_json(text:str):
    """Parse the given string as JSON."""
    return loads(text)


def parse_xml(text:str):
    """Parse the given string as XML."""
    return etree.fromstring(text)