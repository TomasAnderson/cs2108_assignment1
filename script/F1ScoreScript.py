import os
import cPickle
from sets import Set
#from search_cmd import Search_cmd

NAME_TO_CLASS_MAPPING_FILEPATH = 'ITCM.dat' # Change the file path if you change the location of ITCM.dat 
CLASS_TO_NAME_MAPPING_FILEPATH = 'CTNM.dat' # Change the file path if you change the location of CTNM.dat 

class F1Calculator:
    
    def __init__(self):
        
        # Load name to class mapping (hashmap of lists)
        if os.path.exists(NAME_TO_CLASS_MAPPING_FILEPATH):
            nameToClassMappingFile = open(NAME_TO_CLASS_MAPPING_FILEPATH, 'rb')
            self.nameToClassMapping = cPickle.Unpickler(nameToClassMappingFile).load()
            nameToClassMappingFile.close()
        else:
            print NAME_TO_CLASS_MAPPING_FILEPATH, 'does not exist'
            
        # Load class to name mapping (hashmap of lists)
        if os.path.exists(CLASS_TO_NAME_MAPPING_FILEPATH):
            classToNameMappingFile = open(CLASS_TO_NAME_MAPPING_FILEPATH, 'rb')
            self.classToNameMapping = cPickle.Unpickler(classToNameMappingFile).load()
            classToNameMappingFile.close()
        else:
            print CLASS_TO_NAME_MAPPING_FILEPATH, 'does not exist'
            
        # Load search cmd instance
        #self.evaluator = Search_cmd()
        
    # relevantImgs is a set while retrievedImgs is a list
    def calculatePrecision(self, relevantImgs, retrievedImgs):
        
        retrievedCount = len(retrievedImgs)
        if retrievedCount <= 0:
            return 0
        
        relevantRetrievedCount = 0
        for retrievedImg in retrievedImgs:
            if retrievedImg in relevantImgs:
                relevantRetrievedCount += 1
                
        return relevantRetrievedCount/float(retrievedCount)
        
    # relevantImgs is a set while retrievedImgs is a list
    def calculateRecall(self, relevantImgs, retrievedImgs):
        
        relevantCount = len(relevantImgs)
        if relevantCount <= 0:
            return 0
        
        relevantRetrievedCount = 0
        for retrievedImg in retrievedImgs:
            if retrievedImg in relevantImgs:
                relevantRetrievedCount += 1
                
        return relevantRetrievedCount/float(relevantCount)
        
    # Assumes retrievedImgs is a list
    # Returns a hashset of relevant images
    def getRelevantImgs(self, imageName):
        
        relevantImgs = Set()
        
        if imageName is None:
            return relevantImgs
        
        classLst = self.nameToClassMapping.get(imageName)
        if classLst is None:
            return relevantImgs
        
        for cls in classLst:
            nameLst = self.classToNameMapping.get(cls)
            if nameLst is not None:
                for name in nameLst:
                    relevantImgs.add(name)
                    
        return relevantImgs
    
    # If returned value is -1, loading of mappings is not successful or imageNames is None or the retrievedImgs is None
    def getF1Score(self, imageName, outputFileName):
        
        if imageName is None or self.classToNameMapping is None or self.nameToClassMapping is None:
            return -1
        
        retrievedImgs = self.evaluator.search(imageName)
        
        if retrievedImgs is None:
            return -1
        
        relevantImgs = self.getRelevantImgs(imageName, retrievedImgs)
        
        recall = self.calculateRecall(relevantImgs, retrievedImgs)
        precision = self.calculatePrecision(relevantImgs, retrievedImgs)
        denom = recall + precision
        f1Score = 0
        
        if denom > 0:
            f1Score = 2 * ((recall*precision)/denom)
            
        if outputFileName is not None:
            outputFile = open(outputFileName, 'w')
            outputFile.write( imageName + ' ' + f1Score )
            outputFile.close()
            
        return f1Score
        
    # Assumes imageNames is a list
    # Returns a list of f1 scores in the same order as imageNames
    def getF1Scores(self, imageNames, outputFileName):
        
        f1Scores = []
        if imageNames is not None:
            for imageName in imageNames:
                f1Scores.append(self.getF1Score(imageName, None))
                
        if outputFileName is not None:
            outputFile = open(outputFileName, 'w')
            for f1Score in f1Scores:
                outputFile.write( imageName + ' ' + f1Score + '\n' )
            outputFile.close()
                
        return f1Scores