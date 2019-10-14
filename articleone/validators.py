"""
validators
~~~~~~~~~~

This module contains the general validators for the articleone 
module.
"""
import unicodedata as ucd

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


def val_whitelist(self, value, whitelist):
    """Validate the value is whitelisted."""
    if value not in whitelist:
        reason = 'not an allowed value'
        raise ValueError(self.msg.format(reason))
    return value


# Validating descriptors.
Text = valfactory('Text', val_text, 'Invalid text ({})')