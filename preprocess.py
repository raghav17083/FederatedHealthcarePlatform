# -*- coding: utf-8 -*-
"""
Created on Sun May 16 00:10:39 2021

@author: Raghav Rathi
"""
import pandas as pd #for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, Namespace #basic RDF handling
from rdflib.namespace import FOAF , XSD, RDF, RDFS  #most common namespaces
import urllib.parse #for parsing strings to URI's\
import numpy as np
from datetime import datetime, date
#%%

def split_con(s):
    s=''.join(e for e in s if (e.isalnum() or e.isspace()))
    l=s.split()
    x=""
    for i in l:
      x+=i+"_" 
    return x[:-1]   
# print(split_con("x'ian county"))

#%%

def split_comma(s):
    l=s.split(",")
    for i in range(len(l)):
        l[i]=l[i].strip()
    return l 


#%%

"""Concept Id"""
conceptID_df=pd.read_csv("data_dictionary.csv")

conceptID_dic={}

for i, row in conceptID_df.iterrows():
    conceptID_dic[row['concept_id']]=row['concept_name']
        # device_exposure_dic[row['concept_id']]=row['concept_name']

        
#%%

def age(born):
    born = datetime.strptime(born, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, 
                                      today.day) < (born.month, 
                                                    born.day))
#%%     

"""Person Dataset"""            
person_df=pd.read_csv('person.csv')
person_df['age']=person_df['birth_datetime'].apply(age)

person_df.to_csv("transformation/person_transformed.csv")

#%%
"""Condition"""

condition_df=pd.read_csv('condition_occurrence.csv')

condition_df['condition_name']=""

for i, row in condition_df.iterrows():
    if(row['condition_concept_id'] in conceptID_dic.keys()):
        condition_df.loc[i,'condition_name']=conceptID_dic[row['condition_concept_id']]

condition_df.to_csv("transformation/condition_transformed.csv")
#%%
"""Drug exposure"""                                           
drug_df=pd.read_csv('drug_exposure.csv')

drug_df['drug_name']=""

for i, row in drug_df.iterrows():
    if(row['drug_concept_id'] in conceptID_dic.keys()):
        drug_df.loc[i,'drug_name']=conceptID_dic[row['drug_concept_id']]


drug_df.to_csv("transformation/drug_transformed.csv")
