import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QStackedWidget,
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QFont, QIcon
import database

# Import modern UI components
from modern_ui_components import EmployeesPage, MissionsPage

# Modern Dark Theme QSS
MODERN_QSS = """
QMainWindow {
    background-color: #1E1E2E;
}
QWidget {
    font-family: 'Arial', 'Segoe UI';
    color: #CDD6F4;
}
QFrame#Sidebar {
    background-color: #181825;
    border-right: 1px solid #313244;
}
QPushButton.SidebarBtn {
    background-color: transparent;
    color: #A6ADC8;
    text-align: right;
    padding: 15px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14pt;
    font-weight: bold;
    margin: 5px 10px;
}
QPushButton.SidebarBtn:hover {
    background-color: #313244;
    color: #CDD6F4;
}
QPushButton.SidebarBtn:checked {
    background-color: #89B4FA;
    color: #11111B;
}
QLabel#HeaderTitle {
    color: #89B4FA;
    font-size: 24pt;
    font-weight: bold;
    margin-bottom: 20px;
}
"""

class ModernMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MissionTrack DZ - النسخة الحديثة")
        self.setMinimumSize(1000, 750)

        # Native PyQt6 RTL Support
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # Init DB
        database.init_db()

        # Apply Style
        self.setStyleSheet(MODERN_QSS)

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_lbl = QLabel("MissionTrack DZ")
        title_lbl.setObjectName("HeaderTitle")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_lbl)

        # Sidebar Buttons
        self.btn_emp = QPushButton("إدارة الموظفين")
        self.btn_emp.setProperty("class", "SidebarBtn")
        self.btn_emp.setCheckable(True)
        self.btn_emp.setChecked(True)

        self.btn_mis = QPushButton("المهمات والكشوفات")
        self.btn_mis.setProperty("class", "SidebarBtn")
        self.btn_mis.setCheckable(True)

        sidebar_layout.addWidget(self.btn_emp)
        sidebar_layout.addWidget(self.btn_mis)
        sidebar_layout.addStretch()

        # Footer in Sidebar
        footer_lbl = QLabel("إعداد وتطوير:\nالسيد مصباح مراد")
        footer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_lbl.setStyleSheet("color: #6C7086; font-size: 10pt;")
        sidebar_layout.addWidget(footer_lbl)

        # Main Content Area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #1E1E2E;")

        # Pages
        self.mis_page = MissionsPage()
        self.emp_page = EmployeesPage(refresh_missions_callback=self.mis_page.refresh_emp_combo)

        self.content_stack.addWidget(self.emp_page)
        self.content_stack.addWidget(self.mis_page)

        # Connect buttons to stack
        self.btn_emp.clicked.connect(lambda: self.switch_page(0))
        self.btn_mis.clicked.connect(lambda: self.switch_page(1))

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        if index == 0:
            self.btn_emp.setChecked(True)
            self.btn_mis.setChecked(False)
        else:
            self.btn_emp.setChecked(False)
            self.btn_mis.setChecked(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    locale = QLocale(QLocale.Language.Arabic, QLocale.Country.Algeria)
    QLocale.setDefault(locale)

    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    window = ModernMainWindow()
    window.show()

    sys.exit(app.exec())
