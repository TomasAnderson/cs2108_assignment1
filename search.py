# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.VWEvaluator import FeatureEvaluator
import pyimagesearch.TRSolver as TRS
from pyimagesearch.colorHistogramSearcher import colorHistogramSearcher
import pyimagesearch.TFSFSolver as TFSFS

import cv2 as cv
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk

import operator
import os
import cPickle

class UI_class:
    def __init__(self, master, search_path):
        self.search_path = search_path
        self.master = master
        topframe = Frame(self.master)
        topframe.pack()

        #Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton= Button(topframe, text=" Choose an image ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ", command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=2)
        downspace = Label(topframe).grid(row=3, columnspan=4)

        self.master.mainloop()


    def browse_query_img(self):

        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(title='Choose an Image File').name

        # process query image to feature vector
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))
        classifierFilePath = './pyimagesearch/VWClassifier.dat'
        fe = FeatureEvaluator(classifierFilePath) 

        # load the query image and describe it
        query = cv.imread(self.filename)
        self.queryfeatures = cd.describe(query)
        # print len(self.queryfeatures) = 1440
        self.vmfeatures = fe.predictFromImage(query, k=1469)
        self.trfeatures = TRS.TRSolver(self.filename).result
        self.sffeatures = TFSFS.SemanticFeatureSolver(self.filename).result

        # show query image
        image_file = Image.open(self.filename)
        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(resized)
        image_label = Label(self.query_img_frame, image=im)
        image_label.pack()

        self.query_img_frame.mainloop()


    def show_results_imgs(self):
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()

        # perform color search
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
        
        # check if SF feature is showing a dominant class
        mappingFile = open('ITCM.dat', 'rb')
        mapping = cPickle.load(mappingFile)
        category_count = {}
        for (result, score) in image_list:
            categories = mapping[resultID]
            for category in categories:
                if resultID in category_count:
                    category_count[category] += 1
                else:
                    category_count[category] = 1
        category_c_list = sorted(category_count.items(), key=operator.itemgetter(1), reverse=True)
        if category_c_list[0] > 10:
            image_list = [(t[1],t[0]) for t in sfResults[:k]]


        # show result pictures
        COLUMNS = 5
        image_count = 0
        for (resultID, score) in image_list:
            # load the result image and display it
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)
            im = Image.open( self.search_path + os.sep + resultID)
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.result_img_frame, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=r, column=c)

        self.result_img_frame.mainloop()


root = Tk()
window = UI_class(root,'./image/dataset')
