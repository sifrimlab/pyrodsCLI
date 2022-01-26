import os
import ssl
from irods.session import iRODSSession

def first_line(text):
    """
    Returns the first line of the given text, ignoring leading and trailing
    whitespace.
    """
    return text.strip().splitlines()[0]

def open_session():
    try:
        env_file = os.environ['IRODS_ENVIRONMENT_FILE']
    except KeyError:
        env_file = os.path.expanduser('~/.irods/irods_environment.json')

    ssl_context = ssl.create_default_context(purpose = ssl.Purpose.SERVER_AUTH, cafile = None, capath=None, cadata=None)
    ssl_settings = {'ssl_context': ssl_context}

    with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
        return session


