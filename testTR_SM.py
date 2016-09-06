import pyimagesearch.TRIndexer as TR
import pyimagesearch.TRSolver as TRS
import os
import pyimagesearch.SFIndexer as SF
import pyimagesearch.SFSolver as SFS

#TR.TagIndex()
#TR_Result = TRS.TRSolver("queryimage.jpg")
#print TR_Result.result

#all = image_classify then consolidate
SF.SemanticFeatureIndex("consolidate")
#SF.SemanticFeatureIndex("all")
x = SFS.SemanticFeatureSolver(".." + os.sep+".." + os.sep + "queryimage.jpg")
print x.result
