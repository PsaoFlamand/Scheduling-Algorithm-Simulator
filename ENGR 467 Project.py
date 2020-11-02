import re
import tkinter as tk
import threading
import tkinter.scrolledtext as tkst
import requests
import youtube_dl
from tkinter.ttk import Progressbar
import multiprocessing
import subprocess
import time

class App(tk.Tk): 

    def __init__(self, *args, **kwargs):

        #Standard setup

        tk.Tk.__init__(self, *args, **kwargs) 
        self.title('SammaSounds')
        self.configure(bg='light grey')         
        self.minsize(width=500, height=120)
        self.maxsize(width=500, height=120)

        #Implement Widgets
        
        self.txt0 = tk.Label(self, text="Search for Music:",bg='light grey')
        self.txt0.grid(row=0, column=0, sticky='w')
        self.txtin0 = tk.Entry(self,width=45) 
        self.txtin0.grid(row=0,column=0, sticky='n')
        self.button0 = tk.Button(self, text="Search", command=self.threadstarter) 
        self.button0.grid(row=0,column=0,sticky='e')
        self.lstbox0 = tk.Listbox(self,width=77,height=5) 
        self.lstbox0.bind("<Double-Button-1>", self.selector) 
        self.lstbox0.grid(row=1,column=0,sticky='nsw') 
        self.scroll0 = tk.Scrollbar(self, orient="vertical") 
        self.scroll0.config(command=self.lstbox0.yview) 
        self.scroll0.grid(row=1,column=1,sticky='nsw')
        self.lstbox0.config(yscrollcommand=self.scroll0.set)
        self.p = Progressbar(self,orient='vertical',length=90,mode="determinate",takefocus=True,maximum=5)
        self.p.grid(row=1,column=2)

if __name__ == "__main__": 

        app = App() 
        app.mainloop() 
