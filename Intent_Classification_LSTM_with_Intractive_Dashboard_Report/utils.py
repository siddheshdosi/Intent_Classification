# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 11:31:21 2021

@author: Siddhesh.Dosi
"""

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import shap
import numpy as np

def create_tokenizer_encoding_padding(corpus,padding):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)
    word_index_dict = tokenizer.word_index
    index_word_dict = {value:key for key,value in word_index_dict.items()}
    vocab_size = len(word_index_dict)+1
    token_list = tokenizer.texts_to_sequences(corpus)
    max_input_length =  max([len(line) for line in token_list])
    input_vector = pad_sequences(token_list,maxlen=max_input_length,padding='post')
    return tokenizer,word_index_dict,index_word_dict,vocab_size,max_input_length,input_vector

def prepare_train_test(input_vector,target,test_size=0.20):
    xs = input_vector
    ys =target
    cut_index = round(len(xs)*(1-test_size))
    x_train,y_train = xs[0:cut_index],ys[0:cut_index]
    x_test,y_test = xs[cut_index:],ys[cut_index:]
    return x_train,y_train,x_test,y_test

def label_encode(label):
    le = LabelEncoder()
    le.fit(label)
    label = le.transform(label)
    return le,label

def shap_values(model,expainer,text,tokenizer,num2word,max_input_length,padding='post'):
    seq = tokenizer.texts_to_sequences([text])
    pad = pad_sequences(seq,maxlen=max_input_length,padding=padding)
    shap_values = explainer.shap_values(pad)
    x_test_words = np.stack([np.array(list(map(lambda x: num2word.get(x, "NONE"), pad[i]))) for i in range(1)])
    shap_value = shap_values[0][0]
    category_list,count_list=[],[]
    for cat,score in zip(x_test_words[0],shap_value):
        if cat != 'NONE':
            category_list.append(cat)
            count_list.append(score)
    return category_list,count_list

    