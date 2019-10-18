"""
cli
~~~

A module for running articleone's command line interface.
"""
import argparse
import sys
import time

from articleone import common
from articleone import unitedstates as us


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


def write_term(title, tmp, matrix):
    print()
    print(title.upper())
    print('-' * len(title))
    for row in matrix:
        print(tmp.format(*row))
    print('-' * len(title))
    print()


# Command scripts.
def members():
    """Output a list of the members of the U.S. Congress."""
    mbr_list = us.members()
    matrix = common.build_member_matrix(mbr_list)
    tmp = '{:<20} {:<20} {}'
    title = 'List of Members'
    write_term(title, tmp, matrix)


def senators():
    """Output a list of the members of the U.S. Senate."""
    mbr_list = us.senators()
    matrix = common.build_member_matrix(mbr_list)
    tmp = '{:<20} {:<20} {}'
    title = 'List of Senators'
    write_term(title, tmp, matrix)


# Mainline.
if __name__ == '__main__':
    p = argparse.ArgumentParser(description='U.S. legislative branch info.')
    p.add_argument('-m', '--members', help='Get list of MoCs.', 
                   action='store_true')
    p.add_argument('-s', '--senators', help='Get list of senators.', 
                   action='store_true')
    args = p.parse_args()
    
    if args.members:
        members()
    if args.senators:
        senators()