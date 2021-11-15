import tkinter as tk
from tkinter import Tk, Canvas, Frame, BOTH, font


class Algorithms():
    
    def look_ahead_earliest_deadline_first(self, release, period, execution_time, ac1, ac2, number_of_tasks, rounded_frequency):
        '''outputs'''
        tasks = []
        starts = []
        ends = []
        deadlines_missed = []
        frequencies = []
        explanations = []
        
        '''calculation variables'''
        prioritized_periods = []
        prioritized_tasks = []
        
        get_index = {}
        get_task = {}

        sorted_periods = sorted(period.items(), key=lambda x: x[1])
        
        queue = []
        frequency=0
        prev_start=0
        
        '''Prioritize task depending upon lowest period'''
        for index, (prioritized_task, prioritized_period) in enumerate(sorted_periods):
            prioritized_tasks.append(int(prioritized_task))
            prioritized_periods.append(int(prioritized_period))
                        
            get_index[int(prioritized_task)] = index    
            get_task[index] = int(prioritized_task)
                    
        '''simulate the first two invocations'''
        for invocation in range(2):
            for current, deadline in enumerate(prioritized_periods):
                if invocation:
                    if prev_start < period[get_task[current]]:
                        prev_start = period[get_task[current]]
                        
                queue = []
                queue.append(prioritized_tasks[current])
                
                if current == len(prioritized_periods) - 1:
                    next = 0
                else:
                    next=current + 1
                    
                '''Check Deference INV1'''
                for i in range(number_of_tasks-1):
                    deadline_difference = prioritized_periods[next] - prioritized_periods[current]

                    '''If we can't defer, add task to queue'''
                    if execution_time[prioritized_tasks[next]] > deadline_difference:
                        queue.append(prioritized_tasks[next])
                        
                    next += 1
                    if next == number_of_tasks:
                        next = 0
                        
                '''Calculate Freqencies in the queue INV 1'''  
                for task in queue:
                    '''if this is the second iteration, use the starting point of the second period as the starting point of reference'''
                    if (prioritized_periods[get_index[task]] - period[task]) != 0 and not invocation:
                        frequency += execution_time[task] / (prioritized_periods[get_index[task]]-period[task])
                    else:
                        '''otherwise assume that the current starting point is the previous start'''
                        frequency += execution_time[task] / (prioritized_periods[get_index[task]]-prev_start)

                '''Double the period value in order to update its deadline'''
                prioritized_periods[current] = prioritized_periods[current]*2

                '''rounding frequencies'''
                if rounded_frequency == True:
                    if frequency <= 1 and frequency > 0.75: 
                        frequency = 1
                    elif frequency <= 0.75 and frequency > 0.5:
                        frequency = 0.75
                    elif frequency <= 0.5:
                        frequency = 0.5
                else:
                    frequency = round(frequency,3)
                    
                if invocation:  duration = ac2[prioritized_tasks[current]] / frequency
                else:           duration = ac1[prioritized_tasks[current]] / frequency
                    
                end = duration + prev_start
                
                frequencies.append(frequency)
                ends.append(end)
                tasks.append(prioritized_tasks[current])
                starts.append(prev_start)
                
                prev_start = end
                frequency = 0
                
        return tasks, starts, ends, deadlines_missed, frequencies, explanations

                  
    def first_in_first_out(self, release, period, execution_time, deadline):
        '''Output Variables'''
        tasks = []
        starts = []
        ends = []
        deadlines_missed = []
        explanations = []

        '''Calculation Variables'''
        prioritized_releases = []
        prioritized_tasks = []
        
        '''prioritize by release'''
        for prioritized_task,prioritized_release in sorted(release.items(), key=lambda x: x[1]):
            prioritized_tasks.append(int(prioritized_task))
            prioritized_releases.append(int(prioritized_release))

        prev_start = prioritized_releases[0]
        
        for task in prioritized_tasks:
            '''bring start up to next task release'''
            if prev_start < release[task]:
                prev_start = release[task]
                
            for duration in range(0, int(execution_time[task])+1,1):
                end = duration + prev_start
                
                '''detect missed deadline'''
                if end > deadline[task]:
                    deadlines_missed.append(deadline[task])
                    explanations.append("task %s Missed Its Deadline At The Time Interval: %s"%(task+1,deadline[task]))

                if duration - int(execution_time[task]) == 0:
                    ends.append(end)
                    tasks.append(task)
                    starts.append(prev_start)
                    prev_start = end
                    
        return tasks, starts, ends, deadlines_missed, list(set(explanations))

    
    def round_robin(self, release, period, execution_time, deadline, quantum, number_of_tasks, context_switching): 
        '''Output Variables'''
        explanations = []
        tasks = []
        starts = []
        ends = []

        '''Calculation Variables'''
        remaining_executions = []
        deadlines_missed = []
        queue = [0]
        
        prioritized_releases = []
        prioritized_tasks = []
        prioritized_task_mem = []

        execution_count = 0

        for prioritized_task, prioritized_release in sorted(release.items(), key=lambda x: x[1]):
            prioritized_tasks.append(int(prioritized_task))
            prioritized_task_mem.append(int(prioritized_task))
            prioritized_releases.append(int(prioritized_release))

        prev_start = float(prioritized_releases[0])
        task = prioritized_tasks.pop(0)
        
        remaining_executions.append(int(execution_time[prioritized_task_mem[0]]))
        
        '''Loops until all tasks are drained'''
        while not all(remaining_execution == 0 for remaining_execution in remaining_executions):
            prev_task = queue[0]
            write = 1
            
            for duration in range(1, int(quantum) + 1,1):
                if remaining_executions[queue[0]] != 0:
                    end = duration + prev_start
                    
                '''detect missed deadline'''
                if (end) > deadline[prioritized_task_mem[queue[0]]]:
                    deadlines_missed.append(deadline[prioritized_task_mem[queue[0]]])
                    explanations.append("Task %s Missed Its Deadline At The Time Interval: %s"%(str(prioritized_task_mem[queue[0]]+1),str(deadline[prioritized_task_mem[queue[0]]])))

                '''If no remaining execution_time in task, do not add to task execution_time'''
                if not remaining_executions[queue[0]]:
                    write = 0
                    break

                remaining_executions[queue[0]] -= 1
                if not remaining_executions[queue[0]]:
                    break

            if write:
                ends.append(end)
                tasks.append(prioritized_task_mem[queue[0]])
                starts.append(prev_start)
                prev_start = end
                
            
            '''Queue organization'''
            count = 0

            for prioritized_task in prioritized_tasks:
                if release[prioritized_task] <= end:
                    if (release[prioritized_task] != end and len(queue) >= 1) or (release[prioritized_task] == end and len(queue) > 1):
                        remaining_executions.append(int(execution_time[prioritized_task]))
                        execution_count = len(remaining_executions) - 1
                        queue.append(execution_count)
                        count += 1
                    
            prioritized_tasks = prioritized_tasks[count:]
            
            '''add remaining execution time to queue'''
            if remaining_executions[queue[0]]:
                remaining_execution = queue.pop(0)
                queue.append(remaining_execution)
            else: 
                queue.pop(0)

            if queue:
                if prev_task != queue[0]:
                    prev_start += float(context_switching)
                
        return tasks, starts, ends, deadlines_missed, list(set(explanations))


