import pyimagesearch.TRIndexer as TR
import pyimagesearch.TRSolver as TRS
import os
import pyimagesearch.SFIndexer as SF
import pyimagesearch.SFSolver as SFS
import cProfile
import time

#TR.TagIndex()
#TR_Result = TRS.TRSolver("test\\data\\train\\0253_421644823.jpg")
#cProfile.run("TRS.TRSolver('test'+os.sep+'data'+os.sep+'train'+os.sep+'0253_421644823.jpg')")
#print TR_Result.result


#all = image_classify then consolidate
#SF.SemanticFeatureIndex("consolidate")
#SF.SemanticFeatureIndex("all")
x = SFS.SemanticFeatureSolver(".." + os.sep+".." + os.sep + "queryimage.jpg")
#cProfile.run('SFS.SemanticFeatureSolver(".." + os.sep+".." + os.sep + "queryimage.jpg")')
#print x.result
