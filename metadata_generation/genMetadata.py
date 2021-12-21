import os
import re
import tifffile as tf

def generateMetaFromName(filename: str):
    filebase = os.path.splitext(filename)[0]
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
    tif = tf.TiffFile(filename)
    # image = tf.imread(filename)
    metadata_attrs = [attr for attr in dir(tif) if "meta" in attr]
    print(metadata_attrs)
    print(tif.andor_metadata)

if __name__ == '__main__':
    image_path = "/home/david/Documents/presentation_10nov/imgs/1_ME_distal_20X_18WKJuly2021_img10_c0_maxIP.tiff"
    generateMetaFromImage(image_path)
