from .errors import *
from .connection import Connection

# Helper constructor....
def create(*args, **kwargs):
    return Connection(*args, **kwargs)
