#!/usr/bin/env python
# coding: utf-8

"""
In this script, the results of the friction tests are visualised.
All visualisations are stored in /figures/
"""

__author__ = "Eva Zillen"
__copyright__ = "Copyright 2021, TU Delft Biomechanical Design"
__credits__ = ["Eva Zillen, Heike Vallery, Gerwin Smit"]
__license__ = "CC0-1.0 License"
__version__ = "1.0.0"
__maintainer__ = "Eva Zillen"
__email__ = "e.zillen@student.tudelft.nl"

# Imports
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean

# Global variables

# The diameter (in m) of the pneumatic cylinder
d_25 = 25 / 1000
# The radius (in m) of the pneumatic cylinder
r_25 = d_25 / 2
# The surface area (in m^2) of the pneumatic cylinder
area = math.pi * r_25**2

# The diameter (in m) of the pneumatic cylinder for the X-ring and corresponding O-ring
d_257 = 25.7 / 1000
# The radius (in m) of the pneumatic cylinder for the X-ring and corresponding O-ring
r_257 = d_257 / 2
# The surface area (in m^2) of the pneumatic cylinder for the X-ring and corresponding O-ring
large_area = math.pi * r_257**2

# The models with different sealing mechanism used in this test
rings = ['O-ring','NAPN','NAP310','PK','KDN','O-ring257','X-ring257']
# The models with different cross-sectional shape used in this test
shapes = ['Circle','Stadium','Kidney','Stadium_lc','Kidney_lc']
# Remove first 15 data points to avoid deviating starting values
drop_amount = 15


# # Friction force test

# Define a dictionary to store all data from the friction force tests
# For each model all variables are stored in this nested dictionary
friction_force = {}

# For each ring type
for ring in rings:
    friction_force[ring] = {}
    for bar in [1,3,5,7]:
        # Load the data of the corresponding results in .CSV and drop unncessary columns
        ring_df = pd.read_csv(f'./data/friction/{ring}_{bar}bar.csv',delimiter='\s+',header=None,names=(['Time','A','B','C','Laser(mm)','Pressure(bar)','Force(N)']))
        ring_df.drop(columns=['A','B','C'],index=ring_df.index[range(drop_amount)],axis=1,inplace=True)

        # Store the data in our larger dictionary
        friction_force[ring][bar] = {}
        # Set the time (in s) and laser (in mm)
        friction_force[ring][bar]['Time'] = ring_df['Time']/1000
        friction_force[ring][bar]['Laser(mm)'] = ring_df['Laser(mm)']
        # Set the pressure (in MPa) and force (in N)
        friction_force[ring][bar]['Pressure(bar)'] = ring_df['Pressure(bar)']/10
        friction_force[ring][bar]['Force(N)'] = ring_df['Force(N)']

        # Calculate force Fp based on the measured pressure (see equation 2 in the report)
        # The 25.7 mm rings have a different and larger surface area
        if '257' in ring:
            Fp = ring_df['Pressure(bar)'] * 10**5 * large_area
        else:
            Fp = ring_df['Pressure(bar)'] * 10**5 * area

        # Calculate the friction force by substracting the measured force with Fp (see equation 3 in the report)
        FF = ring_df['Force(N)'] - Fp
        friction_force[ring][bar]['FrictionForce'] = FF
        friction_force[ring][bar]['FrictionFrom'] = FF[FF>FF.mean()].mean()
        friction_force[ring][bar]['FrictionTo'] = FF[FF<FF.mean()].mean()

