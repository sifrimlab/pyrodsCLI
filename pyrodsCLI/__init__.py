import argparse
import re
import os
import sys
import importlib
from types import SimpleNamespace
from .utils import first_line

recursion_limit = os.environ.get("IRODS_RECURSION_LIMIT")
if recursion_limit:
    sys.setrecursionlimit(int(recursion_limit))

command_strings = [
    "get",
    "put",
    "metadata",
    "query",
]

COMMANDS = [importlib.import_module('pyrodsCLI.' + c) for c in command_strings]

def make_parser():
    parser = argparse.ArgumentParser(
        prog        = "pyrodsCLI",
        description = "Collection of commands to use iRODS, the Open Source Data Management Software")

    subparsers = parser.add_subparsers()

    add_default_command(parser)
    add_version_alias(parser)

    for command in COMMANDS:
        # Add a subparser for each command.
        subparser = subparsers.add_parser(
            command_name(command),
            help        = first_line(command.__doc__),
            description = command.__doc__)

        subparser.set_defaults(__command__ = command)

        # Let the command register arguments on its subparser.
        command.register_arguments(subparser)

        # Use the same formatting class for every command for consistency.
        # Set here to avoid repeating it in every command's register_parser().
        subparser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    return parser


def run(argv):
    args = make_parser().parse_args(argv)
    try:
        return args.__command__.run(args)
    except RecursionError:
        print("FATAL: Maximum recursion depth reached. You can set the env variable IRODS_RECURSION_LIMIT to adjust this (current limit: {})".format(sys.getrecursionlimit()))
        sys.exit(2)


def add_default_command(parser):
    """
    Sets the default command to run when none is provided.
    """
    class default_command():
        def run(args):
            parser.print_help()
            return 2

    parser.set_defaults(__command__ = default_command)


def add_version_alias(parser):
    """
    Add --version as a (hidden) alias for the version command.
    It's not uncommon to blindly run a command with --version as the sole
    argument, so its useful to make that Just Work.
    """

    class run_version_command(argparse.Action):
        def __call__(self, *args, **kwargs):
            opts = SimpleNamespace()
            sys.exit( version.run(opts) )

    return parser.add_argument(
        "--version",
        nargs  = 0,
        help   = argparse.SUPPRESS,
        action = run_version_command)


def command_name(command):
    """
    Returns a short name for a command module.
    """

    def remove_prefix(prefix, string):
        return re.sub('^' + re.escape(prefix), '', string)

    package     = command.__package__
    module_name = command.__name__

    return remove_prefix(package, module_name).lstrip(".").replace("_", "-")
