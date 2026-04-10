from AlgoPkg.FCFS import FCFS
from ProcessPkg.Process import Process

def main():
    processes = [
        Process(1, ArrivalTime=0, BurstTime=5),
        Process(2, ArrivalTime=6, BurstTime=3),
        Process(3, ArrivalTime=8, BurstTime=1),
        Process(4, ArrivalTime=9, BurstTime=2)
    ]
 
    Algo = FCFS(processes)
    processes,AvgW,AvgT=Algo.FCFSAlgo()

    for p in processes:
        print(p,"-")
    print("Average TurnAround = ",AvgT)
    print("Average Waiting = ",AvgW)

if __name__ == "__main__":
    main()