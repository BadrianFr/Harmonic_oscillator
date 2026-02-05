# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 08:29:25 2026

@author: adria
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import Fjeder_Fysik as fysik
import Animation as Ani
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button


paused=True
current_frame = 0

#fysikken
fjeder = fysik.Fjeder(0, 500)
lod = fysik.Lod(1,0.5)

m = fysik.getSamletMasse(fjeder, lod)

omega = fysik.getVinkelhastighed(fjeder, lod, m)
dæmp = 0.4
A = 10

#tidsindtillinger
t_max= 40 
dt= 0.01


t_values = np.arange(0, t_max, dt)

#grafgrænser:
v_max = max(abs(fysik.getHastighed(t, A, omega, dæmp)) for t in t_values)
a_max = max(abs(fysik.getAcceleration(t, A, omega, dæmp)) for t in t_values)
y_min, y_max = -20, 20


#skab animationsbox

fig = plt.figure(figsize=(8, 6))
gs = GridSpec(2, 2, width_ratios=[1, 3], height_ratios=[1, 1])

ax1 = fig.add_subplot(gs[:, 0])   # venstre: høj og tynd (fylder begge rækker)
ax2 = fig.add_subplot(gs[0, 1])   # øverst højre
ax3 = fig.add_subplot(gs[1, 1])   # nederst højre

plt.tight_layout()

#akseproperties
ax1.set_ylim(y_min, y_max)
ax1.set_xlim(-5, 5)
ax1.set_xlabel("x [m]")
ax1.set_ylabel("y [m]")

ax2.set_xlim(0, t_max)
ax2.set_ylim(-v_max*1.2, v_max*1.2)
ax2.set_ylabel("v [m/s]")

ax3.set_xlim(0, t_max)
ax3.set_ylim(-a_max*1.2, a_max*1.2)
ax3.set_ylabel("a [m/s²]")
ax3.set_xlabel("t [s]")

#lav et plot for loddet
lod_radius = lod.getRadius()  
x0, y0 = 0, 0
point = Circle((x0, y0), lod_radius, color = '#a89d9d')
ax1.add_patch(point)

#lav fjederen
line, = ax1.plot([], [], linestyle='-', linewidth=2, color='gray', solid_capstyle='round')

#datahistorik
v_data = []
a_data = []
t_data = []

#linjer til a og v
v_line, = ax2.plot([], [], color='red')
a_line, = ax3.plot([], [], color='green')

#init
def init_func():
    point.center = (x0, y0)
    line.set_data([], [])
    v_line.set_data([], [])
    a_line.set_data([], [])
    
    
    return point, line, v_line, a_line

#update
def update_plot(i):
    if paused:
        return point, line, v_line, a_line
    
    global current_frame
    t = t_values[current_frame]
    current_frame += 1
    
    if current_frame >= len(t_values):
        current_frame = 0
        
    y = fysik.getSted(t, A, omega, dæmp)
    v = fysik.getHastighed(t, A, omega, dæmp)
    a = fysik.getAcceleration(t, A, omega, dæmp)
    
    point.center = (0, y)
    
    fjeder_x, fjeder_y = Ani.fjeder_linje(y_max, y+lod_radius, 40, 1, 0.25)
    line.set_data(fjeder_x, fjeder_y)
    
    t_data.append(t)
    v_data.append(v)
    a_data.append(a)
    v_line.set_data(t_data, v_data)
    a_line.set_data(t_data, a_data)
    
    return point, line, v_line, a_line

mid_line, = ax1.plot(ax1.get_xlim(), [0, 0], color='black', linestyle='--', linewidth=2, alpha=0.25, label="Ligevægt")
ax1.legend()

#animatoin
anim = FuncAnimation(fig,
                     update_plot,
                     frames=len(t_values)   ,
                     init_func=init_func,
                     interval=dt*1000,  # ms
                     blit=True)
fig.canvas.draw()
anim.event_source.stop()  # vigtig

# knap
ax_button = plt.axes([0.4, 0.05, 0.2, 0.1])
button = Button(ax_button, "Start")

def start_reset(event):
    global paused, current_frame
    paused = False       # animation starter
    current_frame = 0    # reset til t = 0
    t_data.clear()       # ryd historik
    v_data.clear()
    a_data.clear()

button.on_clicked(start_reset)


plt.show()
