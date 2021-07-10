#!/usr/bin/env python
# coding: utf-8

"""
In this script, the variable dimensions of our models are determined.
In the first part we calculate the piston sealing grooves.
Secondly, the dimensions of the non-circular shapes are determined.
"""

__author__ = "Eva Zillen"
__copyright__ = "Copyright 2021, TU Delft Biomechanical Design"
__credits__ = ["Eva Zillen, Heike Vallery, Gerwin Smit"]
__license__ = "CC0-1.0 License"
__version__ = "1.0.0"
__maintainer__ = "Eva Zillen"
__email__ = "e.zillen@student.tudelft.nl"


# # Definitions

# ## Imports
import numpy as np
import math
from sympy import symbols, Eq, solve, pi

# ## Functions

def calculate_groove(ID,S,r_sq,C):
    # Determine the outer diameter of the O-ring
    OD = ID+2*S
    # Determine the squeeze dimension of the O-ring
    S_sq = S * (1 - r_sq)
    # Determine the pison groove diameter
    D_PG = OD - 2 * S_sq
    # Set the width of the piston groove
    W_PG = S + 1
    # Determine the piston diameter
    P_D = OD - 2 * C
    return f'\nOuter diameter O-ring: {OD} mm \nPiston diameter: {P_D} mm \nPiston groove diameter: {D_PG} mm \nWidth piston groove: {round(W_PG,2)} mm\n'


# # Determining the dimensions of the O-ring groove

# #### O-ring Lidl, SLA print

# The O-ring used had the dimensions (18x3.5)
ID = 18
S = 3.5
# A clearance of 0.5 mm was used between the piston and the cylinder
C = 0.5
# 10% squeeze ration was used in this study
r_sq = 0.1

print ("O-ring Lidl, 18*3.5")
print(calculate_groove(ID,S,r_sq,C))

print('------------------')

# #### O-ring en X-ring Eriks

# The O-ring used had the dimensions (18.64x3.53)
ID = 18.64
S = 3.53
# A clearance of 0.5 mm was used between the piston and the cylinder
C = 0.5
# 10% squeeze ration was used in this study
r_sq = 0.1

print ("O-ring and X-ring Eriks, 18.64*3.53")
print(calculate_groove(ID,S,r_sq,C))

print('------------------')
# # Determining the dimensions of the non-conventional cylinders

# ### Stadium shape

def stadium(ID,S):
    # Variables defining the stadium shape (see Figure 2 in report)
    L = symbols('L')
    D = 0

    # Target area - the area of the circular shape with diameter = 25 mm
    A_target = math.pi * (25/2)**2
    # Determine the outer diameter of the O-ring
    OD = ID + 2 * S
    # Determine the perimeter of the O-ring
    P_c = math.pi * OD

    # Variable necessary to perform the optimization
    A_s = 0

    # To find the variables D & L we use for the stadium surface area (A_s) and the perimeter (P_s) equations
    # Optimization is done by varying D and finding corresponding L
    for D_optimize in np.arange(5,20,0.1):
        # Variables necessary for optimization, to remember the previous values
        previous_A_s = A_s
        previous_L = L
        previous_D = D

        # L is reset each round, define it again
        L = symbols('L')

        # Rounding necessary for limitations on floating point numbers in Python
        D = round(D_optimize,2)

        # Solve for the perimeter
        P_s_eq = (math.pi * D) + 2 * L - P_c
        result = solve((P_s_eq), (L))

        # Solving returns a list, L is the only value in this list
        L = result[0]

        # Applying the equation for the surface area
        A_s = math.pi * (D/2)**2 + L * D

        # Finding the right value: if the surface area is larger than the target area, take the previous and continue
        if previous_A_s <= A_target and A_s >= A_target:
            print(f"Optimizing found: \narea = {previous_A_s} with D = {previous_D} and L = {previous_L} is closest to the target surface area of {A_target}")
            break

    return previous_D,previous_L

# Example calculations for an O-ring of 22x3.5mm
ID = 22
S = 3.5
D, L = stadium(ID,S)
print(f"\n--------------------------------------")
print(f"Resulting values for an stadium shape with O-ring of {ID} x {S} mm")
print(f"D = {D} mm")
print(f"L = {L} mm")
print(f"--------------------------------------")


# ### Kidney shape

def optimize_range(ID, S, gamma):
    # Variables defining the kidney shape (see Figure 2 in report)
    r = symbols('r')
    a = 0

    # Target area - the area of the circular shape with diameter = 25 mm
    A_target = math.pi*(25/2)**2
    # Determine the outer diameter of the O-ring
    OD = ID+2*S
    # Determine the perimeter of the O-ring
    P_c = math.pi*OD

    # Variable necessary to perform the optimization
    A_k = 0

    # To find the variables r & a we use the stadium surface area (A_k) and the perimeter (P_k) equations
    # Optimization is done by varying a and finding corresponding r
    for a_optimize in np.arange(5,20,0.1):
        # Variables necessary for optimization, to remember the previous values
        previous_A_k = A_k
        previous_r = r
        previous_a = a

        # L is reset each round, define it again
        r = symbols('r')

        # Rounding necessary for limitations on floating point numbers in Python
        a = round(a_optimize,2)

        # Solve for the perimeter
        P_k_eq = math.pi* a +(gamma*(2 * r + a)) - P_c
        result = solve((P_k_eq), (r))

        # Solving returns a list, L is the only value in this list
        r = result[0]

        # Applying the equation for the surface area
        A_k = math.pi * (a / 2)**2 + (gamma * (r * a + (a**2 / 2)))

        # Finding the right value: if the surface area is larger than the target area, take the previous and continue
        if previous_A_k <= A_target and A_k >= A_target:
            print(f"Optimizing found:\narea = {previous_A_k} with a = {previous_a} and r = {previous_r} is closest to the target surface area of {A_target}")
            break

    return previous_a,previous_r

# Example calculations for an O-ring of 22x3.5mm
ID = 22
S = 3.5
gamma = 100/180*math.pi

a, r = optimize_range(ID, S, gamma)
print(f"\n--------------------------------------")
print(f"Resulting values for a kidney shape with O-ring of {ID} x {S} mm")
print(f"a = {a} mm")
print(f"r = {r} mm")
print(f"--------------------------------------")
