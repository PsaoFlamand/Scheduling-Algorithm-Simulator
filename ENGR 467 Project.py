import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import font
global counter
counter=0
class Algorithms():
    def __init__(self):
        print("Nothing to do here")
        
    def eedf(self, Release, period, Execution, ac1, ac2): #Energy saving EDF
        #############Ahmed
        print("THis is energy EDF")
        #Execution = worst case execution
        #ac1 = invocation1, ac2 = invocation2
        #frequency = 1, 0.75, 0.5
        Task_List = []
        Begin_List = []
        End_List = []
        deadline_missed =[]
        frequency = []
        print(f'Release = {Release}, Execution (worst case) = {Execution} ms, period = {period} ms, invocation 1 = {ac1} ms, invocation 2 = {ac2} ms')
        print(f'Frequency = {frequency}Fm')
        U = 0
        sort_period= sorted(period.items(), key=lambda x: x[1])
        #Runs through a list and outputs the begin and end
        print('sort_period',sort_period)
        #for priority in sort_release:
        prioritized_period=[]
        prioritized_task=[]
        for priority in sort_period:
            print('priority',priority[0])
            prioritized_task.append(int(priority[0]))
            prioritized_period.append(int(priority[1]))
        #prev_start=prioritized_period[0]
        print(prioritized_period)
        print(prioritized_task)

        for task_num in prioritized_task:
            U = U + (Execution[task_num]/period[task_num])
        Ut = 1/U
        print(U)
        print(Ut)
        return Task_List,Begin_List,End_List,deadline_missed,frequency
        
    def fcfs (self,release,deadline,Execution): #FCFS algorithm###!!!!!!!!!!!!!!!!!!DONE
        Task_List=[]
        Begin_List=[]
        End_List=[]
        deadline_missed=[]
        count =0
        prev_start=0
        print(release)
        print(deadline)
        print(Execution)
        #["30,15,20","20,39,20","10,60,15","5,65,15"]
        
        sort_release= sorted(release.items(), key=lambda x: x[1])
        #Runs through a list and outputs the begin and end
        print('sort_release',sort_release)
        #for priority in sort_release:
        prioritized_release=[]
        prioritized_task=[]
        for priority in sort_release:
            print('priority',priority[0])
            prioritized_task.append(int(priority[0]))
            prioritized_release.append(int(priority[1]))
        prev_start=prioritized_release[0]

        print('prioritized_task',prioritized_task)
        print('prioritized_release',prioritized_release)
        
        for task_num in prioritized_task:
            
            while prev_start<release[task_num]:
                print("we are waiting")
                prev_start+=1
            
            reset=0
            
            for width in range(0,int(Execution[task_num])+1,1):
                end=width+prev_start               
                if (end)>deadline[task_num] and reset==0:#detect missed deadline
                    reset=1
                    print("Missssseeeeddd : end:",end," deadline:",deadline[task_num])
                    deadline_missed.append(deadline[task_num])
                #print("width",width," remaining", Execution[remaining])
                if (width-int(Execution[task_num])==0):
                    #print("width",width," remaining", Execution[remaining])
                    End_List.append(end)
                    Task_List.append(task_num)
                    Begin_List.append(prev_start)
                    prev_start=width+prev_start
                    count+=1
                    
        #print(deadline_missed)
        #print('Task_List',Task_List,'Begin_List',Begin_List,'End_List',End_List)
        return Task_List,Begin_List,End_List,deadline_missed
    
    def rr (self,release,deadline,Execution, quantum, N): #RR algorithm###!!!!!!!!!!!!!!!!!!DONE
        #["30,60,20","20,70,20","10,80,15","5,90,15"]
        Task_List=[]
        Begin_List=[]
        End_List=[]       
        remaining_execution=[]
        deadline_missed=[]
       # for i in Execution:
            
        sort_release= sorted(release.items(), key=lambda x: x[1])
        #Runs through a list and outputs the begin and end
        print(sort_release)
        #for priority in sort_release:
        prioritized_release=[]
        prioritized_task=[]
        for priority in sort_release:
            print('priority',priority[0])
            prioritized_task.append(int(priority[0]))
            prioritized_release.append(int(priority[1]))
        prev_start=prioritized_release[0]

        exe_count=0
        task_num=prioritized_task[0]
        del prioritized_task[0]
        print(prev_start)
        remaining_execution.append(int(Execution[prioritized_task[0]]))
        while not all(remains == 0 for remains in remaining_execution):
            #print('remaining_execution: ',remaining_execution)
            #print('task_num: ',(N-1)-exe_count)
            write=1
            reset=0
           # print('prev_start: ',prev_start,'task: ',(N-1)-exe_count)
            #while prev_start<release[(N-1)-exe_count]:
             #   print("we are waiting")
             #   prev_start+=1
            for width in range(1,int(quantum)+1,1):
                if remaining_execution[exe_count]!=0:
                    end=width+prev_start
                print('end ',end)
                
                if (end)>deadline[(N-1)-exe_count] and reset==0:#detect missed deadline
                    reset=1
                   # print("Missssseeeeddd : end:",end," deadline:",deadline[task_num])
                    deadline_missed.append(deadline[(N-1)-exe_count])

                
                if remaining_execution[exe_count]==0:
                    write=0
                    break
                remaining_execution[exe_count]-=1
                if remaining_execution[exe_count]==0:
                    break
            if write==1:
                End_List.append(end)
                Task_List.append((N-1)-exe_count)
                Begin_List.append(prev_start)
                prev_start=width+prev_start
            ###decides which task to drain
            #if exe_count==(len(remaining_execution)-1):
            #    exe_count=0
            #else:
            #    exe_count+=1
            if exe_count==0:
                exe_count=(len(remaining_execution)-1)
            else:
                exe_count-=1                
            for task_num_s in prioritized_task:
                #print('task_num_s',(N-1)-exe_count)
               # print('task',(N-1)-exe_count,'release[task_num]>',release[task_num_s],'end',end)
                if release[task_num_s]>=end:
                    #print("WON'T RUN : ",(N-1)-exe_count)
                  
                    break
                else:
                    #print('release[task_num_s]',release[task_num_s],'end',end)
                    if release[task_num_s]!=end:
                        remaining_execution.append(int(Execution[task_num_s]))
                        del Execution[task_num_s]
                        del prioritized_task[0]
                    
                        exe_count=len(remaining_execution)-1
                        break
                    else:
                        break
            #print('len(remaining_execution)-1: ',(len(remaining_execution)-1),'exe_count: ',exe_count)

        return Task_List,Begin_List,End_List,deadline_missed

