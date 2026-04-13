from ProcessPkg.Process import Process
import copy
class SJF:
    def __init__(self,ProcessList):
        self.ProcessList=copy.deepcopy(ProcessList)
        self.AvgTurnAround=0 
        self.AvgWaitingTime=0 
 

    def SJFAlgoNonPreemptive (self):
        Counter=0
        SortedProcessList=[]
        #sorting proc3ess list according to arrival time and burst time
        self.ProcessList.sort(key=lambda p: (p.BurstTime,p.ArrivalTime))
        shortestProcess=min(self.ProcessList,key =lambda p:p.ArrivalTime)
        SortedProcessList.append(shortestProcess)
        self.ProcessList.remove(shortestProcess)
        #calculating start time and end time for first process
        SortedProcessList[0].StartTime=SortedProcessList[0].ArrivalTime
        SortedProcessList[0].EndTime=SortedProcessList[0].StartTime+SortedProcessList[0].BurstTime
        SortedProcessList[0].TurnAround=SortedProcessList[0].EndTime-SortedProcessList[0].ArrivalTime
        SortedProcessList[0].WaitingTime=SortedProcessList[0].TurnAround-SortedProcessList[0].BurstTime
        
        self.AvgTurnAround+=SortedProcessList[0].TurnAround
        self.AvgWaitingTime+=SortedProcessList[0].WaitingTime
        
        Counter+=SortedProcessList[0].EndTime
        #searching for leastBurst avilable process
        #calculating the ProcessProperities in the same iteration
        while (len(self.ProcessList)):
            shortestProcess=next((p for p in self.ProcessList if p.ArrivalTime<=Counter),None)
            if(shortestProcess==None):
                #finding the next processupon arrival
                shortestProcess=min(self.ProcessList,key=lambda p:p.ArrivalTime)
                #calculate the Prop
                shortestProcess.StartTime=shortestProcess.ArrivalTime
                shortestProcess.EndTime=shortestProcess.StartTime+shortestProcess.BurstTime
                shortestProcess.TurnAround=shortestProcess.EndTime-shortestProcess.ArrivalTime
                shortestProcess.WaitingTime=shortestProcess.TurnAround-shortestProcess.BurstTime
                #Append in the sorted List and update the counter
                SortedProcessList.append(shortestProcess)
                self.ProcessList.remove(shortestProcess)
                Counter=shortestProcess.EndTime
            else:
                shortestProcess.StartTime=Counter
                shortestProcess.EndTime=shortestProcess.StartTime+shortestProcess.BurstTime
                shortestProcess.TurnAround=shortestProcess.EndTime-shortestProcess.ArrivalTime
                shortestProcess.WaitingTime=shortestProcess.TurnAround-shortestProcess.BurstTime
                SortedProcessList.append(shortestProcess)
                self.ProcessList.remove(shortestProcess)
                Counter=shortestProcess.EndTime
            self.AvgTurnAround+=shortestProcess.TurnAround
            self.AvgWaitingTime+=shortestProcess.WaitingTime

            
        self.ProcessList=SortedProcessList
        self.AvgTurnAround=self.AvgTurnAround/len(self.ProcessList)
        self.AvgWaitingTime=self.AvgWaitingTime/len(self.ProcessList)
        return self.ProcessList,self.AvgWaitingTime,self.AvgTurnAround

    def SJFAlgoPreemptive (self): 
        SortedProcessList=[] 
        ##self.ProcessList.sort(key=lambda p: (p.RemainingTime,p.ArrivalTime))
        Counter=0
        FinishedProcess=0
        LastProcessPID=None
        while(len(self.ProcessList)!=FinishedProcess):
            #intialize the minimum remaining time to infinity and selected process to null
            minRemain= float('inf')
            selectProcess=None
            #searching for leastBurst avilable process
            for p in self.ProcessList:
                if(p.ArrivalTime<=Counter and (p.RemainingTime<minRemain and p.RemainingTime>0)):
                    minRemain=p.RemainingTime
                    selectProcess=p
            #if there is no process available increase the counter and continue searching
            if(selectProcess==None):
                available = [p for p in self.ProcessList if p.ArrivalTime > Counter]
                nextprocess=min(available,key=lambda p:p.ArrivalTime)
                Counter+=nextprocess.ArrivalTime-Counter       
                print("Counter: ",Counter)  
                continue
            #if there is a process available execute it for 1 unit of time
            else:
                # if The pocess is starting for the first time set the start time
                if(selectProcess.RemainingTime==selectProcess.BurstTime):
                    selectProcess.StartTime=Counter

                selectProcess.RemainingTime-=1
                
                #if the process is finished calculate the properties and update the counter
                if(selectProcess.RemainingTime==0):
                    selectProcess.EndTime=Counter+1
                    FinishedProcess+=1
                    ProcessTurnAround=selectProcess.EndTime-selectProcess.ArrivalTime
                    selectProcess.TurnAround=ProcessTurnAround
                    self.AvgTurnAround+=ProcessTurnAround
                    ProcessWaitingTime=ProcessTurnAround-selectProcess.BurstTime
                    selectProcess.WaitingTime=ProcessWaitingTime    
                    self.AvgWaitingTime += ProcessWaitingTime
                #creating a new process with burst time 1 to be added in the sorted list
                if (selectProcess.PID ==LastProcessPID):
                    SortedProcessList[-1].EndTime=Counter+1
                    SortedProcessList[-1].BurstTime+=1
                    SortedProcessList[-1].TurnAround=ProcessTurnAround
                    SortedProcessList[-1].WaitingTime=ProcessWaitingTime    
                else:
                    CreatedProcess= Process(selectProcess.PID,ArrivalTime=selectProcess.ArrivalTime,TurnAround=0,WaitingTime=0)
                    CreatedProcess.StartTime=Counter
                    CreatedProcess.EndTime=Counter+1
                    CreatedProcess.BurstTime=1
                    SortedProcessList.append(CreatedProcess)
                    LastProcessPID=CreatedProcess.PID
            Counter +=1
            print("Counter: ",Counter)  

        n = len(self.ProcessList)
        self.AvgTurnAround /= n
        self.AvgWaitingTime /= n
        return SortedProcessList,self.AvgWaitingTime,self.AvgTurnAround

        
        
