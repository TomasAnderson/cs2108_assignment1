import os
import cPickle

TRAINING_SET_FILEPATH = 'image/data'
MAPPING_FILEPATH = 'ITCM.dat'

if os.name == 'nt':
    PATH_DELIMITER = '/'
else:
    PATH_DELIMITER = os.sep

if __name__ == '__main__':
    
    mapping = {}
    
    print 'Initiate mapping process'
    
    for categoryName in os.listdir(TRAINING_SET_FILEPATH):
        categoryPath = TRAINING_SET_FILEPATH + PATH_DELIMITER + categoryName
        for imageName in os.listdir(categoryPath):
            categoryLst = mapping.get(imageName)
            if categoryLst is None:
                categoryLst = []
                mapping[imageName] = categoryLst
            else:
                print 'There is multiple category =', imageName
            categoryLst.append(categoryName)
    
    #mapping = cPickle.load('ITCM.dat')
    
    outputFile = open(MAPPING_FILEPATH, 'w')
    cPickle.dump(mapping, outputFile, protocol=cPickle.HIGHEST_PROTOCOL)
    outputFile.close()
    
    print 'Mapping process completed'
    
    print 'mapping =\n', mapping 