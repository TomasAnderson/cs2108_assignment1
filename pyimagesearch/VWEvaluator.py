import os
from os.path import basename
from sets import Set
import numpy as np
import cv2 as cv
from scipy.cluster.vq import vq
from sklearn.externals import joblib as input

if os.name == 'nt':
    PATH_DELIMITER = '/'
else:
    PATH_DELIMITER = os.sep

class FeatureEvaluator:
    
    def __init__(self, classifierFilePath):
        self.databaseImagePaths, self.invertedIndex, self.wordBook, self.histograms, self.featureEvaluatorName = self.loadState( classifierFilePath )

    def loadState( self, savedStateFileName ):
        return input.load(savedStateFileName)

    def getImagePaths( self, testFilePath ):
        
        imagePaths = []
        
        for categoryName in os.listdir(testFilePath):
            
            categoryFilePath = testFilePath + PATH_DELIMITER + categoryName
            
            for imageName in os.listdir(categoryFilePath):
                imagePaths.append( categoryFilePath + PATH_DELIMITER + imageName )
            
        return imagePaths

    def getDescriptorFromImg( self, image, detector, extractor ):
        
        keypoints = detector.detect(image)
        keypoints, descriptor = extractor.compute( image, keypoints )
        return descriptor

    def getDescriptor( self, imagePath, detector, extractor ):
        
        image = cv.imread(imagePath)
        keypoints = detector.detect(image)
        keypoints, descriptor = extractor.compute( image, keypoints )
        return descriptor

    def getRelevantImgs( self, descriptor, invertedIndex, wordBook, histograms, databaseImagePaths ):
    
        histogram = np.zeros( len(wordBook), dtype=np.int32 )
        imgsToMatch = []
        imgsAdded = Set()
        
        words, dist = vq(descriptor, wordBook)
        for word in words:
            histogram[word] += 1
            relevantImgs = invertedIndex[word]
            if relevantImgs is not None:
                for relevantImg in relevantImgs:
                    if relevantImg not in imgsAdded:
                        imgsToMatch.append(relevantImg)
                        imgsAdded.add(relevantImg)
        
        relevantIndex = []
        
        for imgToMatch in imgsToMatch:
            histogramToMatch = histograms[imgToMatch]
            dist = np.sqrt( sum( (histogram - histogramToMatch)**2 ) )
            relevantIndex.append( (basename(databaseImagePaths[imgToMatch]), dist) )
            
        relevantIndex = sorted( relevantIndex, key=lambda idx: idx[1])
            
        return relevantIndex

    def predict( self, fileName, k ):
        
        if  fileName is None or self.databaseImagePaths is None or self.invertedIndex is None \
            or self.wordBook is None or self.histograms is None or self.featureEvaluatorName is None:
            return None
        
        detector = cv.FeatureDetector_create(self.featureEvaluatorName)
        extractor = cv.DescriptorExtractor_create(self.featureEvaluatorName)
        descriptor = self.getDescriptor( fileName, detector, extractor )
        
        if descriptor is None:
            return None
        
        relevantImgs = self.getRelevantImgs( descriptor, self.invertedIndex, self.wordBook, self.histograms, self.databaseImagePaths )
        
        if relevantImgs is None:
            return None
       
        if k >= 0:
            kRelevantImgs = []
            k = min( k, len(relevantImgs) )
            for i in range(k):
                kRelevantImgs.append(relevantImgs[i])
            return kRelevantImgs
        else:
            return relevantImgs 
    
    def predictFromImage( self, image, k ):
        
        if  image is None or self.databaseImagePaths is None or self.invertedIndex is None \
            or self.wordBook is None or self.histograms is None or self.featureEvaluatorName is None:
            return None
        
        detector = cv.FeatureDetector_create(self.featureEvaluatorName)
        extractor = cv.DescriptorExtractor_create(self.featureEvaluatorName)
        descriptor = self.getDescriptorFromImg(image, detector, extractor)
        
        if descriptor is None:
            return None
        
        relevantImgs = self.getRelevantImgs( descriptor, self.invertedIndex, self.wordBook, self.histograms, self.databaseImagePaths )
        
        if relevantImgs is None:
            return None
        
        if k >= 0:
            kRelevantImgs = []
            k = min( k, len(relevantImgs) )
            for i in range(k):
                kRelevantImgs.append(relevantImgs[i])
            return kRelevantImgs
        else:
            return relevantImgs
