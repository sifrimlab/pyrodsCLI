import sys
import json



def generateJson(filename,*args, **kwargs):
    data_dict = {"name": filename}

    for key in args:
        data_dict[key] = ""

    for key, value in kwargs.items():
        data_dict[key] = str(value)

    with open(f'{filename}.json', 'w') as f:
        json.dump(data_dict, f, indent=4)


if __name__ == '__main__':
    filename = sys.argv[1]
    args = [sys.argv[i] for i in range(2,len(sys.argv))]
    generateJson(filename, *args)

    

