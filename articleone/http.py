"""
http
~~~~

A module to handle making HTTP requests.
"""
import requests


# Exceptions.
class AuthenticationError(RuntimeError):
    """The request received a 401 error from the server."""

class NotFoundError(RuntimeError):
    """The request received a 404 error from the server."""

class ServerError(RuntimeError):
    """The request received a 500 error from the server."""


# HTTP calls.
def get(url:str, session: requests.Session = None):
    """Make an HTTP GET request."""
    if session:
        resp = session.get(url)
    else:
        resp = requests.get(url)
    
    if resp.status_code == 401:
        raise AuthenticationError('Authentication failed.')
    if resp.status_code == 404:
        raise NotFoundError('Page not found.')
    if resp.status_code >= 500 and resp.status_code < 600:
        print(resp.text)
        raise ServerError('Encountered a server error.')
    
    return resp.text


# Utility functions.
def build_session():
    """Provide a session object for use in tracking session."""
    return requests.Session()