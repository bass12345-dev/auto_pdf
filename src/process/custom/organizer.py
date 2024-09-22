from src.process.query.query import query_info
from src.process.custom.cus_func import capitalize_first_and_after_spaces
from src.process.custom.pdf_create_sql import shortened_ids
import re
import json

def group_guidlines_by_category(q_data):
    filtered_data = {}
    inner_counter = 0
    # Loop through each item in the data list
    for item in q_data:
        inner_counter += 1
        key_category = item['key_category']
        category = item['category']
        
        # If the key_category does not exist in the dictionary, initialize it
        if key_category not in filtered_data:
            filtered_data[key_category] = {}
        
        # If the category does not exist under the key_category, initialize it with an empty list
        if category not in filtered_data[key_category]:
            filtered_data[key_category][category] = []
        
        # Append the item to the category key under the key_category
        filtered_data[key_category][category].append({'data' : item, 'paging': inner_counter})

    return filtered_data



# def group_guidlines_by_category(q_data):
 
#     # Create an empty dictionary to store the results
#     filtered_data = {}
#     inner_counter = 0
#     # Loop through each item in the data list
#     for item in q_data:
#         inner_counter += 1
#         category = item['category']
        
#         # If the category does not exist in the dictionary, initialize it with an empty list
#         if category not in filtered_data:
#             filtered_data[category] = []
        
#         # Append the item to the category key
#         filtered_data[category].append({'data' : item, 'paging': inner_counter})

#     # Output the result
#     return filtered_data
        
        


def categories(data):
    categories = []
    filter_categories = []
    #Filter Every Category Value 
    for key, value in data.items():
        if 'cat' in key:
            for row,value1 in value.items():
                if isinstance(value1,str):
                    if value1 != '':
                        categories.append(key)  
                elif isinstance(value1,list):
                    if(len(value1)):
                        categories.append(key)

    current_category = None
    category = None 
    for row in categories:
        category = row
        if category != current_category:
            filter_categories.append(category)
            current_category = category
    return filter_categories

def capitalize_category(row):
    pattern = "cat_"
    cat1 = re.sub(pattern, "", row)
    cat2 = re.sub("_", " ", cat1)
    caps = capitalize_first_and_after_spaces(cat2)
    return caps

def get_data(data):
    query           = []
    useful_columns  = [] 
  
    for key, value in data.items():
      
        if 'cat' in key:
            for row,value1 in value.items():
                
                if row == 'title_color' or row == 'caption_color' :

                    if isinstance(value1,str):
                        if value1 != '':
                            x = [0, value1,'', capitalize_category(row)]
                            query.append({'data' : x, 'key': key})
                         
                    elif isinstance(value1,list):
                        if(len(value1)):
                            # result = ' , '.join(value1)
                            x = [0,value1,'',capitalize_category(row)]
                            query.append({'data' : x, 'key': key})

                else:
                    if isinstance(value1,str):
                        if value1 != '':
                            x = query_info(key,value1)
                            # print(key +' '+value1)
                            query.append({'data' : x, 'key': key})
                    elif isinstance(value1,list):
                        if(len(value1)):
                            
                            for row in value1:
                                # print(key +' '+row)
                                x = query_info(key,row)
                                query.append({'data' : x, 'key': key})
                            
    for row in query:
        a_row = row['data']
        notion_id = a_row[2]
        if notion_id is not None:
            notion_id = shortened_ids(notion_id)

        useful_columns.append({
                            "link"          : a_row[2],
                            "notion_id"     : notion_id,
                            "name"          : a_row[1],
                            "category"      : a_row[3],
                            "key_category"  : row['key'],
                           
                         }
                         
        )
    return useful_columns