"""
cli
~~~

A module for running articleone's command line interface.
"""


class Status:
    """A terminal status updater."""
    def __init__(self, title):
        self.title = title