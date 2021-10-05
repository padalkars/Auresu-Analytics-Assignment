#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[1]:


#List of functions
'''
1. missing_value_analysis
2. outlier_Analysis
3. get_statistics
'''


# In[2]:


def missing_value_analysis(data):
    '''
    Input
    data:- The data for which missing values are to be analyzed
    Return
    missing_values:- A data frame with the statistics
    '''
    features = list(data.columns)
    missing_counts = data.isnull().sum().values
    missing_value_perc = (missing_counts * 100)/data.shape[0]
    
    #Create a data frame
    missing_values_df = pd.DataFrame({"Features": features,                                       "Missing Value Counts": missing_counts,                                     "Missing Value Percentage": missing_value_perc},                                    columns = ["Features", "Missing Value Counts",                                              "Missing Value Percentage"])
    
    #Sort the data in descending order of missing values
    missing_values_df = missing_values_df.sort_values(by="Missing Value Counts",                                                      ascending=False)
    return missing_values_df


# In[2]:


#(data_types_df.loc[ind, "Data Types"] == "float64")|\
def get_data_types(data):
    data_types = data.dtypes #Returns a Series
    data_types_df = pd.DataFrame({"Features": data_types.index.tolist(),                 "Data Types": list(data_types.values)},                 columns = ["Features", "Data Types"])
    
    variable_type = []
    for ind in data_types_df.index:
        if(data_types_df.loc[ind, "Data Types"] == object):
            variable_type.append("Categorical")
            
        elif((data_types_df.loc[ind, "Data Types"] == float)|            (data_types_df.loc[ind, "Data Types"] == int)):
            variable_type.append("Numeric")
        elif((data_types_df.loc[ind, "Data Types"] == pd.datetime)|            (data_types_df.loc[ind, "Data Types"] == np.dtype('datetime64[ns]'))):
            variable_type.append("Data Time")
        else:
            variable_type.append(np.nan)
    
    #Create a column Varaible Type
    data_types_df["Variable Type"] =variable_type
    
    return data_types_df

def get_unique_cat_count(data_stats, data):
    cat_vars = data_stats.loc[data_stats["Data Types"]==object, "Features"].tolist()
    unique_cat_count = list(map(lambda var: len(set(data[var])) if(var in cat_vars)                               else np.nan, data_stats["Features"].tolist()))
    return unique_cat_count
        
def get_statistics(data):
    '''
    Data types of Variables
    Continuous Variables:- Mean, Q_25, Q_50, Q75, Min, Max 
    Categorical Variables:- # Unique Categories
    '''
    #Missing Value Stats
    missing_values = missing_value_analysis(data)

    #Get the data types
    data_stats = get_data_types(data)
    
    #For numeric variables find the 
    numeric_vars = data_stats.loc[(data_stats["Data Types"]==float) |                                  (data_stats["Data Types"]==int), "Features"]
    
    #Obtain the number of unique categories for every categorical variable
    data_stats["# Unique Categories"] = get_unique_cat_count(data_stats, data)  
    
    #Obtain the stats for numeric variables (Mean, Median, Q25, Q50, Q75)
    numeric_stats = data[numeric_vars].describe().T
    numeric_stats = numeric_stats.reset_index()
    numeric_stats = numeric_stats.rename(columns={'index':'Features'})
    
    #Merge numeric_stats and missing_values with data_stats
    data_stats = pd.merge(data_stats, missing_values, how='left', on="Features")
    data_stats = pd.merge(data_stats, numeric_stats, how='left', on="Features")
    #Sort in descending order of missing values
    data_stats = data_stats.sort_values(by="Missing Value Counts",                                                      ascending=False)
    return data_stats


# In[ ]:




