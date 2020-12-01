import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import font
global counter
counter=0
class Algorithms():
    def __init__(self):
        print("Nothing to do here")
    def eedf(self): #Energy saving EDF
        #############Ahmed
        print("THis is energy EDF")
    def fcfs (self,Execution): #FCFS algorithm###!!!!!!!!!!!!!!!!!!DONE
        Task_List=[]
        Begin_List=[]
        End_List=[]
        count =0
        prev_start=0
        
        for i in Execution:
            
            print(i)
            for width in range(0,int(i)+1,1):
                if (width-int(i)==0):
                    End_List.append(width+prev_start)
                    Task_List.append(count)
                    Begin_List.append(prev_start)
                    prev_start=width+prev_start
                    count+=1    
        return Task_List,Begin_List,End_List
    def rr (self,Execution,quantum): #RR algorithm###!!!!!!!!!!!!!!!!!!DONE
        #print('''["53","8","68","24"]''')
        Task_List=[]
        Begin_List=[]
        End_List=[]

        Task_List=[]
        Begin_List=[]
        End_List=[]
        count =0
        prev_start=0
        remaining_execution=[]
        for i in Execution:
            remaining_execution.append(int(i))
        exe_count=0
        breaker=1
        count=0
        prev_start=0
        
        while not all(remains == 0 for remains in remaining_execution):
            write=1
            count+=1
            for width in range(1,int(quantum)+1,1):
                if remaining_execution[exe_count]==0:
                    write=0
                    w=0
                    break
                remaining_execution[exe_count]-=1
                if remaining_execution[exe_count]==0:

                    break
            print (width)
            if write==1:
                End_List.append(width+prev_start)
                Task_List.append(exe_count)
                Begin_List.append(prev_start)
                prev_start=width+prev_start
            if exe_count==(len(remaining_execution)-1):
                exe_count=0
            else:
                exe_count+=1
        return Task_List,Begin_List,End_List

#####################################################All Graphics and controls beyond  this point
class Draw_Schedule(Frame):
    
    def __init__(self,Release,Period,Execution,N,algo_type,quantum):
        super().__init__()
        algo=Algorithms()
        if (algo_type=="eedf"):
            print("we eedfed")
            Task,Begin,End=algo.eedf(Release,Period,Execution)

        if (algo_type=="fcfs"):
            print("we fcfsed")
            Task,Begin,End=algo.fcfs(Execution)
        if (algo_type=="rr"):
            print("we rred")
            Task,Begin,End=algo.rr(Execution, quantum)
        self.Draw_Structure(N)
        self.Draw_Task(Task,Begin,End)

    def Draw_Structure(self,N):##################################### Must Adjust Schedule Diagram to Number Of tasks Len(Task_Number) and change the range by Task_Number/30
        #This is where the Schedule base is Drawn 
        
        Schedule = tk.Toplevel(app,width=1000,height=450)
        self.grid()
        Counter = 0
        self.canvas = Canvas(Schedule,width=1000,height=450)
       # print(N)
        self.canvas.create_line(25, 10, 1000, 10)
        tsknum=0
        for i in range(40,(((N+1)*30)),30):                  #Draws the Initial X-Axis Lines
            self.canvas.create_line(25, i, 1000, i) #Format(x1,y1,x2,y2)
            self.canvas.create_text(10,i-13,fill="darkblue",font="Times 12 italic bold",text="T"+str(tsknum))
            tsknum+=1

        self.canvas.grid()
        
    def Draw_Task(self,Task_List,Begin_List,End_List):
        scale=1
        Counter = 0
        mx=End_List[len(End_List)-1]
        if (mx>320):
            scale=20
        if(mx>160 and mx <=320):
            scale=10
        if(mx>60 and mx<=160):
            scale=5
        elif(mx>30 and mx<=60):
            scale=2
        elif(mx<=30):
            scale=1
        for i1 in range(25,1000,30):                #Draws the Y-Axis Lines
            self.canvas.create_line(i1, (((N+1)*30)-20), i1, (((N+1)*30)-10))
            self.canvas.create_text(i1,(((N+1)*30)),fill="darkblue",font="Times 12 italic bold",text=str(Counter))
        
            Counter+=scale
        for i in range(0,len(Task_List)):

            Task=Task_List[i]
            Begin=Begin_List[i]/scale
            End=End_List[i]/scale
            
            self.canvas.create_rectangle((30*(Begin)+25), ((Task*30)+10), (30*(End)+25), ((Task*30)+40),fill="blue")

