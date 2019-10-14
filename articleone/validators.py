"""
validators
~~~~~~~~~~

This module contains the general validators for the articleone 
module.
"""
import unicodedata as ucd

# Validator functions.
def val_text(self, value, charset='utf_8', form='NFC'):
    """Normalize and validate text data."""
    if isinstance(value, bytes):
        try:
            value = value.decode(charset)
        except UnicodeDecodeError:
            reason = 'invalid unicode character'
            raise ValueError(self.msg.format(reason))
    else:
        value = str(value)
    return ucd.normalize(form, value)
