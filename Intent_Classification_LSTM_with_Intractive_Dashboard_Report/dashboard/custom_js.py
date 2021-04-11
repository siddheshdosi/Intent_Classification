# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:22:16 2021

@author: Siddhesh.Dosi
"""




def dropdown_on_change_update_code():
    
    code = """ 
            var dropdown_value = dropdown.value;
            table_source.data = source_data.data;
            if (dropdown_value == "All"){
                table_source.data = source_data.data;    
            }
            else{
                var actual_val = (dropdown.value).split(" ")[2];
                var predict_val = (dropdown.value).split(" ")[6]; 
                var update_data = {};
                var data = table_source.data;
                var column = Object.keys(data);
                
                for (var i=0;i<column.length;i++){
                        update_data[column[i]]=[];
                }
                for(var i=0 ; i<data[actual_label].length;i++){
                    if (data[actual_label][i] == actual_val && data[predict_label][i]== predict_val){
                        for (var j=0; j<column.length;j++){
                            var value = data[column[j]][i];
                            update_data[column[j]].push(value);
    
                        }
    
                    }

                }
                table_source.data = update_data;
            }
            table_source.change.emit();
            
        
    """
    return code

def class_dropdown_on_change_update_code():
    
    code = """ 
            var dropdown_value = dropdown.value;
            table_source.data = source_data.data;
            if (dropdown_value == "All"){
                table_source.data = source_data.data;    
            }
            else{
                var actual_val = dropdown_value;
                var update_data = {};
                var data = table_source.data;
                var column = Object.keys(data);
                for (var i=0;i<column.length;i++){
                        update_data[column[i]]=[];
                }
                for(var i=0 ; i<data[actual_label].length;i++){
                    if (data[actual_label][i] == actual_val){
                        for (var j=0; j<column.length;j++){
                            var value = data[column[j]][i];
                            update_data[column[j]].push(value);
    
                        }
    
                    }

                }
                table_source.data = update_data;
            }
            table_source.change.emit();
            
        
    """
    return code

def table_on_change_update_code():
    code = """
        var ind = cb_obj.indices;
        
        var data = table_source.data;
        
        var donut_data = donut_source.data;
        donut_data['target_prob'] = label;
        donut_data['color'] = color;
        var sum_prob = 1;
        var probability_score = [];
        var angle_list = [];
        var angle = 0;
        var score = 0;
        for(var i=0 ; i < label.length ; i++){
                score = data['predict_prob'][ind][i];
                angle = score/sum_prob*2*3.141592653589793;
                probability_score.push(score);
                angle_list.push(angle);
        }
        donut_data['probability_score']=probability_score;
        donut_data['angle']=angle_list;
        donut_source.data = donut_data;
        donut_source.change.emit();
        
        //for tfidf
        var temp_dict={};
        var tokens = table_source.data[doc_column][ind];
        tokens = tokens.split(' ');
        //console.log(tokens);
        for(var t=0; t<tokens.length;t++){
                var key = tokens[t].trim().toLowerCase();
                key = key.replace(/[^a-zA-Z0-9]/g, '');
                if(key in tfidf_dict){
                    temp_dict[key]=tfidf_dict[key];        
                }
        }
        //console.log(temp_dict)
        
        function sortOnKeys(dict,N_TOP) {

                var sorted = [];;
                var reverse_dict = {}
                for (var key in dict){
                    reverse_dict[dict[key]]=key;
                }
                for(var key in reverse_dict){
                    sorted[sorted.length] = key;
                }
                sorted = sorted.sort().reverse();
                
                //console.log(sorted);
                var tempDict = {};
                var tokens =[];
                var weight = [];
                for(var i = 0; i < sorted.length; i++) {
                    if (N_TOP >= i){
                        tempDict[reverse_dict[sorted[i]]] = parseFloat(sorted[i]);
                        //tokens.push(reverse_dict[sorted[i]]);
                        //weight.push(parseFloat(sorted[i]));
                    }
                }
                for (key in dict){
                    if (key in tempDict){
                        tokens.push(key);
                        weight.push(parseFloat(dict[key]));
                    }
                
                }
                var result=[];
                result.push(tempDict);
                result.push(tokens);
                result.push(weight);
                return result;
            }
        var result = sortOnKeys(temp_dict,N_TOP);
        var update_tfidf_source={};
        update_tfidf_source['category'] = result[1];
        update_tfidf_source['total_count']=result[2];
        update_tfidf_source['colors'] = color.slice(0,update_tfidf_source['category'].length);
        //update_tfidf_source['colors'] = tfidf_source.data['colors'].slice(0,update_tfidf_source['category'].length);
        //console.log(update_tfidf_source);
        tfidf_source.data = update_tfidf_source;
        tfidf_hbar.y_range.factors = update_tfidf_source['category'];
        tfidf_source.change.emit();
        
        //frequency count
        var temp_dict={};
        var tokens = table_source.data[doc_column][ind];
        tokens = tokens.split(' ');
        console.log(tokens);
        for(var t=0; t<tokens.length;t++){
                var key = tokens[t].trim().toLowerCase();
                key = key.replace(/[^a-zA-Z0-9]/g, '');
                if(key in freq_count_dict){
                    temp_dict[key]=freq_count_dict[key];        
                }
        }
        console.log(temp_dict)
        var result = sortOnKeys(temp_dict,N_TOP);
        var update_freq_source={};
        update_freq_source['category'] = result[1];
        update_freq_source['total_count']=result[2];
        update_freq_source['colors'] = color.slice(0,update_freq_source['category'].length);
        //update_tfidf_source['colors'] = tfidf_source.data['colors'].slice(0,update_tfidf_source['category'].length);
        console.log(update_freq_source);
        freq_count_source.data = update_freq_source;
        freq_count_hbar.y_range.factors = update_freq_source['category'];
        freq_count_source.change.emit();
        
        
    """
    return code