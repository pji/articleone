"""
unitedstates
~~~~~~~~~~~~

The module is a client for information from the @unitedstates 
project on GitHub.
"""
from articleone import common
from articleone import http


# Configuration.
URL = ('https://theunitedstates.io/congress-'
       'legislators/legislators-current.json')


# Data gathering functions.
def members():
    """Get a list of the members of the U.S. Congress."""
    resp = http.get(URL)
    details = common.parse_json(resp)
    return [common.Member.from_json(detail) for detail in details]


def representatives():
    """Get a list of the members of the U.S. House of 
    Representatives.
    """
    return [mbr for mbr in members() if mbr.chamber == 'House']


def senators():
    """Get a list of the members of the U.S. Senate."""
    return [mbr for mbr in members() if mbr.chamber == 'Senate']