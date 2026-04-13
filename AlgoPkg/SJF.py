class SJF:
    def __init__(self, ProcessList):
        self.ProcessList = ProcessList
        self.AvgTurnAround = 0 
        self.AvgWaitingTime = 0 

    def SJFAlgoNonPreemptive(self):
        Counter = 0
        n = len(self.ProcessList)
        timeline = []
        
        # Copy list to safely remove items as they finish
        remaining = list(self.ProcessList)

        while remaining:
            # Find all processes that have arrived by the current time
            availableProcesses = [p for p in remaining if p.ArrivalTime <= Counter]

            if not availableProcesses:
                # If no process is here yet, jump forward in time to the next arrival
                shortestProcess = min(remaining, key=lambda p: p.ArrivalTime)
                Counter = shortestProcess.ArrivalTime
            else:
                # Pick the one with the shortest burst time. Break ties using Arrival Time.
                shortestProcess = min(availableProcesses, key=lambda p: (p.BurstTime, p.ArrivalTime))
                
                shortestProcess.StartTime = Counter
                shortestProcess.EndTime = Counter + shortestProcess.BurstTime
                
                shortestProcess.TurnAround = shortestProcess.EndTime - shortestProcess.ArrivalTime
                shortestProcess.WaitingTime = shortestProcess.TurnAround - shortestProcess.BurstTime
                
                self.AvgTurnAround += shortestProcess.TurnAround
                self.AvgWaitingTime += shortestProcess.WaitingTime
                
                # Append the solid block to the Gantt chart timeline
                timeline.append((shortestProcess.PID, shortestProcess.StartTime, shortestProcess.EndTime))
                
                Counter = shortestProcess.EndTime
                remaining.remove(shortestProcess)

        self.AvgTurnAround /= n
        self.AvgWaitingTime /= n
        return timeline, self.AvgWaitingTime, self.AvgTurnAround

    def SJFAlgoPreemptive(self): 
        Counter = 0
        FinishedProcess = 0
        n = len(self.ProcessList)
        timeline = []

        while FinishedProcess != n:
            minRemain = float('inf')
            selectProcess = None

            # Find the arrived process with the absolute shortest remaining time
            for p in self.ProcessList:
                if p.ArrivalTime <= Counter and p.RemainingTime > 0:
                    if p.RemainingTime < minRemain:
                        minRemain = p.RemainingTime
                        selectProcess = p
                    # Tie-breaker: If remaining times are equal, pick the one that arrived first
                    elif p.RemainingTime == minRemain:
                        if selectProcess and p.ArrivalTime < selectProcess.ArrivalTime:
                            selectProcess = p

            # If nobody is here yet, tick the clock forward
            if selectProcess is None:
                Counter += 1
                continue
            else:
                # First time starting? Record it.
                if selectProcess.RemainingTime == selectProcess.BurstTime:
                    selectProcess.StartTime = Counter

                selectProcess.RemainingTime -= 1
                
                # Create the 1-second chunk for the Gantt chart
                timeline.append((selectProcess.PID, Counter, Counter + 1))
                Counter += 1

                # If it just finished, calculate final stats
                if selectProcess.RemainingTime == 0:
                    FinishedProcess += 1
                    selectProcess.EndTime = Counter
                    selectProcess.TurnAround = selectProcess.EndTime - selectProcess.ArrivalTime
                    selectProcess.WaitingTime = selectProcess.TurnAround - selectProcess.BurstTime
                    
                    self.AvgTurnAround += selectProcess.TurnAround
                    self.AvgWaitingTime += selectProcess.WaitingTime

        self.AvgTurnAround /= n
        self.AvgWaitingTime /= n
        return timeline, self.AvgWaitingTime, self.AvgTurnAround