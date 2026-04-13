from ProcessPkg.Process import Process
from copy import deepcopy
class FCFS:
    def __init__(self,ProcessList):
        self.ProcessList=deepcopy(ProcessList)
        self.AvgTurnAround=0 
        self.AvgWaitingTime=0 
 

    def FCFSAlgo (self):
        #sorting proc3ess list according to arrival time and burst time
        self.ProcessList.sort(key=lambda p: (p.ArrivalTime))
        #calculating start time and end time for each process
        counter = self.ProcessList[0].BurstTime
        self.ProcessList[0].StartTime=self.ProcessList[0].ArrivalTime
        self.ProcessList[0].EndTime=self.ProcessList[0].StartTime+self.ProcessList[0].BurstTime
        self.ProcessList[0].TurnAround=self.ProcessList[0].EndTime-self.ProcessList[0].ArrivalTime
        self.ProcessList[0].WaitingTime=self.ProcessList[0].TurnAround-self.ProcessList[0].BurstTime
        self.AvgTurnAround+=self.ProcessList[0].TurnAround
        self.AvgWaitingTime+=self.ProcessList[0].WaitingTime
        for i in range(1,len(self.ProcessList)):
            if self.ProcessList[i].ArrivalTime<=counter:
                self.ProcessList[i].StartTime=self.ProcessList[i-1].EndTime
                self.ProcessList[i].EndTime=self.ProcessList[i].StartTime+self.ProcessList[i].BurstTime
            else:
                self.ProcessList[i].StartTime=self.ProcessList[i].ArrivalTime
                self.ProcessList[i].EndTime=self.ProcessList[i].StartTime+self.ProcessList[i].BurstTime
                
            counter =self.ProcessList[i].EndTime   
            self.ProcessList[i].TurnAround=self.ProcessList[i].EndTime-self.ProcessList[i].ArrivalTime
            self.ProcessList[i].WaitingTime=self.ProcessList[i].TurnAround-self.ProcessList[i].BurstTime
            self.AvgTurnAround+=self.ProcessList[i].TurnAround
            self.AvgWaitingTime+=self.ProcessList[i].WaitingTime

        self.AvgTurnAround=self.AvgTurnAround/len(self.ProcessList)
        self.AvgWaitingTime=self.AvgWaitingTime/len(self.ProcessList)
        return self.ProcessList,self.AvgWaitingTime,self.AvgTurnAround
            