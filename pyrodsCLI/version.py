"""
Print the version of pyrodsCLI.
"""

from __version__ import __version__

def register_arguments(parser):
    pass

def run(args):
    print("pyrodsCLI", __version__)
    return 0
