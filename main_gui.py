import sys
from PyQt6.QtWidgets import QApplication


from gui.main_window import CPUSchedulerApp
from theme import get_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet(get_stylesheet())
    
    window = CPUSchedulerApp()
    window.show()
    sys.exit(app.exec())