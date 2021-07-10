#!/usr/bin/env python
# coding: utf-8

"""
In this script, the results of the compressed-air chamber tests are visualised.
All visualisations are stored in /figures/
"""

__author__ = "Eva Zillen"
__copyright__ = "Copyright 2021, TU Delft Biomechanical Design"
__credits__ = ["Eva Zillen, Heike Vallery, Gerwin Smit"]
__license__ = "CC0-1.0 License"
__version__ = "1.0.0"
__maintainer__ = "Eva Zillen"
__email__ = "e.zillen@student.tudelft.nl"


# #### Imports
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# #### Global variables

# The types of additive manufacturing used in this test
models = ['Aluminium','Prusa','Formlabs','Ultimaker_006','Ultimaker_010','Ultimaker_015','Ultimaker_020']


# ## Compressed air chamber test

# Define a dictionary to store all data from the air chamber tests
# For each ring all variables are stored in this nested dictionary
air_chambers = {}

# For each model type
for model in models:
    # Load the data of the corresponding results in .CSV and drop unnecessary columns
    model_df = pd.read_csv(f'./data/{model}.csv',delimiter=';',header=None,names=(['Time','A','Pressure']))
    model_df.drop(columns=['A'],axis=1,inplace=True)

    # Store the data in our larger dictionary
    air_chambers[model]={}
    # Filtering the time data (in s)
    air_chambers[model]['Time'] = model_df['Time'].str.replace('.','').astype('float64')/1000000
    # For all models limit the time (in s) and pressure (in MPa) to the same amount
    air_chambers[model]['Time'] = air_chambers[model]['Time'].head(1400)
    air_chambers[model]['Pressure'] = model_df['Pressure'].head(1400)/10

    # Define the pressure drop by reducing all pressures with the first measures pressure (in MPa)
    air_chambers[model]['PressureDrop'] = air_chambers[model]['Pressure'] - air_chambers[model]['Pressure'][0]


# #### All models with their pressure drop (in MPa) over time (in s)

plt.plot(air_chambers['Aluminium']['Time'],air_chambers['Aluminium']['PressureDrop'],'black', label='Aluminium', linestyle=(0,(1,1,1)),linewidth=2)
plt.plot(air_chambers['Prusa']['Time'],air_chambers['Prusa']['PressureDrop'],'tab:orange', label='SLA Prusa', linestyle='dashdot')
plt.plot(air_chambers['Formlabs']['Time'],air_chambers['Formlabs']['PressureDrop'],'tab:green', label='SLA Formlabs', linestyle='dotted',linewidth=3)
plt.plot(air_chambers['Ultimaker_006']['Time'],air_chambers['Ultimaker_006']['PressureDrop'],'tab:red',label='Ultimaker 0.06 mm')
plt.plot(air_chambers['Ultimaker_010']['Time'],air_chambers['Ultimaker_010']['PressureDrop'],'tab:purple',label='Ultimaker 0.10 mm', linestyle='dashed')
plt.plot(air_chambers['Ultimaker_015']['Time'],air_chambers['Ultimaker_015']['PressureDrop'],'tab:blue',label='Ultimaker 0.15 mm', linestyle=(0,(10,2,2)))
plt.plot(air_chambers['Ultimaker_020']['Time'],air_chambers['Ultimaker_020']['PressureDrop'],'tab:brown',label='Ultimaker 0.20 mm', linestyle=(0,(5,2,2)))

# Set the labels and save the figure
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Pressure drop (MPa)')
plt.savefig('./figures/result_airchamber.pdf',bbox_inches = 'tight')
plt.clf()


# #### Models with their pressure drop (in MPa) over time (in s) (excluding Ultimaker 0.15 mm and 0.20 mm)

# To smoothen out the lines a sampling [::4] and a rolling window of 20 are applied
plt.plot(air_chambers['Aluminium']['Time'][::4],air_chambers['Aluminium']['PressureDrop'].rolling(window=20).mean()[::4],'black', label='Aluminium', linestyle=(0,(1,1,1)),linewidth=2)
plt.plot(air_chambers['Prusa']['Time'][::4],air_chambers['Prusa']['PressureDrop'].rolling(window=20).mean()[::4],'tab:orange', label='SLA Prusa', linestyle='dashdot')
plt.plot(air_chambers['Formlabs']['Time'][::4],air_chambers['Formlabs']['PressureDrop'].rolling(window=20).mean()[::4],'tab:green', label='SLA Formlabs', linestyle='dotted',linewidth=3)
plt.plot(air_chambers['Ultimaker_006']['Time'][::4],air_chambers['Ultimaker_006']['PressureDrop'].rolling(window=20).mean()[::4],'tab:red',label='Ultimaker 0.06 mm')
plt.plot(air_chambers['Ultimaker_010']['Time'][::4],air_chambers['Ultimaker_010']['PressureDrop'].rolling(window=20).mean()[::4],'tab:purple',label='Ultimaker 0.10 mm', linestyle='dashed')

