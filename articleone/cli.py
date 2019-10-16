"""
cli
~~~

A module for running articleone's command line interface.
"""
import sys
import time


# Utility classes.
class Status:
    """A simple terminal status updater."""
    def __init__(self, title:str, prefix:str):
        self.title = title
        self.prefix = prefix
        self.msg = None
        self.t0 = time.time()
    
    def end(self):
        """Announce the end of the status updates."""
        sys.stdout.write('\n')
        duration = time.time() - self.t0
        tmp = ''.join([self.prefix, 'End'])
        sys.stdout.write(tmp.format(duration))
        sys.stdout.write('\n')
        sys.stdout.write('-' * len(self.title))
        sys.stdout.write('\n')
        sys.stdout.flush()
    
    def start(self):
        """Announce the start of the monitored process."""
        print(self.title.upper())
        print('-' * len(self.title))
    
    def set(self, tmp:str, *args):
        """Set a new update message and perform an initial update."""
        sys.stdout.write('\n')
        duration = time.time() - self.t0
        self.tmp = ''.join([self.prefix, tmp])
        self.msg = self.tmp.format(duration, *args)
        sys.stdout.write(self.msg)
        sys.stdout.flush()
        
    def update(self, *args):
        """Update the status message."""
        duration = time.time() - self.t0
        new_msg = self.tmp.format(duration, *args)
        sys.stdout.write('\x08' * len(self.msg))
        sys.stdout.write(new_msg)
        sys.stdout.flush()
        self.msg = new_msg


# Command scripts.
def senators():
    """Output a list of U.S. senators."""
    pass