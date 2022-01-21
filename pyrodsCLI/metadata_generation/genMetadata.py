import os
import re
from skimage import io

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

        

if __name__ == '__main__':
    image_path = "/media/sda1/thesis_data/spatial2/Export_20210412_CartanaISS_AP6_merged_Stitched-MaxIP.tif"
    generateMetaFromImage(image_path)