# Set the labels and save the figure
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Pressure drop (MPa)')
plt.savefig('./figures/result_airchamber_part.pdf',bbox_inches = 'tight')
plt.clf()


# # Repeatability

# We performed two repeatability tests
# - The test was rerun without any changes in the connections (rerun)
# - The model was reconnected prior to taking the tests (reconnected)

# ### Rerun

# Load the data for the rerun repeatability test
test_rerun=pd.read_csv(r'data/Resultaten_opnieuwaanzetten.csv', delimiter=";", header=1, names=(['Time',"Test1","Test2","Test3",'Aluminium','G','SLA Prusa','SLA Formlabs','Ultimaker 0.10']))

# Apply a rolling window for each type of additive manufacturing and convert pressure data to MPa
for model in list(test_rerun.keys())[1:]:
    test_rerun[model]=test_rerun[model].rolling(window=20).mean()/1000

# Format the time accordingly
tr = np.arange(0, len(test_rerun["Time"])/10, 0.1)

# Visualize the rerun repeatability test
plt.plot(tr,test_rerun['Aluminium'], color = 'tab:grey',alpha=0.25, linestyle=(0,(1,1,1)),linewidth=2)
plt.plot(tr,test_rerun['SLA Prusa'], color = 'tab:grey',alpha=0.25, linestyle='dashdot')
plt.plot(tr,test_rerun['SLA Formlabs'], color = 'tab:grey',alpha=0.25, linestyle='dotted',linewidth=3)
plt.plot(tr,test_rerun['Ultimaker 0.10'],color = 'tab:grey',alpha=0.25, linestyle='dashed')
plt.plot(tr,test_rerun['Test1'],'red', label='Test 1')
plt.plot(tr,test_rerun['Test2'], color ='firebrick',label='Test 2')
plt.plot(tr,test_rerun['Test3'], color = 'darkred', label='Test 3')

plt.xlabel('Time (s)')
plt.ylabel('Pressure drop (MPa)')
plt.legend(loc=3)
plt.savefig('./figures/app_airchamber_rerun.pdf',bbox_inches = 'tight')
plt.clf()


# ### Reconnected

# Load the data for the reconnected repeatability test
test_reconnected=pd.read_csv(r'data/Resultaten_In_en_uit_elkaar_deel.csv', delimiter=";", header=1, names=(['Time',"Test1","Test2","Test3",'Aluminium','G','SLA Prusa','SLA Formlabs','Ultimaker 0.10']))

# Apply a rolling window for each type of additive manufacturing and convert pressure data to MPa
for model in list(test_reconnected.keys())[1:]:
    test_reconnected[model]=test_reconnected[model].rolling(window=20).mean()/1000

# Format the time accordingly
tr = np.arange(0, len(test_reconnected["Time"])/10, 0.1)

# Visualize the reconnected repeatability test
plt.plot(tr,test_reconnected['Aluminium'], color = 'tab:grey',alpha=0.25, linestyle=(0,(1,1,1)),linewidth=2)
plt.plot(tr,test_reconnected['SLA Prusa'], color = 'tab:grey',alpha=0.25, linestyle='dashdot')
plt.plot(tr,test_reconnected['SLA Formlabs'], color = 'tab:grey',alpha=0.25, linestyle='dotted',linewidth=3)
plt.plot(tr,test_reconnected['Ultimaker 0.10'],color = 'tab:grey',alpha=0.25, linestyle='dashed')
plt.plot(tr,test_reconnected['Test1'], color = 'skyblue', label='Test 1')
plt.plot(tr,test_reconnected['Test2'], color ='cornflowerblue',label='Test 2')
plt.plot(tr,test_reconnected['Test3'], color = 'steelblue', label='Test 3')

plt.xlabel('Time (s)')
plt.ylabel('Pressure drop (MPa)')
plt.legend(loc=3)
plt.savefig('./figures/app_airchamber_reconnected.pdf',bbox_inches = 'tight')
plt.clf()

print(f'\n ------ Succesfully saved all visualisations to /figures/ ------')
