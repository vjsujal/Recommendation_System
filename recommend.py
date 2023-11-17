import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
from numpy.linalg import norm
import os
import numpy as np
import pandas as pd
from IPython.display import Image
from IPython.core.display import HTML
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

products = pd.read_csv('styles.csv', on_bad_lines="skip")
url=pd.read_csv('images.csv', on_bad_lines="skip")


def txt_train(test_text):
    new_products = products[['id','productDisplayName','usage','season']]
    new_products.dropna(inplace=True)
    new_products['merged']=new_products['productDisplayName']+' '+new_products['usage']+ ' '+new_products['season']
    vectorizer = TfidfVectorizer(ngram_range=(1,2))

    tfidf = vectorizer.fit_transform(new_products["merged"])
    title=test_text
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -100)[-100:]
    text_results = new_products.iloc[indices].iloc[::-1]
    txt_result_id=[]
    for i in text_results['id']:
        txt_result_id.append(str(i).strip()+'.jpg')
    lst=[]
    for i in range(5):
        lst.append(products[products['id']==int(txt_result_id[i].replace('.jpg',''))]['productDisplayName'].values[0])
        # display(Image(url=url[url['filename']==txt_result_id[i]]['link'].values[0], width=150, height=150))
    return lst
    

