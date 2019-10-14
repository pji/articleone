"""
senate
~~~~~~

The module is a client for information on the U.S. Senate.
"""
# from lxml import etree

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
            'last_name': xml.xpath('/member/last_name/text()')[0],
            'first_name': xml.xpath('/member/first_name/text()')[0],
            'party': xml.xpath('/member/party/text()')[0],
        }
        return cls(**kwargs)