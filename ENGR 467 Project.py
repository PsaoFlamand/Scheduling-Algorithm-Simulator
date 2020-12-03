import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import font
global counter
counter=0
class Algorithms():

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
        explanation = []
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
        print('prioritized_period:' , prioritized_period)
        print('prioritized_task:', prioritized_task)
        print (len(prioritized_task))
        
        initial = 0
        t = 0
        #Might need an additional nested for loop
        for i in range(1,3):
            for task_num in range(len(prioritized_task)):
                if (initial == 0): #initial condition or calculating U for the worst case (current process)
                    U = U + (Execution[task_num]/period[task_num])
                    #frequency.append(U)
                    #print('U = ', U)
                    t = ac1[task_num] / U
                    End_List.append(t)
                elif (len(prioritized_task) % (task_num+1) == 0):
                    pass
                elif (i == 1 or initial == 1): #First invocation
                    U = U + (ac1[task_num]/period[task_num])
                    #frequency.append(U)
                    #print('U = ', U)
                    t = ac1[task_num] / U
                    End_List.append(t)
                elif (i == 2 or initial == 2): #Second invocation
                    U = U + (ac2[task_num]/period[task_num])
                    #frequency.append(U)
                    #print('U = ', U)
                    t = ac2[task_num] / U
                    End_List.append(t + period[task_num])
                frequency.append(U)
                print('U =', U)
            #Ut = 1/U
            initial += 1
            print('t = ',t)
            print(End_List)
        return Task_List,Begin_List,End_List,deadline_missed,frequency,explanation
        
    def fcfs (self,release,period,Execution,deadline): #FCFS algorithm###!!!!!!!!!!!!!!!!!!DONE
        Task_List=[]
        Begin_List=[]
        End_List=[]
        deadline_missed=[]
        count =0
        prev_start=0
        sort_release= sorted(release.items(), key=lambda x: x[1])
        #for priority in sort_release:
        prioritized_release=[]
        prioritized_task=[]
        for priority in sort_release:
            prioritized_task.append(int(priority[0]))
            prioritized_release.append(int(priority[1]))
        prev_start=prioritized_release[0]
        for task_num in prioritized_task:
            while prev_start<release[task_num]:
                prev_start+=1
            reset=0
            for width in range(0,int(Execution[task_num])+1,1):
                end=width+prev_start               
                if (end)>deadline[task_num] and reset==0:#detect missed deadline
                    reset=1
                    deadline_missed.append(deadline[task_num])
                if (width-int(Execution[task_num])==0):
                    End_List.append(end)
                    Task_List.append(task_num)
                    Begin_List.append(prev_start)
                    prev_start=width+prev_start
                    count+=1      

        return Task_List,Begin_List,End_List,deadline_missed
    
    def rr (self,release,period,Execution,deadline, quantum, N,context_switching): #RR algorithm###!!!!!!!!!!!!!!!!!!DONE
        explanation=[]
        Task_List=[]
        Begin_List=[]
        End_List=[]       
        remaining_execution=[]
        deadline_missed=[]
        q=[]
        sort_release= sorted(release.items(), key=lambda x: x[1])
        prioritized_release=[]
        prioritized_task=[]
        prioritized_task_test=[]
        for priority in sort_release:
            prioritized_task.append(int(priority[0]))
            prioritized_task_test.append(int(priority[0]))
            prioritized_release.append(int(priority[1]))
        prev_start=float(prioritized_release[0])
        exe_count=0
        task_num=prioritized_task[0]
        q.append(exe_count)
        del prioritized_task[0]
        remaining_execution.append(int(Execution[prioritized_task_test[0]]))
        while not all(remains == 0 for remains in remaining_execution):#Loops until all tasks are drained
            write=1
            reset=0
            for width in range(1,int(quantum)+1,1):
                if remaining_execution[q[0]]!=0:
                    end=width+prev_start                
                if (end)>deadline[prioritized_task_test[q[0]]] and reset==0:#detect missed deadline
                    reset=1
                    deadline_missed.append(deadline[prioritized_task_test[q[0]]])
                    explanation.append("Task "+str(prioritized_task_test[q[0]])+ " Missed Its Deadline At The Time Interval: "+str(deadline[prioritized_task_test[q[0]]]))
                if remaining_execution[q[0]]==0:
                    write=0
                    break
                remaining_execution[q[0]]-=1
                if remaining_execution[q[0]]==0:
                    break
            if write==1:
                End_List.append(end)
                Task_List.append(prioritized_task_test[q[0]])
                Begin_List.append(prev_start)
                prev_start=width+prev_start
            ###decides which task to drain
            c=0
            for task_num_s in prioritized_task:
                
                if release[task_num_s]>end:
                    print('nope')

                else:
                    if release[task_num_s]!=end and len(q)==1:#Queue organization
                        remaining_execution.append(int(Execution[task_num_s]))
                        exe_count=len(remaining_execution)-1
                        q.append(exe_count)
                        c+=1
                    elif release[task_num_s]==end and len(q)>1:
                        remaining_execution.append(int(Execution[task_num_s]))
                        exe_count=len(remaining_execution)-1
                        q.append(exe_count)
                        c+=1
                    elif release[task_num_s]!=end and len(q)>1:
                        remaining_execution.append(int(Execution[task_num_s]))
                        exe_count=len(remaining_execution)-1
                        q.append(exe_count)
                        c+=1      
            for i in range(0,c,1):
                del prioritized_task[0]
            if remaining_execution[q[0]]!=0:#Am I calling the right tasks?
                excess=q.pop(0)
                q.append(excess)
            else:
                excess=q.pop(0)

            prev_start+=float(context_switching)
            
        return Task_List,Begin_List,End_List,deadline_missed,explanation

#####################################################All Graphics and controls beyond  this point
class Draw_Schedule(Frame):
    
    def __init__(self,Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time):
        super().__init__()
        algo=Algorithms()
        if (algo_type=="eedf"):
            Task,Begin,End,missed_deadline,frequency,explanation=algo.eedf(Release,Period,Execution,ac1,ac2)
            #Task_List,Begin_List,End_List,deadline_missed,frequency
        if (algo_type=="fcfs"):
            Task,Begin,End,missed_deadline,explanation=algo.fcfs(Release,Period,Execution,deadline)
        if (algo_type=="rr"):
            Task,Begin,End,missed_deadline,explanation=algo.rr(Release,Period,Execution,deadline, quantum,N, float(context))
        self.Draw_Structure(N)
        self.Draw_Task(Task,Begin,End,missed_deadline,explanation,int(end_time))

    def Draw_Structure(self,N):##################################### Must Adjust Schedule Diagram to Number Of tasks Len(Task_Number) and change the range by Task_Number/30
        #This is where the Schedule base is Drawn 
        Schedule = tk.Toplevel(app,width=1000,height=450)
        self.grid()
        Counter = 0
        self.canvas = Canvas(Schedule,width=1000,height=450)
        self.canvas.create_line(25, 10, 1000, 10)
        tsknum=0
        for i in range(40,(((N+1)*30)),30):                  #Draws the Initial X-Axis Lines
            self.canvas.create_line(25, i, 1000, i) #Format(x1,y1,x2,y2)
            self.canvas.create_text(10,i-13,fill="darkblue",font="Times 12 italic bold",text="T"+str(tsknum))
            tsknum+=1
        self.canvas.grid()
        
    def Draw_Structure_EEDF(self,N,frequency):#
        #This is where the Schedule base is Drawn 
        Schedule = tk.Toplevel(app,width=1000,height=450)
        self.grid()
        Counter = 0
        self.canvas = Canvas(Schedule,width=1000,height=450)
        self.canvas.create_line(25, 10, 1000, 10)
        tsknum=0
                         #Draws the Initial X-Axis Lines
        self.canvas.create_line(25, 1000, 1000, 1000) #Format(x1,y1,x2,y2)
        self.canvas.create_text(10,i-13,fill="darkblue",font="Times 12 italic bold",text="F"+str(frequency))
        #tsknum+=1
        #for freq in frequency:
            
        #self.canvas.grid()
        #
    def Draw_Task(self,Task_List,Begin_List,End_List,missed_deadline,explanation,end_time):
        scale=1
        Counter = 0
        if end_time==0:
            mx=End_List[len(End_List)-1]
        else:
            mx=end_time#End_List[len(End_List)-1]
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
            count=0
        for dead in missed_deadline:
            self.canvas.create_line((30*(dead/scale)+25), (10), (30*(dead/scale)+25), (((N+1)*26)),fill="red",width=5)
        count=float(1)
        count_for_break=0
        if len(explanation)==0:
            self.canvas.create_text(200,(((N+1)*40)*count),fill="darkblue",font="Times 10 italic bold",text="All Tasks Were Schedulable!")
        else:
            for exp in explanation:
                print(exp)
                self.canvas.create_text(200,(((N+1)*40)*count),fill="darkblue",font="Times 10 italic bold",text=str(exp))
                count+=float(0.1)
                print(N)
                if count_for_break==N-1:
                    break
                count_for_break+=1
            
