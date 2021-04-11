# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 18:57:33 2021

@author: Siddhesh.Dosi
"""

import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,TableColumn,DataTable,FactorRange
from bokeh.models import Legend
from bokeh.palettes import Category20
from bokeh.transform import cumsum,factor_cmap


def nested_vertical_bar(actual,predict,x_axis_label='',y_axis_label='',title='',plot_width=500,plot_height=300):
    labels = list(set(actual))
    names = ['True','False']
    true_dict = {}
    false_dict = {}
    for l in labels:
        true_dict[l],false_dict[l]=0,0
    for a,p in zip(actual,predict):
        if a==p:
            true_dict[a]+=1
        else:
            false_dict[a]+=1
        #actual_dict[a]+=1
        #predict_dict[p]+=1
    true_count = [v for k,v in true_dict.items()]
    false_count = [v for k,v in false_dict.items()]
    x = [ (label, name) for label in labels for name in names]
    counts = sum(zip(true_count, false_count), ())
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(x_range=FactorRange(*x),x_axis_label=x_axis_label,y_axis_label=y_axis_label,plot_width=plot_width,plot_height=plot_height, title=title,
           toolbar_location=None, tools="",tooltips='@x:@counts')

    
    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
       # use the palette to colormap based on the the x[1:2] values
       fill_color=factor_cmap('x', palette=('#3288bd','#d53e4f'), factors=names, start=1, end=2))
    
    #p.xaxis.major_tick_line_color = None        # turn off x-axis major ticks
    #p.xaxis.minor_tick_line_color = None        # turn off x-axis minor ticks
    #p.xaxis.major_label_text_font_size = '0pt'
    p.xaxis.visible = False
    p.grid.grid_line_color = None
    return p

    

def create_horizonatal_bar_source(category_list,count_list):
    hbar_source = pd.DataFrame(list(zip(category_list,count_list)),columns=['category','total_count'])
    colors = list(Category20[20])*len(category_list)
    colors = colors[0:len(category_list)-1]
    hbar_source = ColumnDataSource(dict(category=category_list,total_count=count_list,colors=colors))
    return hbar_source


def horizontal_bar_chart(hbar_source,title,plot_width=400,plot_height=300):
    max_count = max(list(hbar_source.data['total_count']))
    min_count = min(0,min(list(hbar_source.data['total_count'])))
    h_bar = figure(y_range=hbar_source.data['category'],
                              x_range=(min_count,max_count),
                              plot_width=plot_width,plot_height=plot_height,
                              tooltips="@category: @total_count",
                              title=title)
    h_bar.hbar(y='category', right='total_count', height=0.8, source=hbar_source,
       color='colors')
    h_bar.grid.grid_line_color = None
    return h_bar

def create_data_table_source(data):
    table_source = ColumnDataSource(dict(data))
    return table_source

def data_table(table_source,columns,width=800,height=280):
    table_columns = [TableColumn(field=col, title=col) for col in columns]
    table = DataTable(source=table_source, columns=table_columns, width=width, height=height,css_classes=["my_table"])
    return table

def create_donut_source(target_prob=[],probability_score=[],angle=[],color=[]):
    donut_source = ColumnDataSource(dict(target_prob=target_prob,probability_score=probability_score,angle=angle,color=color))
    return donut_source

def donut_chart(donut_source,title='',width=400,height=300):
    donut_chart = figure(plot_height=height, plot_width=width,title=title, toolbar_location=None,
        tools="hover", tooltips="@target_prob: @probability_score",x_range=(-.5, .5))
    donut_chart.annular_wedge(x=0, y=1, inner_radius=0.15, outer_radius=0.25,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='target_prob', source=donut_source)
    donut_chart.axis.axis_label=None
    donut_chart.add_layout(donut_chart.legend[0], 'right')
    donut_chart.axis.visible=False
    donut_chart.grid.grid_line_color = None
    return donut_chart