# For each shape type
for shape in shapes:
    friction_force[shape] = {}
    for bar in [1,2,3,4,5,6,7]:
        # Some shapes extrude at higher pressure, no data is available for them
        if bar > 3 and shape not in ['Stadium_lc','Kidney_lc','Kidney', 'Circle']:
            break
        if bar > 4 and shape not in ['Stadium_lc', 'Kidney_lc', 'Circle']:
            break
        if bar > 5 and shape not in ['Kidney_lc', 'Circle']:
            break
        # Load the data of the corresponding results in .CSV and drop unncessary columns
        shape_df = pd.read_csv(f'./data/friction/{shape}_{bar}bar.csv',delimiter='\s+',header=None,names=(['Time','A','B','C','Laser(mm)','Pressure(bar)','Force(N)']))
        shape_df.drop(columns=['A','B','C'],index=shape_df.index[range(drop_amount)],axis=1,inplace=True)

        # Store the data in our larger dictionary
        friction_force[shape][bar] = {}
        # Set the time (in s) and laser (in mm)
        friction_force[shape][bar]['Time'] = shape_df['Time']/1000
        friction_force[shape][bar]['Laser(mm)'] = shape_df['Laser(mm)']
        # Set the pressure (in MPa) and force (in N)
        friction_force[shape][bar]['Pressure(bar)'] = shape_df['Pressure(bar)']/10
        friction_force[shape][bar]['Force(N)'] = shape_df['Force(N)']

        # Calculate force Fp based on the measured pressure (see equation 2 in the report)
        Fp = shape_df['Pressure(bar)'] * 10**5 * area

        # Calculate the friction force by substracting the measured force with Fp (see equation 3 in the report)
        FF = shape_df['Force(N)'] - Fp
        friction_force[shape][bar]['FrictionForce'] = FF
        friction_force[shape][bar]['FrictionFrom'] = FF[FF>FF.mean()].mean()
        friction_force[shape][bar]['FrictionTo'] = FF[FF<FF.mean()].mean()


# #### Friction force range definement plot - visual for in methodology

plt.annotate(text='',xy=(12,friction_force['O-ring'][1]['FrictionFrom']), xytext=(12,friction_force['O-ring'][1]['FrictionTo']), arrowprops=dict(arrowstyle='<->', lw=2))
plt.hlines(xmin=0, xmax=70,y=friction_force['O-ring'][1]['FrictionFrom'], linestyles='dashed', colors='0', lw=2)
plt.hlines(xmin=0, xmax=70,y=friction_force['O-ring'][1]['FrictionTo'], linestyles='dashed', colors='0', lw=2)
plt.plot(friction_force['O-ring'][1]['Time'],friction_force['O-ring'][1]['FrictionForce'],'tab:blue',label='O-ring')
plt.plot(friction_force['NAPN'][1]['Time'],friction_force['NAPN'][1]['FrictionForce'],'tab:orange',alpha=0.25,label='NAPN')
plt.plot(friction_force['NAP310'][1]['Time'],friction_force['NAP310'][1]['FrictionForce'],'tab:green',alpha=0.25,label='NAP 330')
plt.plot(friction_force['PK'][1]['Time'],friction_force['PK'][1]['FrictionForce'],'tab:red',alpha=0.25,label='PK')
plt.plot(friction_force['KDN'][1]['Time'],friction_force['KDN'][1]['FrictionForce'],'tab:purple', alpha=0.25,label='KDN')

plt.xlim([5,15])
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.legend(loc='lower center',bbox_to_anchor=(0.5,-0.3),ncol=5)
plt.savefig('./figures/method_frictionforce_1bar_zoom.pdf',bbox_inches = 'tight')
plt.clf()


# #### Standard deviation & Standard error

# Function to calculate standard error for a specific test
def calculate_se(friction_force,model,bar):
    # Calculate the mean to define retracting and extending parts
    frictionforce_mean = friction_force[model][bar]['FrictionForce'].mean()
    # Variable to store the friction force
    frictionforce = list(friction_force[model][bar]['FrictionForce'])
    # Variables for results and counter
    frictionforce_se_means = []
    i = 0

    # Loop through the data and break them up into separate tests
    while i < len(frictionforce) - 1:
        # Lists for retracting and extending parts of a single test
        retracting = []
        extending = []

        # First the retracting part of a test is done
        # Get all values above the mean
        while len(retracting) < 100 or frictionforce[i] > frictionforce_mean:
            retracting.append(frictionforce[i])
            i += 1
            # Break if it gets below the mean
            if i > len(frictionforce) - 1:
                break

        # Secondly the extending part of a test is done
        # Get all values below the mean
        while len(extending) < 100 or frictionforce[i] < frictionforce_mean:
            extending.append(frictionforce[i])
            i += 1
            # Break if it gets above the mean
            if i > len(frictionforce) - 1:
                break

        # The friction force range is defined as the difference between the mean friction force of the retracting and extending strokes
        frictionforce_se_means.append(mean(retracting)-mean(extending))

    # Standard error is calculated by the standard deviation of the means
    # Also return the mean of the friction force ranges across the tests
    # Finally return the last test to determine the standard deviation of one extending and retracting stroke
    return mean(frictionforce_se_means),np.std(frictionforce_se_means),extending,retracting

