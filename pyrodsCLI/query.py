"""
Query your iRODS library
"""
import os
from .utils import open_session
from irods.column import Criterion
from irods.models import DataObject, DataObjectMeta, Collection, CollectionMeta

def register_arguments(parser):
    parser.add_argument("search_string", type=str, help="String to search")
    parser.add_argument("-c", "--col", action="store_true", help="Search for collections instead of data objects")
    parser.add_argument("--start_dir", type=str, default="home", help="From which collection to start the query. Default = home dir")
    parser.add_argument("--exact_match", action="store_true", help="find an exact_match to the search strong, don't use like")
    parser.add_argument("--trash", action="store_true", help="Also find matches in the trash bin")
    

def queryCollections(search_string: str,  session, home_dir, start_dir: str = "home",  exact_match=False, trash = False):
        if start_dir == "home":
            start_dir = home_dir

        if exact_match:
            results = session.query(Collection.name).filter(Criterion('=', Collection.name, os.path.join(start_dir, search_string)))
        else:
            results = session.query(Collection.name).filter(Criterion('like', Collection.name, f'%{search_string}%'))

        if not trash:
            results = [result for result in results if "trash" not in str(result)]

        for item in results:
            print(item[Collection.name])

def queryObjects(search_string: str, session, home_dir, start_dir: str = "home", exact_match=False, trash = False):
        if start_dir == "home":
            start_dir = home_dir

        if exact_match:
            results = session.query(DataObject.name, DataObject.path).filter(Criterion('=', DataObject.name, os.path.join(start_dir, search_string)))
        else:
            results = session.query(DataObject.name, DataObject.path).filter(Criterion('like', DataObject.name, f'%{search_string}%'))

        if not trash:
            results = [result for result in results if "trash" not in str(result)]

        for item in results:
            print(item[DataObject.name], "\t", item[DataObject.path])

def run(args):
    session, home_dir = open_session()
    if args.col:
        queryCollections(args.search_string, session, home_dir, start_dir = args.start_dir, exact_match=args.exact_match, trash = args.trash)
    else:
        queryObjects(args.search_string, session, home_dir, start_dir = args.start_dir, exact_match=args.exact_match, trash = args.trash)

