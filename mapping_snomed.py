# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 22:25:16 2021

@author: Raghav Rathi
"""

"""Synapse Dataset"""

import pandas as pd #for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, Namespace #basic RDF handling
from rdflib.namespace import FOAF , XSD, RDF, RDFS  #most common namespaces
import urllib.parse #for parsing strings to URI's\

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

"""Concept Ide"""
conceptID_df=pd.read_csv("data_dictionary.csv")


# condition_occurrence_dic={} 
# observation_dic={}
# drug_exposure_dic={}
# measurement_dic={}
# visit_occurrence_dic={} 
# procedure_occurrence_dic={}
# device_exposure_dic={}

conceptID_dic={}

for i, row in conceptID_df.iterrows():
    conceptID_dic[row['concept_id']]=row['concept_name']
        # device_exposure_dic[row['concept_id']]=row['concept_name']


#%%

person_df=pd.read_csv('person.csv')
# print(person_df.columns)

""""Index(['person_id', 'gender_concept_id', 'year_of_birth', 'month_of_birth',
       'day_of_birth', 'birth_datetime', 'race_concept_id',
       'ethnicity_concept_id', 'location_id', 'provider_id', 'care_site_id',
       'person_source_value', 'gender_source_value',
       'gender_source_concept_id', 'race_source_value',
       'race_source_concept_id', 'ethnicity_source_value',
       'ethnicity_source_concept_id'],
      dtype='object')
