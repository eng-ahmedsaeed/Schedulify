import sys
from PyQt6.QtWidgets import QApplication

# Import your newly separated UI and Theme
from gui.main_window import CPUSchedulerApp
from theme import get_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply the global theme immediately
    app.setStyleSheet(get_stylesheet())
    
    window = CPUSchedulerApp()
    window.show()
    sys.exit(app.exec())