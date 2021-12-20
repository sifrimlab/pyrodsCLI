import os
import ssl
import json
from icecream import ic
from tqdm import tqdm
from glob import glob
from pathlib import Path, PurePath
from irods.session import iRODSSession
from irods.meta import iRODSMeta, AVUOperation
# from irods.meta import iRODSMeta

try:
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
except KeyError:
    env_file = os.path.expanduser('~/.irods/irods_environment.json')

ssl_context = ssl.create_default_context(purpose = ssl.Purpose.SERVER_AUTH, cafile = None, capath=None, cadata=None)
ssl_settings = {'ssl_context': ssl_context}

def add_metadata_from_json(obj, json_file):
    with open(json_file) as jsonFile:
        jsonObject = json.load(jsonFile)
        avus = [item for item in jsonObject.items()]
        obj.metadata.apply_atomic_operations(*[AVUOperation(operation='add', avu=iRODSMeta("{}".format(str(meta[0]))
        , "{}".format(str(meta[1])))) for meta in avus])

def metadata_to_json(obj, output_dir = "./"):
    json_dict = {}
    json_name = os.path.splitext(obj.name)[0] + ".json"

    for item in obj.metadata.items():
        json_dict[item.name] = item.value

    with open(Path(output_dir , json_name), "w") as outfile:
        json.dump(json_dict, outfile)

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
def irods_put(pattern: str, target_collection, session, metadata: dict = {}):
    # gotta check if target collection exists first, by accessing its id
    irods_makedirs(target_collection, session)

    for file in tqdm(glob(pattern)):
        target_file = target_collection / os.path.basename(file)
        session.data_objects.put(str(file),str(target_file)) # casting to string since irods uses os.path under the hood

    
   
def irods_get(collection: str, session, target_dir = "./", start = "./"):
    # First define irods' current working directory if start isn't given, cause ./ doesn't mean anything
    if start == "./":
        start = PurePath(f'/{session.zone}') / 'home' / session.username 

    # Get collection object
    coll = session.collections.get(collection)

    # Walk over the colleciton
    for root, _, files in tqdm(coll.walk(topdown=True)): 
        rel_path = (os.path.relpath(root.path, start=start)) # cut start off of absolute irods path
        local_path = Path(target_dir, rel_path) # path based on local target dir and irods rel path root
        local_path.mkdir(parents=True, exist_ok=True) # make the dir if it doesnt exist already

        for file in files:
            obj = session.data_objects.get(file.path, Path(local_path, file.name))
            metadata_to_json(obj, output_dir = local_path)


if __name__ == "__main__":
    with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
        home_dir = PurePath(f'/{session.zone}') / 'home' / session.username 
        irods_get(str(home_dir / "pipeline_test_data/iss/Round1"), session)

