import google.generativeai as palm
import re
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

palm.configure(api_key="AIzaSyCVeFW87-H5c32e4i0E8KRJ7jgnDOR5lIY")

products = pd.read_csv('data/test.csv', on_bad_lines="skip")
url=pd.read_csv('data/test.csv', on_bad_lines="skip")
final=pd.read_csv('data/imagedata.csv', on_bad_lines="skip")

def get_random():
    lst=[]
    index_lst=[]
    for i in range(9):
        lst.append(random.randint(0,products.shape[0]))
    for i in lst:
        index_lst.append(products.iloc[i]['id'])
    return index_lst

# def get_info_home(item_id):
#     lst={
#         'id': item_id,
#         'name': products[products['id']==item_id]['productDisplayName'].values[0],
#         'url': url[url['filename']==str(item_id).strip()+'.jpg']['link'].values[0],
#     }
#     return lst

def get_info(item_id):
    try:
        lst={
            'id': item_id,
            'name': products[products['id']==item_id]['productDisplayName'].values[0],
            'url': url[url['filename']==str(item_id).strip()+'.jpg']['link'].values[0],
            'price': int(products[products['id']==item_id]['price'].values[0]),
            'og_price': int(products[products['id']==item_id]['ogprice'].values[0]),
            'discount': int(products[products['id']==item_id]['discount'].values[0])
        }
        return lst
    except IndexError:
        lst={
            'id': item_id,
            'name': final[final['id']==item_id]['productDisplayName'].values[0],
            'url': final[final['filename']==str(item_id).strip()+'.jpg']['link'].values[0],
            'price': int(final[final['id']==item_id]['price'].values[0]),
            'og_price': int(final[final['id']==item_id]['ogprice'].values[0]),
            'discount': int(final[final['id']==item_id]['discount'].values[0])
        }
        return lst

def txt_train(test_text):
    new_products = products[['id','productDisplayName']]
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(new_products["productDisplayName"])
    title=test_text
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argsort(similarity)[-20:][::-1]
    text_results = new_products.iloc[indices]
    name_id=list(text_results['id'])
    lst1=[]
    for i in name_id:
        lst=[]
        lst.append(i)
        lst.append(products[products['id']==i]['productDisplayName'].values[0])
        lst.append(url[url['filename']==str(i).strip()+'.jpg']['link'].values[0])
        lst.append(int(products[products['id']==i]['price'].values[0]))
        lst.append(int(products[products['id']==i]['ogprice'].values[0]))
        lst.append(int(products[products['id']==i]['discount'].values[0]))
        lst1.append(lst)
    return lst1

def txt_train_price(test_text):
    new_products = products[['id','productDisplayName']]
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(new_products["productDisplayName"])
    title=test_text
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argsort(similarity)[-100:][::-1]
    text_results = new_products.iloc[indices]
    name_id=list(text_results['id'])
    lst1=[]
    for i in name_id:
        lst=[]
        lst.append(i)
        lst.append(products[products['id']==i]['productDisplayName'].values[0])
        lst.append(url[url['filename']==str(i).strip()+'.jpg']['link'].values[0])
        lst.append(int(products[products['id']==i]['price'].values[0]))
        lst.append(int(products[products['id']==i]['ogprice'].values[0]))
        lst.append(int(products[products['id']==i]['discount'].values[0]))
        lst1.append(lst)
    return lst1

    
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
        lst.append(final[final['id']==int(i)]['productDisplayName'].values[0])
        lst.append(final[final['filename']==str(i).strip()+'.jpg']['link'].values[0])
        lst.append(int(final[final['id']==int(i)]['price'].values[0]))
        lst.append(int(final[final['id']==int(i)]['ogprice'].values[0]))
        lst.append(int(final[final['id']==int(i)]['discount'].values[0]))
        
        lst1.append(lst)
    return lst1
    
def txt_image_test(test_text,test_image):
    lst1=txt_train(test_text)
    lst2=image_test(test_image)
    return lst1[:3]+lst2[:2]



def prompt_helper(prompt):

    pre_prompt = "you are a person which classify the input of user into 6 catagories  \
    After categorization you should return a key-value pair json according to catagories and their answer\
    In category 1 it will identify that the input is a general greeting question you should answer the greet so you will return answer having key-value pair category number, reply to user's greeting \
    In category 2 it will identify that the input is an type of enquiry about we offer discounts or not so you will return ans having key-value pair category number, reply to user's enquiry \
    In category 3 you will identify weather user is asking about some products which are on discounts so you will return ans having key-value pair category number,discount ,product name (given by user) \
    In category 4 you will identify weather user is asking about some products which are on under some price so you will return ans having key-value pair category  number, price , product name\
    In category 5 you will identify weather user is asking about some products only so you will return ans having keys category number, product name(key name)\
    In category 6 it will identify that the input is a irrelevant  question you should answer the i could not understand so you will return answer having key-value pair category number, reply to user\
    Don't mention that you are not a fashion recommender specialist as it is already assumed.\
    "
    pre_prompt+=" User: "+prompt
    response = palm.generate_text(prompt=pre_prompt,temperature=0.2)

    string = response.result
    pattern = r'\{.*?\}'
    try:
        match = re.search(pattern, string)
        dictionary_string = match.group()
        dictionary = eval(dictionary_string)
        return dictionary
    except:
        return {'category':1,'reply':"Sorry, Unable to process your request. Please try again."}
    