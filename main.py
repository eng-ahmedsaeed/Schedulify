from AlgoPkg.FCFS import FCFS
from AlgoPkg.SJF import SJF
from ProcessPkg.Process import Process

def main():
    processes = [
            Process(1, ArrivalTime=1, BurstTime=7),
            Process(2, ArrivalTime=3, BurstTime=4),
            Process(3, ArrivalTime=5, BurstTime=1),
            Process(4, ArrivalTime=7, BurstTime=2),
            Process(5, ArrivalTime=13, BurstTime=5),
            Process(6, ArrivalTime=14, BurstTime=2)
        ]
 
    Algo = SJF(processes)
    processes,AvgW,AvgT=Algo.SJFAlgoNonPreemptive()

    for p in processes:
        print(p,"-")
    print("Average TurnAround = ",AvgT)
    print("Average Waiting = ",AvgW)

if __name__ == "__main__":
    main()