# For each model use the calculate_se() function to acquire the friction force range and the standard error
# Additionally for each of the rings and shapes the standard deviation of a single test is saved
std_single_test_rings = pd.DataFrame(columns=['Bar']+rings)
std_single_test_rings = std_single_test_rings.set_index('Bar')

for ring in rings:
    for bar in [1,3,5,7]:
        mean_ff,se_ff,extending,retracting = calculate_se(friction_force,ring,bar)
        friction_force[ring][bar]['SE_FrictionForce'] = se_ff
        friction_force[ring][bar]['Mean_FrictionForce'] = mean_ff

        # For each retracting and extending test, check if the index already exists
        if str(bar)+'_bar_retracting' not in list(std_single_test_rings.index):
            std_single_test_rings = std_single_test_rings.append(pd.Series(name= str(bar)+'_bar_retracting'))
        if str(bar)+'_bar_extending' not in list(std_single_test_rings.index):
            std_single_test_rings = std_single_test_rings.append(pd.Series(name= str(bar)+'_bar_extending'))

        # For each individual test save the average and standard deviation
        std_single_test_rings.loc[str(bar)+'_bar_retracting'][ring] = f'{str(round(mean(retracting),2))} $\pm$ {round(np.std(retracting),2)}'
        std_single_test_rings.loc[str(bar)+'_bar_extending'][ring] = f'{str(round(mean(extending),2))} $\pm$ {round(np.std(extending),2)}'

# Again define a dataframe to store the standard deviations of each single test
std_single_test_shapes = pd.DataFrame(columns=['Bar']+shapes)
std_single_test_shapes = std_single_test_shapes.set_index('Bar')
for shape in shapes:
    for bar in [1,2,3,4,5,6,7]:
        try:
            mean_ff,se_ff,extending,retracting = calculate_se(friction_force,shape,bar)
            friction_force[shape][bar]['SE_FrictionForce'] = se_ff
            friction_force[shape][bar]['Mean_FrictionForce'] = mean_ff

            # For each retracting and extending test, check if the index already exists
            if str(bar)+'_bar_retracting' not in list(std_single_test_shapes.index):
                std_single_test_shapes = std_single_test_shapes.append(pd.Series(name= str(bar)+'_bar_retracting'))
            if str(bar)+'_bar_extending' not in list(std_single_test_shapes.index):
                std_single_test_shapes = std_single_test_shapes.append(pd.Series(name= str(bar)+'_bar_extending'))

            # For each test save the average and standard deviation
            std_single_test_shapes.loc[str(bar)+'_bar_retracting'][shape] = f'{str(round(mean(retracting),2))} $\pm$ {round(np.std(retracting),2)}'
            std_single_test_shapes.loc[str(bar)+'_bar_extending'][shape] = f'{str(round(mean(extending),2))} $\pm$ {round(np.std(extending),2)}'

        except Exception as e:
            print(f'No data for {shape} - {e} bar due to extrusion of the O-ring')

print(std_single_test_rings)
# print(std_single_test_rings.to_latex(escape=False))

print(std_single_test_shapes)
# print(std_single_test_shapes.to_latex(escape=False))


# #### Friction force range plot 25mm

# Variables to make plotting of friction force range with standard error more clear
fr = {'Pressure': [.1,.3,.5,.7],
     'O_ring': [friction_force['O-ring'][i]['Mean_FrictionForce'] for i in friction_force['O-ring']],
     'NAPN': [friction_force['NAPN'][i]['Mean_FrictionForce'] for i in friction_force['NAPN']],
     'NAP310': [friction_force['NAP310'][i]['Mean_FrictionForce'] for i in friction_force['NAP310']],
     'PK': [friction_force['PK'][i]['Mean_FrictionForce'] for i in friction_force['PK']],
     'KDN': [friction_force['KDN'][i]['Mean_FrictionForce'] for i in friction_force['KDN']],
     'O_ring257': [friction_force['O-ring257'][i]['Mean_FrictionForce'] for i in friction_force['O-ring257']],
     'X_ring257': [friction_force['X-ring257'][i]['Mean_FrictionForce'] for i in friction_force['X-ring257']],
    }
fr = pd.DataFrame(data=fr)

