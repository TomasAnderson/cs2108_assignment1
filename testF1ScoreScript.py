from F1ScoreScript import F1Calculator

if __name__ == '__main__':
    
    F1C = F1Calculator()
    imageName = 'image/dataset/0001_389068663.jpg'
    imageNames = [ imageName, 'image/dataset/0001_352403456.jpg' ]
    
    # For one image and do not save f1 score to any file
    f1Score = F1C.getF1Score(imageName, None)
    print '< For one image and do not save f1 score to any file >'
    print imageName, f1Score
    print ''
    
    # For many images and and do not save f1 scores to any file
    f1Scores = F1C.getF1Scores(imageNames, None)
    print '< For many images and and do not save f1 scores to any file >'
    for i in range( len(imageNames) ):
        print imageNames[i], f1Scores[i]
    print ''
    
    # Format of outputfile (look out for -1 f1score because it means an error occurred)
    # imageName1.jpg f1score1
    # imageName2.jpg f1score2
    
    # For one image and save f1 score to a file
    f1Score = F1C.getF1Score(imageName, 'singleF1Score.txt')
    print '< For one image and save f1 score to a file >'
    print imageName, f1Score
    print ''
    
    # For many images and and save f1 scores to a file
    f1Scores = F1C.getF1Scores(imageNames, 'manyF1Scores.txt')
    print '< For many images and and do not save f1 scores to any file >'
    for i in range( len(imageNames) ):
        print imageNames[i], f1Scores[i]
    
    