from flask import Flask
import json
import random 
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

@app.route('/')
def index():
    return 'home'

@app.route('/result')
def food_choice(food_list, weight):
    ms = MinMaxScaler()
    w = ms.fit_transform(np.array(weight).reshape(-1,1))
    res = random.choices(food_list, weights=w)
    return res

def get_result(weights, needed_cals):
    foods = pd.read_csv('./food_units.csv')
    food_list = []
    food_types = list(foods['종류'].unique())

    for f in food_types:
        food_list.append([foods[foods['종류']==f].iloc[:, 1].tolist(),
                          foods[foods['종류']==f].iloc[:, 2].tolist()])
    res_list = []

    for i in range(len(weights)):
        res = food_choice(food_list[i][0], weights[i]) # string: name of food
        result_str = res +" " + str(needed_cals[i] * food_list[i][1][food_list[i][0].index(res)])
        res_list.append(result_str)
    
    return json.dumps(res_list)
