import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
global counter
counter=0
class Algorithms():
    def __init__(self):
        print("Nothing to do here")
    def eedf(self): #Energy saving EDF
        #############Ahmed
        print("THis is energy EDF")

    def edf(self,Release,Period,Execution): #EDF algorithm
        #(8, 1), (15, 3), (20, 4), and (22, 6) test
        #Release, Period, and Execution Time        
        Task_List=[0,2,4]
        Begin_List=[1,2,5]
        End_List=[3,1,6]
        Priority=list(Period.items())
        Priority.sort()

        Prioritized_Period=dict(Priority)
        
        return Task_List,Begin_List,End_List

class Draw_Schedule(Frame):
    
    def __init__(self,Release,Period,Execution,N):
        super().__init__()
        test=Algorithms()
        Task,Begin,End=test.edf(Release,Period,Execution)
        self.Draw_Structure(N)
        self.Draw_Task(Task,Begin,End)

    def Draw_Structure(self,N):##################################### Must Adjust Schedule Diagram to Number Of tasks Len(Task_Number) and change the range by Task_Number/30
        #This is where the Schedule base is Drawn 
        
        Schedule = tk.Toplevel(app,width=1000,height=450)
        self.grid()
        Counter = 0
        self.canvas = Canvas(Schedule,width=1000,height=450)
        print(N)
        self.canvas.create_line(10, 10, 1000, 10)
        for i in range(40,(((N+1)*30)),30):                  #Draws the Initial X-Axis Lines
            self.canvas.create_line(10, i, 1000, i) #Format(x1,y1,x2,y2)

        for i1 in range(10,1000,30):                #Draws the Y-Axis Lines
            self.canvas.create_line(i1, (((N+1)*30)-20), i1, (((N+1)*30)-10))
            self.canvas.create_text(i1,(((N+1)*30)),fill="darkblue",font="Times 12 italic bold",text=str(Counter))
            Counter+=1

        self.canvas.grid()
        
        #self.Draw_Task(5,0,3) #Test drawing task (Task,start,end)
        #self.Draw_Task(3,5,13)
        
    def Draw_Task(self,Task_List,Begin_List,End_List):
        for i in range(0,len(Task_List)):
            Task=Task_List[i]
            Begin=Begin_List[i]
            End=End_List[i]
            print(Task,Begin,End)
            self.canvas.create_rectangle((30*(Begin)+10), ((Task*30)+10), (30*(End)+10), ((Task*30)+40),fill="blue")

        
      


class Main(Tk): #This Module sets up the original window with search boxes, labels, and a button
    
    def __init__(self, *args, **kwargs):
        global entry_list
        global label_list
        global N
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
        
        self.button0 = tk.Button(self, text="Start", command=lambda: self.Execute()) # When Clicked, The Schedule is drawn
        self.button0.grid(row=0,column=1)
        self.button1 = tk.Button(self, text="Add Task", command=lambda: self.Add_Task()) # When Clicked, A task is added
        self.button1.grid(row=0,column=4)
        self.button2 = tk.Button(self, text="Clear", command=lambda: self.clear()) # When Clicked, All tasks are cleared
        self.button2.grid(row=0,column=5)

    def Add_Task(self):
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
        global N
        count=0
        Release={}
        Period={}
        Execution={}
        N=len(entry_list)
        for i in entry_list:
            Task=i.get()
            Task = Task.split(",")
        
            Release.update({int(Task[0]):count})
            Period.update({int(Task[1]):count})
            Execution.update({int(Task[2]):count})
            count+=1

        counter=0
        
        Draw_Schedule(Release,Period,Execution,N)
        self.clear()
        N=0
    def clear(self):
        global N
        global counter
        global entry_list
        global label_list
        for i in entry_list:
            i.grid_forget()
        for i in label_list:
            i.grid_forget()
        entry_list.clear()
        label_list.clear()
        counter = 0
        N=0
if __name__ == "__main__": 

        app = Main()        
        app.mainloop()
