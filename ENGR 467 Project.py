import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
global counter
counter=0
class Algorithms():
    def __init__(self, selection):
        if(selection == "E-EDF"):
            self.eedf()
        elif(selection == "RM"):
            self.rm()
        elif(selection == "EDF"):
            self.edf()
            
    def eedf(self): #Energy saving EDF
        #############Ahmed
        print("THis is energy EDF")

    def edf(self): #EDF algorithm
        #(8, 1), (15, 3), (20, 4), and (22, 6) test
        #Release, Period, and Execution Time        
        Task0 = "0,8,1"     #self.txtin0.get()
        Task1 = "0,15,3"    #self.txtin1.get()
        Task2 = "0,20,4"    #self.txtin2.get()
        Task3 = "0,22,6"    #self.txtin3.get()
        Task4 = "0,0,0"     #self.txtin4.get()

        #TimeQuantum=20      #self.txtin5.get() #For round robin, not part of EDF or RM
        
        Task0 = Task0.split(",")
        Task1 = Task1.split(",")
        Task2 = Task2.split(",")
        Task3 = Task3.split(",")
        Task4 = Task4.split(",")
        
        Release={int(Task0[0]):0, int(Task1[0]):1, int(Task2[0]):2, int(Task3[0]):3, int(Task4[0]):4}
        Period={int(Task0[1]):0, int(Task1[1]):1, int(Task2[1]):2, int(Task3[1]):3, int(Task4[1]):4}
        Execution={int(Task0[2]):0, int(Task1[2]):1, int(Task2[2]):2, int(Task3[2]):3, int(Task4[2]):4}

        Priority=list(Period.items())
        Priority.sort()

        Prioritized_Period=dict(Priority)
        return Prioritized_Period

class Draw_Schedule(Frame):
    
    def __init__(self):
        super().__init__()
        
        self.Draw_Structure()

    def Draw_Structure(self):
        #This is where the Schedule base is Drawn
        
        Schedule = tk.Toplevel(app)
        self.grid()
        Counter = 0
        self.canvas = Canvas(Schedule,width=1000, height=300)
        
        for i in range(10,220,30):                  #Draws the Initial X-Axis Lines
            self.canvas.create_line(10, i, 1000, i) #Format(x1,y1,x2,y2)

        for i1 in range(10,1000,30):                #Draws the Y-Axis Lines
            self.canvas.create_line(i1, 220, i1, 230)
            self.canvas.create_text(i1,240,fill="darkblue",font="Times 12 italic bold",text=str(Counter))
            Counter+=1

        self.canvas.grid()
        
        self.Draw_Task(5,0,3) #Test drawing task (Task,start,end)
        self.Draw_Task(3,5,13)
        
    def Draw_Task(self,Task,Begin,End):
        self.canvas.create_rectangle((30*(Begin)+10), ((Task*30)+10), (30*(End)+10), ((Task*30)+40),fill="blue")

        test=Algorithms("EDF")
        #print(test.edf())


class Main(Tk): #This Module sets up the original window with search boxes, labels, and a button
    
    def __init__(self, *args, **kwargs):
        global entry_list
        global label_list
        label_list= []
        entry_list = []

        #Standard setup
  
        tk.Tk.__init__(self, *args, **kwargs) 
        self.title('Scheduling')
        self.configure(bg='light grey')         
        self.minsize(width=500, height=300)
        self.maxsize(width=500, height=300)

        #Set up the Textboxes,  text, and button
        
        self.txt0 = tk.Label(self, text="Enter the Release, Period, and Execution Time. Eg:'1,2,3'",bg='light grey')
        self.txt0.grid(row=0, column=0, sticky='w')
        
        self.button0 = tk.Button(self, text="Start", command=lambda: self.Execute()) # When Clicked, the draw class is called
        self.button0.grid(row=0,column=1)
        self.button1 = tk.Button(self, text="Add Task", command=lambda: self.Real_Add()) # When Clicked, the draw class is called
        self.button1.grid(row=0,column=4)
        self.button2 = tk.Button(self, text="Clear", command=lambda: self.clear()) # When Clicked, the draw class is called
        self.button2.grid(row=0,column=5)

    def Real_Add(self):
        global counter
        counter +=1
        descript="Task " + str(counter) + ":"

        self.txtin=tk.Entry(self,width=20)
        self.txt = tk.Label(self, text=descript,bg='light grey')
        self.txt.grid(row=counter, column=0, sticky='w')
        entry_list.append(self.txtin)
        label_list.append(self.txt)
        self.txtin.grid(row=counter,column=0)
    def Execute(self):
        #self.txtin.grid_forget()
        global counter
        global entry_list
        global label_list
        for i in entry_list:
            print(i.get())

        counter=0
        Draw_Schedule()
    def clear(self):
        global counter
        global entry_list
        global label_list
        for i in entry_list:
            i.grid_forget()
        for i in label_list:
            i.grid_forget()
        entry_list.clear()
        label_list.clear()
        counter =0
        


if __name__ == "__main__": 

        app = Main()        
        app.mainloop()
