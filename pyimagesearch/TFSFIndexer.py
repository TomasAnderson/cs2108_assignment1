import argparse
import glob
import sys, string, os, platform
import cPickle as pickle
import TFloadModel as tfl
import tensorflow as tf
import numpy as np

# open the output index file for writing
class SemanticFeatureIndex:
    
        def __init__(self,):
                self.index = dict()
		tfl.create_graph()
		self.extractFeatureVec()
		self.storeToFile()            
        def extractFeatureVec(self):
		with tf.Session() as sess:
			softmax_tensor= sess.graph.get_tensor_by_name('softmax:0')	
                	for line in open(args["category"], "r"):
                        	# use glob to grab the image paths and loop over them
                        	for imagePath in glob.glob(os.path.join(os.path.join(args["dataset"], line.strip()),"*.jpg")):
                                	imgID = imagePath[imagePath.rfind(os.sep) + 1:]
                                	print imgID
                                	image_data = tf.gfile.FastGFile(imagePath,'rb').read()
                                	feature = sess.run(softmax_tensor, {'DecodeJpeg/contents:0':image_data})
					feature = np.squeeze(feature)
                                	self.index[imgID]=feature
                                	print feature

        def storeToFile(self):
                output = open(args["index"], "wb")
                pickle.dump(self.index, output, pickle.HIGHEST_PROTOCOL)
                output.close()
                

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = False, default='image'+os.sep+'data',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-cn", "--category", required = False, default='image'+os.sep+'category_names.txt',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = False, default='pyimagesearch'+os.sep+'i2vSFProperties.txt',
	help = "Path to where the computed index will be stored")

args = vars(ap.parse_args())

    
