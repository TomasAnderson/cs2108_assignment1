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
                self.taglist = []
                self.imagelist = []
                self.query_pos = 0
                for line in doc:
                        line = line.split()
                        self.stem_word(line, self.taglist)
                #print self.taglist[243], self.imagelist[243]
                doc.close()
                self.read_test_tags()
		self.extend_tags_w_cat()
                self.storeToFile(args["index"])

	def extend_tags_w_cat(self):
		for line in open(args["category"], "r"):
			for imagePath in glob.glob(os.path.join(os.path.join(args["dataset"], line.strip()),"*.jpg")):
				imgID = imagePath[imagePath.rfind(os.sep) + 1:]
				if imgID in self.imagelist:
					print "extendinglist"
					category = LancasterStemmer().stem(line.strip())
					self.taglist[self.imagelist.index(imgID)] += " "+category
					print self.taglist[self.imagelist.index(imgID)]
				else:
					print len(self.imagelist)
					self.imagelist.append(imgID)
					self.taglist.append(line.strip())
					print len(self.imagelist)
			
        def read_test_tags(self):
                self.query_pos = dict()
                fs = open (args["test"],"r")
                pointer = 0
                line = fs.readline()
                while (line):
                        self.query_pos [line.split()[0]] = pointer
                        pointer = fs.tell()
                        line = fs.readline()
                
        def stem_word(self, line, taglist):
                tags_length = len(line)
                image_name = line[0]
                string = []
                self.imagelist.append(image_name)
                for i in range (1,tags_length):
                        try:
                                tag = LancasterStemmer().stem(line[i])
                                #tag = nltk.wordnet.WordNetLemmatizer().lemmatize(tag)
                                if (isinstance(tag, unicode)==False):
                                        tag = unicode(tag,"utf-8")
                                #print type(tag)
                                string.append(tag)
                        except UnicodeDecodeError:
                                continue
                string = " ".join(string)
                taglist.append(string)

        def storeToFile(self, filepath):
                indexfile = open(filepath, 'w')
                pickle.dump(self.imagelist,indexfile)
                pickle.dump(self.taglist, indexfile)
                if (self.query_pos):
                        pickle.dump(self.query_pos, indexfile)
                indexfile.close()

        def printToDisplay(self):
                for k in self.taglist:
                        print k, self.taglist[k]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = False, default='image'+os.sep+'data',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-t", "--tags", required = False, default='image'+os.sep+'train_text_tags.txt',
	help = "Path to where the file describing images and their list of tags are stored")
ap.add_argument("-i", "--index", required = False, default='pyimagesearch'+os.sep+'TR_index.txt',
	help = "Path to where the computed index will be stored")
ap.add_argument("-tt", "--test", required = False, default='test'+os.sep+'test_text_tags.txt',
	help = "Path to where the computed index will be stored")
ap.add_argument("-cn", "--category", required = False, default='image'+os.sep+'category_names.txt',
        help = "Path to the directory that contains the images to be indexed")

args = vars(ap.parse_args())

#printToDisplay()
