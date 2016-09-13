import argparse
import glob
import sys, string, os, platform
import subprocess
import cPickle as pickle

# open the output index file for writing
class SemanticFeatureIndex:
    
        def __init__(self, mode):
                self.datalist = open(args["datalist"], "w")
                self.index = dict()
                for line in open(args["category"], "r"):
                        # use glob to grab the image paths and loop over them
                        for imagePath in glob.glob(os.path.join(os.path.join(args["dataset"], line.strip()),"*.jpg")):
                        # extract the image ID (i.e. the unique filename) from the image
                        # path and load the image itself
                                #imageID = imagePath[imagePath.rfind("/") + 1:]
                                self.datalist.write(".." + os.sep + ".." + os.sep + imagePath + "\n")
                self.datalist.close()
                if (mode == 'consolidate'):
                     self.consolidate()
                elif (mode == 'all'):
                    self.runImageClassification()
                    self.consolidate()
                else:
                    print "incorrect argument"
                
        def runImageClassification(self):
                cwd = os.getcwd()
                os.chdir(args["programpath"])
                if (platform.system() =="Windows"):
                        runnable = args["program"] + ' "' + cwd + os.sep + args["datalist"] + '"'
                else:
                        runnable = 'wine ' + args["program"] + ' "' + cwd + os.sep + args["datalist"] + '"'
                print runnable
                os.system(runnable)
                os.chdir(os.getcwd)
                
        def consolidate(self):
                self.output = open(args["index"], "wb")
                for line in open(args["category"], "r"):
                        # use glob to grab the image paths and loop over them
                        for imagePath in glob.glob(os.path.join(os.path.join(args["dataset"], line.strip()),"*.txt")):
                            file = open(imagePath, "r")
                            for line in file:
                                values = line.split()
                                imageID = imagePath[imagePath.rfind(os.sep) + 1:].replace("txt", "jpg")
                                self.index[imageID] = [float(i) for i in values]
                pickle.dump(self.index, self.output, pickle.HIGHEST_PROTOCOL)
                self.output.close()

                

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = False, default='image'+os.sep+'data',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-cn", "--category", required = False, default='image'+os.sep+'category_names.txt',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = False, default='pyimagesearch'+os.sep+'SFProperties.txt',
	help = "Path to where the computed index will be stored")
ap.add_argument("-dl", "--datalist", required = False, default='pyimagesearch'+os.sep+'datalist.txt',
	help = "Path to where the images are stored")
ap.add_argument("-p", "--programpath", required = False, default='FeatureExtractor'+os.sep+'semanticFeature',
	help = "Path to where the image_classification.exe is stored")
ap.add_argument("-pr", "--program", required = False, default='image_classification.exe',
	help = "Path to where the image_classification.exe is stored")
ap.add_argument("-m", "--mode", required = False, default='consolidate',
	help = "'consolidate' or 'all' -(classify then consolidate)")
args = vars(ap.parse_args())

    
