import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QComboBox, QTableWidget, QTableWidgetItem, 
                             QGridLayout, QGraphicsScene, QGraphicsView, QHeaderView, QAbstractItemView, QCheckBox
                             , QMessageBox)
from PyQt6.QtGui import QFont, QColor, QBrush, QPen, QPixmap,QMovie
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import Qt, QRectF, QTimer, QSize
from ProcessPkg.Process import Process
from AlgoPkg.FCFS import FCFS
from AlgoPkg.RR import RR
from AlgoPkg.Priority import Priority
from AlgoPkg.SJF import SJF

class CPUSchedulerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Schedulify")
        self.setFixedSize(1024, 750) 
        
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.timer = QTimer()
        self.timer.timeout.connect(self.draw_next_tick)
        self.current_time = 0
        self.master_timeline = []
        self.x_offset = 20 

        self.setup_ui()
        self.setup_sounds()

    def setup_ui(self):
        labels = ["PID", "Burst Time", "Arrival Time", "Priority", "Round Robin Quantum"]
        self.entries = {}

        for i, text in enumerate(labels):
            lbl = QLabel(text)
            entry = QLineEdit()
            entry.returnPressed.connect(self.submit) 
            
            self.layout.addWidget(lbl, i, 0)
            self.layout.addWidget(entry, i, 1)
            self.entries[text] = entry

        self.layout.setColumnStretch(1, 1)

        self.btn_submit = QPushButton("Submit (Add to List)")
        self.btn_submit.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_submit.clicked.connect(self.submit)
        self.layout.addWidget(self.btn_submit, 5, 0)

        self.btn_inject = QPushButton("Inject Live Process")
        self.btn_inject.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_inject.setStyleSheet("""
            QPushButton { color: #118AB2; border: 1px solid #118AB2; background-color: #2A2A2A; border-radius: 5px; padding: 8px;}
            QPushButton:hover { background-color: #118AB2; color: #1A1919; }
        """)
        self.btn_inject.clicked.connect(self.inject_process) 
        self.layout.addWidget(self.btn_inject, 5, 1)

        self.layout.addWidget(QLabel("Select Scheduling Algorithm:"), 6, 0)
        self.dropdown = QComboBox()
        self.algorithms = ["FCFS", "SJF (Preemptive)", "SJF (Non-Preemptive)", "Priority (Preemptive)", "Priority (Non-Preemptive)", "Round Robin"]
        self.dropdown.addItems(self.algorithms)
        self.layout.addWidget(self.dropdown, 6, 1)

        self.dropdown.currentTextChanged.connect(self.toggle_inputs)
       

        self.chk_live_mode = QCheckBox("Enable Live Animation")
        self.chk_live_mode.setChecked(True) # Checked by default
        self.chk_live_mode.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.layout.addWidget(self.chk_live_mode, 7, 0)

        self.btn_reset = QPushButton("Reset All")
        self.btn_reset.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.btn_reset.setStyleSheet("""
            QPushButton { color: #FF6B6B; border: 1px solid #FF6B6B; background-color: #2A2A2A; border-radius: 5px; padding: 8px;}
            QPushButton:hover { background-color: #FF6B6B; color: #1A1919; }
        """)
        self.btn_reset.clicked.connect(self.reset_system) 
        self.layout.addWidget(self.btn_reset, 7, 1)

        self.btn_start = QPushButton("Start Simulation")
        self.btn_start.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.btn_start.clicked.connect(self.run_simulation) 
        self.layout.addWidget(self.btn_start, 8, 0, 1, 2) # Spans 2 columns

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["PID", "Arrival", "Burst", "Remaining", "Priority"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        self.layout.addWidget(self.table, 0, 2, 9, 1)
        self.layout.setColumnStretch(2, 2)

        lbl_chart = QLabel("Gantt Chart")
        lbl_chart.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.layout.addWidget(lbl_chart, 9, 0, 1, 3)

        self.scene = QGraphicsScene()
        self.gantt_view = QGraphicsView(self.scene)
        self.gantt_view.setFixedHeight(120)
        self.gantt_view.setStyleSheet("background-color: #1A1919; border: none;")
        self.layout.addWidget(self.gantt_view, 10, 0, 1, 3)

        self.lbl_avg_wait = QLabel("Average Waiting Time: N/A")
        self.lbl_avg_wait.setFont(QFont("Segoe UI", 16))
        self.layout.addWidget(self.lbl_avg_wait, 11, 0, 1, 2)

        self.lbl_avg_turn = QLabel("Average Turnaround Time: N/A")
        self.lbl_avg_turn.setFont(QFont("Segoe UI", 16))
        self.layout.addWidget(self.lbl_avg_turn, 12, 0, 1, 2)

        self.gif_label = QLabel(self)
        
        self.movie = QMovie(resource_path("assets/processing.gif")) 
        self.movie.setScaledSize(QSize(64, 64))
        self.gif_label.setMovie(self.movie)
        
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        
        self.layout.addWidget(self.gif_label, 11, 2, 2, 1)
        self.toggle_inputs()


    def add_table_row(self, pid, arrival, burst, remaining, priority):
        row_pos = self.table.rowCount()
        self.table.insertRow(row_pos)
        items = [pid, str(arrival), str(burst), str(remaining), str(priority)]
        for col, text in enumerate(items):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_pos, col, item)

    def submit(self):
        pid = self.entries["PID"].text()
        burst = self.entries["Burst Time"].text()
        arrival = self.entries["Arrival Time"].text()
        priority = self.entries["Priority"].text()

        if not pid or not burst:
            self.show_Error_Burst_PID()
            return
        if not burst.isdigit() or int(burst) <=0:
            #QMessageBox.warning(self, "Invalid Input", "Burst Time should be positive Number")
            self.show_Error_Invalid("Burst Time should be positive Number")
            return
        if arrival and not arrival.isdigit():
            #QMessageBox.warning(self, "Invalid Input", "Arrival Time should be Non Negative Number")
            self.show_Error_Invalid("Arrival Time should be Non Negative Number")
            return
        if priority and not priority.lstrip('-').isdigit(): # Allows negative priorities if you want
            #QMessageBox.warning(self, "Invalid Input", "Priority must be a valid number")
            self.show_Error_Invalid("Priority must be a valid number")
            return
        
        if not arrival: arrival = "0"
        if not priority: priority = "0"

        self.add_table_row(pid, arrival, burst, burst, priority)

        fields_to_clear = ["PID", "Burst Time", "Arrival Time", "Priority"]
        for field in fields_to_clear:
            self.entries[field].clear()
        self.entries["PID"].setFocus()

    def inject_process(self):
        # 1. Grab the essential info
        pid = self.entries["PID"].text()
        burst = self.entries["Burst Time"].text()
        priority = self.entries["Priority"].text()

        if not pid or not burst:
            print("Missing information!")
            return

        if not priority: priority = "0"

        if self.timer.isActive():
            # If the live clock is ticking, the arrival time is EXACTLY right now!
            arrival = str(self.current_time)
        else:
            # If the clock is stopped (or in Instant Mode), use what they typed in the box.
            arrival = self.entries["Arrival Time"].text()
            if not arrival: arrival = "0"

        # 2. Add it to the table with the calculated arrival time
        self.add_table_row(pid, arrival, burst, burst, priority)

        # 3. Clear the boxes
        fields_to_clear = ["PID", "Burst Time", "Arrival Time", "Priority"]
        for field in fields_to_clear:
            self.entries[field].clear()
        self.entries["PID"].setFocus()

        # 4. Trigger the seamless recalculation
        if self.chk_live_mode.isChecked() and self.timer.isActive():
            self.run_simulation()
        elif not self.chk_live_mode.isChecked():
            self.run_simulation()
    

    def toggle_inputs(self):
        algo = self.dropdown.currentText()
        
        # Toggle Priority Field
        if "Priority" in algo:
            self.entries["Priority"].setEnabled(True)
            self.table.setColumnHidden(4, False)
        else:
            self.entries["Priority"].clear()
            self.entries["Priority"].setEnabled(False)
            self.table.setColumnHidden(4, True)

        # Toggle Round Robin Field
        if algo == "Round Robin":
            self.entries["Round Robin Quantum"].setEnabled(True)
        
        else:
            self.entries["Round Robin Quantum"].clear()
            self.entries["Round Robin Quantum"].setEnabled(False)
        

    def run_simulation(self):
        process_list = []
        for row in range(self.table.rowCount()):
            pid = self.table.item(row, 0).text()
            arrival = int(self.table.item(row, 1).text())
            burst = int(self.table.item(row, 2).text())
            priority = int(self.table.item(row, 4).text())

            self.table.item(row, 3).setText(str(burst))
            
            p = Process(PID=pid, ArrivalTime=arrival, BurstTime=burst, Priority=priority)
            process_list.append(p)

        if not process_list:
            return

        selected_algo = self.dropdown.currentText()
        timeline = []
        avg_wait = 0
        avg_turn = 0
        
        if selected_algo == "FCFS":
            scheduler = FCFS(process_list)
            completed, avg_wait, avg_turn = scheduler.FCFSAlgo()
            timeline = [(p.get_PID(), p.get_StartTime(), p.get_EndTime()) for p in completed]
        elif selected_algo == "Round Robin":
            q_text = self.entries["Round Robin Quantum"].text()
            quantum = int(q_text) if q_text.isdigit() else 2
            scheduler = RR(process_list)
            timeline, avg_wait, avg_turn = scheduler.RRAlgo(quantum)
        elif selected_algo == "Priority (Non-Preemptive)":
            scheduler = Priority(process_list)
            timeline, avg_wait, avg_turn = scheduler.PriorityAlgoNonPreemptive()
        elif selected_algo == "Priority (Preemptive)":
            scheduler = Priority(process_list)
            timeline, avg_wait, avg_turn = scheduler.PriorityAlgoPreemptive()
        elif selected_algo == "SJF (Non-Preemptive)":
            scheduler = SJF(process_list)
            timeline, avg_wait, avg_turn = scheduler.SJFAlgoNonPreemptive()
        elif selected_algo == "SJF (Preemptive)":
            scheduler = SJF(process_list)
            timeline, avg_wait, avg_turn = scheduler.SJFAlgoPreemptive()

        self.master_timeline = timeline
        self.lbl_avg_wait.setText(f"Average Waiting Time: {avg_wait:.2f}")
        self.lbl_avg_turn.setText(f"Average Turnaround Time: {avg_turn:.2f}")

        # --- MODE ROUTING ---
        if self.chk_live_mode.isChecked():
            # Start Live Animation
            if not self.timer.isActive():
                self.scene.clear()
                self.current_time = 0
                self.x_offset = 20
                start_text = self.scene.addText("0", QFont("Arial", 10))
                start_text.setDefaultTextColor(QColor("white"))
                start_text.setPos(self.x_offset - 5, 95)
                self.timer.start(1000) 

                self.entries["Arrival Time"].clear()
                self.entries["Arrival Time"].setEnabled(False)
                self.entries["Arrival Time"].setPlaceholderText("Auto (Live)")
                self.entries["Arrival Time"].setStyleSheet("background-color: #111111; color: #555555;")
                self.movie.start()
        else:
            # Stop timer and Draw Instantly
            self.timer.stop()
            self.draw_instant_gantt()


    def draw_next_tick(self):
        """Draws exactly 1 second of time per tick (Live Mode)"""
        scale = 30 
        
        current_event = None
        for event in self.master_timeline:
            # Handle Dicts (RR), Process Objects (SJF), or Tuples safely
            if isinstance(event, dict):
                pid = str(event.get("PID", "Unknown"))
                start = int(event.get("StartTime", 0))
                end = int(event.get("EndTime", 0))
            elif hasattr(event, "PID") or hasattr(event, "pid"): # It's a Process Object
                pid = str(getattr(event, "PID", getattr(event, "pid", "Unknown")))
                start = int(getattr(event, "StartTime", 0))
                end = int(getattr(event, "EndTime", 0))
            else:
                pid, start_str, end_str = event
                pid = str(pid)
                start = int(start_str)
                end = int(end_str)

            if start <= self.current_time < end:
                # Store the clean integer version
                current_event = (pid, start, end)
                break

        if current_event:
            pid, start, end = current_event
            palette = ["#69F0AE", "#00BFA6", "#6C63FF", "#FF6B6B", "#FFD166", "#118AB2", "#EF476F"]
            color = palette[sum(ord(c) for c in pid) % len(palette)]
            
            self.scene.addRect(QRectF(self.x_offset, 10, scale, 80), QPen(Qt.PenStyle.NoPen), QBrush(QColor(color)))
            
            if self.current_time == 0 or self.get_pid_at(self.current_time - 1) != pid:
                text = self.scene.addText(pid, QFont("Arial", 11, QFont.Weight.Bold))
                text.setDefaultTextColor(QColor("#1A1919" if color in ["#69F0AE", "#00BFA6", "#FFD166"] else "white"))
                text.setPos(self.x_offset + (scale/2) - 10, 40)

            self.update_live_table(pid)
        else:
            self.scene.addRect(QRectF(self.x_offset, 10, scale, 80), QPen(Qt.PenStyle.NoPen), QBrush(QColor("#3A3A3A")))

        self.x_offset += scale
        self.tick_sound.play()
        self.current_time += 1
        
        ts = self.scene.addText(str(self.current_time), QFont("Arial", 10))
        ts.setDefaultTextColor(QColor("white"))
        ts.setPos(self.x_offset - 5, 95)

        self.gantt_view.setSceneRect(0, 0, self.x_offset + 50, 120)
        self.gantt_view.horizontalScrollBar().setValue(int(self.x_offset))

        # Safely extract the EndTime to check if we are done
        max_end_time = 0
        for e in self.master_timeline:
            if isinstance(e, dict):
                e_end = int(e.get("EndTime", 0))
            elif hasattr(e, "EndTime"):
                e_end = int(getattr(e, "EndTime", 0))
            else:
                e_end = int(e[2])
            if e_end > max_end_time:
                max_end_time = e_end
                
        if self.master_timeline and self.current_time >= max_end_time:
            self.timer.stop()
            self.entries["Arrival Time"].setEnabled(True)
            self.entries["Arrival Time"].setPlaceholderText("")
            self.entries["Arrival Time"].setStyleSheet("background-color: #2A2A2A; color: white;")
            
            self.movie.stop()
            self.success_sound.play()
            self.show_custom_success()


    def draw_instant_gantt(self):
        """Draws the entire timeline immediately (Instant Mode)"""
        self.scene.clear()
        if not self.master_timeline: return

        scale = 30
        x_offset = 20
        current_time = 0

        start_text = self.scene.addText("0", QFont("Arial", 10))
        start_text.setDefaultTextColor(QColor("white"))
        start_text.setPos(x_offset - 5, 95)

        palette = ["#69F0AE", "#00BFA6", "#6C63FF", "#FF6B6B", "#FFD166", "#118AB2", "#EF476F"]

        # Standardize all incoming data into strict [pid(str), start(int), end(int)]
        clean_timeline = []
        for event in self.master_timeline:
            if isinstance(event, dict):
                clean_timeline.append([str(event.get("PID")), int(event.get("StartTime")), int(event.get("EndTime"))])
            elif hasattr(event, "PID") or hasattr(event, "pid"):
                pid = str(getattr(event, "PID", getattr(event, "pid", "Unknown")))
                clean_timeline.append([pid, int(getattr(event, "StartTime", 0)), int(getattr(event, "EndTime", 0))])
            else:
                clean_timeline.append([str(event[0]), int(event[1]), int(event[2])])

        # Sort based on the integer start time
        clean_timeline.sort(key=lambda x: x[1])

        consolidated_timeline = []
        for event in clean_timeline:
            if not consolidated_timeline:
                consolidated_timeline.append(list(event))
            else:
                last_event = consolidated_timeline[-1]
                if last_event[0] == event[0] and last_event[2] == event[1]:
                    last_event[2] = event[2] # Extend the block
                else:
                    consolidated_timeline.append(list(event))

        for event in consolidated_timeline:
            pid, start_time, end_time = event

            # Idle Check
            if start_time > current_time:
                idle_width = (start_time - current_time) * scale
                self.scene.addRect(QRectF(x_offset, 10, idle_width, 80), QPen(Qt.PenStyle.NoPen), QBrush(QColor("#3A3A3A")))
                
                text = self.scene.addText("Idle", QFont("Arial", 10))
                text.setDefaultTextColor(QColor("#888888"))
                text.setPos(x_offset + (idle_width / 2) - 15, 40)
                
                x_offset += idle_width
                current_time = start_time
                ts = self.scene.addText(str(current_time), QFont("Arial", 10))
                ts.setDefaultTextColor(QColor("white"))
                ts.setPos(x_offset - 5, 95)

            # Process Block
            block_width = (end_time - start_time) * scale
            color = palette[sum(ord(c) for c in pid) % len(palette)]
            
            self.scene.addRect(QRectF(x_offset, 10, block_width, 80), QPen(Qt.PenStyle.NoPen), QBrush(QColor(color)))
            
            text = self.scene.addText(pid, QFont("Arial", 11, QFont.Weight.Bold))
            text.setDefaultTextColor(QColor("#1A1919" if color in ["#69F0AE", "#00BFA6", "#FFD166"] else "white"))
            text.setPos(x_offset + (block_width / 2) - 10, 40)

            x_offset += block_width
            current_time = end_time

            ts = self.scene.addText(str(end_time), QFont("Arial", 10))
            ts.setDefaultTextColor(QColor("white"))
            ts.setPos(x_offset - 5, 95)

        self.gantt_view.setSceneRect(0, 0, x_offset + 50, 120)
        self.gantt_view.horizontalScrollBar().setValue(0)
        self.success_sound.play()
        self.show_custom_success()

    def get_pid_at(self, time):
        """Returns the PID of the process running at a specific given time."""
        for e in self.master_timeline:
            if isinstance(e, dict):
                pid = str(e.get("PID", "Unknown"))
                start = int(e.get("StartTime", 0))
                end = int(e.get("EndTime", 0))
            elif hasattr(e, "PID") or hasattr(e, "pid"):
                pid = str(getattr(e, "PID", getattr(e, "pid", "Unknown")))
                start = int(getattr(e, "StartTime", 0))
                end = int(getattr(e, "EndTime", 0))
            else:
                pid = str(e[0])
                start = int(e[1])
                end = int(e[2])

            # Check if the requested time falls within this block
            if start <= time < end:
                return pid
                
        return None
        
    def update_live_table(self, running_pid):
        """Finds the running process in the table and ticks its remaining time down by 1."""
        for row in range(self.table.rowCount()):
            # Check if the PID in Column 0 matches the one currently running
            if self.table.item(row, 0).text() == running_pid:
                # Grab the current remaining time from Column 3
                current_rem = int(self.table.item(row, 3).text())
                
                # Tick it down!
                if current_rem > 0:
                    self.table.item(row, 3).setText(str(current_rem - 1))
                break

    def show_custom_success(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Simulation Complete")
        msg.setText("All processes have been successfully scheduled!")
    
        # Load and set your custom image (e.g., a green checkmark or a CPU icon)
        pixmap = QPixmap(resource_path("assets/success_icon.png"))
    
        # Optional: Scale the image down so it isn't massive
        pixmap = pixmap.scaled(128, 128) 
    
        msg.setIconPixmap(pixmap)
        msg.setStyleSheet("background-color: #2A2A2A; color: white;")
        msg.exec()

    def show_Error_Burst_PID(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("No input")
        msg.setText("Please Provide PID and Burst Time")
        pixmap = QPixmap(resource_path("assets/No_input_icon.png"))

        pixmap = pixmap.scaled(128, 128) 

        msg.setIconPixmap(pixmap)
        msg.setStyleSheet("background-color: #2A2A2A; color: white;")
        msg.exec()

    def show_Error_Invalid(self, error_msg):
        msg =QMessageBox(self)
        msg.setWindowTitle("Invalid Input")
        msg.setText(error_msg)
        pixmap =QPixmap(resource_path("assets/No_input_icon.png"))
        pixmap= pixmap.scaled(128,128)
        msg.setIconPixmap(pixmap)
        msg.setStyleSheet("background-color: #2A2A2A; color: white;")
        msg.exec()


    def reset_system(self):
        self.timer.stop()
        self.current_time = 0
        self.master_timeline = []
        self.x_offset = 20
        
        self.table.setRowCount(0)
        self.scene.clear()
        
        self.lbl_avg_wait.setText("Average Waiting Time: N/A")
        self.lbl_avg_turn.setText("Average Turnaround Time: N/A")
        
        for entry in self.entries.values():
            entry.clear()

        self.entries["Arrival Time"].setEnabled(True)
        self.entries["Arrival Time"].setPlaceholderText("")
        self.entries["Arrival Time"].setStyleSheet("background-color: #2A2A2A; color: white;")
        self.movie.stop()
        self.entries["PID"].setFocus()

    def setup_sounds(self):
        self.success_sound = QSoundEffect()
        self.success_sound.setSource(QUrl.fromLocalFile(resource_path("assets/success.wav")))
        self.success_sound.setVolume(1)

        self.tick_sound = QSoundEffect()
        self.tick_sound.setSource(QUrl.fromLocalFile(resource_path("assets/pop.wav")))
        self.tick_sound.setVolume(0.8)

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


