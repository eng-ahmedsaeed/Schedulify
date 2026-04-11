from AlgoPkg.FCFS import FCFS
from AlgoPkg.SJF import SJF
from AlgoPkg.RR import RR
from AlgoPkg.Priority import Priority
from ProcessPkg.Process import Process

def main():
    processes = [
        Process(1, ArrivalTime=0, BurstTime=6, Priority=3),
        Process(2, ArrivalTime=2, BurstTime=4, Priority=1),
        Process(3, ArrivalTime=3, BurstTime=5, Priority=2),
        Process(4, ArrivalTime=7, BurstTime=2, Priority=1)
    ]
    
    quantum = 2
    Algo = Priority(processes)
    processes, AvgW, AvgT , original  = Algo.PriorityAlgoPreemptive()

    for p in processes:
        print(p,"-")
    print("Average TurnAround = ",AvgT)
    print("Average Waiting = ",AvgW)

if __name__ == "__main__":
    main()