"""
#%%

"""DEFINE NAMESPACES"""
onto=Namespace("http://www.semanticweb.org/btp/clinical/ontology/")
ex=Namespace("http://www.example.org/btp_ontology/individual/")
#%%
g1=Graph()

g1.bind('ex',ex)
g1.bind('schema',onto)



for i, row in person_df.iterrows():
    person="patient_"+str(row['person_id'])
    
    g1.add((URIRef(ex+person), RDF.type, URIRef(onto+"Patient")))
    
    g1.add((URIRef(ex+person), URIRef(onto+"hasPatientID"),
           Literal("subject_id_"+str(row['person_id']),datatype=XSD.str)))#2
    
    
    g1.add((URIRef(ex+person), URIRef(onto+"dateOfBirth"),
           Literal(str(row['birth_datetime']),datatype=XSD.datetime)))
    
    g1.add((URIRef(ex+person), URIRef(onto+"age"),
           Literal((2021-row['year_of_birth']),datatype=XSD.int)))
    
    g1.add((URIRef(ex+person),URIRef(onto+"gender"),Literal(row['gender_source_value'])))

with open("person.ttl",'w+') as file:
    file.write(g1.serialize(format='turtle').decode('UTF-8'))

#%%
"""Condition occurrence"""
condition_df=pd.read_csv('condition_occurrence.csv')
# print(condition_df.columns)
"""'person_id', 'condition_occurrence_id', 'condition_concept_id',
       'condition_start_date', 'condition_start_datetime',
       'condition_end_date', 'condition_end_datetime',
       'condition_type_concept_id', 'stop_reason', 'provider_id',
       'visit_occurrence_id', 'visit_detail_id', 'condition_source_value',
       'condition_source_concept_id', 'condition_status_source_value',
       'condition_status_concept_id'],"""
    
    
g2=Graph()
g2.bind('ex',ex)
g2.bind('schema',onto)

for i, row in condition_df.iterrows():
    person="patient_"+str(row['person_id'])
    
    
    """The actual condition"""
    cur_cond="conditionConceptID_"+str(row['condition_concept_id'])

    
    """Individual Condition of the person"""
    person_cond="conditionConceptID_"+str(row['condition_concept_id'])+"_"+str(row['person_id'])
        
    g2.add((URIRef(ex+cur_cond),RDF.type,URIRef(onto+"Condition")))
    g2.add((URIRef(ex+person_cond),RDF.type,URIRef(onto+"IndividualCondition")))
    
    g2.add((URIRef(ex+person),URIRef(onto+"hasCondition"), URIRef(ex+person_cond)))
    
    g2.add((URIRef(ex+cur_cond), URIRef(onto+"snomed_id"), Literal(row['condition_concept_id'],datatype=XSD.int)))
    
    g2.add((URIRef(ex+person_cond),URIRef(onto+"conditionType"),URIRef(ex+cur_cond)))
    g2.add((URIRef(ex+person_cond), URIRef(onto+"dateOfOnset"), Literal(row['condition_start_date'],datatype=XSD.datetime)))
    g2.add((URIRef(ex+person_cond), URIRef(onto+"dateOfOffset"), Literal(row['condition_end_date'],datatype=XSD.datetime)))
    
    if(row['condition_concept_id'] in conceptID_dic.keys()):
        condition=conceptID_dic[row['condition_concept_id']]
        
        g2.add((URIRef(ex+cur_cond),RDFS.label,Literal(conceptID_dic[row['condition_concept_id']])))
        
        # g2.add((URIRef(onto+cur_cond),URIRef(onto+"id_to_symptom"), URIRef(onto+condition)))
        
        
    
    
  
    # g2.add((URIRef(onto+person), URIRef(onto+"dateOfOnset"), Literal(row['condition_start_datetime'],datatype=XSD.datetime)))
    # g2.add((URIRef(onto+person), URIRef(onto+"dateOfOffset"), Literal(row['condition_end_datetime'],datatype=XSD.datetime)))


with open("condition.ttl",'w+') as file:
    file.write(g2.serialize(format='turtle').decode('UTF-8'))


#%%


"""Drug_exposure"""

drug_df=pd.read_csv('drug_exposure.csv')
"""''person_id', 'drug_exposure_id', 'drug_concept_id',
       'drug_exposure_start_date', 'drug_exposure_start_datetime',
       'drug_exposure_end_date', 'drug_exposure_end_datetime',
       'verbatim_end_date', 'drug_type_concept_id', 'stop_reason', 'refills',
       'quantity', 'days_supply', 'sig', 'route_concept_id', 'lot_number',
       'provider_id', 'visit_occurrence_id', 'visit_detail_id',
       'drug_source_value', 'drug_source_concept_id', 'route_source_value',
       'dose_unit_source_value'],
      dtype='object',"""
    
    
g3=Graph()
g3.bind('ex',ex)
g3.bind('schema',onto)

for i, row in drug_df.iterrows():
    person="patient_"+str(row['person_id'])
    
    
    """The actual drug"""
    cur_drug="drugConceptID_"+str(row['drug_concept_id'])

    
    """Individual Drug Administered to the person"""
    person_drug="drugConceptID_"+str(row['drug_concept_id'])+"_"+str(row['person_id'])
        
    g3.add((URIRef(ex+cur_drug),RDF.type,URIRef(onto+"Drug")))
    g3.add((URIRef(ex+person_drug),RDF.type,URIRef(onto+"IndDrug")))
    
    g3.add((URIRef(ex+person),URIRef(onto+"drug_administered"), URIRef(ex+person_drug)))
    
    g3.add((URIRef(ex+cur_drug), URIRef(onto+"snomed_id"), Literal(row['drug_concept_id'])))
    
    g3.add((URIRef(ex+person_drug),URIRef(onto+"drugType"),URIRef(ex+cur_drug)))
    g3.add((URIRef(ex+person_drug), URIRef(onto+"drug_adm_start"), Literal(row['drug_exposure_start_date'],datatype=XSD.datetime)))
    g3.add((URIRef(ex+person_drug), URIRef(onto+"drug_adm_end"), Literal(row['drug_exposure_end_date'],datatype=XSD.datetime)))
    
    if(pd.isnull(row['dose_unit_source_value'])==False):
        g3.add((URIRef(ex+person_drug),URIRef(onto+"doseUnit"), Literal(row['dose_unit_source_value']))) 
    if(pd.isnull(row['quantity'])==False):
        g3.add((URIRef(ex+person_drug),URIRef(onto+"patientDosage"), Literal(row['quantity'],datatype=XSD.float)))
        
    if(pd.isnull(row['route_source_value'])==False):
        
        g3.add((URIRef(ex+person_drug),URIRef(onto+"routeOfAdministration"), Literal(row['route_source_value'],datatype=XSD.str)))
    if(row['drug_concept_id'] in conceptID_dic.keys()):
        condition=conceptID_dic[row['drug_concept_id']]
        g3.add((URIRef(ex+cur_drug),RDFS.label,Literal(conceptID_dic[row['drug_concept_id']])))
        
    

with open("drug_exposure.ttl",'w+') as file:
    file.write(g3.serialize(format='turtle').decode('UTF-8'))





