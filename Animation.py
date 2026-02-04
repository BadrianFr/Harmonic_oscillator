# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 04:26:32 2026

@author: adria
"""
import numpy as np

def fjeder_linje(y_start, y_end, n_coils, bredde, lige_stykke):
 
    # punkt hvor bølgerne stopper
    y_wave_end = y_end + lige_stykke
    if y_wave_end > y_start:  # sikkerhed mod negativ længde
        y_wave_end = y_start

    # lav bølget del
    y_wave = np.linspace(y_start, y_wave_end, n_coils*20)
    x_wave = bredde * np.sin(np.linspace(0, n_coils*2*np.pi, len(y_wave)))

    # lav lige stykke
    y_straight = np.linspace(y_wave_end, y_end, 2)
    x_straight = np.linspace(x_wave[-1], 0, 2)  # går til y=0 ved kassen

    # samle delene
    y_total = np.concatenate([y_wave, y_straight])
    x_total = np.concatenate([x_wave, x_straight])
    return x_total, y_total

