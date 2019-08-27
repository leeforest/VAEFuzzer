#-*-coding:utf-8-*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import get_distribution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# The usual creation of arrays produces wrong format (as cosine_similarity works on matrices)
#x = np.array([2,3,1,0])
#y = np.array([2,3,0,0])

x = np.array(['a','b','c','d'])
y = np.array(['c','a','a','d'])

print x.shape

# Need to reshape these
x = x.reshape(1,-1)
y = y.reshape(1,-1)

# Or just create as a single row matrix
z = np.array([[1,1,1,1]])

print x.shape

# Now we can compute similarities
cosine_similarity(x,y) # = array([[ 0.96362411]]), most similar
cosine_similarity(x,z) # = array([[ 0.80178373]]), next most similar
cosine_similarity(y,z) # = array([[ 0.69337525]]), least similar
