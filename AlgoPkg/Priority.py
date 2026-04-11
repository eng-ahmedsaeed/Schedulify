from ProcessPkg.Process import Process
import copy

class Priority:
    def __init__(self, ProcessList):
        self.ProcessList = ProcessList
        self.AvgTurnAround = 0
        self.AvgWaitingTime = 0


    def PriorityAlgoNonPreemptive(self):
        Counter = 0
        SortedProcessList = []

        # Sort by priority then arrival time; pick the earliest arriving process first
        self.ProcessList.sort(key=lambda p: (p.Priority, p.ArrivalTime))
        shortestProcess = min(self.ProcessList, key=lambda p: p.ArrivalTime)
        SortedProcessList.append(shortestProcess)
        self.ProcessList.remove(shortestProcess)

        # Calculating start time and end time for first process
        SortedProcessList[0].StartTime  = SortedProcessList[0].ArrivalTime
        SortedProcessList[0].EndTime    = SortedProcessList[0].StartTime + SortedProcessList[0].BurstTime
        SortedProcessList[0].TurnAround = SortedProcessList[0].EndTime   - SortedProcessList[0].ArrivalTime
        SortedProcessList[0].WaitingTime = SortedProcessList[0].TurnAround - SortedProcessList[0].BurstTime

        self.AvgTurnAround += SortedProcessList[0].TurnAround
        self.AvgWaitingTime += SortedProcessList[0].WaitingTime

        Counter += SortedProcessList[0].EndTime

        # Search for highest-priority available process at each step
        # Calculating process properties in the same iteration
        while len(self.ProcessList):
            # Filter processes that have arrived by Counter, pick the one with highest priority
            availableProcesses = [p for p in self.ProcessList if p.ArrivalTime <= Counter]

            if not availableProcesses:
                # No process has arrived yet — jump to the next arriving process
                shortestProcess = min(self.ProcessList, key=lambda p: p.ArrivalTime)
                shortestProcess.StartTime   = shortestProcess.ArrivalTime
                shortestProcess.EndTime     = shortestProcess.StartTime + shortestProcess.BurstTime
                shortestProcess.TurnAround  = shortestProcess.EndTime   - shortestProcess.ArrivalTime
                shortestProcess.WaitingTime = shortestProcess.TurnAround - shortestProcess.BurstTime
                SortedProcessList.append(shortestProcess)
                self.ProcessList.remove(shortestProcess)
                Counter = shortestProcess.EndTime
            else:
                # Pick process with highest priority (lowest Priority number); break ties by ArrivalTime
                shortestProcess = min(availableProcesses, key=lambda p: (p.Priority, p.ArrivalTime))
                shortestProcess.StartTime   = Counter
                shortestProcess.EndTime     = shortestProcess.StartTime + shortestProcess.BurstTime
                shortestProcess.TurnAround  = shortestProcess.EndTime   - shortestProcess.ArrivalTime
                shortestProcess.WaitingTime = shortestProcess.TurnAround - shortestProcess.BurstTime
                SortedProcessList.append(shortestProcess)
                self.ProcessList.remove(shortestProcess)
                Counter = shortestProcess.EndTime

            self.AvgTurnAround  += shortestProcess.TurnAround
            self.AvgWaitingTime += shortestProcess.WaitingTime

        self.ProcessList = SortedProcessList
        self.AvgTurnAround  = self.AvgTurnAround  / len(self.ProcessList)
        self.AvgWaitingTime = self.AvgWaitingTime / len(self.ProcessList)
        return self.ProcessList, self.AvgWaitingTime, self.AvgTurnAround


    def PriorityAlgoPreemptive(self):
        SortedProcessList = []
        ##self.ProcessList.sort(key=lambda p: (p.Priority, p.ArrivalTime))
        Counter = 0
        FinishedProcess = 0

        while len(self.ProcessList) != FinishedProcess:
            minPriority   = float('inf')
            selectProcess = None

            # Search for highest-priority available process (lowest Priority number)
            self.ProcessList.sort(key=lambda p: (p.ArrivalTime, p.Priority))
            for p in self.ProcessList:
                if p.ArrivalTime <= Counter and p.Priority < minPriority and p.RemainingTime > 0:
                    minPriority   = p.Priority
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
                    selectProcess.EndTime    = Counter + 1
                    FinishedProcess += 1
                    ProcessTurnAround        = selectProcess.EndTime - selectProcess.ArrivalTime
                    selectProcess.TurnAround = ProcessTurnAround
                    self.AvgTurnAround      += ProcessTurnAround
                    ProcessWaitingTime       = ProcessTurnAround - selectProcess.BurstTime
                    selectProcess.WaitingTime = ProcessWaitingTime
                    self.AvgWaitingTime      += ProcessWaitingTime

                # Create a 1-unit snapshot of the executed slice for the Gantt chart
                CreatedProcess            = copy.deepcopy(selectProcess)
                CreatedProcess.StartTime  = Counter
                CreatedProcess.EndTime    = Counter + 1
                CreatedProcess.BurstTime  = 1
                SortedProcessList.append(CreatedProcess)
                Counter += 1

        n = len(self.ProcessList)
        self.AvgTurnAround  /= n
        self.AvgWaitingTime /= n
        return SortedProcessList, self.AvgWaitingTime, self.AvgTurnAround, self.ProcessList