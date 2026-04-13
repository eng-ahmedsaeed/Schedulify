class Priority:
    def __init__(self, ProcessList):
        self.ProcessList = ProcessList
        self.AvgTurnAround = 0
        self.AvgWaitingTime = 0

    def PriorityAlgoNonPreemptive(self):
        Counter = 0
        n = len(self.ProcessList)
        timeline = []
        
        # We make a copy of the list so we can remove items safely
        remaining = list(self.ProcessList)

        # Sort by priority then arrival time; pick the earliest arriving process first
        remaining.sort(key=lambda p: (p.Priority, p.ArrivalTime))
        shortestProcess = min(remaining, key=lambda p: p.ArrivalTime)
        remaining.remove(shortestProcess)

        # First process
        shortestProcess.StartTime = shortestProcess.ArrivalTime
        shortestProcess.EndTime = shortestProcess.StartTime + shortestProcess.BurstTime
        shortestProcess.TurnAround = shortestProcess.EndTime - shortestProcess.ArrivalTime
        shortestProcess.WaitingTime = shortestProcess.TurnAround - shortestProcess.BurstTime

        self.AvgTurnAround += shortestProcess.TurnAround
        self.AvgWaitingTime += shortestProcess.WaitingTime
        Counter = shortestProcess.EndTime

        # Append to Gantt chart timeline
        timeline.append((shortestProcess.PID, shortestProcess.StartTime, shortestProcess.EndTime))

        while remaining:
            availableProcesses = [p for p in remaining if p.ArrivalTime <= Counter]

            if not availableProcesses:
                shortestProcess = min(remaining, key=lambda p: p.ArrivalTime)
                shortestProcess.StartTime = shortestProcess.ArrivalTime
                shortestProcess.EndTime = shortestProcess.StartTime + shortestProcess.BurstTime
                Counter = shortestProcess.EndTime
            else:
                shortestProcess = min(availableProcesses, key=lambda p: (p.Priority, p.ArrivalTime))
                shortestProcess.StartTime = Counter
                shortestProcess.EndTime = shortestProcess.StartTime + shortestProcess.BurstTime
                Counter = shortestProcess.EndTime

            shortestProcess.TurnAround = shortestProcess.EndTime - shortestProcess.ArrivalTime
            shortestProcess.WaitingTime = shortestProcess.TurnAround - shortestProcess.BurstTime
            
            self.AvgTurnAround += shortestProcess.TurnAround
            self.AvgWaitingTime += shortestProcess.WaitingTime
            remaining.remove(shortestProcess)

            # Append to Gantt chart timeline
            timeline.append((shortestProcess.PID, shortestProcess.StartTime, shortestProcess.EndTime))

        self.AvgTurnAround /= n
        self.AvgWaitingTime /= n
        return timeline, self.AvgWaitingTime, self.AvgTurnAround

    def PriorityAlgoPreemptive(self):
        Counter = 0
        FinishedProcess = 0
        n = len(self.ProcessList)
        timeline = []

        while n != FinishedProcess:
            minPriority = float('inf')
            selectProcess = None

            # Search for highest-priority available process (lowest Priority number)
            self.ProcessList.sort(key=lambda p: (p.ArrivalTime, p.Priority))
            for p in self.ProcessList:
                if p.ArrivalTime <= Counter and p.Priority < minPriority and p.RemainingTime > 0:
                    minPriority = p.Priority
                    selectProcess = p

            # No process available — advance time
            if selectProcess is None:
                Counter += 1
                continue
            else:
                # If the process is starting for the first time, set the start time
                if selectProcess.RemainingTime == selectProcess.BurstTime:
                    selectProcess.StartTime = Counter

                selectProcess.RemainingTime -= 1

                # If the process has finished, calculate its properties
                if selectProcess.RemainingTime == 0:
                    selectProcess.EndTime = Counter + 1
                    FinishedProcess += 1
                    ProcessTurnAround = selectProcess.EndTime - selectProcess.ArrivalTime
                    selectProcess.TurnAround = ProcessTurnAround
                    self.AvgTurnAround += ProcessTurnAround
                    ProcessWaitingTime = ProcessTurnAround - selectProcess.BurstTime
                    selectProcess.WaitingTime = ProcessWaitingTime
                    self.AvgWaitingTime += ProcessWaitingTime

                # Create the 1-unit snapshot of the executed slice for the Gantt chart
                timeline.append((selectProcess.PID, Counter, Counter + 1))
                Counter += 1

        self.AvgTurnAround /= n
        self.AvgWaitingTime /= n
        return timeline, self.AvgWaitingTime, self.AvgTurnAround