
import exifread
import cPickle as pickle
import ast
import os
import nltk
import operator

class TRSolver:
    def __init__(self, queryname):
        self.querypath = queryname
        self.indexpath = "pyimagesearch" + os.sep + "TR_Index.txt"
        self.result = dict()
        self.extractTag()
        self.lookupIndex()
        self.convertDictToOrderedList()

    def extractTag(self):
        img = open(self.querypath, 'rb')
        exif = exifread.process_file(img)
        try:
            comment = ast.literal_eval(str(eval("exif['Image XPComment']")))
            comment = comment[0:-2:2]
            comment = ''.join(chr(i) for i in comment)
            comment = comment.split()
        except KeyError:
            comment = []
        except SyntaxError:
            print  'comment',exif['Image XPComment']
        try:
            keyword = ast.literal_eval(str(eval("exif['Image XPKeywords']")))
            keyword = keyword[0:-2:2]
            keyword = ''.join(chr(i) for i in keyword)
            keyword = keyword.split(';')
        except KeyError:
            keyword = []
        except SyntaxError:
            print 'keyword', exif['Image XPKeywords']
        self.tags = keyword + comment

    def lookupIndex(self):
        pk_file = open(self.indexpath,'rb')
        self.imagetagcnt = pickle.load(pk_file)
        index_dict = pickle.load(pk_file)
        #for k in index_dict:
        #    print k, index_dict[k]
        '''
        for each tag in query, check index, get whole list of corresponding images
        '''
        stemmer = nltk.LancasterStemmer()
        self.query_length = len(self.tags)
        for tag in self.tags:
            tag = stemmer.stem(tag.lower())
            tag_index_list = index_dict.get(tag, None)
            if (tag_index_list):
                for image in tag_index_list:
                    self.addToSim(image)

    def addToSim(self, image):
        no_of_tags = self.imagetagcnt[image]
        self.result[image] = self.result.setdefault(image, 0.0) + ((1.0/no_of_tags) * (1.0/self.query_length))

    def convertDictToOrderedList(self):
        self.result = sorted(list(self.result.items()),key=lambda x:x[1], reverse=True)
        
