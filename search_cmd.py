from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.VWEvaluator import FeatureEvaluator
import pyimagesearch.TRSolver as TRS
from pyimagesearch.colorHistogramSearcher import colorHistogramSearcher
import pyimagesearch.TFSFSolver as TFSFS

import cv2 as cv

import operator
import os
import cPickle
import sys

class Search_cmd:
    
    def search(self, fileName):
        
        query = cv.imread(fileName)
        
        #Added check for file exist
        if query is None:
            return []
        
        cd = ColorDescriptor((8, 12, 3))
        classifierFilePath = './pyimagesearch/VWClassifier.dat'
        fe = FeatureEvaluator(classifierFilePath)
        
        self.queryfeatures = cd.describe(query)
        self.vmfeatures = fe.predictFromImage(query, k=-1)
        self.trfeatures = TRS.TRSolver(fileName).result
        self.sffeatures = TFSFS.SemanticFeatureSolver(fileName).result

        colorSearcher = colorHistogramSearcher("index.csv")
        colorResults = colorSearcher.search(self.queryfeatures)
        color_max = max(score for (score, resultID) in colorResults)
        chResults = [(1-t[0]*(1/color_max), t[1]) for t in colorResults]
        
        # perform VW search
        vm_max = max(score for (resultID, score) in self.vmfeatures)
        vmResults = [(1-t[1]*(1/vm_max), t[0]) for t in self.vmfeatures]

        # perform TR search
        tr_max = max(score for (resultID, score) in self.trfeatures)
        trResults = [(t[1], t[0]) for t in self.trfeatures]

        # perform SF search
        sfResults = [(t[1], t[0]) for t in self.sffeatures]
        
        #TODO: join results (top 16)

        image_dict = {}
        sf_weight = 0.6
        vm_weight = 0.2
        ch_weight = 0.1
        tr_weight = 0.1
        for (score, resultID) in sfResults:
            image_dict[resultID] = score*sf_weight

        for (score, resultID) in vmResults:
            if resultID in image_dict:
                image_dict[resultID] = image_dict[resultID] + score*vm_weight
            else:
                image_dict[resultID] = score*vm_weight

        for (score, resultID) in chResults:
            if resultID in image_dict:
                image_dict[resultID] = image_dict[resultID] + score*ch_weight
            else:
                image_dict[resultID] = score*ch_weight

        for (score, resultID) in trResults:
            if resultID in image_dict:
                image_dict[resultID] = image_dict[resultID] + score*tr_weight
            else:
                image_dict[resultID] = score*tr_weight

        k = 16
        image_list = sorted(image_dict.items(), key=operator.itemgetter(1), reverse=True)[:k]
        result = [resultID for (resultID, score) in image_list]
        return result

