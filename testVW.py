import cv2 as cv
from pyimagesearch.VWEvaluator import FeatureEvaluator

queryFileName = './image/data/rainbow/0076_280274406.jpg'
classifierFilePath = './pyimagesearch/VWClassifier.dat'

# Using predict
print '<Using predict() with >= 0 value of k>'
fe = FeatureEvaluator(classifierFilePath)     # Loading of cached data is done in the constructor
predictions = fe.predict( queryFileName, k=10 )

if predictions is None:
    print 'Cached data was not loaded properly or image was not loaded properly'
else:
    print 'For', queryFileName + ':'
    for prediction in predictions:
        
        # the similarity value is actually euclidian distance, so the smaller the value, the greater the similarity
        # the values are NOT within 0 to 1 but vary from 0 to < int.max
        print prediction    
    print ''
    
# Using predict from Image
print '<Using predictFromImage() with >= 0 value of k>'
image = cv.imread(queryFileName)
predictions = fe.predictFromImage(image, k=10)

if predictions is None:
    print 'Cached data was not loaded properly or image was not loaded properly'
else:
    print 'For', queryFileName + ':'
    for prediction in predictions:
        
        # the similarity value is actually euclidian distance, so the smaller the value, the greater the similarity
        # these floating point values are NOT within 0 to 1 but can vary from 0 to < int.max
        print prediction
    print ''

# Using predict from Image using negative k value (It will return all similar images sorted by euclidian distance - smallest distance first)
print '<Using predictFromImage() using negative k value>'
image = cv.imread(queryFileName)
predictions = fe.predictFromImage(image, k=-1)

if predictions is None:
    print 'Cached data was not loaded properly or image was not loaded properly'
else:
    print 'For', queryFileName + ':'
    for prediction in predictions:
        
        # the similarity value is actually euclidian distance, so the smaller the value, the greater the similarity
        # these floating point values are NOT within 0 to 1 but can vary from 0 to < int.max
        print prediction
