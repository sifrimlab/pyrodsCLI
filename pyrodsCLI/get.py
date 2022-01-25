"""
Retrieve data from your iRODS server
"""

def register_arguments(parser):
    parser.add_argument("collection", type=str, help="Path to collection to get")
    parser.add_argument("target_dir", type=str, help="Path to directory to get to")


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

if __name__ == '__main__':
    with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
        home_dir = PurePath(f'/{session.zone}') / 'home' / session.username 
        target_collection = home_dir / "BrainReceptorShowcase" / "Slice1" / "Replicate1" 
        irods_get("/media/gojira/MERFISH_datasets/BrainReceptorShowcase/Slice1/Replicate1/*", target_collection , session)
        # irods_get(str(home_dir / "pipeline_test_data/iss/Round1"), session)
