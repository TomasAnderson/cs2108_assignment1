import os
import cv2 as cv
import csv
from pyimagesearch.colordescriptor import ColorDescriptor

cd = ColorDescriptor((8, 12, 3))

with open("ch.csv", "w") as f:
	writer = csv.writer(f)
	for dirPath, dirName, fileNames in os.walk("./image/dataset/"):
		for item in fileNames:
			if item.endswith(".jpg"):
				filePath = os.path.join(dirPath, item)
				query = cv.imread(filePath)
				queryfeatures = cd.describe(query)
				writer.writerow([item]+queryfeatures)