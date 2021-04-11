# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 11:21:23 2021

@author: Siddhesh.Dosi
"""

from tensorflow.keras.layers import Dense,LSTM,Bidirectional,Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import numpy as np
import pandas as pd

def build_lstm_model(vocab_size,input_length,n_classes,loss):
    model = Sequential()
    model.add(Embedding(vocab_size,128,input_length=input_length-1))
    model.add(Bidirectional(LSTM(20)))
    model.add(Dense(n_classes,activation='softmax'))
    model.compile(loss=loss, optimizer='adam', metrics=['accuracy'])
    return model

def predict(model,text,tokenizer,label_encoding,max_input_length,padding):
    seq = tokenizer.texts_to_sequences([text])
    pad = pad_sequences(seq, maxlen=max_input_length,padding=padding)
    pred = model.predict(pad)
    label_index =   np.argmax(pred)
    pred_result = label_encoding.inverse_transform([[label_index]])
    pred_score = pred[0][label_index]
    #return pred_result[0],pred_score,pred[0]
    return pd.Series({'predict':pred_result[0],'score':pred_score,'predict_prob':pred[0]})

