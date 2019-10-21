"""
unitedstates
~~~~~~~~~~~~

The module is a client for information from the @unitedstates 
project on GitHub.
"""
from operator import itemgetter

from articleone import common
from articleone import http
from articleone import model
from articleone import validators as val


# Configuration.
URL = ('https://theunitedstates.io/congress-'
       'legislators/legislators-current.json')
CLASSES = (1, 2, 3)
DISTRICTS = (0, 53)
RANKS = ['junior', 'senior', None]


# Validating functions.
def val_class(self, value):
    normal = int(value)
    if normal not in CLASSES:
        reason = 'not a valid Senate class'
        raise ValueError(self.msg.format(reason))
    return normal


def val_district(self, value):
    """Is the value a possible U.S. House district number?"""
    try:
        value = int(value)
    except ValueError:
        reason = 'district must be able to be an int'
        raise TypeError(self.msg.format(reason))
    if value < DISTRICTS[0]:
        reason = f'district cannot be less than {DISTRICTS[0]}'
        raise ValueError(self.msg.format(reason))
    if value > DISTRICTS[1]:
        reason = f'district cannot be more than {DISTRICTS[1]}'
        raise ValueError(self.msg.format(reason))
    return value


def val_rank(self, value):
    if value not in RANKS:
        reason = 'not a valid Senate state rank'
        raise ValueError(self.msg.format(reason))
    return value


# Validating descriptors.
ValidClass = val.valfactory('ValidClass', val_class, 'Invalid class ({}).')
ValidRank = val.valfactory('ValidRank', val_rank, 'Invalid rank ({}).')
ValidDistrict = val.valfactory('ValidDistrict', val_district, 'Invalid district ({}).')


# Trusted classes.
@model.trusted
class Representative(common.Member):
    """A member of the House of Representatives."""
    district = ValidDistrict()
    url = val.HttpUrl()
    phone = val.Phone()
    
    def __init__(self, details):
        """Initialize an instance of the class."""
        last_name = details['name']['last']
        first_name = details['name']['first']
        term = details['terms'][-1]
        party = term['party']
        type = term['type']
        state = term['state']
        super().__init__(last_name, first_name, party, type, state)
        
        self.district = term['district']
        self.url = term['url']
        self.phone = term['phone']


@model.trusted
class Senator(common.Member):
    """A member of the Senate."""
    rank = ValidRank()
    senate_class = ValidClass()
    url = val.HttpUrl()
    phone = val.Phone()
    
    def __init__(self, details):
        """Initialize an instance of the class."""
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
        self.phone = term.setdefault('phone', None)


# Data gathering functions.
def members():
    """Get a list of the members of the U.S. Congress."""
    details = _get_members_details()
    return [common.Member.from_json(detail) for detail in details]


def representatives():
    """Get a list of the members of the U.S. House of 
    Representatives.
    """
    details = _get_members_details()
    return [Representative(detail) for detail in details 
            if detail['terms'][-1]['type'] == 'rep']


def senators():
    """Get a list of the members of the U.S. Senate."""
    details = _get_members_details()
    return [Senator(detail) for detail in details 
            if detail['terms'][-1]['type'] == 'sen']


# Matrix building functions.
def build_sen_matrix(sen_list):
    """Return a matrix of information on the given Senator objects."""
    headers = [
        'Name',                 # sen.last_name, sen.first_name
        'State',                # sen.state
        'Rank',                 # sen.rank
        'Party',                # sen.party
    ]
    rows = []
    for sen in sen_list:
        row = [
            ', '.join((sen.last_name, sen.first_name)),
            sen.state,
            sen.rank,
            sen.party,
        ]
        rows.append(row)
    rows = sorted(rows, key=itemgetter(1))
    sorted(rows, key=itemgetter(2), reverse=True)
    matrix = [headers,]
    matrix.extend(rows)
    return matrix


# Internal functions.
def _get_members_details():
    resp = http.get(URL)
    return common.parse_json(resp)