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
        self.vmfeatures = fe.predictFromImage(query, k=10)
        self.trfeatures = TRS.TRSolver(self.filename).result[0: 10]
        self.sffeatures = TFSFS.SemanticFeatureSolver(self.filename).result[0:10]

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
        
        # perform VW search
        vmResults = [(t[1], t[0]) for t in self.vmfeatures]

        # perform TR search
        trResults = [(t[1], t[0]) for t in self.trfeatures]

        # perform SF search
        sfResults = [(t[1], t[0]) for t in self.sffeatures]
        
        #TODO: join Rresults
        image_list = []
        for (score, resultID) in sfResults[:5]:
            if resultID not in image_list:
                image_list.append(resultID)

        for (score, resultID) in vmResults[:5]:
            if resultID not in image_list:
                image_list.append(resultID)

        for (score, resultID) in colorResults[:3]:
            if resultID not in image_list:
                image_list.append(resultID)

        for (score, resultID) in trResults[:3]:
            if resultID not in image_list:
                image_list.append(resultID)


        # show result pictures
        COLUMNS = 5
        image_count = 0
        for resultID in image_list:
            # load the result image and display it
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)
            im = Image.open( self.search_path + "/" + resultID)
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.result_img_frame, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=r, column=c)

        self.result_img_frame.mainloop()


root = Tk()
window = UI_class(root,'./image/dataset/')
