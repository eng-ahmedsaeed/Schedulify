from ProcessPkg.Process import Process
import copy

class RR:
    def __init__(self, ProcessList):
        self.ProcessList = ProcessList
        self.AvgTurnAround = 0
        self.AvgWaitingTime = 0

    def RRAlgo(self, TimeQuantum):
        SortedProcessList = []
        Counter = 0
        n = len(self.ProcessList)
        FinishedProcess = 0

        remaining = sorted(self.ProcessList, key=lambda p: p.ArrivalTime)
        queue = []
        
        while FinishedProcess != n:
            
            #filling queue with arrived processes
            for p in remaining:
                if p.ArrivalTime <= Counter and p.RemainingTime > 0:
                    queue.append(p)

            # idle time
            if not queue:
                Counter += 1
                continue

            process = queue.pop(0)

            if process.RemainingTime == process.BurstTime:
                process.StartTime = Counter

            timeTaking = min(process.RemainingTime, TimeQuantum)
            Counter += timeTaking
            process.RemainingTime -= timeTaking

            if process.RemainingTime == 0:
                FinishedProcess += 1
                process.EndTime = Counter
                process.TurnAround = process.EndTime - process.ArrivalTime
                self.AvgTurnAround += process.TurnAround
                process.WaitingTime = process.TurnAround - process.BurstTime
                self.AvgWaitingTime += process.WaitingTime
            else:
                queue.append(process) 

            for secondTime in range(Counter - timeTaking, Counter):
                CreatedProcess = copy.deepcopy(process)
                CreatedProcess.BurstTime = 1
                CreatedProcess.StartTime = secondTime
                CreatedProcess.EndTime = secondTime + 1
                SortedProcessList.append(CreatedProcess)

        self.AvgTurnAround /= n
        self.AvgWaitingTime /= n
        return SortedProcessList, self.AvgWaitingTime, self.AvgTurnAround