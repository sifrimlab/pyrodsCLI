import os
import ssl
from pathlib import PurePath
from irods.column import Criterion
from irods.session import iRODSSession
from irods.models import DataObject, DataObjectMeta, Collection, CollectionMeta

try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

ssl_context = ssl.create_default_context(purpose = ssl.Purpose.SERVER_AUTH, cafile = None, capath=None, cadata=None)
ssl_settings = {'ssl_context': ssl_context}

def queryCollections(search_string: str, start_dir: str = "home", exact_match=False, no_trash = True):
    with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
        if start_dir == "home":
            start_dir = PurePath(f'/{session.zone}') / 'home' / session.username

        if exact_match:
            results = session.query(Collection.name).filter(Criterion('=', Collection.name, start_dir / search_string))
        else:
            results = session.query(Collection.name).filter(Criterion('like', Collection.name, f'%{search_string}%'))

        if no_trash:
            results = [result for result in results if "trash" not in str(result)]

        for item in results:
            print(item[Collection.name])

def queryObjects(search_string: str, start_dir: str = "home", exact_match=False, no_trash = True):
    with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
        if start_dir == "home":
            start_dir = PurePath(f'/{session.zone}') / 'home' / session.username

        if exact_match:
            results = session.query(DataObject.name).filter(Criterion('=', Collection.name, start_dir / search_string))
        else:
            results = session.query(DataObject.name)

            # results = session.query(Collection.name).filter(Criterion('like', Collection.name, f'%{search_string}%'))

        # if no_trash:
        #     results = [result for result in results if "trash" not in str(result)]

        for item in results:
            print(item[DataObject.name])



if __name__ == '__main__':
    queryObjects("mouse")
    # ap = argparse.ArgumentParser(description="DESC")
    
    # ap.add_argument('NAME',type=TYPE, default="DEF"help="TYPE")
    
    # args = ap.parse_args()