class Main(Tk): #This Module sets up the original window with search boxes, labels, and a button
    
    def __init__(self, *args, **kwargs):
        global entry_list
        global label_list
        global N
        global var1
        global var2
        global var3
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
        self.check1 = tk.Checkbutton(self, text='Cycle-Saving EDF',variable=var1, onvalue=1, offvalue=0,bg='yellow',font=self.task_text)
        self.check1.grid(row=4,column=1, sticky='w')
        self.check4 = tk.Checkbutton(self, text='FCFS',variable=var2, onvalue=1, offvalue=0,bg='yellow',font=self.task_text)
        self.check4.grid(row=5,column=1, sticky='w')
        self.check5 = tk.Checkbutton(self, text='RR',variable=var3, onvalue=1, offvalue=0,bg='yellow',font=self.task_text)
        self.check5.grid(row=6,column=1, sticky='w')
        
        self.quantum_get=tk.Entry(self,width=10)
        self.context_get=tk.Entry(self,width=10)
        self.end_time_get=tk.Entry(self,width=10)
        self.quantum_text = tk.Label(self, text="Quantum",bg='yellow',font=self.task_text)
        self.context_text = tk.Label(self, text="Context",bg='yellow',font=self.task_text)
        self.end_time_text = tk.Label(self, text="End Time",bg='yellow',font=self.task_text)
        self.quantum_get.grid(row=7,column=1, sticky='e')
        self.quantum_text.grid(row=7, column=1, sticky='w')
        self.context_get.grid(row=8,column=1, sticky='e')
        self.context_text.grid(row=8,column=1, sticky='w')
        self.end_time_get.grid(row=9,column=1, sticky='e')
        self.end_time_text.grid(row=9,column=1, sticky='w')
        
        ##Explanation of input
        self.explainEEDF = tk.Label(self, text="|Release,Period,Exe,Dead|",bg='yellow',font=self.explain_text)
        self.explainEEDF.grid(row=10,column=1, sticky='w')

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
        deadline={}
        ac1={}
        ac2={}
        N=len(entry_list)
        if (var1.get() == 1):#EEDF
            entry_list_test=["0,8,3,2,1,0","0,10,3,1,1,0","0,14,1,1,1,0"]#added deadline as the last bit
            for i in entry_list_test:
                Task=i#.get()
                Task = Task.split(",")
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                
                ac1.update({count: int(Task[3])})
                ac2.update({count: int(Task[4])})
                deadline.update({count:int(Task[5])})
                count+=1
            algo_type="eedf"
            quantum=0
            context=0#self.context_get.get()
            end_time=self.end_time_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time)
        elif (var2.get() == 1):###FCFS#######################################
            entry_list_test=["10,100,20","5,60,20","20,20,15","30,100,15"] #(release,deadline,execution)
            for i in entry_list_test:
                Task=i#.get()
                Task = Task.split(",")
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                deadline.update({count:int(Task[3])})
                count+=1
            algo_type="fcfs"
            quantum=0
            context=0#self.context_get.get()
            end_time=self.end_time_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time)
        elif (var3.get() == 1):###RR
            #entry_list_test=["30,0,20,60","20,0,20,70","10,0,15,80","5,0,15,90"]
            entry_list_test=["0,0,75,300","10,0,40,500","10,0,25,700","80,0,20,900","85,0,45,1010"]
            for i in entry_list:
                Task=i.get()
                Task = Task.split(",")
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                deadline.update({count:int(Task[3])})
                count+=1
            algo_type="rr"
            quantum=self.quantum_get.get()
            context=0#self.context_get.get()
            end_time=0#self.end_time_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time)
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
