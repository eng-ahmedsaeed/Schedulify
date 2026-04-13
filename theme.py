def get_stylesheet():
        qss = """
        QWidget { background-color: #1A1919; color: #EAEAEA; font-family: 'Segoe UI'; }
        QLabel { font-size: 12px; }
        QLineEdit { background-color: #2A2A2A; border: 1px solid #3A3A3A; border-radius: 4px; padding: 8px; color: white; }
        QLineEdit:focus { border: 1px solid #00BFA6; }
        QLineEdit:disabled { background-color: #111111; color: #555555; border: 1px solid #1A1A1A; }
        QComboBox { background-color: #2A2A2A; border: 1px solid #3A3A3A; border-radius: 4px; padding: 5px; color: white; }
        QPushButton { color: #00BFA6; background-color: #2A2A2A; border: 1px solid #00BFA6; border-radius: 5px; padding: 8px; }
        QPushButton:hover { background-color: #00BFA6; color: #1A1919; }
        QCheckBox { font-size: 14px; }
        QCheckBox::indicator { width: 18px; height: 18px; border: 1px solid #3A3A3A; background: #2A2A2A; border-radius: 3px; }
        QCheckBox::indicator:checked { background: #00BFA6; border: 1px solid #00BFA6; }
        QTableWidget { background-color: #232323; alternate-background-color: #2A2A2A; border: 1px solid #3A3A3A; }
        QHeaderView::section { background-color: #00BFA6; color: #111111; font-weight: bold; padding: 5px; border: none; border-right: 1px solid #19D3C5;}
        """