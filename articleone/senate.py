"""
senate
~~~~~~

The module is a client for information on the U.S. Senate.
"""
from lxml import etree

from articleone import common
from articleone import model


# Data objects specific to the Senate.
@model.trusted
class Senator(common.Member):
    """A United States Senator."""
    @classmethod
    def from_xml(cls, xml):
        """Create a new object from XML."""
        kwargs = {
            'last_name': xml.xpath('last_name/text()')[0],
            'first_name': xml.xpath('first_name/text()')[0],
            'party': xml.xpath('party/text()')[0],
        }
        return cls(**kwargs)


# Functions to pull information from senate.gov.
def get_senators():
    """Get the list of current U.S. Senators."""
    xml = common.parse_xml()
    xpath = '/contact_information/member'
    return [Senator.from_xml(details) for details in xml.xpath(xpath)]


def _fetch_senate_xml():
    pass