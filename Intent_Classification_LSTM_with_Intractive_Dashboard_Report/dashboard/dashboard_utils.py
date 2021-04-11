# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 14:01:17 2021

@author: Siddhesh.Dosi
"""
from bokeh.models import Div
from sklearn.metrics import confusion_matrix

def get_dropdown_options(n_class,actual,predict,labels):
    options=['All']
    cm = confusion_matrix(actual,predict)
    for i in range(n_class):
        for j in range(n_class):
            option = 'Actual : '+labels[i]+'  Predicted : '+labels[j] + '  Total : '+str(cm[i,j])
            options.append(option)
    return options

def define_header(header_name):
    text ='<h1 style="text-align: center">'+header_name+'</h1>'
    header = Div(text=text)
    return header


