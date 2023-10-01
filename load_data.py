import json
import os
from keys import Keys
import datetime
import numpy as np

DATA_FOLDER_NAME = "Data"

def parse(key,val):
    if key == Keys.date:
        try:
            return datetime.datetime.strptime(val, '%d/%m/%Y %H:%M')
        except:
            return datetime.datetime.strptime(val, '%d/%m/%Y')
    if key == Keys.temperature:
        if val == "-" or val is None:
            return np.nan
        else:
            return float(val)
    else:
        return val

def find_illegal_data(key,vals):
    if key == Keys.date:
        return np.full(vals.shape, False)
    if key == Keys.temperature:
        return np.isnan(vals)
    else:
        return np.full(vals.shape, False)

def load_all_data():
    data_points_list = []
    for f_name in os.listdir(DATA_FOLDER_NAME):
        with open(os.path.join(DATA_FOLDER_NAME,f_name),"r",encoding="utf-8") as f:
            data_points_list += json.load(f)
    
    ret = dict()
    for key in data_points_list[0]:
        ret[key] = np.array([parse(key,data_point[key]) for data_point in data_points_list])
    
    num_points = ret[Keys.date].shape
    nan_indexes = np.full(num_points, False)
    for key in data_points_list[0]:
        nan_indexes = np.logical_or(nan_indexes,find_illegal_data(key,ret[key]))
    
    for key in data_points_list[0]:
        ret[key] = ret[key][np.logical_not(nan_indexes)]
        
    return ret