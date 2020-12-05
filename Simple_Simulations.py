import tkinter as tk

from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import font
global counter
counter=1
class Algorithms():

    def eedf(self, Release, period, Execution, ac1, ac2,N,round_freq): #Energy saving EDF
        Task_List = []
        Begin_List = []
        End_List = []
        deadline_missed =[]
        frequency = []
        explanation = []
        U = 0
        sort_period= sorted(period.items(), key=lambda x: x[1])
        prioritized_period=[]
        prioritized_task=[]
        for priority in sort_period:
            prioritized_task.append(int(priority[0]))
            prioritized_period.append(int(priority[1]))
        prev_start = 0
        invocation = 1
        task_list_with_2_iterations = 2*prioritized_task
        for task in (task_list_with_2_iterations):
            prev_start = 0
            if task==0:
                U=0
                if invocation == 1:
                    Begin_List.append(0)
                else:
                    if End_List[-1] > prioritized_period[task]:
                        prev_start = End_List[-1] - prioritized_period[task]
                    Begin_List.append(prioritized_period[task] + prev_start)
                for task_num in prioritized_task:
                    if invocation == 1:
                        U += Execution[task_num] / period[task_num]
                    else:
                        if task_num == task:
                            U += Execution[task_num] / period[task_num]
                        else:
                            U += ac1[task_num] / period[task_num]
                if round_freq:
                    if U<=1 and U>0.75: #rounding frequency
                        U=1
                    elif U<=0.75 and U>0.5:
                        U=0.75
                    elif U<=0.5:
                        U=0.5
                if invocation==1:
                    t = ac1[task] / U
                else:
                    t = (ac2[task] / U) + prioritized_period[task]
                Task_List.append(task)
                End_List.append(t)
                frequency.append(round(U,3))
            elif task==1:
                U=0
                if invocation == 1:
                    Begin_List.append(End_List[-1])
                else:
                    if End_List[-1] > prioritized_period[task]:
                        prev_start = End_List[-1] - prioritized_period[task]
                    Begin_List.append(prioritized_period[task] + prev_start)
                for task_num in prioritized_task:
                    if invocation == 1:
                        if task_num >= task:
                            U += Execution[task_num] / period[task_num]
                        else:
                            U += ac1[task_num] / period[task_num]
                    else:
                        if task_num == task:
                            U += Execution[task_num] / period[task_num]
                        elif task_num < task:
                            U += ac2[task_num] / period[task_num]
                        elif task_num > task:
                            U += ac1[task_num] / period[task_num]
                if round_freq:
                    if U<=1 and U>0.75: #rounding frequency
                        U=1
                    elif U<=0.75 and U>0.5:
                        U=0.75
                    elif U<=0.5:
                        U=0.5
                if invocation==1:
                    t += ac1[task] / U
                else:
                    t = (ac2[task] / U) + prioritized_period[task] + prev_start
                Task_List.append(task)
                End_List.append(t)
                frequency.append(round(U,3))
            elif task==2:
                U=0
                if invocation==1:
                    Begin_List.append(End_List[-1])
                else:
                    if End_List[-1] > prioritized_period[task]:
                        prev_start = abs(End_List[-1] - prioritized_period[task])
                        print(prev_start)
                    Begin_List.append(prioritized_period[task] + prev_start)
                for task_num in prioritized_task:
                    if invocation==1:
                        if task_num == task:
                            U += Execution[task_num] / period[task_num]
                        else:
                            U += ac1[task_num] / period[task_num]
                    else:
                        if task_num == task:
                            U += Execution[task_num] / period[task_num]
                        else:
                            U += ac2[task_num] / period[task_num]
                if round_freq:
                    if U<=1 and U>0.75: #rounding frequency
                        U=1
                    elif U<=0.75 and U>0.5:
                        U=0.75
                    elif U<=0.5:
                        U=0.5
                if invocation==1:
                    t += ac1[task] / U
                else:
                    t = (ac2[task] / U) + prioritized_period[task] + prev_start
                Task_List.append(task)
                End_List.append(t)
                frequency.append(round(U,3))
            if task==(int(0.5 * len(task_list_with_2_iterations))-1):
                invocation += 1
        print('Begin list =',Begin_List)
        print('End list = ', End_List)
        print('Frequencies =',frequency)
        print('task_list',Task_List)
        return Task_List,Begin_List,End_List,deadline_missed,frequency,explanation
    
    def laedf(self, Release, period, Execution, ac1, ac2,N,round_freq): #Look ahead Energy saving EDF

        Task_List = []
        Begin_List = []
        End_List = []
        deadline_missed =[]
        frequency = []
        explanation = []
        deadline=[]
        sort_period= sorted(period.items(), key=lambda x: x[1])
        prioritized_period=[]
        prioritized_task=[]
        tracker={}
        op_tracker={}
        c=0
        for priority in sort_period:
            prioritized_task.append(int(priority[0]))
            prioritized_period.append(int(priority[1]))
            deadline.append(int(priority[1]))
            tracker.update({int(priority[0]):c})
            op_tracker.update({c:int(priority[0])})
            c+=1
        #Task_List=prioritized_task
        #for dead in prioritized_task:
            
        selector=1
        count=0
        q=[]
        freq=0
        prev_start=0
        print('deadline',deadline)
        for dead in range(0,len(deadline)): #invocation 1
            print('dead',dead)
            q=[]
            q.append(prioritized_task[dead])
            if dead==len(deadline)-1:
                selector=0
            else:
                selector=dead+1
            for i in range(0,N-1):#Check Deference INV1
                deadline_difference=deadline[selector]-deadline[dead]
                if Execution[prioritized_task[selector]]>deadline_difference:
                    q.append(prioritized_task[selector])#We know which ones we can't defer  
                selector+=1
                if selector==N:
                    selector=0
            for task in q: #Calculate Freqencies in the queue INV 1     
                if (deadline[tracker[task]]-period[task])!=0:
                    freq += Execution[task]/(deadline[tracker[task]]-period[task])
                    print('Execution[task]',Execution[task],'/','(deadline[task]-period[task])',(deadline[task]-period[task]))
                else:
                    freq += Execution[task]/(deadline[tracker[task]]-prev_start)
                    print('Execution[task]',Execution[task],'/','(deadline[task]-prev_start)',(deadline[task]-prev_start))
            deadline[dead]=deadline[dead]*2
            if round_freq==True:
                if freq<=1 and freq>0.75: #rounding frequency
                    freq=1
                elif freq<=0.75 and freq>0.5:
                    freq=0.75
                elif freq<=0.5:
                    freq=0.5
            else:
                freq=round(freq,3)
            width=ac1[prioritized_task[dead]]/freq
            end_time=width+prev_start
            frequency.append(freq)
            End_List.append(end_time)
            Task_List.append(prioritized_task[dead])
            Begin_List.append(prev_start)
            prev_start+=width
            freq=0
            
        for dead in range(0,len(deadline)): #invocation 2 Deferance check
            if prev_start<period[op_tracker[dead]]:
                prev_start=period[op_tracker[dead]]
            q=[]
            q.append(prioritized_task[dead])
            if dead==len(deadline)-1:
                selector=0
            else:
                selector=dead+1
            for i in range(0,N-1):
                deadline_difference=deadline[selector]-deadline[dead]
                if Execution[prioritized_task[selector]]>deadline_difference:
                    q.append(prioritized_task[selector])#We know which ones we can't defer  
                selector+=1
                if selector==N:
                    selector=0
            for task in q:#Calculate the Invocation 2 queue frequencies
                freq += Execution[task]/(deadline[tracker[task]]-prev_start)
            deadline[dead]=deadline[dead]*2
            if round_freq==True:
                if freq<=1 and freq>0.75:
                    freq=1
                elif freq<=0.75 and freq>0.5:
                    freq=0.75
                elif freq<=0.5:
                    freq=0.5
            else:
                freq=round(freq,3)
            width=ac2[prioritized_task[dead]]/freq
            end_time=width+prev_start
            frequency.append(freq)
            End_List.append(end_time)
            Task_List.append(prioritized_task[dead])
            Begin_List.append(prev_start)
            prev_start+=width
            freq=0
        return Task_List,Begin_List,End_List,deadline_missed,frequency,explanation
                  
    def fcfs (self,release,period,Execution,deadline): #FCFS algorithm###!!!!!!!!!!!!!!!!!!DONE
        Task_List=[]
        Begin_List=[]
        End_List=[]
        deadline_missed=[]
        explanation=[]
        count =0
        prev_start=0
        sort_release= sorted(release.items(), key=lambda x: x[1])
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
                    explanation.append("Task "+str(task_num)+ " Missed Its Deadline At The Time Interval: "+str(deadline[task_num]))
                if (width-int(Execution[task_num])==0):
                    End_List.append(end)
                    Task_List.append(task_num)
                    Begin_List.append(prev_start)
                    prev_start=width+prev_start
                    count+=1      
        return Task_List,Begin_List,End_List,deadline_missed,explanation
    
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
            prev_task=q[0]
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
                if release[task_num_s]<=end:
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
            if len(q)!=0:
                if prev_task!=q[0]:
                    prev_start+=float(context_switching)
        res = [] 
        for i in explanation: 
            if i not in res: 
                res.append(i)
                
        return Task_List,Begin_List,End_List,deadline_missed,res

