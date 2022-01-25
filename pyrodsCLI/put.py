"""
Push data to your iRODS server
"""

def register_arguments(parser):
    parser.add_argument("glob_pattern", type=str, help="glob_pattern that determines what to put to the server")
    parser.add_argument("target_collection", type=str, help="Path to target collection, doesn't need to exist")
    parser.add_argument("--metadata", type=str, help="path to json file from which to pull data and add it to the to be put file")

# remember that inside python, every path to irods location has to be absolute
def irods_put(glob_pattern: str, target_collection, session, metadata: dict = {}):
    # gotta check if target collection exists first, by accessing its id
    irods_makedirs(target_collection, session)

    for glob_string in tqdm(glob(glob_pattern)):
        # If the it's a file, put it to the correct place
        if os.path.isfile(glob_string): 
            target_file = target_collection / os.path.basename(glob_string)
            session.data_objects.put(str(glob_string),str(target_file)) # casting to string since irods uses os.path under the hood

        # If it's a directory, calle this function again with adapter target collection
        elif os.path.isdir(glob_string):
            recursive_target_collection = target_collection / os.path.basename(glob_string)
            irods_put(f"{glob_string}/*", recursive_target_collection, session)
