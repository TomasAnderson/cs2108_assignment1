import os
import sys


for dirPath, dirName, fileNames in os.walk("."):
    for item in fileNames:
        if item.endswith(".jpg"):
            filePath = os.path.join(dirPath, item)
            command = "python DL_Classify_image.py --image_file "+filePath
            print filePath
            os.system(command)