#####################################################All Graphics and controls beyond  this point
class Draw_Schedule(Frame):
    
    def __init__(self,Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time,round_freq):
        super().__init__()
        algo=Algorithms()
        if (algo_type=="eedf"):
            Task,Begin,End,missed_deadline,frequency,explanation=algo.eedf(Release,Period,Execution,ac1,ac2,N,round_freq)
            #Task_List,Begin_List,End_List,deadline_missed,frequency
        if (algo_type=="laedf"):
            Task,Begin,End,missed_deadline,frequency,explanation=algo.laedf(Release,Period,Execution,ac1,ac2,N,round_freq)
            #Task_List,Begin_List,End_List,deadline_missed,frequency
        if (algo_type=="fcfs"):
            Task,Begin,End,missed_deadline,explanation=algo.fcfs(Release,Period,Execution,deadline)
            frequency=[]
        if (algo_type=="rr"):
            Task,Begin,End,missed_deadline,explanation=algo.rr(Release,Period,Execution,deadline, quantum,N, float(context))
            frequency=[]
        self.Draw_Structure(N,algo_type)
        self.Draw_Task(Task,Begin,End,missed_deadline,explanation,int(end_time),algo_type,frequency)

    def Draw_Structure(self,N,algo_type):##################################### Must Adjust Schedule Diagram to Number Of tasks Len(Task_Number) and change the range by Task_Number/30
        #This is where the Schedule base is Drawn
        if algo_type=="eedf" or algo_type=='laedf':
            print('edf')
            Schedule = tk.Toplevel(app,width=1000,height=450)
            self.grid()
            Counter = 0
            self.canvas = Canvas(Schedule,width=1000,height=450)
            self.canvas.create_line(45, 10, 45, 350)
            self.canvas.create_text(15,(10),fill="darkblue",font="Times 12 italic bold",text='Fm')
            self.canvas.create_text(15,(30),fill="darkblue",font="Times 12 italic bold",text='1')
            self.canvas.create_text(15,(105),fill="darkblue",font="Times 12 italic bold",text='0.75')
            self.canvas.create_text(15,(185),fill="darkblue",font="Times 12 italic bold",text='0.5')
            tsknum=0
           #Draws the Initial X-Axis Lines
            self.canvas.create_line(45, 350, 1000, 350) #Format(x1,y1,x2,y2)
            self.canvas.grid()
        else:
            Schedule = tk.Toplevel(app,width=1000,height=450)
            self.grid()
            Counter = 0
            self.canvas = Canvas(Schedule,width=1000,height=450)
            self.canvas.create_line(25, 10, 1000, 10)
            tsknum=0
            for i in range(40,(((N+1)*30)),30):                  #Draws the Initial X-Axis Lines
                self.canvas.create_line(25, i, 1000, i) #Format(x1,y1,x2,y2)
                self.canvas.create_text(10,i-13,fill="darkblue",font="Times 12 italic bold",text="T"+str(tsknum+1))
                tsknum+=1
            self.canvas.grid()

    def Draw_Task(self,Task_List,Begin_List,End_List,missed_deadline,explanation,end_time,algo_type,frequency):
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
        if algo_type=="eedf" or algo_type=='laedf':
            for i1 in range(45,1000,30):                #Draws the Y-Axis Lines
                self.canvas.create_line(i1, (350), i1, (360))
                self.canvas.create_text(i1-10,(360),fill="darkblue",font="Times 12 italic bold",text=str(Counter))
                Counter+=scale
            for i in range(0,len(frequency)):
                Task=Task_List[i]
                Begin=Begin_List[i]/scale
                End=End_List[i]/scale
                if frequency[i]>1:
                    self.canvas.create_rectangle((30*(Begin)+45), (350), (30*(End)+45), (350-(350*frequency[i])),fill="red")
                    self.canvas.create_text((30*(Begin)+53),((325-(325*frequency[i]))+350),fill="darkred",font="Times 12 italic bold",text=str('T'+str(Task+1)))
                    self.canvas.create_text((30*(Begin)+65),(50),fill="darkblue",font="Times 10 italic bold",text=str(frequency[i]))
                else:
                    self.canvas.create_rectangle((30*(Begin)+45), (350), (30*(End)+45), (350-(325*frequency[i])),fill="blue")
                    self.canvas.create_text((30*(Begin)+65),((350-(325*frequency[i]))-10),fill="darkblue",font="Times 12 italic bold",text=str(frequency[i]))
                    self.canvas.create_text((30*(Begin)+65),((350-(325*frequency[i]))+15),fill="light grey",font="Times 16 italic bold",text=str('T'+str(Task+1)))
        else:
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
        global var
        global var_round
        label_list= []
        entry_list = []
        #Standard setup
        tk.Tk.__init__(self, *args, **kwargs) 
        self.title('Scheduling')
        self.configure(bg='yellow')         
        self.minsize(width=400, height=280)
        self.maxsize(width=400, height=280)
        #Set up the Textboxes,  text, and button
        title_text = font.Font(family='Times', weight = 'bold', size = 13)
        self.task_text = font.Font(family='Times', weight = 'bold', size = 10)
        self.explain_text = font.Font(family='Times', weight = 'bold', size = 7)
        self.txt0 = tk.Label(self, text="Welcome To Simple Simulations!",bg='yellow',font=title_text,fg='dark blue')
        self.txt0.grid(row=0, column=0, sticky='w')
        self.input_des = tk.Label(self, text="Select an Algorithm",bg='yellow',fg='dark blue')
        self.input_des.grid(row=1, column=0, sticky='w')

        self.button0 = tk.Button(self, text="Start", bg='white',command=lambda: self.Execute(),font=self.task_text) # When Clicked, The Schedule is drawn
        self.button0.grid(row=0,column=1, sticky='w')
        self.button1 = tk.Button(self, text="Add Task",bg='white', command=lambda: self.Add_Task(),font=self.task_text) # When Clicked, A task is added
        self.button1.grid(row=1,column=1, sticky='w')
        self.button2 = tk.Button(self, text="Clear",bg='white', command=lambda: self.clear(),font=self.task_text) # When Clicked, All tasks are cleared
        self.button2.grid(row=2,column=1, sticky='w')
        var = tk.IntVar()
        var_round = tk.IntVar()
        self.check1 = tk.Radiobutton(self, text='Cycle-Saving EDF',variable=var, value=1,bg='yellow',font=self.task_text,command=lambda: self.set_text())
        self.check1.grid(row=3,column=1, sticky='w')
        self.check1 = tk.Radiobutton(self, text='Look Ahead EDF',variable=var, value=2,bg='yellow',font=self.task_text,command=lambda: self.set_text())
        self.check1.grid(row=4,column=1, sticky='w')
        self.check4 = tk.Radiobutton(self, text='First In First Out',variable=var, value=3,bg='yellow',font=self.task_text,command=lambda: self.set_text())
        self.check4.grid(row=5,column=1, sticky='w')
        self.check5 = tk.Radiobutton(self, text='Round Robin',variable=var, value=4,bg='yellow',font=self.task_text,command=lambda: self.set_text())
        self.check5.grid(row=6,column=1, sticky='w')
        self.check5 = tk.Radiobutton(self, text='All Frequencies',variable=var_round, value=False,bg='yellow',font=self.task_text)
        self.check5.grid(row=7,column=1, sticky='w')
        self.check5 = tk.Radiobutton(self, text='Round Frequencies',variable=var_round, value=True,bg='yellow',font=self.task_text)
        self.check5.grid(row=8,column=1, sticky='w')
        self.quantum_get=tk.Entry(self,width=10)
        self.context_get=tk.Entry(self,width=10)
        self.quantum_text = tk.Label(self, text="Quantum",bg='yellow',font=self.task_text)
        self.context_text = tk.Label(self, text="Context",bg='yellow',font=self.task_text)
        self.quantum_get.grid(row=9,column=1, sticky='e')
        self.quantum_text.grid(row=9, column=1, sticky='w')
        self.context_get.grid(row=10,column=1, sticky='e')
        self.context_text.grid(row=10,column=1, sticky='w')
        ##Explanation of input
    def set_text(self):
        if var.get() == 1:
            self.input_des.config(text="|WC,Period,AC 1, AC 2| Max 3 Tasks",bg='yellow',fg='dark blue')
        if var.get() == 2:
            self.input_des.config(text="|WC,Period,AC 1, AC 2| Unlimited Tasks",bg='yellow',fg='dark blue')

        if var.get() ==3 or var.get()==4: #FIFO 
            self.input_des.config(text="|Release,Execution,Deadline| Unlimited Tasks",bg='yellow',fg='dark blue')

    def Add_Task(self):
        global counter
        counter +=1
        descript="Task " + str(counter-1) + ":"
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
        if (var.get() == 1):#EEDF
            entry_list_test=["3,8,2,1","3,9,1,1","1,14,1,1"]#added deadline as the last bit
            for i in entry_list:
                Task=i.get()
                Task = Task.split(",")
                Execution.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                ac1.update({count: int(Task[2])})
                ac2.update({count: int(Task[3])})
                count+=1
            algo_type="eedf"
            quantum=0
            context=0#self.context_get.get()
            end_time=0#self.end_time_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time,var_round.get())
        if (var.get() == 2):#laEDF
            #entry_list_test=["2,6,1,1","3,8,1,1","3,12,2,1"]#added deadline as the last bit
            entry_list_test=['3,8,2,1','3,10,1,1','1,14,1,1']
            for i in entry_list:
                Task=i.get()
                Task = Task.split(",")
                Execution.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                ac1.update({count: int(Task[2])})
                ac2.update({count: int(Task[3])})
                count+=1
            algo_type="laedf"
            quantum=0
            context=0#self.context_get.get()
            end_time=0#self.end_time_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time,var_round.get())
        elif (var.get() == 3):###FCFS#######################################
            entry_list_test=["0,75,300","10,40,300","10,25,300","80,20,145","85,45,300"] #(release,deadline,execution)
            for i in entry_list:
                Task=i.get()
                Task = Task.split(",")
                Release.update({count:int(Task[0])})
                Execution.update({count:int(Task[1])})
                deadline.update({count:int(Task[2])})
                count+=1
            round_freq=0
            algo_type="fcfs"
            quantum=0
            context=0#self.context_get.get()
            end_time=0#self.end_time_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time,round_freq)
        elif (var.get() == 4):###RR
            entry_list_test=["30,20,60","20,20,70","10,15,80","5,15,90"]
            #entry_list_test=["0,75,300","10,40,500","10,25,700","80,20,900","85,45,1010"]
            for i in entry_list:
                Task=i.get()
                Task = Task.split(",")
                Release.update({count:int(Task[0])})
                Execution.update({count:int(Task[1])})
                deadline.update({count:int(Task[2])})
                count+=1
            algo_type="rr"
            round_freq=0
            quantum=self.quantum_get.get()
            context=self.context_get.get()
            if context=='':
                context=0
            end_time=0#self.end_time_get.get()
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum,ac1,ac2,context,deadline,end_time,round_freq)
        #self.clear()
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
        counter = 1
        N=0
        
if __name__ == "__main__": 
        app = Main()        
        app.mainloop()