#####################################################All Graphics and controls beyond  this point
class draw_schedule(Frame):
    
    def __init__(self, release, period, execution_time, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency=0, context_switching_time=0, quantum=0):
        super().__init__()
        algo = Algorithms()

        if (algorithm == "look_ahead_earliest_deadline_first"):
            task, start, end, missed_deadline, frequencies, explanations = algo.look_ahead_earliest_deadline_first(release, period, execution_time, ac1, ac2, number_of_tasks, rounded_frequency)
            
        if (algorithm == "first_in_first_out"):
            task, start, end, missed_deadline, explanations = algo.first_in_first_out(release,period, execution_time,deadline)
            frequencies = []
            
        if (algorithm == "round_robin"):
            task, start, end, missed_deadline, explanations = algo.round_robin(release, period, execution_time, deadline, quantum, number_of_tasks, float(context_switching_time))
            frequencies = []
            
        self.Draw_Structure(number_of_tasks, algorithm)
        self.Draw_task(task, start, end, missed_deadline, explanations, algorithm, frequencies, number_of_tasks)


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


    def Draw_task(self, tasks, starts, ends, missed_deadline, explanations, algorithm, frequencies, number_of_tasks):
        scale = 1
        x_point = 0
        max_range = ends[len(ends)-1]
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
                
            for index, task in enumerate(tasks):
                task = tasks[index]
                start = starts[index] / scale
                end = ends[index] / scale
                
                if frequencies[index] > 1:
                    self.canvas.create_rectangle((30*(start)+45), (350), (30*(end)+45), (350-(350*frequencies[i])), fill="red")
                    self.canvas.create_text((30*(start)+53),((325-(325*frequencies[i]))+350),fill="darkred",font="Times 12 italic bold",text=str('T%s'%(task+1)))
                    self.canvas.create_text((30*(start)+65),(50),fill="darkblue",font="Times 10 italic bold",text=str(frequencies[index]))
                else:
                    self.canvas.create_rectangle((30*(start)+45), (350), (30*(end)+45), (350-(325*frequencies[index])),fill="blue")
                    self.canvas.create_text((30*(start)+65),((350-(325*frequencies[index]))-10),fill="darkblue",font="Times 12 italic bold",text=str(frequencies[index]))
                    self.canvas.create_text((30*(start)+65),((350-(325*frequencies[index]))+15),fill="light grey",font="Times 16 italic bold",text='T%s'%(task+1))
        else:
            for i1 in range(25,1000,30):                #Draws the Y-Axis Lines
                self.canvas.create_line(i1, (((N+1)*30)-20), i1, (((N+1)*30)-10))
                self.canvas.create_text(i1,(((N+1)*30)),fill="darkblue",font="Times 12 italic bold",text=str(x_point))
                x_point += scale
                
            for index, task in enumerate(tasks):
                start = starts[index]/scale
                end = ends[index]/scale
                self.canvas.create_rectangle((30*(start)+25), ((task*30)+10), (30*(end)+25), ((task*30)+40),fill="blue")
                count = 0
                
            for deadline in missed_deadline:
                self.canvas.create_line((30*(deadline/scale)+25), (10), (30*(deadline/scale)+25), (((N+1)*26)),fill="red",width=5)
                
            count = float(1)
            count_for_break = 0
            
            if not explanations:
                self.canvas.create_text(200,(((N+1)*40)*count),fill="darkblue",font="Times 10 italic bold",text="All tasks Were Schedulable!")
            else:
                for explanation in explanations:
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
            self.txt1.config(text="|Release Time, execution_time Duration, Deadline|",bg='yellow',fg='dark blue')


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
        execution_time = {}
        deadline = {}
        ac1 = {}
        ac2 = {}
        number_of_tasks = len(self.entry_list)
        
        if (self.var.get() == 1):#look_ahead_earliest_deadline_first
            entry_list_test=["3,12,2,1","2,6,1,1","3,8,1,1"]#added deadline as the last bit
            #entry_list_test = ['3,8,2,1','3,10,1,1','1,14,1,1']
            self.entry_list = entry_list_test
            number_of_tasks = len(self.entry_list)
            
            for count, entry in enumerate(self.entry_list):
                task = entry#.get()
                task = task.split(",")
                ac2[count] = int(task[3])
                ac1[count] = int(task[2])
                period[count] = int(task[1])
                execution_time[count] = int(task[0])

                
            algorithm = "look_ahead_earliest_deadline_first"
            rounded_frequency = self.var_round.get()
            quantum = 0
            context_switching_time = self.context_get.get()
            if not context_switching_time:
                context_switching_time = 0
                
            draw_schedule(release, period, execution_time, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency, context_switching_time, quantum)
            
        elif (self.var.get() == 2):###first_in_first_out#######################################
            entry_list_test = ["0,75,300","10,40,300","10,25,300","80,20,145","85,45,300"] #(release,deadline,execution_time)
            self.entry_list = entry_list_test
            number_of_tasks = len(self.entry_list)
            
            for count, entry in enumerate(self.entry_list):
                task = entry#.get()
                task = task.split(",")
                release[count] = int(task[0])
                deadline[count] = int(task[2])
                execution_time[count] = int(task[1])
                
            algorithm = "first_in_first_out"
            rounded_frequency = 0
            quantum = 0
            context_switching_time = self.context_get.get()
            
            if not context_switching_time:
                context_switching_time = 0
                
            draw_schedule(release, period, execution_time, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency, context_switching_time, quantum)
            
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
                execution_time[count] = int(task[1])
                
            algorithm = "round_robin"
            rounded_frequency = 0
            quantum = self.quantum_get.get()
            context_switching_time = self.context_get.get()
            
            if not context_switching_time: 
                context_switching_time = 0
            if not quantum:
                quantum = 5
        
            draw_schedule(release, period, execution_time, number_of_tasks, algorithm, ac1, ac2, deadline,  rounded_frequency, context_switching_time, quantum)
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
