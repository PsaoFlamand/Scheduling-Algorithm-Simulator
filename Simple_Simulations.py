import tkinter as tk
from tkinter import Tk, Canvas, Frame, BOTH, font


class Algorithms():

    
    def look_ahead_earliest_deadline_first(self, release, period, execution, ac1, ac2, number_of_tasks, rounded_frequency): #Look ahead Earliest Deadline First
        task_list = []
        start_list = []
        end_list = []
        deadline_missed = []
        frequency_list = []
        explanation_list = []
        deadline_list=[]
        sort_period = sorted(period.items(), key=lambda x: x[1])
        prioritized_period =[]
        prioritized_task_list = []
        tracker = {}
        op_tracker = {}
        
        
        for count, priority in enumerate(sort_period):
            prioritized_task_list.append(int(priority[0]))
            prioritized_period.append(int(priority[1]))
            deadline_list.append(int(priority[1]))
            
            tracker[int(priority[0])] = count    
            op_tracker[count] = int(priority[0])
            
        selector = 1
        queue = []
        frequency=0
        prev_start=0

        for index, deadline in enumerate(deadline_list): #invocation 1
            queue = []
            queue.append(prioritized_task_list[index])
            
            if index == len(deadline_list) - 1:
                selector = 0
            else:
                selector=index + 1
                
            for i in range(0,number_of_tasks-1):#Check Deference INV1
                deadline_difference = deadline_list[selector] - deadline_list[index]
                if execution[prioritized_task_list[selector]] > deadline_difference:
                    queue.append(prioritized_task_list[selector])#We know which ones we can't defer  
                selector += 1
                if selector == number_of_tasks:
                    selector = 0

            for task in queue: #Calculate Freqencies in the queue INV 1     
                if (deadline_list[tracker[task]] - period[task]) != 0:
                    frequency += execution[task] / (deadline_list[tracker[task]]-period[task])
                else:
                    frequency += execution[task] / (deadline_list[tracker[task]]-prev_start)
            deadline_list[index] = deadline_list[index]*2
            
            if rounded_frequency == True:
                if frequency <= 1 and frequency > 0.75: #rounding frequency_list
                    frequency = 1
                elif frequency <= 0.75 and frequency > 0.5:
                    frequency = 0.75
                elif frequency <= 0.5:
                    frequency = 0.5
            else:
                frequency = round(frequency,3)
                
            width = ac1[prioritized_task_list[index]]/frequency
            end_time = width + prev_start
            frequency_list.append(frequency)
            end_list.append(end_time)
            task_list.append(prioritized_task_list[index])
            start_list.append(prev_start)
            prev_start += width
            frequency = 0
            
        for index, deadline in enumerate(deadline_list): #invocation 2 Deferance check
            if prev_start < period[op_tracker[index]]:
                prev_start = period[op_tracker[index]]
                
            queue = []
            queue.append(prioritized_task_list[index])
            
            if index == len(deadline_list) - 1:
                selector = 0
            else:
                selector = index + 1
                
            for i in range(0,number_of_tasks-1):
                deadline_difference = deadline_list[selector]-deadline_list[index]
                if execution[prioritized_task_list[selector]]>deadline_difference:
                    queue.append(prioritized_task_list[selector])#We know which ones we can't defer  
                selector += 1
                if selector == number_of_tasks:
                    selector = 0
                    
            for task in queue:#Calculate the Invocation 2 queue frequencies
                frequency += execution[task] / (deadline_list[tracker[task]]-prev_start)
            deadline_list[index] = deadline_list[index]*2
            
            if rounded_frequency == True:
                if frequency <= 1 and frequency > 0.75:
                    frequency = 1
                elif frequency <= 0.75 and frequency > 0.5:
                    frequency = 0.75
                elif frequency <= 0.5:
                    frequency = 0.5
            else:
                frequency = round(frequency, 3)

            width = ac2[prioritized_task_list[index]] / frequency
            end_time = width + prev_start
            frequency_list.append(frequency)
            end_list.append(end_time)
            task_list.append(prioritized_task_list[index])
            start_list.append(prev_start)
            prev_start += width
            frequency = 0
            
        return task_list, start_list, end_list, deadline_missed, frequency_list, explanation_list

                  
    def first_come_first_serve (self, release, period, execution, deadline): #first_come_first_serve algorithm###!!!!!!!!!!!!!!!!!!DONE
        task_list = []
        start_list = []
        end_list = []
        deadline_missed = []
        explanation_list = []
        count = 0
        prev_start = 0
        sort_release = sorted(release.items(), key=lambda x: x[1])
        prioritized_release = []
        prioritized_task_list = []
        
        for priority in sort_release:
            prioritized_task_list.append(int(priority[0]))
            prioritized_release.append(int(priority[1]))
        prev_start = prioritized_release[0]
        
        for task_num in prioritized_task_list:
            while prev_start < release[task_num]:
                prev_start += 1
            reset = 0
            for width in range(0, int(execution[task_num])+1,1):
                end = width + prev_start               

                if (end) > deadline[task_num] and reset == 0:#detect missed deadline
                    reset = 1
                    deadline_missed.append(deadline[task_num])
                    explanation_list.append("task %s Missed Its Deadline At The Time Interval: %s"%(task_num+1,deadline[task_num]))

                if (width - int(execution[task_num]) == 0):
                    end_list.append(end)
                    task_list.append(task_num)
                    start_list.append(prev_start)
                    prev_start = width + prev_start
                    count += 1
                    
        return task_list, start_list, end_list, deadline_missed, explanation_list

    
    def round_robin (self, release, period, execution, deadline, quantum, number_of_tasks, context_switching): #round_robin algorithm###!!!!!!!!!!!!!!!!!!DONE
        explanation_list = []
        task_list = []
        start_list = []
        end_list = []       
        remaining_execution = []
        deadline_missed = []
        queue = []
        sort_release = sorted(release.items(), key=lambda x: x[1])
        prioritized_release = []
        prioritized_task_list = []
        prioritized_task_test = []

        for priority in sort_release:
            prioritized_task_list.append(int(priority[0]))
            prioritized_task_test.append(int(priority[0]))
            prioritized_release.append(int(priority[1]))

        prev_start = float(prioritized_release[0])
        exe_count = 0
        task_num = prioritized_task_list[0]
        queue.append(exe_count)
        del prioritized_task_list[0]
        remaining_execution.append(int(execution[prioritized_task_test[0]]))

        while not all(remains == 0 for remains in remaining_execution):#Loops until all tasks are drained
            prev_task = queue[0]
            write = 1
            reset = 0
            
            for width in range(1, int(quantum) + 1,1):
                if remaining_execution[queue[0]] != 0:
                    end = width + prev_start
                    
                if (end) > deadline[prioritized_task_test[queue[0]]] and reset == 0:#detect missed deadline
                    reset = 1
                    deadline_missed.append(deadline[prioritized_task_test[queue[0]]])
                    explanation_list.append("Task %s Missed Its Deadline At The Time Interval: %s"%(str(prioritized_task_test[queue[0]]+1),str(deadline[prioritized_task_test[queue[0]]])))

                '''If no remaining execution in task, do not add to task execution'''
                if not remaining_execution[queue[0]]:
                    write = 0
                    break

                remaining_execution[queue[0]] -= 1
                if not remaining_execution[queue[0]]:
                    break

            if write:
                end_list.append(end)
                task_list.append(prioritized_task_test[queue[0]])
                start_list.append(prev_start)
                prev_start = width + prev_start
                
            ###decides which task to drain
            count = 0
            
            for prioritized_task in prioritized_task_list:
                if release[prioritized_task] <= end:
                    if release[prioritized_task] != end and len(queue) == 1:#Queue organization
                        remaining_execution.append(int(execution[prioritized_task]))
                        exe_count = len(remaining_execution) - 1
                        queue.append(exe_count)
                        count += 1
                    elif release[prioritized_task] == end and len(queue) > 1:
                        remaining_execution.append(int(execution[prioritized_task]))
                        exe_count = len(remaining_execution)-1
                        queue.append(exe_count)
                        count += 1
                    elif release[prioritized_task] != end and len(queue) > 1:
                        remaining_execution.append(int(execution[prioritized_task]))
                        exe_count = len(remaining_execution)-1
                        queue.append(exe_count)
                        count += 1
            for i in range(count): 
                del prioritized_task_list[0]
                
            if remaining_execution[queue[0]] != 0:#Am I calling the right tasks?
                excess = queue.pop(0)
                queue.append(excess)
            else: 
                excess = queue.pop(0)

            if queue:
                if prev_task != queue[0]:
                    prev_start += float(context_switching)
        res = [] 
        for i in explanation_list: 
            if i not in res: 
                res.append(i)
                
        return task_list, start_list, end_list, deadline_missed, res


