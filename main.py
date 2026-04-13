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
        Process(4, ArrivalTime=20, BurstTime=2)
    ]

    Algo = SJF(processes)
    processes, AvgW, AvgT ,details = Algo.SJFAlgoPreemptive()
    print("Processes after SJF Preemptive Scheduling:")
    for p in processes:
        print(p,"-")
    print("==========================================")
    print("Average TurnAround = ",AvgT)
    print("Average Waiting = ",AvgW)
    print("==========================================")
    print("Details:")
    for detail in details:
        print(detail)


    



if __name__ == "__main__":
    main()