import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
class Draw(Frame):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #This is where the Schedule is Drawn

        self.master.title("Schedule")
        self.grid()
        Counter = 0
        self.canvas = Canvas(self,width=1000, height=300)
        for i in range(10,220,30):
            self.canvas.create_line(10, i, 1000, i) #Format(x1,y1,x2,y2)
        for i1 in range(10,1000,30):
            self.canvas.create_line(i1, 220, i1, 230)
            self.canvas.create_text(i1,240,fill="darkblue",font="Times 12 italic bold",text=str(Counter))
            Counter+=1

        self.canvas.grid()
        self.Draw_Task(5,0,3)
        self.Draw_Task(2,9,13)
    def Draw_Task(self,Task,Begin,End):
        self.canvas.create_rectangle((30*(Begin)+10), ((Task*30)+10), (30*(End)+10), ((Task*30)+40),fill="blue")
        
    def Logic(self):
        #(8, 1), (15, 3), (20, 4), and (22, 6) test
        #Release, Period, and Execution Time
        self.update()
        Total_Task=[]
        Task0 = "0,0,70"     #self.txtin0.get()
        Task1 = "5,0,40"    #self.txtin1.get()
        Task2 = "10,0,35"    #self.txtin2.get()
        Task3 = "0,0,0"    #self.txtin3.get()
        Task4 = "0,0,0"     #self.txtin4.get()
        #TimeQuantum=20      #self.txtin5.get()
        Task0 = Task0.split(",")
        Task1 = Task1.split(",")
        Task2 = Task2.split(",")
        Task3 = Task3.split(",")
        Task4 = Task4.split(",")
        Release=[int(Task0[0]),int(Task1[0]),int(Task2[0]),int(Task3[0]),int(Task4[0])]
        Period=[int(Task0[1]),int(Task1[1]),int(Task2[1]),int(Task3[1]),int(Task4[1])]
        Execution=[int(Task0[2]),int(Task1[2]),int(Task2[2]),int(Task3[2]),int(Task4[2])]
        for i in range(0,len(Release)-1):
            #print(i)
            Width=Release[i+1]-Release[i]
            #print(Release[i])
            print(Width)

class App(Tk): 

    def __init__(self, *args, **kwargs):

        #Standard setup

        tk.Tk.__init__(self, *args, **kwargs) 
        self.title('Scheduling')
        self.configure(bg='light grey')         
        self.minsize(width=1000, height=600)
        self.maxsize(width=1000, height=600)

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
