"""
Stub function and module used as a setuptools entry point.
"""

import pyrodsCLI
from sys import argv, exit

# Entry point for setuptools-installed script and bin/augur dev wrapper.
def main():
    return pyrodsCLI.run( argv[1:] )

# Run when called as `python -m augur`, here for good measure.
if __name__ == "__main__":
    exit( main() )
