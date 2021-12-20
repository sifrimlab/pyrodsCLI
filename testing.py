import os
import ssl
from glob import glob
from pathlib import PurePath
from irods.session import iRODSSession
# from irods.meta import iRODSMeta

try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

ssl_context = ssl.create_default_context(purpose = ssl.Purpose.SERVER_AUTH, cafile = None, capath=None, cadata=None)
ssl_settings = {'ssl_context': ssl_context}

def irods_makedirs(dir_path: str, session): 
    """Creates a collection in irods if it doesn't exist already

    Parameters
    ----------
    dir_path : str
        dir_path
    """

    try:
        session.collections.get(dir_path)
    except:
        session.collections.create(dir_path)

# remember that inside python, every path to irods location has to be absolute
def irods_put(filename: str, target_collection, session, metadata: dict = {}):

    # gotta check if target colleciton exists first, by accessing its id
    irods_makedirs(target_collection, session)

    target_file = target_collection / os.path.basename(filename)

    session.data_objects.put(str(filename),str(target_file)) # casting to string since irods uses os.path under the hood

if __name__ == "__main__":
    with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
        home_dir = PurePath(f'/{session.zone}') / 'home' / session.username 
        testing_dir = home_dir / "testing"
        irods_put("/home/david/Documents/iRODS/test_col1/*", testing_dir, session = session)

