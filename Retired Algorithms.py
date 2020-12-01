        elif (var3.get() == 1):###RM
            entry_list_test=["0,25,5","0,60,20","0,35,8","0,105,15"]
            for i in entry_list_test:
                Task=i#.get()
            
                Task = Task.split(",")
        
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                count+=1
            algo_type="rm"
            quantum=0
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum)
            
        elif (var2.get() == 1):

            entry_list_test=["0,50,12","0,40,10","0,30,10"]
            for i in entry_list_test:
                Task=i#.get()
            
                Task = Task.split(",")
        
                Release.update({count:int(Task[0])})
                Period.update({count:int(Task[1])})
                Execution.update({count:int(Task[2])})
                count+=1
            algo_type="edf"
            quantum=0
            Draw_Schedule(Release,Period,Execution,N,algo_type,quantum)


        if (algo_type=="edf"):
            print("we edfed")
            Task,Begin,End=algo.edf(Release,Period,Execution)
        if (algo_type=="rm"):
            print("we rmed")
            Task,Begin,End=algo.rm(Release,Period,Execution)

    def rm (self,Release,Period,Execution): #RM algorithm
        #entry_list_test=["0,25,5","0,60,20","0,35,8","0,105,15"]
        Task_List=[]
        Begin_List=[]
        End_List=[]
        sort_period = sorted(Period.items(), key=lambda x: x[1])

        count =0

        prev_start=0
        while (count<10):
            count+=1
            for i in sort_period:
                count+=1

                #print("test->",Execution[i[0]]+1)
                for width in range(0,Execution[i[0]]+1,1):
                    Execution[i[0]]-=1
                    print(Execution)
                    #print(width,prev_start,Execution[i[0]])

                    if (width-(Execution[i[0]])==0):
                        End_List.append(width+prev_start)
                        Task_List.append(i[0])
                        Begin_List.append(prev_start)
                        prev_start=width+prev_start

        #print(Task_List,Begin_List,End_List)        
        print (sort_period)
        return Task_List,Begin_List,End_List

    def edf (self,Release,Period,Execution): #EDF algorithm
        #Ta(50, 12), Tb(40, 10),Tc(30, 10).
        #Release, Period, and Execution Time
        #
        
        #print(Release, Period, Execution)
        #for i in Release:
        #    print(Release[i])
        #     print("The Task value is ->", i)
        # for i1 in Period:
        #     print(Period[i1])
        #    print("The Task value is ->", i1)
        #for i2 in Execution:
        #    print(Execution[i2])
        #    print("The Task value is ->", i2)
        print(Release)
        print(Period)
        print(Execution)
        Task_List=[]
        Begin_List=[]
        End_List=[]
        sort_Period = sorted(Period.items(), key=lambda x: x[1])

        count =0

        prev_start=0
        while (count<10):
            count+=1
            for i in sort_Period:
                count+=1
                #print (i)
                #print("test->",Execution[i[0]]+1)
                for width in range(0,Execution[i[0]]+1,1):
                    #print(width,prev_start,Execution[i[0]])

                    if (width-(Execution[i[0]])==0):
                        End_List.append(width+prev_start)
                        Task_List.append(i[0])
                        Begin_List.append(prev_start)
                        prev_start=width+prev_start

        #print(Task_List,Begin_List,End_List)        
        
        return Task_List,Begin_List,End_List
