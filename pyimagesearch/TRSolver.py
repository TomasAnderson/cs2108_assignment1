
import exifread
import cPickle as pickle
import ast
import os
import nltk
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import operator
import time

class TRSolver:
    def __init__(self, queryname):
        start = time.clock()
        self.querypath = queryname
        self.indexpath = "pyimagesearch" + os.sep + "TR_Index.txt"
        self.result = dict()
        self.known_query_tags = 0
        self.computeSimMatrix()
        self.convertDictToOrderedList()
        print str(time.clock() - start)

    def extractTag(self):
        stemmer = LancasterStemmer()
        querytagfile = self.querypath.replace("jpg","txt");
        imgname = self.querypath[self.querypath.rfind(os.sep)+1:]
        query_known = self.known_query_tags.get(imgname, None)
        if (query_known != None):
            fs = open("test"+os.sep+"test_text_tags.txt","r")
            fs.seek(query_known)
            line = fs.readline().split()[1:]
            string = []
            for term in line:
                try:
                    tag = stemmer.stem(term)
                    if (isinstance(tag, unicode) == False):
                        tag = unicode(tag, "utf-8")
                    string.append(tag)
                except UnicodeDecodeError:
                    continue
            string = " ".join(string)
            self.tags = [string,]
            fs.close()
        elif (os.path.isfile(querytagfile)):
            fs = open(querytagfile,"r")
            line = fs.readline().split()
            string = []
            for term in line:
                try:
                    tag = stemmer.stem(term)
                    if (isinstance(tag, unicode) == False):
                        tag = unicode(tag, "utf-8")
                    string.append(tag)
                except UnicodeDecodeError:
                    continue
            string = " ".join(string)
            self.tags = [string,]
        else:
            img = open(self.querypath, 'rb')
            exif = exifread.process_file(img)
            keyword = ""
	    try:
               	comment = ast.literal_eval(str(eval("exif['Image XPComment']")))
                comment = comment[0:-2:2]
                comment = ''.join(chr(i) for i in comment)
                comment = comment.replace(";","")
            except KeyError:
                comment = ""
            except SyntaxError:
                print  'comment',exif['Image XPComment']
            try:
                keyword = ast.literal_eval(str(eval("exif['Image XPKeywords']")))
                keyword = keyword[0:-2:2]
                keyword = ''.join(chr(i) for i in keyword)
                keyword = keyword.replace(";","")
            except KeyError:
                keyword = ""
            except SyntaxError:
                print 'keyword', exif['Image XPKeywords']
            line = keyword + comment;
            string = []
            for term in line:
                try:
                    tag = stemmer.stem(term)
                    if (isinstance(tag, unicode) == False):
                        tag = unicode(tag, "utf-8")
                    string.append(tag)
                except UnicodeDecodeError:
                    continue
            string = " ".join(string)

            self.tags = [string,]
            print "here are the tags"
            print self.tags
            img.close()

    def computeSimMatrix(self):
        self.tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english', norm = 'l2', use_idf=True, sublinear_tf=True)
        pk_file = open(self.indexpath,'rb')
        self.imagelist = pickle.load(pk_file)
        self.tagslist = pickle.load(pk_file)
        self.known_query_tags = pickle.load(pk_file)
        self.extractTag()
        q_data =  self.tags + self.tagslist
        #print q_data
        self.tfidf_matrix = self.tf.fit_transform(q_data)
        cos_score = cosine_similarity(self.tfidf_matrix[0:1], self.tfidf_matrix)
        cos_score = cos_score[0][1:]
        self.result = dict(zip(self.imagelist, cos_score))
        #euc_score = euclidean_distances(self.tfidf_matrix[0:1], self.tfidf_matrix)
        #euc_score = euc_score[0][1:]
        #self.result = dict(zip(self.imagelist, euc_score))
        pk_file.close()
        
        
    def convertDictToOrderedList(self):
        self.result = sorted(list(self.result.items()),key=lambda x:x[1], reverse=True)

    def topK(self,K):
        list1, list2 = zip(*self.result[0:K])
        print list1