#####################################################All Graphics and controls beyond  this point
class draw_schedule(Frame):

    
    def __init__(self, release, period, execution, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency=0, context_switching_time=0, quantum=0):
        super().__init__()
        algo = Algorithms()

        if (algorithm == "look_ahead_earliest_deadline_first"):
            task, start, end, missed_deadline, frequency_list, explanation_list = algo.look_ahead_earliest_deadline_first(release, period, execution, ac1, ac2, number_of_tasks, rounded_frequency)
            
        if (algorithm == "first_come_first_serve"):
            task, start, end, missed_deadline, explanation_list = algo.first_come_first_serve(release,period, execution,deadline)
            frequency_list = []
            
        if (algorithm == "round_robin"):
            task, start, end, missed_deadline, explanation_list = algo.round_robin(release, period, execution, deadline, quantum, number_of_tasks, float(context_switching_time))
            frequency_list = []
            
        self.Draw_Structure(number_of_tasks, algorithm)
        self.Draw_task(task, start, end, missed_deadline, explanation_list, algorithm, frequency_list, number_of_tasks)


    def Draw_Structure(self, number_of_tasks, algorithm):##################################### Must Adjust schedule Diagram to Number Of tasks Len(task_Number) and change the range by task_Number/30
        #This is where the schedule base is Drawn
        if algorithm == 'look_ahead_earliest_deadline_first':
            print('edf')
            schedule = tk.Toplevel(app,width=1000,height=450)
            self.grid()
            counter = 0

            self.canvas = Canvas(schedule,width=1000,height=450)
            self.canvas.create_line(45, 10, 45, 350)
            self.canvas.create_text(15,(10),fill="darkblue",font="Times 12 italic bold",text='Fm')
            self.canvas.create_text(15,(30),fill="darkblue",font="Times 12 italic bold",text='1')
            self.canvas.create_text(15,(105),fill="darkblue",font="Times 12 italic bold",text='0.75')
            self.canvas.create_text(15,(185),fill="darkblue",font="Times 12 italic bold",text='0.5')
            task_number = 0
            
           #Draws the Initial X-Axis Lines
            self.canvas.create_line(45, 350, 1000, 350) #Format(x1,y1,x2,y2)
            self.canvas.grid()

        else:
            schedule = tk.Toplevel(app,width=1000,height=450)
            self.grid()
            counter = 0
            self.canvas = Canvas(schedule,width=1000,height=450)
            self.canvas.create_line(25, 10, 1000, 10)
            task_number = 0
            
            for i in range(40,(((number_of_tasks+1)*30)),30):                  #Draws the Initial X-Axis Lines
                self.canvas.create_line(25, i, 1000, i) #Format(x1,y1,x2,y2)
                self.canvas.create_text(10,i-13,fill="darkblue",font="Times 12 italic bold",text="T%s"%(task_number+1))
                task_number += 1
            self.canvas.grid()


    def Draw_task(self, task_list, start_list, end_list, missed_deadline, explanation_list, algorithm, frequency_list, number_of_tasks):
        scale = 1
        x_point = 0
        max_range = end_list[len(end_list)-1]
        N = number_of_tasks
        
        if (max_range > 320):
            scale = 20
        if(max_range > 160 and max_range <= 320):
            scale = 10
        if(max_range > 60 and max_range <= 160):
            scale = 5
        elif(max_range > 30 and max_range <= 60):
            scale = 2
        elif(max_range <= 30):
            scale = 1
            
        if algorithm == "eedf" or algorithm == 'look_ahead_earliest_deadline_first':
            for i1 in range(45,1000,30):#Draws the Y-Axis Lines
                self.canvas.create_line(i1, (350), i1, (360))
                self.canvas.create_text(i1-10,(360),fill="darkblue",font="Times 12 italic bold",text=str(x_point))
                x_point += scale
                
            for index, task in enumerate(task_list):
                task = task_list[index]
                start = start_list[index] / scale
                end = end_list[index] / scale
                
                if frequency_list[index] > 1:
                    self.canvas.create_rectangle((30*(start)+45), (350), (30*(end)+45), (350-(350*frequency_list[i])), fill="red")
                    self.canvas.create_text((30*(start)+53),((325-(325*frequency_list[i]))+350),fill="darkred",font="Times 12 italic bold",text=str('T%s'%(task+1)))
                    self.canvas.create_text((30*(start)+65),(50),fill="darkblue",font="Times 10 italic bold",text=str(frequency_list[index]))
                else:
                    self.canvas.create_rectangle((30*(start)+45), (350), (30*(end)+45), (350-(325*frequency_list[index])),fill="blue")
                    self.canvas.create_text((30*(start)+65),((350-(325*frequency_list[index]))-10),fill="darkblue",font="Times 12 italic bold",text=str(frequency_list[index]))
                    self.canvas.create_text((30*(start)+65),((350-(325*frequency_list[index]))+15),fill="light grey",font="Times 16 italic bold",text='T%s'%(task+1))
        else:
            for i1 in range(25,1000,30):                #Draws the Y-Axis Lines
                self.canvas.create_line(i1, (((N+1)*30)-20), i1, (((N+1)*30)-10))
                self.canvas.create_text(i1,(((N+1)*30)),fill="darkblue",font="Times 12 italic bold",text=str(x_point))
                x_point += scale
                
            for index, task in enumerate(task_list):
                start = start_list[index]/scale
                end = end_list[index]/scale
                self.canvas.create_rectangle((30*(start)+25), ((task*30)+10), (30*(end)+25), ((task*30)+40),fill="blue")
                count = 0
                
            for deadline in missed_deadline:
                self.canvas.create_line((30*(deadline/scale)+25), (10), (30*(deadline/scale)+25), (((N+1)*26)),fill="red",width=5)
                
            count = float(1)
            count_for_break = 0
            
            if not explanation_list:
                self.canvas.create_text(200,(((N+1)*40)*count),fill="darkblue",font="Times 10 italic bold",text="All tasks Were Schedulable!")
            else:
                for explanation in explanation_list:
                    self.canvas.create_text(200,(((N+1)*40)*count),fill="darkblue",font="Times 10 italic bold",text=str(explanation))
                    count += float(0.1)
                    
                    if count_for_break == N-1:
                        break
                    
                    count_for_break += 1

            
