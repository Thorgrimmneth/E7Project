import ctypes
import math
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex

import backend
from win32api import GetMonitorInfo, MonitorFromPoint

monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
work_area = monitor_info.get("Work")
root = tk.Tk()
root.title("Some stats")
root.state("zoomed")
root.geometry(f"{work_area[2]}x{work_area[3]}")
width_screen = work_area[2]
height_screen = work_area[3]
ctypes.windll.shcore.SetProcessDpiAwareness(2)
height_screen-=ctypes.windll.user32.GetSystemMetrics(4)
width_percentage = 100/13  # Adjust this value based on your preference
height_percentage = 100/26  # Adjust this value based on your preference
rect_width = round((width_screen * width_percentage) // 100)
rect_height = round((height_screen * height_percentage) // 100)
"""
for i in range(24):
    root.grid_rowconfigure(i, weight=1)
    for j in range(7):
        root.grid_columnconfigure(j, weight=1)

root.grid_columnconfigure(7, weight=5)
root.grid_rowconfigure(0, weight=25)"""

for i in range(25):
    for j in range(7):
        cell = tk.Canvas(root, width=rect_width, height=rect_height, highlightthickness=0)
        cell.grid(row=i, column=j)

# Create the separate canvas (1x7)
separate_canvas = tk.Canvas(root, width=rect_width * 5, height=rect_height * 25, highlightthickness=0)
separate_canvas.grid(row=0, column=7, rowspan=24, columnspan=4)

dictResultsLevel, dictResultsStats, dictResultsGraph = backend.analyse(backend.itemList)
tailleTextGras=round(15*(work_area[2]/2560))
tailleTextNormal=round(13*(work_area[2]/2560))
counterRow = 0
counterColumn = 0
for i, j in dictResultsLevel.items():
    label1 = tk.Label(root, text=f"{j}", font=("Arial", tailleTextGras, "bold"))
    label2 = tk.Label(root, text=f"{i}", font=("Arial", tailleTextNormal))
    label1.grid(row=counterRow, column=counterColumn, sticky="nsew")
    label2.grid(row=counterRow + 1, column=counterColumn, sticky="nsew")
    if counterColumn % 2:
        counterRow += 2
    counterColumn = (counterColumn + 1) % 2

counterRow = 0
counterColumn = 2
for i, j in dictResultsStats.items():
    label1 = tk.Label(root, text=f"{j}", font=("Arial", tailleTextGras, "bold"))
    label2 = tk.Label(root, text=f"{i}", font=("Arial", tailleTextNormal))
    label1.grid(row=counterRow, column=counterColumn, sticky="nsew")
    label2.grid(row=counterRow + 1, column=counterColumn, sticky="nsew")
    if counterColumn % 2:
        counterRow += 2
    counterColumn = (counterColumn + 1) % 2 + 2

counterRow = 0
counterColumn = 4
for i, j in dictResultsGraph["number_of_item_per_archetypes"].items():
    label1 = tk.Label(root, text=f"{j}", font=("Arial", tailleTextGras, "bold"))
    label2 = tk.Label(root, text=f"{i}", font=("Arial", tailleTextNormal))
    label1.grid(row=counterRow, column=counterColumn, sticky="nsew")
    label2.grid(row=counterRow + 1, column=counterColumn, sticky="nsew")
    if counterColumn % 2:
        counterRow += 2
    counterColumn = (counterColumn + 1) % 2 + 4


total=dictResultsLevel["number of items"]
listKeys=list(dictResultsGraph["number_of_item_per_archetypes"].keys())
listValues=list(dictResultsGraph["number_of_item_per_archetypes"].values())
listPourcentage=[i/total*100 for i in listValues]

fig, ax = plt.subplots()
ax.pie(listPourcentage, labels=listKeys, autopct='%1.1f%%', startangle=90, colors=['#4040FF', 'green', 'orange', 'red', 'purple', 'pink', 'gray', 'cyan'])
ax.set_title("Legend of the archetypes")
box=ax.get_position()
ax.set_position((box.x0, box.y0, box.width * 0.8, box.height))
default_bg_color = root.cget("background")

valueColor=root.winfo_rgb(default_bg_color)
fig.set_facecolor((valueColor[0]/65535 ,valueColor[1]/65535 ,valueColor[2]/65535 ))
# Ajout d'une légende
ax.legend(listKeys, loc="center right", bbox_to_anchor=(1, 0, 0.5, 1))

# Création du widget FigureCanvasTkAgg
paintingField = FigureCanvasTkAgg(fig, master=root)
canvas_widget = paintingField.get_tk_widget()
canvas_widget.grid(row=10,column=4,rowspan=10,columnspan=3,sticky="nswe")

categories = list(dictResultsGraph["number_of_item_per_archetypes_per_set"].keys())
listSets=list(dictResultsGraph["number_of_item_per_set"].keys())
values = [[dictResultsGraph["number_of_item_per_archetypes_per_set"][j][i] if i in dictResultsGraph["number_of_item_per_archetypes_per_set"][j] else 0 for j in categories] for i in listKeys]
# Largeur des barres
bar_width = 0.4

colorRGB=root.winfo_rgb(default_bg_color)
# Création du diagramme à barres chevauchées

fig, ax = plt.subplots(1,1,figsize=(round(18*(work_area[2]/2560)), round(13*(work_area[2]/2560))),facecolor=(colorRGB[0] / 65535,colorRGB[1] / 65535,colorRGB[2] / 65535))
indices = np.arange((len(values[0])))
bottom_values = np.zeros(len(values[0]))
for i in range(len(values)):
    ax.bar(indices, values[i], bar_width, label=listKeys[i], bottom=bottom_values)
    bottom_values += values[i]


# Ajout de légendes et d'étiquettes
ax.set_xlabel('Sets')
ax.set_ylabel('Archetypes')
ax.autoscale(axis='y')
ax.set_xticks(indices - (bar_width+0.1), )
ax.set_xticklabels(categories,rotation=45)
ax.tick_params(length=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_position((box.x0, box.y0, box.width * 0.8, box.height))
ax.legend(loc="center right", bbox_to_anchor=(1, 0.5))
fig.savefig('temp_plot.png', bbox_inches='tight',facecolor=fig.get_facecolor(), transparent=True)
bg_image = tk.PhotoImage(file='temp_plot.png')

separate_canvas.create_image(0,0,image=bg_image,anchor="nw")

root.mainloop()
