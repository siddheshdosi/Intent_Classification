# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 14:14:37 2021

@author: Siddhesh.Dosi
"""

from bokeh.models import Select,PreText
import dashboard_utils

def Dropdown(options,title):
    #options = dashboard_utils.get_dropdown_options(n_class, actual, predict, labels)
    dropdown=Select(title=title,value='', options=options)
    return dropdown

def Pretext(text):
    pretext = PreText(text=text)
    return pretext

