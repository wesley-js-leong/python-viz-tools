# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 2020
@author: Wesley Leong
"""

from matplotlib import pyplot as plt
import matplotlib.colors as mpc
import numpy as np

def gen_color_cycle():
    """
    Function to generate a 1024x3 color matrix with each row = RGB values
    
    """
    ascending = np.linspace(0, 1, 256)
    descending = np.flip(ascending)
    steady_255 = np.ones(256)
    steady_0 = np.zeros(256)
    
    base_color_cycle = np.concatenate([ascending, steady_255, descending, steady_0])
    g = base_color_cycle
    r = np.roll(base_color_cycle, -256)
    b = np.roll(base_color_cycle, 256)
    full_color_matrix = np.vstack([r, g, b]).T
    
    return full_color_matrix

def desaturate(rgb_value, saturation):
    """
    Function to scale an rgb value closer to 0 or 1, depending on saturation level
    
    Args:
    rgb_value (float): 0 to 1 scalar representing an r, g, or b value
    saturation (float): -1 to 1 scalar representing % saturation of the resulting color
    
    Returns:
    rgb_value_saturated (np.array): 0 to 1 scalar
    
    """
    if saturation > 0:
        rgb_value_saturated = rgb_value + (1-rgb_value)*saturation 
    else:
        rgb_value_saturated = rgb_value + (rgb_value)*saturation 
        
    return rgb_value_saturated

desaturate_vec = np.vectorize(desaturate)

def rainbowify(n, saturation):
    """
    Function to produce a sequential, evenly-spaced array of colors for plotting, starting from pure red
    If monochrome gradients are desired (including black to white), use monochromify() instead
    
    Args:
    n (float): number of colors to generate
    saturation (float between 0 and 1): saturation of the resulting colors. 0 is full saturation, +1 is white, -1 is black
    
    Returns:
    colors (np.array): Nx3 array of RGB values where [1, 1, 1] is white and [0, 0, 0] is black
    
    """
    assert -1 <= saturation <= 1

    full_color_matrix = gen_color_cycle()
    
    # Select n number of evenly-spaced colors from the color matrix
    indices = np.linspace(0, 1023, n+1). astype(int) # n+1 because we don't want duplicate reds
    colors = full_color_matrix[indices[:-1]]
    
    # Scale color values by saturation level
    colors = desaturate_vec(colors, saturation)
    
    return colors

def monochromify(n, base_color):
    """
    Function to produce a sequential, evenly-spaced monochrome array for plotting, starting from black
    If rainbow gradients are desired, use rainbowify() instead
    
    Args:
    n (float): number of colors to generate
    base_color (3x1 np.array OR string): the basic RGB color with full saturation
    
    Returns:
    colors (np.array): Nx3 array of RGB values where [1, 1, 1] is white and [0, 0, 0] is black
    
    """
    # If base color is a string, map it to rgb
    if type(base_color)==str:
        base_color = mpc.to_rgb(base_color)

    sats = np.linspace(-1, 1, n+1)

    colors = np.tile(base_color, (n, 1))

    # Scale color values by saturation level
    for ii in range(len(sats)-1):
        sat = sats[ii]
        colors[ii] = desaturate_vec(colors[ii], saturation=sat)

    print(colors[-10:])
    return colors