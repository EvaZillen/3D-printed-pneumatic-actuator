#!/usr/bin/env python
# coding: utf-8

# # Definitions

# ## Imports
import numpy as np
import math
from sympy import symbols, Eq, solve, pi


# ## Functions

def calculate_groove(inner_diameter_o_ring,section_o_ring,clearance,squeeze_ratio):
    outer_diameter_o_ring = inner_diameter_o_ring+2*section_o_ring
    inner_diameter_cylinder = outer_diameter_o_ring
    outer_diameter_piston = inner_diameter_cylinder - 2*clearance

    section_o_ring_squeezed = (1-squeeze_ratio) * section_o_ring
    depth_notch = section_o_ring_squeezed-clearance
    width_notch = section_o_ring + 1
    return f'\nInner diameter cylinder:{inner_diameter_cylinder} mm \nOuter diameter piston:{outer_diameter_piston} mm \nDepth notch:{depth_notch} mm \nWidth notch:{width_notch} mm'


# # Determining the dimensions of the O-ring groove 

# #### O-ring Lidl, SLA print
diameter_oring = 18
o_ring_thickness = 3.5
clearance = 0.5
squeeze_ratio = 0.1
print ("O-ring Lidl, 18*3.5")
print(calculate_groove(diameter_oring,o_ring_thickness,clearance,squeeze_ratio))


# #### O-ring en X-ring Eriks
diameter_oring = 18.64
o_ring_thickness = 3.53
clearance = 0.5
squeeze_ratio = 0.1
print("O-ring en X-ring Eriks, 18.64*3.53") 
print(f"{calculate_groove(diameter_oring,o_ring_thickness,clearance,squeeze_ratio)}\n")


# # Determining the dimensions of the non-conventional cylinders

# ## Oval shape
def ovaal(inner_diameter_o_ring,o_ring_thickness):
    print("Calculating results for oval shape, this might take up to 30s")
    
    # Define constants
    L = symbols('L')
    area = 0
    D = 0
    target_surface_area = math.pi*(25/2)**2 
    outer_diameter_o_ring = inner_diameter_o_ring+2*o_ring_thickness
    perimeter = math.pi*outer_diameter_o_ring

    # To determine the dimensions as acurate as possible, we perform two iterations of optimizations
    # First round
    for i in np.arange(5,20,0.1):
        # Define variables
        previous_area = area
        previous_L = L
        previous_D = D
        L = symbols('L')
        D = round(i,2)

        # Solve for the perimeter
        perimeter_eq = (math.pi*D) + 2*L - perimeter
        result = solve((perimeter_eq), (L))

        L = result[0]
        
        # Applying the equation for the surface area
        area = math.pi*(D/2)**2 + L*D
        
        # Finding the right value: if the surface area is larger than the target area, take the previous and continue
        if previous_area <= target_surface_area and area >= target_surface_area:
            print(f"First round: area={previous_area} met D={previous_D} en L={previous_L} is closet to the target surface area of {target_surface_area}")
            break
            
    # Second round
    for i in np.arange(previous_D-1,previous_D+1,0.001):
        # Define variables
        previous_area = area
        previous_L = L
        previous_D = D
        L = symbols('L')
        D = round(i,4)
        
        # Solve for the perimeter
        perimeter_eq = (math.pi*D) + 2*L - perimeter
        result = solve((perimeter_eq), (L))

        L = result[0]
        
        # Applying the equation for the surface area
        area = math.pi*(D/2)**2 + L*D
        
        # Finding the right value: if the surface area is larger than the target area, take the previous and stop
        if previous_area <= target_surface_area and area >= target_surface_area:
            print(f"Second round: area={previous_area} met D={previous_D} en L={previous_L} is closet to the target surface area of {target_surface_area}")
            break
            
    return previous_D,previous_L


# Example calculations for an O-ring of 22x3.5mm
inner_diameter_o_ring = 22
o_ring_thickness = 3.5
D, L = ovaal(inner_diameter_o_ring,o_ring_thickness)
print(f"\n--------------------------------------")
print(f"Resulting values for an oval shape with O-ring of {inner_diameter_o_ring} x {o_ring_thickness} mm")
print(f"D = {D}")
print(f"L = {L}")
print(f"--------------------------------------\n")


# ## Kidney shape
def optimize_range(inner_diameter_o_ring,o_ring_thickness, h):
    print("Calculating results for kidney shape, this might take up to 60s")
    # Define constants
    r = symbols('r')
    area = 0
    d = 0
    target_surface_area = math.pi*(25/2)**2 
    outer_diameter_o_ring = inner_diameter_o_ring+2*o_ring_thickness
    perimeter = math.pi*outer_diameter_o_ring
    
    # To determine the dimensions as acurate as possible, we perform two iterations of optimizations
    # First round
    for i in np.arange(5,20,0.1):
        # Define variables
        previous_area = area
        previous_r = r
        previous_d = d
        r = symbols('r')
        d = round(i,2)

        # Solve for the perimeter
        perimeter_eq = math.pi*d+(gamma*(2*r +d)) - perimeter
        result = solve((perimeter_eq), (r))

        r = result[0]

        # Applying the equation for the surface area
        area = math.pi*(d/2)**2+(gamma*(r*d+(d**2/2)))
        
        # Finding the right value: if the surface area is larger than the target area, take the previous and continue
        if previous_area <= target_surface_area and area >= target_surface_area:
            print(f"First round: area={previous_area} with d={previous_d} and r={previous_r} is closet to the target surface area of {target_surface_area}")
            break
            
    # Second round
    for i in np.arange(previous_d-1,previous_d+1,0.001):
        # Define variables
        previous_area = area
        previous_r = r
        previous_d = d
        r = symbols('r')
        d = round(i,4)

        # Solve for the perimeter
        perimeter_eq = math.pi*d+(gamma*(2*r +d)) - perimeter
        result = solve((perimeter_eq), (r))
        
        r = result[0]

        # Applying the equation for the surface area
        area = math.pi*(d/2)**2+(gamma*(r*d+(d**2/2)))
        
        # Finding the right value: if the surface area is larger than the target area, take the previous and stop
        if previous_area <= target_surface_area and area >= target_surface_area:
            print(f"Second round: area={previous_area} met d={previous_d} en r={previous_r} is closet to the target surface area of {target_surface_area}")
            break
            
    return previous_d,previous_r


# Example calculations for an O-ring of 22x3.5mm
inner_diameter_o_ring = 22
o_ring_thickness = 3.5
gamma = 100/180*math.pi

d, r = optimize_range(inner_diameter_o_ring,o_ring_thickness, gamma)
print(f"\n--------------------------------------")
print(f"Resulting values for a kidney shape with O-ring of {inner_diameter_o_ring} x {o_ring_thickness} mm")
print(f"d = {d}")
print(f"r = {r}")
print(f"--------------------------------------")
