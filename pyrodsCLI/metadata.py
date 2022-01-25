"""
Generate metadata for local or irods files
"""

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