class Main(Tk): #This Module sets up the original window with search boxes, labels, and a button
    
    def __init__(self, *args, **kwargs):
        global entry_list
        global label_list
        global N
        global var1
        global var2
        global var3
        global var4
        global var5
        label_list= []
        entry_list = []

        #Standard setup
  
        tk.Tk.__init__(self, *args, **kwargs) 
        self.title('Scheduling')
        self.configure(bg='yellow')         
        self.minsize(width=400, height=310)
        self.maxsize(width=400, height=310)

        #Set up the Textboxes,  text, and button
        title_text = font.Font(family='Times', weight = 'bold', size = 13)
        self.task_text = font.Font(family='Times', weight = 'bold', size = 10)
        self.txt0 = tk.Label(self, text="Welcome! Please Enter Your Input...",bg='yellow',font=title_text)
        
        self.txt0.grid(row=0, column=0, sticky='w')
        
        self.button0 = tk.Button(self, text="Start", bg='white',command=lambda: self.Execute(),font=self.task_text) # When Clicked, The Schedule is drawn
        self.button0.grid(row=1,column=1, sticky='w')
        self.button1 = tk.Button(self, text="Add Task",bg='white', command=lambda: self.Add_Task(),font=self.task_text) # When Clicked, A task is added
        self.button1.grid(row=2,column=1, sticky='w')
        self.button2 = tk.Button(self, text="Clear",bg='white', command=lambda: self.clear(),font=self.task_text) # When Clicked, All tasks are cleared
        self.button2.grid(row=3,column=1, sticky='w')
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        var3 = tk.IntVar()
        var4 = tk.IntVar()
        var5 = tk.IntVar()
        self.check1 = tk.Checkbutton(self, text='Cycle-Saving EDF',variable=var1, onvalue=1, offvalue=0,bg='yellow',font=self.task_text)
        self.check1.grid(row=4,column=1, sticky='w')

        self.check4 = tk.Checkbutton(self, text='FCFS',variable=var4, onvalue=1, offvalue=0,bg='yellow',font=self.task_text)
        self.check4.grid(row=5,column=1, sticky='w')
        self.check5 = tk.Checkbutton(self, text='RR',variable=var5, onvalue=1, offvalue=0,bg='yellow',font=self.task_text)
        self.check5.grid(row=6,column=1, sticky='w')
    
        self.quantum_get=tk.Entry(self,width=10)
        self.quantum_text = tk.Label(self, text="Quantum",bg='yellow',font=self.task_text)
        self.quantum_get.grid(row=7,column=1, sticky='e')
        self.quantum_text.grid(row=7, column=1, sticky='w')
    def Add_Task(self):
        global counter
        counter +=1
        descript="Task " + str(counter) + ":"

        self.txtin=tk.Entry(self,width=20)
        self.txt = tk.Label(self, text=descript,bg='yellow',font=self.task_text)
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
        Simple_Execution=[]
        N=len(entry_list)

        if (var1.get() == 1):

            entry_list_test=["0,50,12","0,40,10","0,30,10"]
            for i in entry_list_test:
                Task=i#.get()
            
                Task = Task.split(",")
        
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                count+=1
            algo_type="eedf"
            quantum=0
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum)

        elif (var4.get() == 1):###FCFS

            #entry_list_test=["12","40","10"]
            for i in entry_list:
                Task=i.get()
                Simple_Execution.append(Task)
                count+=1
            algo_type="fcfs"
            quantum=0
            Draw_Schedule(Release,Period,Simple_Execution,N,algo_type,quantum)
        elif (var5.get() == 1):###RR
            #entry_list_test=["53","8","68","24"]
            for i in entry_list:
                Task=i.get()
                Simple_Execution.append(Task)
                count+=1

            algo_type="rr"
            quantum=self.quantum_get.get()
            Draw_Schedule(Release,Period,Simple_Execution,N,algo_type,quantum)
            
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
