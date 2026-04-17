class Process:
    def __init__(self,PID,ArrivalTime=None,Priority=None,BurstTime=None,StartTime=None,EndTime=None,TurnAround=None,WaitingTime=None,RemainingTime=None):
        self.PID=PID
        self.ArrivalTime=ArrivalTime
        self.Priority=Priority
        self.BurstTime=BurstTime
        self.StartTime = StartTime
        self.EndTime=EndTime
        self.TurnAround=TurnAround
        self.WaitingTime=WaitingTime
        self.RemainingTime=BurstTime
        self.status="Not Started"
#setter and getters   
    def get_PID(self):
        return self.PID
    def get_ArrivalTime(self): 
        return self.ArrivalTime
    def get_Priority(self):
        return self.Priority
    def get_BurstTime(self):
        return self.BurstTime
    def get_StartTime(self):
        return self.StartTime
    def get_EndTime(self):
        return self.EndTime
    def get_TurnAround(self):
        return self.TurnAround
    def get_WaitingTime(self):
        return self.WaitingTime
    def get_status(self):   
        return self.status
    
    def set_PID(self,PID):
        self.PID=PID
    def set_ArrivalTime(self,ArrivalTime):
        self.ArrivalTime=ArrivalTime
    def set_Priority(self,Priority):
        self.Priority=Priority
    def set_BurstTime(self,BurstTime):
        self.BurstTime=BurstTime
    def set_StartTime(self,StartTime):
        self.StartTime=StartTime
    def set_EndTime(self,EndTime):
        self.EndTime=EndTime
    def set_status(self,status):
        self.status=status      
    def set_TurnAround(self,TurnAround):
        self.TurnAround=TurnAround
    def set_WaitingTime(self,WaitingTime):
        self.WaitingTime=WaitingTime

    def __str__(self):
        return (f"PID={self.PID}, "
                f"ArrivalTime={self.ArrivalTime}, "
                f"Priority={self.Priority}, "
                f"BurstTime={self.BurstTime}, "
                f"StartTime={self.StartTime}, "
                f"EndTime={self.EndTime}, "
                f"TurnAround={self.TurnAround}, "
                f"WaitingTime={self.WaitingTime}, "
                f"Status={self.status}")
    def __repr__(self):
        return self.__str__()