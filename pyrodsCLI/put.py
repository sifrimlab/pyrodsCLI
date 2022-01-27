"""
Push data to your iRODS server
"""
import os
from tqdm import tqdm
from glob import glob
from icecream import ic
from .utils import open_session, irods_makedirs

def register_arguments(parser):
    parser.add_argument("local_target", type=str, help="Local dir to put to iRODS")
    parser.add_argument("-o", "--target_collection", type=str, default="", help="Path to target collection. Default is home_dir of the session")
    parser.add_argument("--metadata", type=str, help="path to json file from which to pull data and add it to the to be put file")

def irods_put(local_target: str, session, home_dir,  target_collection:str = "",metadata: dict = {}):
    if not target_collection:
        target_collection = os.path.join(home_dir, os.path.relpath(local_target))
    # If target_collection isn't an absolute path, add the home dir to it
    if not target_collection.startswith("/"):
        target_collection = os.path.join(home_dir, target_collection)

    irods_makedirs(target_collection, session)

    for glob_string in tqdm(glob(f"{local_target}/*")):
        # If the it's a file, put it to the correct place
        if os.path.isfile(glob_string): 
            target_file = os.path.join(target_collection, os.path.basename(glob_string))
            session.data_objects.put(str(glob_string),str(target_file)) # casting to string since irods uses os.path under the hood

        # If it's a directory, calle this function again with adapter target collection
        elif os.path.isdir(glob_string):
            recursive_target_collection = os.path.join(target_collection, os.path.basename(glob_string))
            irods_put(f"{glob_string}/*", session, home_dir, target_collection = recursive_target_collection)

def run(args):
    session, home_dir = open_session()
    irods_put(local_target = args.local_target, target_collection = args.target_collection, session = session, home_dir = home_dir)

