import argparse
import glob
import sys, string, os, platform
import subprocess
import cPickle as pickle
from scipy import spatial
import time

# open the output index file for writing
class SemanticFeatureSolver:
    
        def __init__(self, querypath):
                #load in semanticProperties Index
                self.index = dict()
                indexfile = open(args["index"], "rb")
                start = time.clock()
                self.index = pickle.load(indexfile)
                indexfile.close()
                print str(time.clock() - start)
                self.result = dict()
                self.runImageClassification(querypath)
                start = time.clock()
                self.computeSim(querypath)
                self.convertDictToOrderedList()
                
        def runImageClassification(self,querypath):
                cwd = os.getcwd()
                filename = "pyimagesearch"+os.sep+"SFquerypath.txt"
                querypathdoc = open(filename, "w")
                querypathdoc.write(querypath)
                querypathdoc.close()
                os.chdir(args["programpath"])
                #print cwd
                if (platform.system() == "windows"):
                        runnable = args["program"] + ' "' + cwd + os.sep + filename +'"'
                else:
                        runnable = 'wine ' + args["program"] + ' "' + cwd + os.sep + filename +'"'
                #print runnable
                os.system(runnable)
                os.chdir(cwd)

        def computeSim(self, querypath):
                querypath = querypath[querypath.rfind(os.sep) + 1 ::1].replace("jpg","txt")
                self.queryvector = open(querypath, "r").readline().split()
                self.queryvector = [float(i) for i in self.queryvector]
                for img in self.index:
                        self.result[img] = 1 - spatial.distance.cosine(self.queryvector, self.index[img])

        def convertDictToOrderedList(self):
                self.result = sorted(list(self.result.items()),key=lambda x:x[1], reverse=True)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = False, default='pyimagesearch' + os.sep + 'SFProperties.txt',
	help = "Path to where the computed index will be stored")
ap.add_argument("-p", "--programpath", required = False, default='FeatureExtractor'+os.sep+'semanticFeature',
	help = "Path to where the image_classification.exe is stored")
ap.add_argument("-pr", "--program", required = False, default='image_classification.exe',
	help = "Path to where the image_classification.exe is stored")
args = vars(ap.parse_args())



    
