import os
import numpy as np
import cv2 as cv
from scipy.cluster.vq import kmeans, vq
from sklearn.externals import joblib as output

if os.name == 'nt':
    PATH_DELIMITER = '/'
else:
    PATH_DELIMITER = os.sep

TRAINING_DATA_FILEPATH = '../image/data'
FEATURE_EVALUATOR_NAME = 'SIFT'
TOTAL_CLUSTER_COUNT = 500
FEATURES_INVERTED_INDEX_FILENAME = 'VWClassifier.dat'

class FeatureTrainer:
        
    def getImagePaths( self, trainFilePath ):
        
        imagePaths = []
        
        for categoryName in os.listdir(trainFilePath):
            
            categoryFilePath = trainFilePath + PATH_DELIMITER + categoryName
            
            for imageName in os.listdir(categoryFilePath):
                imagePaths.append( categoryFilePath + PATH_DELIMITER + imageName )
            
        return imagePaths

    def getDescriptors( self, imagePaths ):
        
        detector = cv.FeatureDetector_create(FEATURE_EVALUATOR_NAME)
        extractor = cv.DescriptorExtractor_create(FEATURE_EVALUATOR_NAME)
        descriptors = []
        
        for imagePath in imagePaths:
            image = cv.imread(imagePath)
            keypoints = detector.detect(image)
            keypoints, descriptor = extractor.compute( image, keypoints )
            descriptors.append(descriptor)
            
        return descriptors

    def getInvertedIndex( self, descriptors ):
        
        if len(descriptors) <= 0:
            return None
        
        stackedDescriptors = descriptors[0]
        for i in range(1, len(descriptors)):
            stackedDescriptors = np.vstack((stackedDescriptors, descriptors[i]))
            
        wordBook, var = kmeans( stackedDescriptors, TOTAL_CLUSTER_COUNT )
        
        imageCount = len(descriptors)
        histograms = np.zeros( (imageCount, len(wordBook)), dtype=np.int32 )
        invertedIndex = {}
        
        for i in range(imageCount):
            words, dist = vq(descriptors[i], wordBook)
            for word in words:
                lst = invertedIndex.get(word)
                if lst is None:
                    lst = []
                    invertedIndex[word] = lst
                lst.append(i)
                histograms[i, word] += 1
                
        return invertedIndex, wordBook, histograms

    def saveState( self, savedStateFileName, imagePaths, invertedIndex, wordBook, histograms ):
        return output.dump( (imagePaths, invertedIndex, wordBook, histograms, FEATURE_EVALUATOR_NAME), savedStateFileName, compress=1 ) is not None

    def train( self, trainFilePath, classifierOutputFilePath ):
        
        print 'Getting image paths'
        
        imagePaths = self.getImagePaths( trainFilePath )
        
        if imagePaths is None or len(imagePaths) <= 0:
            return False
        
        print 'Getting descriptors'
        
        descriptors = self.getDescriptors(imagePaths)
        
        if descriptors is None:
            return False
        
        print 'Constructing inverted index'
        
        invertedIndex, wordBook, histograms = self.getInvertedIndex(descriptors)
    
        if invertedIndex is None or histograms is None:
            return False
    
        print 'Saving state'
    
        if self.saveState(classifierOutputFilePath, imagePaths, invertedIndex, wordBook, histograms) is False:
            return False
        
        print 'Successfully cached database images\' features'
        
        return True

    # Used for debug
    def visualiseKeypointsSIFT( self, fileName ):
        
        greyImg = cv.imread( fileName, cv.CV_LOAD_IMAGE_GRAYSCALE )
        
        if greyImg is not None:
            
            detector = cv.FeatureDetector_create('SIFT')
            extractor = cv.DescriptorExtractor_create('SIFT')
            keypoints = detector.detect(greyImg)
            keypoints, descriptor = extractor.compute( greyImg, keypoints )
            displayImg = cv.drawKeypoints(greyImg, keypoints)
            cv.imshow('SIFT', displayImg)
    
    def visualiseKeypointsSURF( self, fileName ):
        
        greyImg = cv.imread( fileName, cv.CV_LOAD_IMAGE_GRAYSCALE )
        
        if greyImg is not None:
            
            detector = cv.FeatureDetector_create('SURF')
            extractor = cv.DescriptorExtractor_create('SURF')
            keypoints = detector.detect(greyImg)
            keypoints, descriptor = extractor.compute( greyImg, keypoints )
            displayImg = cv.drawKeypoints(greyImg, keypoints)
            cv.imshow('SURF', displayImg)
            
    def visualiseKeypointsORB( self, fileName ):
        
        greyImg = cv.imread( fileName, cv.CV_LOAD_IMAGE_GRAYSCALE )
        
        if greyImg is not None:
            
            detector = cv.FeatureDetector_create('ORB')
            extractor = cv.DescriptorExtractor_create('ORB')
            keypoints = detector.detect(greyImg)
            keypoints, descriptor = extractor.compute( greyImg, keypoints )
            displayImg = cv.drawKeypoints(greyImg, keypoints)
            cv.imshow('ORB', displayImg)
    
#main
#ft = FeatureTrainer()
#ft.train(TRAINING_DATA_FILEPATH, FEATURES_INVERTED_INDEX_FILENAME)