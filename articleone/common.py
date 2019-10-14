"""
common
~~~~~~

The module contains the basic classes used in articleone.
"""
from functools import partial

from articleone import validators as valid


# Common configuration.
PARTIES = ['D', 'I', 'R']


# Common object validator functions.
def val_party(self, value):
    if value not in PARTIES:
        reason = 'value not in list'
        raise ValueError(self.msg.format(reason))
    return value


# Common object validating descriptors.
ValidParty = valid.valfactory('ValidParty', val_party, 'Invalid party ({}).')


# Common objects.
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