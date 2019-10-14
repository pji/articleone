"""
common
~~~~~~

The module contains the basic classes used in articleone.
"""
from articleone import validators as valid


class Member:
    """A member of Congress."""
    last_name = valid.Text()
    first_name = valid.Text()
    
    def __init__(self, last_name: str, first_name: str):
        """Initialize an instance."""
        self.last_name = last_name
        self.first_name = first_name