se = {'Pressure': [.1,.3,.5,.7],
     'O_ring': [friction_force['O-ring'][i]['SE_FrictionForce'] for i in friction_force['O-ring']],
     'NAPN': [friction_force['NAPN'][i]['SE_FrictionForce'] for i in friction_force['NAPN']],
     'NAP310': [friction_force['NAP310'][i]['SE_FrictionForce'] for i in friction_force['NAP310']],
     'PK': [friction_force['PK'][i]['SE_FrictionForce'] for i in friction_force['PK']],
     'KDN': [friction_force['KDN'][i]['SE_FrictionForce'] for i in friction_force['KDN']],
     'O_ring257': [friction_force['O-ring257'][i]['SE_FrictionForce'] for i in friction_force['O-ring257']],
     'X_ring257': [friction_force['X-ring257'][i]['SE_FrictionForce'] for i in friction_force['X-ring257']],
    }
se = pd.DataFrame(data=se)

# Visualize the friction force range - 25 mm cylinder
plt.errorbar(fr.Pressure,fr.O_ring257,se.O_ring257,color='tab:blue',alpha=0.25, linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.X_ring257,se.X_ring257,color='tab:brown',alpha=0.25,linestyle=(0,(5,2,2)),capsize=2)
plt.errorbar(fr.Pressure,fr.O_ring,se.O_ring,color='tab:blue',label='O-ring', linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.NAPN,se.NAPN,color='tab:orange',label='NAPN',linestyle='dashdot',capsize=2)
plt.errorbar(fr.Pressure,fr.NAP310,se.NAP310,color='tab:green',label='NAP310', linestyle=(0,(5,2,2)),capsize=2)
plt.errorbar(fr.Pressure,fr.PK,se.PK,color='tab:red',label='PK',linestyle='dashed',capsize=2)
plt.errorbar(fr.Pressure,fr.KDN,se.KDN,color='tab:purple',label='KDN',linewidth=1,capsize=2)

plt.xlabel('Pressure (MPa)')
plt.ylabel('Dynamic friction force range (N)')
plt.legend()
plt.savefig('./figures/result_frictionforcerange_25mm.pdf',bbox_inches = 'tight')
plt.clf()


# #### Friction force range plot 25.7mm

# Visualize the friction force range - 25.7 mm cylinder
plt.errorbar(fr.Pressure,fr.O_ring,se.O_ring,color='tab:blue',alpha=0.25, linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.NAPN,se.NAPN,color='tab:orange',alpha=0.25,linestyle='dashdot',capsize=2)
plt.errorbar(fr.Pressure,fr.NAP310,se.NAP310,color='tab:green',alpha=0.25, linestyle=(0,(5,2,2)),capsize=2)
plt.errorbar(fr.Pressure,fr.PK,se.PK,color='tab:red',alpha=0.25,linestyle='dashed',capsize=2)
plt.errorbar(fr.Pressure,fr.KDN,se.KDN,color='tab:purple',alpha=0.25,linewidth=1,capsize=2)
plt.errorbar(fr.Pressure,fr.O_ring257,se.O_ring257,color='tab:blue',label='O-ring', linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.X_ring257,se.X_ring257,color='tab:brown',label='X-ring',linestyle=(0,(5,2,2)),capsize=2)

plt.xlabel('Pressure (MPa)')
plt.ylabel('Dynamic friction force range (N)')
plt.legend()
plt.savefig('./figures/result_frictionforcerange_257mm.pdf',bbox_inches = 'tight')
plt.clf()


# ####  Friction force range plot different shapes

# Again variables to make plotting of friction force range with standard error more clear
fr_s = {'Pressure': [.1,.2,.3],
     'Stadium': [friction_force['Stadium'][i]['Mean_FrictionForce'] for i in friction_force['Stadium']],
    }
fr_s = pd.DataFrame(data=fr_s)

se_s = {'Pressure': [.1,.2,.3],
     'Stadium': [friction_force['Stadium'][i]['SE_FrictionForce'] for i in friction_force['Stadium']],
    }
se_s = pd.DataFrame(data=se_s)

fr_ck = {'Pressure': [.1,.2,.3,.4],
      'Circle': [friction_force['Circle'][i]['Mean_FrictionForce'] for i in friction_force['Circle']][:4],
      'Kidney': [friction_force['Kidney'][i]['Mean_FrictionForce'] for i in friction_force['Kidney']],
    }
