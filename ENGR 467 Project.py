import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
class Draw(Frame):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #This is where the Schedule is Drawn

        self.master.title("Lines")
        self.grid()

        canvas = Canvas(self,width=1000, height=300)
        canvas.create_line(10, 10, 1000, 10)
        canvas.create_line(10, 40, 1000, 40)
        canvas.create_line(10, 70, 1000, 70)
        canvas.create_line(10, 100, 1000, 100)
        canvas.create_line(10, 130, 1000, 130)
        canvas.create_line(10, 160, 1000, 160)

        canvas.grid()

class App(tk.Tk): 

    def __init__(self, *args, **kwargs):

        #Standard setup

        tk.Tk.__init__(self, *args, **kwargs) 
        self.title('Scheduling')
        self.configure(bg='light grey')         
        self.minsize(width=1000, height=1000)
        self.maxsize(width=1000, height=1000)

        #Set up the Textboxes,  text, and button
        
        self.txt0 = tk.Label(self, text="Enter the Release, Period, and Execution Time. Eg:'1,2,3'",bg='light grey')
        self.txt0.grid(row=0, column=0, sticky='w')
        self.txt1 = tk.Label(self, text="Task 1:",bg='light grey')
        self.txt1.grid(row=1, column=0, sticky='w')
        self.txt2 = tk.Label(self, text="Task 2:",bg='light grey')
        self.txt2.grid(row=2, column=0, sticky='w')
        self.txt3 = tk.Label(self, text="Task 3:",bg='light grey')
        self.txt3.grid(row=3, column=0, sticky='w')
        self.txt4 = tk.Label(self, text="Task 4:",bg='light grey')
        self.txt4.grid(row=4, column=0, sticky='w')
        self.txt5 = tk.Label(self, text="Task 5:",bg='light grey')
        self.txt5.grid(row=5, column=0, sticky='w')
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
        self.button0 = tk.Button(self, text="Start", command=Draw) #When Clicked, the draw class is called
        self.button0.grid(row=0,column=1,sticky='w')


if __name__ == "__main__": 

        app = App()
        
        app.mainloop()
