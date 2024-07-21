"""Record classes for the Lion framework."""

from .concept import AbstractElement
from .characteristic import Observable, Temporal


class BaseRecord(AbstractElement, Observable, Temporal):
    """
    Base class for records. Combines AbstractElement with Observable and
    Temporal characteristics.
    """


class MutableRecord(BaseRecord):
    """
    Mutable record class. Inherits from BaseRecord and allows
    modifications.
    """


class ImmutableRecord(BaseRecord):
    """
    Immutable record class. Inherits from BaseRecord but prevents
    modifications.
    """
    
# File: lion_core/abc/record.py