fr_ck = pd.DataFrame(data=fr_ck)

se_ck = {'Pressure': [.1,.2,.3,.4],
     'Circle': [friction_force['Circle'][i]['SE_FrictionForce'] for i in friction_force['Circle']][:4],
     'Kidney': [friction_force['Kidney'][i]['SE_FrictionForce'] for i in friction_force['Kidney']],
    }
se_ck = pd.DataFrame(data=se_ck)

# Visualize the friction force range - different shapes
plt.errorbar(fr_ck.Pressure,fr_ck.Circle,se_ck.Circle,color='0.8',label='Circle',linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr_s.Pressure,fr_s.Stadium,se_s.Stadium,color='tab:olive', label='Stadium',linestyle='dashdot',capsize=2)
plt.errorbar(fr_ck.Pressure,fr_ck.Kidney,se_ck.Kidney,color='tab:cyan', label='Kidney',capsize=2)

plt.xlabel('Pressure (MPa)')
plt.ylabel('Dynamic friction force range (N)')
plt.legend(loc='lower center',bbox_to_anchor=(0.5,-0.3),ncol=3)
plt.savefig('./figures/result_frictionforcerange_shape.pdf',bbox_inches = 'tight')
plt.clf()


# ####  Friction force range plot different shapes with lower clearance

# Again variables to make plotting of friction force range with standard error more clear
fr_s_lc = {'Pressure': [.1,.2,.3,.4,.5],
     'Stadium_lc': [friction_force['Stadium_lc'][i]['Mean_FrictionForce'] for i in friction_force['Stadium_lc']],
    }
fr_s_lc = pd.DataFrame(data=fr_s_lc)

se_s_lc = {'Pressure': [.1,.2,.3,.4,.5],
     'Stadium_lc': [friction_force['Stadium_lc'][i]['SE_FrictionForce'] for i in friction_force['Stadium_lc']],
    }
se_s_lc = pd.DataFrame(data=se_s_lc)

fr_lc = {'Pressure': [.1,.2,.3,.4,.5,.6,.7],
      'Kidney_lc': [friction_force['Kidney_lc'][i]['Mean_FrictionForce'] for i in friction_force['Kidney_lc']],
      'Circle': [friction_force['Circle'][i]['Mean_FrictionForce'] for i in friction_force['Circle']],
    }
fr_lc = pd.DataFrame(data=fr_lc)

se_lc = {'Pressure': [.1,.2,.3,.4,.5,.6,.7],
      'Kidney_lc': [friction_force['Kidney_lc'][i]['SE_FrictionForce'] for i in friction_force['Kidney_lc']],
      'Circle': [friction_force['Circle'][i]['SE_FrictionForce'] for i in friction_force['Circle']],
    }
se_lc = pd.DataFrame(data=se_lc)

# Visualize the friction force range - different shapes low clearance
plt.errorbar(fr_s.Pressure,fr_s.Stadium,se_s.Stadium,linestyle='dashdot',color='tab:olive', alpha=0.5, label='Stadium 0.5 mm clearance',capsize=2)
plt.errorbar(fr_ck.Pressure,fr_ck.Kidney,se_ck.Kidney,color='tab:cyan', alpha=0.5, label='Kidney 0.5 mm clearance',capsize=2)
plt.errorbar(fr_lc.Pressure,fr_lc.Circle,se_lc.Circle,linestyle='dotted',color='0.8', alpha=0.5, label='Circle 0.5 mm clearance',linewidth = 2, capsize=2)
plt.errorbar(fr_s_lc.Pressure,fr_s_lc.Stadium_lc,se_s_lc.Stadium_lc,linestyle='dashdot',color='tab:olive', label='Stadium 0.2 mm clearance', linewidth = 2,capsize=2)
plt.errorbar(fr_lc.Pressure,fr_lc.Kidney_lc,se_lc.Kidney_lc,color='tab:cyan', label='Kidney 0.2 mm clearance', linewidth = 2,capsize=2)

plt.xlabel('Pressure (MPa)')
plt.ylabel('Dynamic friction force range (N)')
plt.legend(loc='lower center',bbox_to_anchor=(0.5,-0.42),ncol=2)
plt.savefig('./figures/app_frictionforcerange_shapes_lc.pdf',bbox_inches = 'tight')
plt.clf()


