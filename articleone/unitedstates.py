"""
unitedstates
~~~~~~~~~~~~

The module is a client for information from the @unitedstates 
project on GitHub.
"""
from articleone import common
from articleone import http
from articleone import model
from articleone import validators as val


# Configuration.
URL = ('https://theunitedstates.io/congress-'
       'legislators/legislators-current.json')
CLASSES = (1, 2, 3)
RANKS = ['junior', 'senior', None]


# Validating functions.
def val_class(self, value):
    normal = int(value)
    if normal not in CLASSES:
        reason = 'not a valid Senate class'
        raise ValueError(self.msg.format(reason))
    return normal


def val_rank(self, value):
    if value not in RANKS:
        reason = 'not a valid Senate state rank'
        raise ValueError(self.msg.format(reason))
    return value


# Validating descriptors.
ValidClass = val.valfactory('ValidClass', val_class, 'Invalid class ({}).')
ValidRank = val.valfactory('ValidRank', val_rank, 'Invalid rank ({}).')


# Trusted classes.
@model.trusted
class Senator(common.Member):
    """A member of the Senate."""
    rank = ValidRank()
    senate_class = ValidClass()
    url = val.HttpUrl()
    
    def __init__(self, details):
        """Initialize and instance of the class."""
        last_name = details['name']['last']
        first_name = details['name']['first']
        term = details['terms'][-1]
        party = term['party']
        type = term['type']
        state = term['state']
        super().__init__(last_name, first_name, party, type, state)
        
        self.rank = term.setdefault('state_rank', None)
        self.senate_class = term.setdefault('class', None)
        self.url = term.setdefault('url', None)


# Data gathering functions.
def members():
    """Get a list of the members of the U.S. Congress."""
    details = _get_members_details()
    return [common.Member.from_json(detail) for detail in details]


def representatives():
    """Get a list of the members of the U.S. House of 
    Representatives.
    """
    return [mbr for mbr in members() if mbr.chamber == 'House']


def senators():
    """Get a list of the members of the U.S. Senate."""
    details = _get_members_details()
    return [Senator(detail) for detail in details 
            if detail['terms'][-1]['type'] == 'sen']


# Internal functions.
def _get_members_details():
    resp = http.get(URL)
    return common.parse_json(resp)