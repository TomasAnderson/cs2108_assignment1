from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

class PlotTR:

    def __init__ (self, tfidfmatrix) :
        X = tfidfmatrix.todense()
        pca = PCA(n_components=2).fit(X)
        data2D = pca.transform(X)
 
        kmeans = KMeans(n_clusters=2).fit(X)
        centers2D = pca.transform(kmeans.cluster_centers_)
        
        plt.scatter(data2D[:,0],data2D[:,1], c='b')
        plt.hold(True)
        plt.scatter(centers2D[:,0], centers2D[:,1], marker ='x', s=200, linewidths=3, c = 'r')
        plt.show()
 
