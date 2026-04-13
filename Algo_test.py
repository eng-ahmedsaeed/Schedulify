from AlgoPkg.FCFS import FCFS
from AlgoPkg.SJF import SJF
from AlgoPkg.RR import RR
from AlgoPkg.Priority import Priority
from ProcessPkg.Process import Process

def main():
    processes = [
        Process(1, ArrivalTime=0, BurstTime=3),
        Process(2, ArrivalTime=0, BurstTime=2),
        Process(3, ArrivalTime=0, BurstTime=3),
        Process(4, ArrivalTime=0, BurstTime=2)
    ]
    
    quantum = 2
    Algo = RR(processes)
    processes, AvgW, AvgT  = Algo.RRAlgo(2)

    for p in processes:
        print(p,"-")
    print("Average TurnAround = ",AvgT)
    print("Average Waiting = ",AvgW)

if __name__ == "__main__":
    main()