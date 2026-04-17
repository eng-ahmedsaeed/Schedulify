# Schedulify: CPU Scheduling Simulator 
A modern CPU scheduling simulator with live execution, interactive UI, and support for multiple scheduling algorithms with real-time analytics.

It is built in Python and PyQt6 that simulates and visualizes standard Operating System CPU scheduling algorithms. 

## Key Features

**Core OS Algorithms**
* First Come First Serve (FCFS)
* Shortest Job First (SJF) - Preemptive & Non-Preemptive
* Priority Scheduling - Preemptive & Non-Preemptive
* Round Robin (with dynamic time quantum)

**Advanced UI & Visualization**
* **Dual Simulation Modes:** Run instantly to see final results, or use "Live Mode" to watch the CPU schedule processes in real-time.
* **Dynamic Gantt Chart:** Automatically scales and draws the CPU timeline using a custom PyQT6 Graphics Scene.
* **Analytics:** Automatically calculates Average Waiting Time and Average Turnaround Time.

---

## Screenshots
---

## Tech
* **Language:** Python 3.x
* **GUI Framework:** PyQt6 (Multimedia, GraphicsView, Core)
---

## Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/Schedulify.git](https://github.com/YOUR_USERNAME/Schedulify.git)
cd Schedulify
```
### 2. Install Dependancies
```bash
pip install PyQt6 PyQt6-Multimedia
```
### 3. Run the Application
```bash
python main_gui.py
```

## Project Structure
```plaintext
Schedulify/
├── main_gui.py          # Application entry point
├── theme.py             # Global UI stylesheet and CSS
├── gui/                 # UI components and window logic
│   └── main_window.py   
├── ProcessPkg/          # Core OS Algorithm logic
│   ├── Process.py       
│   ├── FCFS.py          
│   └── ...              
└── assets/              # Icons, Sounds, and GIFs
```