class main(Tk): #This Module sets up the original window with search boxes, labels, and a button

    
    def __init__(self, *args, **kwargs):
        global number_of_tasks

        self.counter = 1
        
        self.label_list = []
        self.entry_list = []
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
        
        self.txt0 = tk.Label(self, text="Welcome To Simple Simulations!", bg='yellow', font=title_text, fg='dark blue')       
        self.txt1 = tk.Label(self, text="Select an Algorithm",bg='yellow',fg='dark blue')

        self.txt0.grid(row=0, column=0, sticky='w')
        self.txt1.grid(row=1, column=0, sticky='w')
        
        self.button0 = tk.Button(self, text="Start", bg='white',command=lambda: self.execute(),font=self.task_text) # When Clicked, The schedule is drawn
        self.button1 = tk.Button(self, text="Add task",bg='white', command=lambda: self.add_task(),font=self.task_text) # When Clicked, A task is added
        self.button2 = tk.Button(self, text="Clear",bg='white', command=lambda: self.clear(),font=self.task_text) # When Clicked, All tasks are cleared
        
        self.button0.grid(row=0, column=1, sticky='w')
        self.button1.grid(row=1, column=1, sticky='w')
        self.button2.grid(row=2, column=1, sticky='w')
        
        self.var = tk.IntVar()
        self.var_round = tk.IntVar()

        self.radio_button1 = tk.Radiobutton(self, text='Look Ahead EDF',variable=self.var, value=1,bg='yellow',font=self.task_text,command=lambda: self.set_text())
        self.radio_button2 = tk.Radiobutton(self, text='First In First Out',variable=self.var, value=2,bg='yellow',font=self.task_text,command=lambda: self.set_text())
        self.radio_button3 = tk.Radiobutton(self, text='Round Robin',variable=self.var, value=3,bg='yellow',font=self.task_text,command=lambda: self.set_text())
        self.radio_button4 = tk.Radiobutton(self, text='All Frequencies',variable=self.var_round, value=False,bg='yellow',font=self.task_text)
        self.radio_button5 = tk.Radiobutton(self, text='Round Frequencies',variable=self.var_round, value=True,bg='yellow',font=self.task_text)

        self.radio_button1.grid(row=4,column=1, sticky='w')
        self.radio_button2.grid(row=5,column=1, sticky='w')
        self.radio_button3.grid(row=6,column=1, sticky='w')
        self.radio_button4.grid(row=7,column=1, sticky='w')
        self.radio_button5.grid(row=8,column=1, sticky='w')

        self.quantum_get = tk.Entry(self, width=10)
        self.context_get = tk.Entry(self, width=10)
        
        self.quantum_text = tk.Label(self, text="Quantum",bg='yellow',font=self.task_text)
        self.context_text = tk.Label(self, text="Context",bg='yellow',font=self.task_text)
        
        self.quantum_get.grid(row=9,column=1, sticky='e')
        self.quantum_text.grid(row=9, column=1, sticky='w')
        self.context_get.grid(row=10, column=1, sticky='e')
        self.context_text.grid(row=10, column=1, sticky='w')


    def set_text(self):
        if self.var.get() == 1:
            self.txt1.config(text="|Worst Case, Period, Actual 1, Actual 2|",bg='yellow',fg='dark blue')
            
        if self.var.get() == 2 or self.var.get() == 3: #FIFO 
            self.txt1.config(text="|Release Time, Execution Duration, Deadline|",bg='yellow',fg='dark blue')


    def add_task(self):
        self.counter += 1
        description = "task %s:"%(self.counter-1)
        self.txtin = tk.Entry(self,width=20)
        self.txt = tk.Label(self, text=description,bg='yellow',font=self.task_text)
        self.txt.grid(row=self.counter, column=0, sticky='w') 
        self.entry_list.append(self.txtin)
        self.label_list.append(self.txt)
        self.txtin.grid(row=self.counter,column=0)

        
    def execute(self):
        global number_of_tasks
        release = {}
        period = {}
        execution = {}
        deadline = {}
        ac1 = {}
        ac2 = {}
        number_of_tasks = len(self.entry_list)
        
        if (self.var.get() == 1):#look_ahead_earliest_deadline_first
            #entry_list_test=["2,6,1,1","3,8,1,1","3,12,2,1"]#added deadline as the last bit
            entry_list_test = ['3,8,2,1','3,10,1,1','1,14,1,1']
            self.entry_list = entry_list_test
            number_of_tasks = len(self.entry_list)
            
            for count, entry in enumerate(self.entry_list):
                task = entry#.get()
                task = task.split(",")
                ac2[count] = int(task[3])
                ac1[count] = int(task[2])
                period[count] = int(task[1])
                execution[count] = int(task[0])

                
            algorithm = "look_ahead_earliest_deadline_first"
            rounded_frequency = self.var_round.get()
            quantum = 0
            context_switching_time = self.context_get.get()
            if not context_switching_time:
                context_switching_time = 0
                
            draw_schedule(release, period, execution, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency, context_switching_time, quantum)
            
        elif (self.var.get() == 2):###first_come_first_serve#######################################
            entry_list_test = ["0,75,300","10,40,300","10,25,300","80,20,145","85,45,300"] #(release,deadline,execution)
            self.entry_list = entry_list_test
            number_of_tasks = len(self.entry_list)
            
            for count, entry in enumerate(self.entry_list):
                task = entry#.get()
                task = task.split(",")
                release[count] = int(task[0])
                deadline[count] = int(task[2])
                execution[count] = int(task[1])
                
            algorithm = "first_come_first_serve"
            rounded_frequency = 0
            quantum = 0
            context_switching_time = self.context_get.get()
            
            if not context_switching_time:
                context_switching_time = 0
                
            draw_schedule(release, period, execution, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency, context_switching_time, quantum)
            
        elif (self.var.get() == 3):###round_robin
            entry_list_test = ["30,20,60","20,20,70","10,15,80","5,15,90"]
            #entry_list_test=["0,75,300","10,40,500","10,25,700","80,20,900","85,45,1010"]
            self.entry_list = entry_list_test
            number_of_tasks = len(self.entry_list)
            
            for count, entry in enumerate(self.entry_list):
                task = entry#.get()
                task = task.split(",")
                release[count] = int(task[0])
                deadline[count] = int(task[2])
                execution[count] = int(task[1])
                
            algorithm = "round_robin"
            rounded_frequency = 0
            quantum = self.quantum_get.get()
            context_switching_time = self.context_get.get()
            
            if not context_switching_time: 
                context_switching_time = 0
            if not quantum:
                quantum = 5
        
            draw_schedule(release, period, execution, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency, context_switching_time, quantum)
        #self.clear()

        
    def clear(self):
        global number_of_tasks

        for _entry,_label in zip(self.entry_list,self.label_list):
            _entry.grid_forget()
            _label.grid_forget()
            
        self.entry_list.clear()
        self.label_list.clear()
        
        self.counter = 1

        
if __name__ == "__main__": 
        app = main()        
        app.mainloop()
