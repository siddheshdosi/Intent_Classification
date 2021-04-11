# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 22:11:37 2021

@author: Siddhesh.Dosi
"""

from bokeh.models import TextInput, Paragraph
from bokeh.plotting import curdoc
from bokeh.layouts import layout,column
from bokeh.io import show,output_file

myMessage = 'You have entered nothing yet: (none)'
text_output = Paragraph(text=myMessage, width=200, height=100)

def my_text_input_handler(attr, old, new):
    myMessage="you just entered: {0}".format(new)
    text_output.text=myMessage # this changes the browser display

text_input = TextInput(value="default", title="Label:")
text_input.on_change("value", my_text_input_handler)

layout = column(text_input,text_output)

curdoc().add_root(layout)
curdoc().title = "Bokeh text input example with text echo"
output_file('layout.html')
show(layout)