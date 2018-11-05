import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import psutil

gpuLoadFile="/sys/devices/gpu.0/load"

# On the Jetson TX1 this is a symbolic link to:
# gpuLoadFile="/sys/devices/platform/host1x/57000000.gpu/load"
# On the Jetson TX2, this is a symbolic link to:
# gpuLoadFile="/sys/devices/platform/host1x/17000000.gp10b/load"

fig = plt.figure(figsize=(14,10))
plt.subplots_adjust(hspace=0.5)
fig.set_facecolor('#F2F1F0')
fig.canvas.set_window_title('Activity Monitor')


gpuAx = plt.subplot2grid((2,2), (0,0), colspan = 1)
cpuAx = plt.subplot2grid((2,2), (0,1), colspan = 1)
memAx = plt.subplot2grid((2,2), (1,0), colspan = 1)

def get_init_graph_vars(ax, x_ticks=60, ping_every=250):
    #60s on the x-axis, we get stats every 250ms, hence 240pts
    num_pts = int(x_ticks/(ping_every*0.001))
    line, = ax.plot([],[])
    y_list = deque([0]*num_pts)
    x_list = deque(np.linspace(x_ticks,0,num=num_pts))
    return line, y_list, x_list, 0
    

gpuLine, gpuy_list, gpux_list, fill_lines_gpu = get_init_graph_vars(gpuAx)
cpuLine, cpuy_list, cpux_list, fill_lines_cpu = get_init_graph_vars(cpuAx)
memLine, memy_list, memx_list, fill_lines_mem = get_init_graph_vars(memAx)

def set_plot_params(ax, x_lim, y_lim, title, x_label, y_label):
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

def initMemGraph():
    global memAx
    global memLine
    global fill_lines_mem

    mem_stats = psutil.virtual_memory()
    total_mem = mem_stats[0]/(1024*1024*1024)

    set_plot_params(memAx, (60, 0), (0, total_mem), 'Memory', 'Seconds', 'Usage (GB)')
    memAx.grid(color='gray', linestyle='dotted', linewidth=1)

    memLine.set_data([],[])
    fill_lines_mem=memAx.fill_between(memLine.get_xdata(),50,0)

def initCPUGraph():
    global cpuAx
    global cpuLine
    global fill_lines_cpu

    set_plot_params(cpuAx, (60, 0), (-5, 105), 'CPU', 'Seconds', 'Usage (%)')
    cpuAx.grid(color='gray', linestyle='dotted', linewidth=1)

    cpuLine.set_data([],[])
    fill_lines_cpu=cpuAx.fill_between(cpuLine.get_xdata(),50,0)    

def initGPUGraph():
    global gpuAx
    global gpuLine
    global fill_lines_gpu

    set_plot_params(gpuAx, (60, 0), (-5, 105), 'GPU', 'Seconds', 'Usage (%)')
    gpuAx.grid(color='gray', linestyle='dotted', linewidth=1)

    gpuLine.set_data([],[])
    fill_lines_gpu=gpuAx.fill_between(gpuLine.get_xdata(),50,0)    


def initGraph():
    initGPUGraph()
    initCPUGraph()
    initMemGraph()
    return [gpuLine] + [fill_lines_gpu] + [cpuLine] + [fill_lines_cpu] + [memLine] + [fill_lines_mem]

def update_plot(ax, y_list, y_val, x_list, line_var, fill_lines, color='cyan'):
    y_list.popleft()
    y_list.append(y_val)
    line_var.set_data(x_list, y_list)
    fill_lines.remove()
    fill_lines = ax.fill_between(x_list, 0, y_list, facecolor=color, alpha=0.50)
    return fill_lines
    
def updateGPUGraph():
    global fill_lines_gpu
    global gpuy_list
    global gpux_list
    global gpuLine
    global gpuAx

    fileData = 0
    with open(gpuLoadFile, 'r') as gpuFile:
        fileData = gpuFile.read()
    
    fill_lines_gpu = update_plot(gpuAx, gpuy_list, int(fileData)/10, gpux_list, gpuLine, fill_lines_gpu)

def updateCPUGraph():
    global fill_lines_cpu
    global cpuy_list
    global cpux_list
    global cpuLine
    global cpuAx

    fill_lines_cpu = update_plot(cpuAx, cpuy_list, psutil.cpu_percent(), cpux_list, cpuLine, fill_lines_cpu)

def updateMemGraph():
    global fill_lines_mem
    global memy_list
    global memx_list
    global memLine
    global memAx

    used_mem = ((psutil.virtual_memory()[3]) or 0)/(1024*1024*1024)
    fill_lines_mem = update_plot(memAx, memy_list, used_mem, memx_list, memLine, fill_lines_mem)   
    
def updateGraph(frame):
    updateGPUGraph()
    updateCPUGraph()
    updateMemGraph()
    return [gpuLine] + [fill_lines_gpu] + [cpuLine] + [fill_lines_cpu] + [memLine] + [fill_lines_mem]


animation = FuncAnimation(fig, updateGraph, frames=200,
                    init_func=initGraph,  interval=250, blit=True)

plt.show()


