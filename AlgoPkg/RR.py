from ProcessPkg.Process import Process

class RR:
    def __init__(self, ProcessList):
        self.ProcessList = ProcessList
        self.AvgTurnAround = 0
        self.AvgWaitingTime = 0

    def RRAlgo(self, TimeQuantum):
        counter = 0
        n = len(self.ProcessList)
        FinishedProcess = 0
        currentTurn = 0
        currentProcess = None
        remaining = sorted(self.ProcessList, key=lambda p: p.ArrivalTime)
        queue = []
        i = 0
        timeLine = []

        while FinishedProcess != n:
            while i < n:
                if remaining[i].ArrivalTime <= counter:
                    queue.append(remaining[i])
                    i += 1
                else:
                    break

            if not queue and currentProcess is None:
                counter += 1
                continue

            if currentTurn <= 0:
                if currentProcess and currentProcess.RemainingTime == 0:
                    currentProcess.EndTime = counter
                    currentProcess.TurnAround = counter - currentProcess.ArrivalTime
                    currentProcess.WaitingTime = currentProcess.TurnAround - currentProcess.BurstTime
                    self.AvgTurnAround += currentProcess.TurnAround
                    self.AvgWaitingTime += currentProcess.WaitingTime
                    FinishedProcess += 1
                    currentProcess = None

                elif currentProcess and currentProcess.RemainingTime > 0:
                    queue.append(currentProcess)
                    currentProcess = None

                if queue:
                    currentProcess = queue.pop(0)
                    if currentProcess.RemainingTime == currentProcess.BurstTime:
                        currentProcess.StartTime = counter

                    currentTurn = min(TimeQuantum, currentProcess.RemainingTime)

                    timeLine.append({
                        "PID": currentProcess.PID,
                        "StartTime": counter,
                        "EndTime": counter + currentTurn
                    })

            if currentProcess:
                currentProcess.RemainingTime -= 1
                currentTurn -= 1

            counter += 1


        self.AvgTurnAround /= n
        self.AvgWaitingTime /= n
        return timeLine, self.AvgWaitingTime, self.AvgTurnAround