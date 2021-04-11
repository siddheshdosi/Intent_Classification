# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 18:57:33 2021

@author: Siddhesh.Dosi
"""

import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,TableColumn,DataTable
from bokeh.palettes import Category20
from bokeh.transform import cumsum

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
    donut_chart.axis.visible=False
    donut_chart.grid.grid_line_color = None
    return donut_chart