# # Repeatablilty

# We performed two repeatability tests
# - The test was rerun without any changes in the connections (rerun)
# - The model was reconnected prior to taking the tests (reconnected)

# ### Rerun

# Define a dictionary to store all data from the repeated test for O-ring 25.7 mm
# For each model all variables are stored in this nested dictionary
friction_rerun = {}

# For each repeated test
for test in range(1,4):
    friction_rerun[test] = {}
    for bar in [1,3,5,7]:
        # Load the data of the corresponding results in .CSV and drop unncessary columns
        test_df = pd.read_csv(f'./data/repeatability/rerun/friction/{test}_O-ring257_{bar}bar.csv',delimiter='\s+',header=None,names=(['Time','A','B','C','Laser(mm)','Pressure(bar)','Force(N)']))
        test_df.drop(columns=['A','B','C'],index=test_df.index[range(drop_amount)],axis=1,inplace=True)

        # Store the data in our larger dictionary
        friction_rerun[test][bar] = {}
        # Set the time (in s) and laser (in mm)
        friction_rerun[test][bar]['Time'] = test_df['Time']/1000
        friction_rerun[test][bar]['Laser(mm)'] = test_df['Laser(mm)']
        # Set the pressure (in MPa) and force (in N)
        friction_rerun[test][bar]['Pressure(bar)'] = test_df['Pressure(bar)']/10
        friction_rerun[test][bar]['Force(N)'] = test_df['Force(N)']

        # Calculate force Fp based on the measured pressure
        # The 25.7 mm rings have a different and larger surface area (see equation 2 in the report)
        Fp = test_df['Pressure(bar)'] * 10**5 * large_area

        # Calculate the friction force by substracting the measured force with Fp (see equation 3 in the report)
        friction_rerun[test][bar]['FrictionForce'] = test_df['Force(N)'] - Fp

# For each test use the calculate_se() function to acquire the mean friction force and standard error
for test in range(1,4):
    for bar in [1,3,5,7]:
        mean_ff,se_ff,_,_ = calculate_se(friction_rerun,test,bar)
        friction_rerun[test][bar]['SE_FrictionForce'] = se_ff
        friction_rerun[test][bar]['Mean_FrictionForce'] = mean_ff

# Again variables to make plotting of friction force range with standard error more clear
fr_rerun = {'Pressure': [.1,.3,.5,.7],
     1: [friction_rerun[1][i]['Mean_FrictionForce'] for i in friction_rerun[1]],
     2: [friction_rerun[2][i]['Mean_FrictionForce'] for i in friction_rerun[2]],
     3: [friction_rerun[3][i]['Mean_FrictionForce'] for i in friction_rerun[3]],
    }
fr_rerun = pd.DataFrame(data=fr_rerun)

se_rerun = {'Pressure': [.1,.3,.5,.7],
     1: [friction_rerun[1][i]['SE_FrictionForce'] for i in friction_rerun[1]],
     2: [friction_rerun[2][i]['SE_FrictionForce'] for i in friction_rerun[2]],
     3: [friction_rerun[3][i]['SE_FrictionForce'] for i in friction_rerun[3]],
    }
se_rerun = pd.DataFrame(data=se_rerun)

# Visualize the repeated tests with all other models for clarity
plt.errorbar(fr.Pressure,fr.O_ring257,se.O_ring257,color='tab:grey',alpha=0.25, linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.X_ring257,se.X_ring257,color='tab:grey',alpha=0.25,linestyle=(0,(5,2,2)),capsize=2)
plt.errorbar(fr.Pressure,fr.O_ring,se.O_ring,color='tab:grey',alpha=0.25,linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.NAPN,se.NAPN,color='tab:grey',alpha=0.25,linestyle='dashdot',capsize=2)
plt.errorbar(fr.Pressure,fr.NAP310,se.NAP310,color='tab:grey',alpha=0.25, linestyle=(0,(5,2,2)),capsize=2)
plt.errorbar(fr.Pressure,fr.PK,se.PK,color='tab:grey',alpha=0.25,linestyle='dashed',capsize=2)
plt.errorbar(fr.Pressure,fr.KDN,se.KDN,color='tab:grey',alpha=0.25,linewidth=1,capsize=2)

