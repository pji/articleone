"""
model
~~~~~

The module contains the basic classes used to build articleone's 
data model.
"""
import abc


class _BaseDescriptor:
    """A basic data descriptor."""
    _counter = 0
    
    def __init__(self):
        cls = self.__class__
        self.storage_name = f'_{cls.__name__}#{self._counter}'
        cls._counter += 1
    
    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
    
    def __get__(self, instance, owner):
        if instance:
            return getattr(instance, self.storage_name)
        return self


class Validated(abc.ABC, _BaseDescriptor):
    """A validating data descriptor."""
    def __set__(self, instance, value):
        """Send the given value for validation before setting it."""
        value = self.validate(value)
        super().__set__(instance, value)
    
    @abc.abstractmethod
    def validate(self, value):
        """Return the validated value or raise ValueError."""


def valfactory(name, validate_fn, message:str):
    """Build a validating data descriptor.
    
    :param name: The value of the name of the new class.
    :param validate_fn: The validating function for the class. 
        It should accept the parameters self and value. It 
        should return the normalized and validate value or 
        raise an exception if the value is invalid.
    :param message: The message the class should add to the 
        exception when the value given is invalid.
    :return: A validating data descriptor that's a subclass of 
        Validated.
    :rtype: type
    """
    attrs = {
        'validate': validate_fn,
        'msg': message,
    }
    return type(name, (Validated,), attrs)


def trusted(cls):
    """A class decorator for classes that use model.Validated 
    descriptors to validate their attributes.
    """
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Validated):
            name = type(attr).__name__
            attr.storage_name = f'_{name}__{key}'
    return cls