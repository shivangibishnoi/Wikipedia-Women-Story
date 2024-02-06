#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 15:34:17 2023

@author: shivangib
"""

#Importing packages required
import os
import numpy as np
import pandas as pd
#from wikidata.client import Client

#client = Client()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Change the directory to the directory where you would want to save thefiles
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

directory = '/Users/shivangibishnoi/Library/CloudStorage/Dropbox/Shivangi/'
os.chdir(directory)


###### Import the file ######
Df_og = pd.read_csv(directory+"cross-verified-database.csv",encoding='latin-1')

columns = Df_og.columns.tolist()

###### Create a mini version to explore #####
Df_check = Df_og.head(10000)


#### Getting counts of people by birth year ####
Df_og = Df_og[Df_og['birth']>=1000]


##### New idea #####


##### Total number of individuals per year ######
tot_num = Df_og['birth'].value_counts().to_frame()
tot_num['year'] = tot_num.index.astype(int)
tot_num = tot_num.sort_values(by=['year'])


#### Number of men and women by year #####
men = Df_og[Df_og['gender']=='Male']
female = Df_og[Df_og['gender']=='Female']

tot_mnum = men['birth'].value_counts().to_frame()
tot_mnum['year'] = tot_mnum.index.astype(int)
tot_mnum = tot_mnum.sort_values(by=['year'])
tot_mnum = tot_mnum.rename(columns={'count':'count_m'})

tot_fnum = female['birth'].value_counts().to_frame()
tot_fnum['year'] = tot_fnum.index.astype(int)
tot_fnum = tot_fnum.sort_values(by=['year'])
tot_fnum = tot_fnum.rename(columns={'count':'count_f'})

#### Average notability of men and women by year #####
men_not = men.groupby(['birth'])['sum_visib_ln_5criteria'].mean().to_frame()
female_not = female.groupby(['birth'])['sum_visib_ln_5criteria'].mean().to_frame()

men_not['year'] = men_not.index.astype(int)
men_not = men_not.sort_values(by=['year'])
men_not = men_not.rename(columns={'sum_visib_ln_5criteria':'score_m'})

female_not['year'] = female_not.index.astype(int)
female_not = female_not.sort_values(by=['year'])
female_not = female_not.rename(columns={'sum_visib_ln_5criteria':'score_f'})

##### Merging everything ######
final_db = pd.merge(tot_num,tot_mnum,on='year',how='left')
final_db = pd.merge(final_db,tot_fnum,on='year',how='left')
final_db = pd.merge(final_db,men_not,on='year',how='left')
final_db = pd.merge(final_db,female_not,on='year',how='left')


final_db['prop_f'] = final_db['count_f']/final_db['count']
final_db['diff_mf'] = final_db['count_m'] - final_db['count_f']
final_db['diff_mf'] = final_db['score_m'] - final_db['score_f']
final_db['diff_fm'] = final_db['score_f'] - final_db['score_m']

final_db.to_csv(directory+"wiki-women-data.csv",index=False)