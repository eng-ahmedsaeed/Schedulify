import tkinter as tk
from tkinter import ttk  # importing the tkinter library to create a GUI application


#creating the main window 

root = tk.Tk()
root.geometry("1024x700")
root.title("CPU Scheduler")
root.configure(bg="#1A1919")  # Set background color

#Submit function

def submit(event=None):
    name = entry_name.get()
    burst = entry_burst.get()
    arrival = entry_arrival.get()
    priority = entry_priority.get()

    print(name, burst, arrival, priority)


#Labels and entry fields


tk.Label(root, text="PID").grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, sticky="ew", pady=10, padx=(0, 10))


tk.Label(root, text="Burst Time").grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
entry_burst = tk.Entry(root)
entry_burst.grid(row=1, column=1, sticky="ew", pady=10, padx=(0, 10))

tk.Label(root, text="Arrival Time").grid(row=2, column=0, sticky="nsew", padx=(10, 5), pady=10)
entry_arrival = tk.Entry(root)
entry_arrival.grid(row=2, column=1, sticky="ew", pady=10, padx=(0, 10))

tk.Label(root, text="Priority").grid(row=3, column=0, sticky="nsew", padx=(10, 5), pady=10)
entry_priority = tk.Entry(root)
entry_priority.grid(row=3, column=1, sticky="ew", pady=10, padx=(0, 10))

tk.Label(root, text="Round Robin Quantum").grid(row=4, column=0, sticky="nsew", padx=(10, 5), pady=10)
entry_quantum = tk.Entry(root)
entry_quantum.grid(row=4, column=1, sticky="ew", pady=10, padx=(0, 10))

# Allow column 1 to expand so entries stretch
root.grid_columnconfigure(1, weight=1)


tk.Button(root, text="Submit", font=("Segoe UI", 20, "bold"), fg="#00BFA6", command=submit).grid(row=5, column=1, pady=10, padx=10)

root.bind('<Return>', submit)  # Submit the form when the Enter key is pressed

tk.Button(root, text="Start", font=("Segoe UI", 15, "bold"), fg="#00BFA6").grid(row=6, column=1, pady=10, padx=10, sticky="nsew")

#Algorithm selection dropdown

label_algorithm = tk.Label(root, text="Select Scheduling Algorithm").grid(row=5, column=0 , padx=10 , sticky="nsew")
scheduler = tk.StringVar()
scheduler.set("FCFS")  # default value

dropdown = tk.OptionMenu(
    root,
    scheduler,
    "FCFS",
    "SJF (Preemptive)",
    "SJF (Non-Preemptive)",
    "Priority (Preemptive)",
    "Priority (Non-Preemptive)",
    "Round Robin"
)

def on_algorithm_change(*args):
    selected = scheduler.get()
    algorithm_map = {
        "FCFS": "fcfs",
        "SJF (Preemptive)": "sjf_preemptive",
        "SJF (Non-Preemptive)": "sjf_non_preemptive",
        "Priority (Preemptive)": "priority_preemptive",
        "Priority (Non-Preemptive)": "priority_non_preemptive",
        "Round Robin": "round_robin"
    }
    algorithm_var = algorithm_map[selected]
    print(f"Selected algorithm: {algorithm_var}")

scheduler.trace("w", on_algorithm_change)

dropdown.grid(row=6, column=0, pady=10, padx=10, sticky="nsew")

# Table style (dark + neon accents)
style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#232323",
    foreground="#EAEAEA",
    fieldbackground="#232323",
    rowheight=30,
    bordercolor="#3A3A3A",
    borderwidth=1,
    font=("Segoe UI", 10)
)
style.configure(
    "Treeview.Heading",
    background="#00BFA6",
    foreground="#111111",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padding=6
)
style.map(
    "Treeview",
    background=[("selected", "#6C63FF")],
    foreground=[("selected", "#FFFFFF")]
)
style.map(
    "Treeview.Heading",
    background=[("active", "#19D3C5")]
)

# Table to display the processes and their details
table = ttk.Treeview(root, columns=("Arrival", "Burst", "Remaining", "Priority"))
table.heading("#0", text="PID")
table.heading("Arrival", text="Arrival")
table.heading("Burst", text="Burst")
table.heading("Remaining", text="Remaining")
table.heading("Priority", text="Priority")

# Let columns stretch when the window grows
table.column("#0", width=80, anchor="w", )
table.column("Arrival", width=90, anchor="center", )
table.column("Burst", width=90, anchor="center", )
table.column("Remaining", width=100, anchor="center", )
table.column("Priority", width=90, anchor="center", )

# Alternate row colors
table.tag_configure("odd", background="#2A2A2A")
table.tag_configure("even", background="#303030")

# Expand horizontally
table.grid(row=0, column=2, rowspan=8, padx=20, pady=10, sticky="nsew")
root.grid_columnconfigure(2, weight=1)

table.insert("", "end", text="P1", values=(0, 5, 5, 1), tags=("odd",))
table.insert("", "end", text="P2", values=(1, 3, 3, 2), tags=("even",))

###################################

#Gantt chart canvas

label_chart = tk.Label(root, text="Gantt Chart", font=("Segoe UI", 14, "bold")).grid(row=7, column=0, columnspan=2, sticky="ew", padx=10)


gantt_canvas = tk.Canvas(root, bg="#1A1919", height=120, width=800)

scale = 20
x_start = 20
colors = ["#69F0AE", "#00BFA6"]  # alternate per process

# P1: burst=5
p1_end = x_start + 5 * scale
gantt_canvas.create_rectangle(x_start, 10, p1_end, 90, fill=colors[0], outline="")
gantt_canvas.create_text((x_start + p1_end) / 2, 50, text="P1", fill="#1A1919", font=("Arial", 11, "bold"))

# P2: burst=3
p2_end = p1_end + 3 * scale
gantt_canvas.create_rectangle(p1_end, 10, p2_end, 90, fill=colors[1], outline="")
gantt_canvas.create_text((p1_end + p2_end) / 2, 50, text="P2", fill="white", font=("Arial", 11, "bold"))

# Timestamps
gantt_canvas.create_text(x_start, 105, text="0", fill="white")
gantt_canvas.create_text(p1_end, 105, text="5", fill="white")
gantt_canvas.create_text(p2_end, 105, text="8", fill="white")

gantt_canvas.grid(row=9, column=0, columnspan=3, pady=20, padx=10, sticky="ew")
root.grid_rowconfigure(9, weight=0)

###################

#AVG waiting time and turnaround time labels

label_avg_waiting = tk.Label(root, text="Average Waiting Time: N/A", font=("Segoe UI", 18)).grid(row=10, column=0, pady=10 , padx=20)
label_avg_turnaround = tk.Label(root, text="Average Turnaround Time: N/A", font=("Segoe UI", 18)).grid(row=11, column=0, pady=10, padx=20)

#####################

#ASU Logo
img = tk.PhotoImage(file="75c5c806d48aa43c13d531ffbed8014e.png").subsample(2, 2)  # Adjust the subsample values to resize the image as needed
label = tk.Label(root, image=img)
label.image = img  # Keep a reference to prevent garbage collection
label.grid(row=10, column=2, rowspan=2, pady=10,  sticky="ne")



root.mainloop() # Launch the finished GUI , at the very end of the code