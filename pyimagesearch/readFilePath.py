import os

for dirPath, dirName, fileNames in os.walk("."):
    for item in fileNames:
        if item.endswith(".jpg"):
            filePath = os.path.join(dirPath, item) 