#####################################################All Graphics and controls beyond  this point
class Draw_Schedule(Frame):
    
    def __init__(self,Release,Period,Execution,N,algo_type,quantum,ac1,ac2):
        super().__init__()
        algo=Algorithms()
        if (algo_type=="eedf"):
            print("we eedfed")
            Task,Begin,End,missed_deadline,frequency=algo.eedf(Release,Period,Execution,ac1,ac2)
            #Task_List,Begin_List,End_List,deadline_missed,frequency

        if (algo_type=="fcfs"):
            print("we fcfsed")
            Task,Begin,End,missed_deadline=algo.fcfs(Release,Period,Execution)
        if (algo_type=="rr"):
            print("we rred")
            Task,Begin,End,missed_deadline=algo.rr(Release,Period,Execution, quantum, N)
        self.Draw_Structure(N)
        self.Draw_Task(Task,Begin,End,missed_deadline)

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
        
    def Draw_Task(self,Task_List,Begin_List,End_List,missed_deadline):
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
            for dead in missed_deadline:
                self.canvas.create_line((30*(dead/scale)+25), (10), (30*(dead/scale)+25), (140),fill="red")

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
        self.explain_text = font.Font(family='Times', weight = 'bold', size = 7)
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
        ##Explanation of input
        self.explainEEDF = tk.Label(self, text="|Release,Period,Execution| or",bg='yellow',font=self.explain_text)
        self.explainEEDF.grid(row=8,column=1, sticky='w')
        self.explainEEDF = tk.Label(self, text="|Release,Deadline,Execution|",bg='yellow',font=self.explain_text)
        self.explainEEDF.grid(row=9,column=1, sticky='w')
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
        ac1={}
        ac2={}
        Simple_Execution=[]
        Simple_Period=[]
        Simple_Release=[]
        
        N=len(entry_list)
        if (var1.get() == 1):#EEDF
            entry_list_test=["0,8,3,2,1","0,10,3,1,1","0,14,1,1,1"]
            for i in entry_list_test:
                Task=i#.get()
            
                Task = Task.split(",")
        
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                ac1.update({count: int(Task[3])})
                ac2.update({count: int(Task[4])})
                count+=1
            algo_type="eedf"
            quantum=0
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2)
            
        elif (var4.get() == 1):###FCFS#######################################
            entry_list_test=["10,100,20","5,60,20","20,20,15","30,100,15"] #(release,deadline,execution)
            for i in entry_list_test:
                Task=i#.get()
            
                Task = Task.split(",")
        
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                count+=1

            algo_type="fcfs"
            quantum=0
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2)
    
        elif (var5.get() == 1):###RR
            entry_list_test=["30,60,20","20,70,20","10,80,15","5,90,15"]
            for i in entry_list_test:
                Task=i#.get()
            
                Task = Task.split(",")
        
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                count+=1
            algo_type="rr"
            quantum=5#self.quantum_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2)
            
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
