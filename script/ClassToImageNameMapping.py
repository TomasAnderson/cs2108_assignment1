import os
import cPickle

TRAINING_SET_FILEPATH = '../image/data'
MAPPING_FILEPATH = 'CTNM.dat'

if os.name == 'nt':
    PATH_DELIMITER = '/'
else:
    PATH_DELIMITER = os.sep

if __name__ == '__main__':
    
    if os.path.exists(MAPPING_FILEPATH):
        print MAPPING_FILEPATH, 'already exist'
    else:
        
        print 'Mapping in process'
        
        reverseIdx = {}
        for categoryName in os.listdir(TRAINING_SET_FILEPATH):
            categoryPath = TRAINING_SET_FILEPATH + PATH_DELIMITER + categoryName
            if os.path.isdir(categoryPath):
                imageLst = []
                for imageName in os.listdir(categoryPath):
                    imageLst.append(imageName)
                reverseIdx[categoryName] = imageLst
        
        outputFile = open(MAPPING_FILEPATH, 'w')
        cPickle.dump(reverseIdx, outputFile, protocol=cPickle.HIGHEST_PROTOCOL)
        outputFile.close()
        
        print 'Mapping done'
        print 'Mapping =\n', reverseIdx