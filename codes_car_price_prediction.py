# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 09:04:03 2024

@author: isehati
"""


"""data scraping from truecar site """
import mysql.connector
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np


cars = []
for page in range(0,10):   
    url = "https://www.truecar.com/used-cars-for-sale/listings/"+"?page="+ str(page)
    #print(page, url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    cards =soup.find_all('div', attrs= {'class': 'flex w-full flex-col'})
    
    #print(len(cards))
    #print(cards[0].text)
    
    #con = mysql.connector.connect(user= 'root', password ='', host= 'localhost')
    #com0 = c.execute('CREATE DATABASE truecar_db')
    con = mysql.connector.connect(user= 'root', password ='', host= 'localhost', database='truecar_db')
    c = con.cursor()

  
    try:   
        com1 ='CREATE TABLE TRUECAR0 (name varchar (50), year int  ,mile int ,accident varchar (20), price int  )'
        c.execute(com1)
    except:
        pass
    
    """ save data in database"""
    
    for card in cards:
        # print(card.text)
        price = card.find('span',attrs= {'data-test':'vehicleListingPriceAmount'})
        price_i = re.findall(r'\$(\d*)\,(\d*)$', price.text)
        price_int = int(price_i[0][0]+price_i[0][1])
        
        # price = card.find('div', attrs= { 'class': 'heading-3 normal-case my-1 font-bold'})
        # mile = card.find('div', attrs= { 'class': 'truncate text-xs'})
        mile = card.find('div', attrs= { 'class': 'flex w-full justify-between'})
        try :
            mile_i = re.findall(r'(\d*)\,(\d*).*$', mile.text)
            mile_int = int(mile_i[0][0]+mile_i[0][1])
        except:
            mile_i = re.findall(r'(\d*).*$', mile.text)
            mile_int = int(mile_i[0])

              
        name = card.find('span', attrs ={'class':'truncate'})  
        
        year = card.find('div', attrs= {'data-test':'vehicleCardYearMakeModel'})
        #print ('year=',year.text)
        year1 = re.finditer('[0-9]{4}?', year.text)
        years =[]
        for y in year1 :
            years.append( y.group())
        #   print (years[0])
        year4 = years[0]
        # year4 = re.findall(r'.*([0-9]{4}).*$', year.text)[0] براي چند رقم در اسم جواب نداد 
    
    
        # accident = card.find('div', attrs={'class':'vehicle-card-location mt-1 text-xs'})
        accident = card.find('div', attrs={'data-test':'vehicleCardCondition'})
        accident1 = re.findall(r'(.*)\,.*$', accident.text)[0]
        
        """ write extracted data in sql / Xampp database  """
        #print (name.text,'********',price.text,price_int,'******',mile.text, mile_int,'++++++', year4,'-----', '@@@',accident1)
        cars.append([name.text, price.text, mile.text])
        com2 = ( """insert into  truecar0 (name,year,mile,accident, price) values (%s,%s,%s,%s,%s)""")
        val = (name.text,year4, mile_int, accident1, price_int)
        c.execute(com2,val)
        con.commit()

"""read data from sql / Xampp database"""
cars = []
con = mysql.connector.connect(user='root',password='',host='localhost', database='truecar_db')
# pd.read_sql_table('truecar5', con)

c = con.cursor()
c.execute('SELECT * FROM TRUECAR11')
rows = c.fetchall()

df = pd.DataFrame(rows).drop_duplicates()
df.columns =['name', "year", "mile", "accident", "price"]
#print(df)
con.close() 

"""ML modeling by sklearn liberary methods"""
#df.hist(bins=150,figsize=(8,5))

#pip install -U scikit-learn

from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

"""   set train and test set / target column """

train, test = train_test_split(df, test_size=0.2, random_state=40,stratify=None)
train_featurs =train.drop(['price'], axis=1)
train_target = train[['price']]
test_featurs =test.drop(['price'], axis=1)
test_target = test[['price']]
test_featurs

numeric_train_featurs =train[['mile']]
categorical_train_featurs =train_featurs.drop(columns=['mile'])


"""transformers /make  pipelines"""

numeric_train_features_pipe = make_pipeline(SimpleImputer(strategy='mean'),
                                            FunctionTransformer(np.log,inverse_func=np.exp,feature_names_out='one-to-one', kw_args=None ),
                                            StandardScaler ())
notorder_categorical_train_features_pipe = make_pipeline(SimpleImputer(strategy='most_frequent'),
                                          OneHotEncoder(handle_unknown='ignore'))
orderd_categorical_train_features_pipe =make_pipeline(SimpleImputer(strategy='most_frequent'),
                                        OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))

defoult_transformer_pipe = make_pipeline(SimpleImputer(strategy='median'),StandardScaler())

            
all_transformers = ColumnTransformer([('num_f',numeric_train_features_pipe,['mile']),
                                      ('ord_cat',orderd_categorical_train_features_pipe,['year','accident']),
                                     ('not_ord_cat',notorder_categorical_train_features_pipe,['name']) 
                                     ])

"""fit transformers"""
transformed_train_featurs =all_transformers.fit_transform(train_featurs)

""" linear regression model- pipeline / fit model and predict"""
""" train set prediction """

from sklearn.linear_model import LinearRegression
model_pipe = make_pipeline(all_transformers ,  LinearRegression())
model_pipe .fit(train_featurs,train_target)
price_predict = model_pipe.predict(train_featurs)
#rice_predict ,train_target



""" train set evaluation """
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
print ('LinearRegression mean_absolute_error for train set:',mean_absolute_error(train_target,price_predict ))
r2_score(train_target,price_predict )


""" predicat test set """

transformed_test_featurs = all_transformers.transform(test_featurs)
test_price_predict = model_pipe.predict(test_featurs)
print ('LinearRegression mean_absolute_error for test set:',mean_absolute_error(test_target,test_price_predict ))
r2_score(test_target,test_price_predict )