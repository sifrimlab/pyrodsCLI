"""
Query your iRODS library
"""

def register_arguments(parser):
    parser.add_argument("search_string", type=str, help="String to search")
    parser.add_argument("start_dir", type=str, default="home", help="From which collection to start the query. Default = home dir")
    parser.add_argument("--exact_match", action="store_true", help="find an exact_match to the search strong, don't use like")
    parser.add_argument("--trash", action="store_true", help="Also find matches in the thrash bin")
    

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

