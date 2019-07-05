import sys, string, os, yaml, tkinter, numpy, scipy
# install the python3-tk package using sudo apt-get/etc.
from tkinter import *
from tkinter import ttk

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

suppliersList = []
for s in config['suppliers']:
    suppliersList.append(s)

app = Tk()
app.title("Stock Management System")
tabs = ttk.Notebook(app)
app.geometry('1000x500')

def editSupplier():
    return

for supplier in suppliersList:
    # tab = ttk.Frame(tabs)
    # tabs.add(tab[supplier], text=suppliersList[supplier])

    tab = ttk.Frame(tabs)
    tabs.add(tab, text=str(supplier))
    label = Label(tab, text=str(supplier))
    label.grid(column=0, row=0)
    count = 0
    for e in config['suppliers'][supplier]:
        label = Label(tab, text=str(e))
        label.grid(column=0, row=count)
        label = Label(tab, text=str(config['suppliers'][supplier][e]))
        label.grid(column=1, row=count)
        count+=1

tabs.pack(expand=1, fill="both")
app.mainloop()
