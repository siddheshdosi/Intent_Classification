# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import utils
from model import build_lstm_model,predict

import score_metrics

import dashboard.data_viz as data_viz
from bokeh.io import show,output_file
from bokeh.layouts import column,row,layout
from bokeh.models import CustomJS
from bokeh.palettes import Category20

from dashboard import dashboard_view,data_viz,dashboard_utils,custom_js

import shap
from tqdm import tqdm
tqdm.pandas()
# Read intent data
data = pd.read_csv('data/intent_classification_data.csv',encoding='latin1',names=['Sentence','Intent'])

#Shuffle data
data = data.sample(frac=1).reset_index(drop=True)

number_of_intent = len(data.Intent.unique())


tokenizer,word_index_dict,index_word_dict,vocab_size,max_input_length,input_vector=utils.create_tokenizer_encoding_padding(data.Sentence, padding='post')

lable_encoding,label = utils.label_encode(data.Intent)

x_train,y_train,x_test,y_test = utils.prepare_train_test(input_vector, label)

model = build_lstm_model(vocab_size, max_input_length, n_classes=number_of_intent, loss='sparse_categorical_crossentropy')

history = model.fit(x_train,y_train,epochs=50,batch_size=30)

##Slice data to define xtest data
validate_data = data.loc[890:]
validate_data = validate_data.reset_index(drop=True)
validate_data[['predict','score','predict_prob']]=validate_data.Sentence.apply(lambda x : predict(model,x,tokenizer,lable_encoding,max_input_length,padding='post'))
category_label = np.unique(validate_data.Intent)
############################
###SHAP Value
############################
#text='How to apply for the loan'
#shap_cat_list,shap_count_list = utils.shap_values(model,x_train,text,tokenizer,index_word_dict,max_input_length,padding='post')
#explainer = shap.KernelExplainer(model, x_train[:10])
#validate_data[['shap_cat_list','shap_value']] = validate_data.Sentence.progress_map(lambda x : utils.shap_values(model,x_train,x,tokenizer,index_word_dict,max_input_length,padding='post'))

##Get word scores
tfidf = score_metrics.tfidf_score(data.Sentence)
tfidf = tfidf.sort_values(by='normalize_score',ascending=False)
freq_count = score_metrics.frequency_count_score(data.Sentence)
freq_count = freq_count.sort_values(by='normalize_score',ascending=False)


############################
### Create Dashboard
############################
options = dashboard_utils.get_dropdown_options(len(category_label), validate_data.Intent, validate_data.predict, category_label)
dropdown = dashboard_view.Dropdown(options,title="Actual Vs Predicted :")

class_dropdown = dashboard_view.Dropdown(['All']+list(category_label),title='Intent Class :')

clf_report_text = score_metrics.get_classification_report(validate_data.Intent, validate_data.predict)
clf_report = dashboard_view.Pretext(clf_report_text)


source_data = data_viz.create_data_table_source(validate_data)
table_source = data_viz.create_data_table_source(validate_data)
data_table = data_viz.data_table(table_source, validate_data.columns)



top20_tfidf = tfidf[:20]
tfidf_source = data_viz.create_horizonatal_bar_source(top20_tfidf.token, top20_tfidf.normalize_score)
tfidf_hbar = data_viz.horizontal_bar_chart(tfidf_source, title='Top 20 TF-IDF Score')

top20_freq_count = freq_count[:20]
freq_count_source = data_viz.create_horizonatal_bar_source(top20_freq_count.token, top20_freq_count.normalize_score)
freq_count_hbar = data_viz.horizontal_bar_chart(freq_count_source, title='Top 20 Frequency Score')

donut_source = data_viz.create_donut_source()
donut_chart = data_viz.donut_chart(donut_source,title='Probablity Distribution',width=900,height=800)


###############################################
### Start CallbackJS for making intractive dashboard
###############################################
dropdown_code = custom_js.dropdown_on_change_update_code()
dropdown_callback = CustomJS(args=dict(source_data=source_data,table_source=table_source,dropdown=dropdown,actual_label='Intent',predict_label='predict'),code=dropdown_code)
dropdown.js_on_change('value',dropdown_callback)


class_dropdown_code = custom_js.class_dropdown_on_change_update_code()
class_dropdown_callback = CustomJS(args=dict(source_data=source_data,table_source=table_source,dropdown=class_dropdown,actual_label='Intent'),code=class_dropdown_code)
class_dropdown.js_on_change('value',class_dropdown_callback)

total_color_code = Category20[20]*len(category_label)
total_color_code = total_color_code[:len(category_label)]
table_click_change_code = custom_js.table_on_change_update_code()
table_callback = CustomJS(args=dict(table_source=table_source,donut_source=donut_source,label=category_label,color= total_color_code),code=table_click_change_code)
table_source.selected.js_on_change('indices', table_callback)


output_file('layout.html')
#filter_layout = column(dropdown,class_dropdown,clf_report)
#chart_layout = row(tfidf_hbar,freq_count_hbar,donut_chart)
#right_layout = column(data_table,chart_layout)

#main_layout = row(filter_layout,right_layout)
#shap_source = data_viz.create_horizonatal_bar_source(shap_cat_list,shap_count_list)
#shap_hbar = data_viz.horizontal_bar_chart(shap_source,title='SHAP Value')


#nested_vbar=data_viz.nested_vertical_bar(validate_data.Intent, validate_data.predict,title='Total Intent Classes Count of Actual vs Predict')
#cm = score_metrics.get_confusion_matrics(validate_data.Intent, validate_data.predict, label)
#cm_source = data_viz.create_data_table_source(cm)
#cm_table = data_viz.data_table(cm_source,cm.columns)


