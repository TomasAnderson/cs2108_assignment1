import argparse
import glob
import sys, string, os, platform
import cPickle as pickle
from scipy import spatial
import tensorflow as tf
import TFloadModel as tfl
import numpy as np
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
                self.extractFeatureVec(querypath)
                start = time.clock()
                self.computeSim()
                self.convertDictToOrderedList()

        def extractFeatureVec(self,querypath):
                tfl.create_graph()
                with tf.Session() as sess:
                        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
                        image_data = tf.gfile.FastGFile(querypath,'rb').read()
                        feature = sess.run(softmax_tensor,{'DecodeJpeg/contents:0':image_data})
                        self.queryvector = np.squeeze(feature)
                        
        def computeSim(self):
                for img in self.index:
                        self.result[img] = 1 - spatial.distance.cosine(self.queryvector, self.index[img])

        def convertDictToOrderedList(self):
                self.result = sorted(list(self.result.items()),key=lambda x:x[1], reverse=True)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required = False, default='pyimagesearch' + os.sep + 'i2vSFProperties.txt',
        help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())



    
