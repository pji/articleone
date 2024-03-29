"""
validators
~~~~~~~~~~

This module contains the general validators for the articleone 
module.
"""
from re import match, sub
import unicodedata as ucd
import urllib.parse as up

from articleone.model import valfactory


# Validator functions.
def val_text(self, value, charset='utf_8', form='NFC'):
    """Normalize and validate text data."""
    if isinstance(value, bytes):
        try:
            value = value.decode(charset)
        except UnicodeDecodeError:
            reason = 'unable to decode character'
            raise ValueError(self.msg.format(reason))
    else:
        value = str(value)
    return ucd.normalize(form, value)


def val_http_url(self, value, charset='utf_8', form='NFC'):
    """Validate the value is an HTTP or HTTPS URL.
    
    Note: urlparse should probably be replaced with a stricter 
    parser in the future.
    """
    url = up.urlparse(value)
    if url.scheme != 'http' and url.scheme != 'https':
        reason = 'URL scheme not http or https'
        raise ValueError
    args = [
        url.scheme,
        up.quote(url.netloc, '@:%'),
        up.quote(url.path, '/%'),
        url.params,
        url.query,
        url.fragment,
    ]
    url = up.ParseResult(*args)
    normal = url.geturl()
    return normal


def val_phone_number(self, value, charset='utf_8', form='NFC'):
    """Is it a valid North American Numbering Plan phone number?"""
    value = val_text(self, value, charset, form)
    pattern = r'^[0-9]{3}-[0-9]{3}-[0-9]{4}$'
    if not match(pattern, value):
        value = sub(r'^[(]([0-9]{3})[)]', r'\1-', value)
        value = sub(r'^([0-9]{3})([0-9]{3})([0-9]{4})$', r'\1-\2-\3', value)
        if not match(pattern, value):
            reason = 'not a valid phone number'
            raise ValueError(self.msg.format(reason))
    return value


def val_whitelist(self, value, whitelist):
    """Validate the value is whitelisted."""
    if value not in whitelist:
        reason = 'not an allowed value'
        raise ValueError(self.msg.format(reason))
    return value


# Validating descriptors.
HttpUrl = valfactory('HttpUrl', val_http_url, 'Invalid HTTP URL ({}).')
Phone = valfactory('Phone', val_phone_number, 'Invalid Phone Number {()}.')
Text = valfactory('Text', val_text, 'Invalid text ({}).')
