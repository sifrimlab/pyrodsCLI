"""
Generate metadata for local or irods files
"""
import os
import json
import re
# from skimage import io
from irods.meta import iRODSMeta, AVUOperation

def register_arguments(parser):
    parser.add_argument("filename", type=str, default="", help="Path to collection to get")
    parser.add_argument("--keys", type=str, default="['name']", help="Keywords to put into the json")
    parser.add_argument("--from-name", action="store_true", help="Generate metadate by parsing the filename")
    parser.add_argument("--from-image", action="store_true", help="Generate metadate by finding image metadata")

def generateJson(filename,*args, **kwargs):
    data_dict = {"name": filename}

    for key in args:
        data_dict[key] = ""

    for key, value in kwargs.items():
        data_dict[key] = str(value)

    with open(f'{filename}.json', 'w') as f:
        json.dump(data_dict, f, indent=4)

def generateMetaFromName(filename: str):
    filebase =os.path.basename(os.path.splitext(filename)[0])
    metadata = {"name" : filebase}
    split_list = filebase.split("_")
    for el in split_list: 
        try:
            temp = re.compile("([a-zA-Z]+)([0-9]+)")
            res = temp.match(el).groups()
            metadata[res[0]] = res[1]
        except:
            res = True
            metadata[el] = res

def generateMetaFromImage(filename: str):
    filebase = os.path.basename(os.path.splitext(filename)[0])
    metadata = {"name" : filebase}
    img = io.imread(filename)
    metadata["X"] = img.shape[1]
    metadata["Y"] = img.shape[0]
    metadata["bit_depth"] = img.dtype
    print(metadata)

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

    with open(os.path.join(output_dir , json_name), "w") as outfile:
        json.dump(json_dict, outfile)