plt.errorbar(fr_rerun.Pressure,fr_rerun[1],se_rerun[1],color='red',label='Test 1',capsize=2)
plt.errorbar(fr_rerun.Pressure,fr_rerun[2],se_rerun[2],color='firebrick',label='Test 2',capsize=2)
plt.errorbar(fr_rerun.Pressure,fr_rerun[3],se_rerun[3],color='darkred',label='Test 3',capsize=2)

plt.xlabel('Pressure (MPa)')
plt.ylabel('Dynamic friction force range (N)')
plt.legend()
plt.savefig('./figures/app_frictionforcerange_rerun.pdf',bbox_inches = 'tight')
plt.clf()

# ### Reconnected

# Define a dictionary to store all data from the repeated test for O-ring 25.7 mm
# For each model all variables are stored in this nested dictionary
friction_reconnected = {}

# For each repeated test
for test in range(1,4):
    friction_reconnected[test] = {}
    for bar in [1,3,5,7]:
        # Load the data of the corresponding results in .CSV and drop unncessary columns
        test_df = pd.read_csv(f'./data/repeatability/reconnected/friction/{test}_O-ring257_{bar}bar.csv',delimiter='\s+',header=None,names=(['Time','A','B','C','Laser(mm)','Pressure(bar)','Force(N)']))
        test_df.drop(columns=['A','B','C'],index=test_df.index[range(drop_amount)],axis=1,inplace=True)

        # Store the data in our larger dictionary
        friction_reconnected[test][bar] = {}
        # Set the time (in s) and laser (in mm)
        friction_reconnected[test][bar]['Time'] = test_df['Time']/1000
        friction_reconnected[test][bar]['Laser(mm)'] = test_df['Laser(mm)']
        # Set the pressure (in MPa) and force (in N)
        friction_reconnected[test][bar]['Pressure(bar)'] = test_df['Pressure(bar)']/10
        friction_reconnected[test][bar]['Force(N)'] = test_df['Force(N)']

        # Calculate force Fp based on the measured pressure
        # The 25.7 mm rings have a different and larger surface area (see equation 2 in the report)
        Fp = test_df['Pressure(bar)'] * 10**5 * large_area

        # Calculate the friction force by substracting the measured force with Fp (see equation 3 in the report)
        friction_reconnected[test][bar]['FrictionForce'] = test_df['Force(N)'] - Fp


# For each test use the calculate_se() function to acquire the mean friction force and standard error
for test in range(1,4):
    for bar in [1,3,5,7]:
        mean_ff,se_ff,_,_ = calculate_se(friction_reconnected,test,bar)
        friction_reconnected[test][bar]['SE_FrictionForce'] = se_ff
        friction_reconnected[test][bar]['Mean_FrictionForce'] = mean_ff

# Again variables to make plotting of friction force range with standard error more clear
fr_reconnected = {'Pressure': [.1,.3,.5,.7],
     1: [friction_reconnected[1][i]['Mean_FrictionForce'] for i in friction_reconnected[1]],
     2: [friction_reconnected[2][i]['Mean_FrictionForce'] for i in friction_reconnected[2]],
     3: [friction_reconnected[3][i]['Mean_FrictionForce'] for i in friction_reconnected[3]],
    }
fr_reconnected = pd.DataFrame(data=fr_reconnected)

se_reconnected = {'Pressure': [.1,.3,.5,.7],
     1: [friction_reconnected[1][i]['SE_FrictionForce'] for i in friction_reconnected[1]],
     2: [friction_reconnected[2][i]['SE_FrictionForce'] for i in friction_reconnected[2]],
     3: [friction_reconnected[3][i]['SE_FrictionForce'] for i in friction_reconnected[3]],
    }
se_reconnected = pd.DataFrame(data=se_reconnected)

# Visualize the repeated tests with all other models for clarity
plt.errorbar(fr.Pressure,fr.O_ring257,se.O_ring257,color='tab:grey',alpha=0.25, linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.X_ring257,se.X_ring257,color='tab:grey',alpha=0.25,linestyle=(0,(5,2,2)),capsize=2)
plt.errorbar(fr.Pressure,fr.O_ring,se.O_ring,color='tab:grey',alpha=0.25,linestyle='dotted',linewidth=2,capsize=2)
plt.errorbar(fr.Pressure,fr.NAPN,se.NAPN,color='tab:grey',alpha=0.25,linestyle='dashdot',capsize=2)
plt.errorbar(fr.Pressure,fr.NAP310,se.NAP310,color='tab:grey',alpha=0.25, linestyle=(0,(5,2,2)),capsize=2)
plt.errorbar(fr.Pressure,fr.PK,se.PK,color='tab:grey',alpha=0.25,linestyle='dashed',capsize=2)
plt.errorbar(fr.Pressure,fr.KDN,se.KDN,color='tab:grey',alpha=0.25,linewidth=1,capsize=2)

