import tkinter as tk
import threading
from tkinter import Tk, Canvas, Frame, BOTH


class Draw(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Lines")
        self.grid()

        canvas = Canvas(self)
        canvas.create_line(15, 25, 200, 25)
        canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
        canvas.create_line(20, 20, 100, 100)

        canvas.grid()


def main():

    root = Tk()
    ex = Draw()
    root.geometry("400x250+300+300")
    root.mainloop()

class App(tk.Tk): 

    def __init__(self, *args, **kwargs):

        #Standard setup

        tk.Tk.__init__(self, *args, **kwargs) 
        self.title('Scheduling')
        self.configure(bg='light grey')         
        self.minsize(width=1000, height=1000)
        self.maxsize(width=1000, height=1000)

        #Implement Widgets
        
        self.txt0 = tk.Label(self, text="Enter the Release, Period, and Execution Time. Eg:'1,2,3'",bg='light grey')
        self.txt0.grid(row=0, column=0, sticky='w')
        self.txt0 = tk.Label(self, text="Task 1:",bg='light grey')
        self.txt0.grid(row=1, column=0, sticky='w')
        self.txt0 = tk.Label(self, text="Task 2:",bg='light grey')
        self.txt0.grid(row=2, column=0, sticky='w')
        self.txt0 = tk.Label(self, text="Task 3:",bg='light grey')
        self.txt0.grid(row=3, column=0, sticky='w')
        self.txt0 = tk.Label(self, text="Task 4:",bg='light grey')
        self.txt0.grid(row=4, column=0, sticky='w')
        self.txt0 = tk.Label(self, text="Task 5:",bg='light grey')
        self.txt0.grid(row=5, column=0, sticky='w')
        self.txtin0 = tk.Entry(self,width=20) 
        self.txtin0.grid(row=1,column=0)
        self.txtin1 = tk.Entry(self,width=20) 
        self.txtin1.grid(row=2,column=0)
        self.txtin2 = tk.Entry(self,width=20) 
        self.txtin2.grid(row=3,column=0)
        self.txtin3 = tk.Entry(self,width=20) 
        self.txtin3.grid(row=4,column=0)
        self.txtin4 = tk.Entry(self,width=20) 
        self.txtin4.grid(row=5,column=0)
        self.button0 = tk.Button(self, text="Start", command=Draw) 
        self.button0.grid(row=0,column=1,sticky='w')


if __name__ == "__main__": 

        app = App() 
        app.mainloop()
