# USAGE
# python index.py --dataset dataset --index index.csv

# import the necessary packages
import argparse
import nltk
import os
from nltk.stem.lancaster import LancasterStemmer
import glob
import time
import cPickle as pickle

class TagIndex:
        def __init__(self):
                doc = open(args["tags"], 'r')
                self.taglist = dict()
                self.imagetagcnt =  dict()
                for line in doc:
                        line = line.split()
                        self.inverse_index(line, self.taglist)
                doc.close()
                self.storeToFile(args["index"])
                
        def inverse_index(self, line, taglist):
                tags_length = len(line) - 1
                image_name = line[0]
                self.imagetagcnt[image_name] = tags_length
                for i in range (1,tags_length):
                        try:
                                tag = LancasterStemmer().stem(line[i])
                                tag = nltk.stem.WordNetLemmatizer().lemmatize(tag)
                        except UnicodeDecodeError:
                                tag = line[i]
                        if taglist.has_key(tag):
                                taglist[tag].append(image_name)
                        else:
                                taglist[tag]=[image_name,]

        def storeToFile(self, filepath):
                indexfile = open(filepath, 'w')
                pickle.dump(self.imagetagcnt,indexfile)
                pickle.dump(self.taglist, indexfile)
                indexfile.close()

        def printToDisplay(self):
                for k in self.taglist:
                        print k, self.taglist[k]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = False, default='dataset',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-t", "--tags", required = False, default='image'+os.sep+'train_text_tags.txt',
	help = "Path to where the file describing images and their list of tags are stored")
ap.add_argument("-i", "--index", required = False, default='pyimagesearch'+os.sep+'TR_index.txt',
	help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

#printToDisplay()