plt.errorbar(fr_reconnected.Pressure,fr_reconnected[1],se_reconnected[1],color='skyblue',label='Test 1',capsize=2)
plt.errorbar(fr_reconnected.Pressure,fr_reconnected[2],se_reconnected[2],color='cornflowerblue',label='Test 2',capsize=2)
plt.errorbar(fr_reconnected.Pressure,fr_reconnected[3],se_reconnected[3],color='steelblue',label='Test 3',capsize=2)

plt.xlabel('Pressure (MPa)')
plt.ylabel('Dynamic friction force range (N)')
plt.legend()
plt.savefig('./figures/app_frictionforcerange_reconnected.pdf',bbox_inches = 'tight')
plt.clf()


# # Velocity calculation

# To fairly compare the calculated friction force range to the friction force of conventional pneumatic actuators, we have to take the velocity of the piston into account. For this we calculate the velocity of the piston during the tests.
# We will only calculate the speeds for specifically the O-ring - 3 bar
time = list(friction_force['O-ring'][3]['Time'])
laser = list(friction_force['O-ring'][3]['Laser(mm)'])

# Boolean variables to keep track of which peak we are looking for next (low or high)
high_peak_found = False
low_peak_found = False

# The peaks will be stored in lists as tuples
high_peaks = []
low_peaks = []

# For each distance measured by the laser, find both peaks
for cur_distance in range(0,len(laser)):
    # Get the previous and next distance points of the laser
    previous_distances = laser[cur_distance-20:cur_distance]
    next_distances = laser[cur_distance:cur_distance+20]

    # Make sure both lists are not empty
    if previous_distances != [] and next_distances != []:
        # A peak can be found if the distance is higher (or lower) than all the surrounding distances
        if (all(laser[cur_distance] >= i for i in previous_distances) and all(laser[cur_distance] >= i for i in next_distances)) == True and high_peak_found == False:
            # If this is true, add the distance and time to our list
            high_peaks.append((laser[cur_distance], time[cur_distance]))
            # A high peak has been found, next will be a low peak
            high_peak_found = True
            low_peak_found = False
        # The next peak can be found if the distance is higher (or lower) than all the surrounding distances
        if (all(laser[cur_distance] <= i for i in previous_distances) and all(laser[cur_distance] <= i for i in next_distances)) == True and low_peak_found == False:
            low_peaks.append((laser[cur_distance], time[cur_distance]))
            low_peak_found = True
            high_peak_found = False

# List to store extending speeds for each run
extending_speeds = []
# For each high peak, calculate the speed
for i in range(0, len(high_peaks)):
    # Delta distance (in mm) is the difference between the high peak and next low peak
    delta_distance = high_peaks[i][0] - low_peaks[i][0]
    # Same goes for the time (in s)
    delta_time = high_peaks[i][1] - low_peaks[i][1]
    # Calculate speed (in mm/s)
    speed = delta_distance/delta_time
    # Add speed to our list
    extending_speeds.append(speed)

# List to store extending speeds for each run
retracting_speeds = []
# For each low peak, calculate the speed
for i in range(0, len(low_peaks)-1):
    # Delta distance (in mm) is the difference between the low peak and next high peak (therefore +1)
    delta_distance = low_peaks[i][0] - high_peaks[i+1][0]
    # Same goes for the time (in s)
    delta_time =  low_peaks[i][1] - high_peaks[i+1][1]
    # Calculate speed (in mm/s)
    speed = delta_distance/delta_time
    # Add speed to our list
    retracting_speeds.append(speed)

print(f'\nAverage extending speed at a pressure of 0.3MPa: {mean(extending_speeds)} mm/s')
print(f'Average retracting speed at a pressure of 0.3MPa: {mean(retracting_speeds)} mm/s')

print(f'\n ------ Succesfully saved all visualisations to /figures/ ------')
