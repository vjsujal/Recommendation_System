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
import random


products = pd.read_csv('data/finaldata.csv', on_bad_lines="skip")
url=pd.read_csv('data/finaldata.csv', on_bad_lines="skip")

def get_random():
    lst=[]
    index_lst=[]
    for i in range(9):
        lst.append(random.randint(0,products.shape[0]))
    for i in lst:
        index_lst.append(products.iloc[i]['id'])
    return index_lst

def get_info_home(item_id):
    lst={
        'id': item_id,
        'name': products[products['id']==item_id]['productDisplayName'].values[0],
        # 'category': products[products['id']==item_id]['subCategory'].values[0],
        'url': url[url['filename']==str(item_id).strip()+'.jpg']['link'].values[0]
    }
    return lst

def get_info(item_id):
    lst={
        'id': item_id,
        'name': products[products['id']==item_id]['productDisplayName'].values[0],
        'url': url[url['filename']==str(item_id).strip()+'.jpg']['link'].values[0]
    }
    return lst

def txt_train(test_text):
    new_products = products[['id','productDisplayName']]
    new_products.dropna(inplace=True)
    new_products['merged']=new_products['productDisplayName']
    vectorizer = TfidfVectorizer(ngram_range=(1,2))

    tfidf = vectorizer.fit_transform(new_products["merged"])
    title=test_text
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argsort(similarity)[-5:][::-1]
    text_results = new_products.iloc[indices]
    name_id=list(text_results['id'])
    lst1=[]
    for i in name_id:
        lst=[]
        lst.append(i)
        lst.append(products[products['id']==i]['productDisplayName'].values[0])
        lst.append(url[url['filename']==str(i).strip()+'.jpg']['link'].values[0])
        lst1.append(lst)
    return lst1[::-1]
    
def image_test(test_image):
    feature_list = np.array(pickle.load(open('data/embeddings.pkl','rb')))
    filenames = pickle.load(open('data/filenames.pkl','rb'))

    model = ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
    model.trainable = False

    model = tensorflow.keras.Sequential([
        model,
        GlobalMaxPooling2D()
    ])
    img = image.load_img(test_image,target_size=(224,224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    neighbors = NearestNeighbors(n_neighbors=6,algorithm='brute',metric='euclidean')
    neighbors.fit(feature_list)

    distances,indices = neighbors.kneighbors([normalized_result])
    name_id=[]
    for i in indices[0]:
       name_id.append(filenames[i].split('/')[1].replace('.jpg',''))
    lst1=[]
    for i in name_id:
        lst=[]
        lst.append(i)
        lst.append(products[products['id']==int(i)]['productDisplayName'].values[0])
        lst.append(url[url['filename']==str(i).strip()+'.jpg']['link'].values[0])
        lst1.append(lst)
    return lst1
    
def txt_image_test(test_text,test_image):
    lst1=txt_train(test_text)
    lst2=image_test(test_image)
    return lst1[:3]+lst2[:2]

print(get_random())