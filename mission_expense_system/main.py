import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QComboBox, QDateTimeEdit, QMessageBox, QFileDialog, QHeaderView, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QDateTime
import db
from calculator import calculate_mission_allowances
from exporter import generate_report

class EmployeesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Form
        form_group = QGroupBox("إضافة / تعديل موظف")
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.rank_input = QLineEdit()
        self.job_input = QLineEdit()
        self.index_input = QLineEdit()
        self.cat_input = QLineEdit()
        self.loc_input = QLineEdit()
        self.bank_type = QComboBox()
        self.bank_type.addItems(["CCP", "BNA", "BEA", "CPA", "BADR"])
        self.bank_acc_input = QLineEdit()

        form_layout.addRow("الاسم واللقب:", self.name_input)
        form_layout.addRow("الرتبة:", self.rank_input)
        form_layout.addRow("الوظيفة:", self.job_input)
        form_layout.addRow("الرقم الاستدلالي:", self.index_input)
        form_layout.addRow("الصنف:", self.cat_input)
        form_layout.addRow("المقر الإداري:", self.loc_input)
        form_layout.addRow("طبيعة الحساب:", self.bank_type)
        form_layout.addRow("رقم الحساب (RIP/RIB):", self.bank_acc_input)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("إضافة موظف")
        self.add_btn.clicked.connect(self.add_employee)
        self.clear_btn = QPushButton("تفريغ الحقول")
        self.clear_btn.clicked.connect(self.clear_fields)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)

        form_layout.addRow(btn_layout)
        form_group.setLayout(form_layout)

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("بحث عن موظف (الاسم، الرقم الاستدلالي...)")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(QLabel("بحث:"))
        search_layout.addWidget(self.search_input)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الرقم", "الاسم واللقب", "الرتبة", "المقر"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.load_selected)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Delete Button
        self.delete_btn = QPushButton("حذف الموظف المحدد")
        self.delete_btn.setStyleSheet("background-color: #d9534f; color: white;")
        self.delete_btn.clicked.connect(self.delete_employee)

        layout.addWidget(form_group)
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.delete_btn)
        self.setLayout(layout)

    def filter_table(self):
        filter_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def delete_employee(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "تنبيه", "الرجاء تحديد موظف للحذف.")
            return

        row = selected_rows[0].row()
        emp_id = int(self.table.item(row, 0).text())
        emp_name = self.table.item(row, 1).text()

        reply = QMessageBox.question(self, "تأكيد الحذف", f"هل أنت متأكد من حذف الموظف: {emp_name} وكافة المهمات التابعة له؟",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            db.delete_employee(emp_id)
            QMessageBox.information(self, "نجاح", "تم حذف الموظف بنجاح.")
            self.refresh_table()

    def add_employee(self):
        data = {
            'full_name': self.name_input.text(),
            'rank': self.rank_input.text(),
            'job_title': self.job_input.text(),
            'index_number': self.index_input.text(),
            'category': self.cat_input.text(),
            'admin_location': self.loc_input.text(),
            'bank_type': self.bank_type.currentText(),
            'bank_account': self.bank_acc_input.text()
        }
        if not data['full_name']:
            QMessageBox.warning(self, "تنبيه", "يجب إدخال اسم الموظف على الأقل.")
            return

        db.add_employee(data)
        QMessageBox.information(self, "نجاح", "تمت إضافة الموظف بنجاح.")
        self.clear_fields()
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        emps = db.get_all_employees()
        for i, emp in enumerate(emps):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(emp[0])))
            self.table.setItem(i, 1, QTableWidgetItem(emp[1]))
            self.table.setItem(i, 2, QTableWidgetItem(emp[2]))
            self.table.setItem(i, 3, QTableWidgetItem(emp[6]))

    def clear_fields(self):
        self.name_input.clear()
        self.rank_input.clear()
        self.job_input.clear()
        self.index_input.clear()
        self.cat_input.clear()
        self.loc_input.clear()
        self.bank_acc_input.clear()
        self.table.clearSelection()

    def load_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        emp_id = int(self.table.item(row, 0).text())
        emp = db.get_employee(emp_id)
        if emp:
            self.name_input.setText(emp[1])
            self.rank_input.setText(emp[2])
            self.job_input.setText(emp[3])
            self.index_input.setText(emp[4])
            self.cat_input.setText(emp[5])
            self.loc_input.setText(emp[6])

            index = self.bank_type.findText(emp[7])
            if index >= 0:
                self.bank_type.setCurrentIndex(index)

            self.bank_acc_input.setText(emp[8])


class MissionsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Select Employee
        emp_layout = QHBoxLayout()
        self.emp_combo = QComboBox()
        self.refresh_emp_combo()
        self.emp_combo.currentIndexChanged.connect(self.refresh_missions_table)
        emp_layout.addWidget(QLabel("اختر الموظف:"))
        emp_layout.addWidget(self.emp_combo)

        # Form
        form_group = QGroupBox("إضافة مهمة")
        form_layout = QFormLayout()

        self.order_num = QLineEdit()
        self.order_date = QLineEdit()
        self.order_date.setPlaceholderText("DD-MM-YYYY")
        self.purpose = QLineEdit()
        self.itinerary = QLineEdit()
        self.transport = QComboBox()
        self.transport.addItems(["سيارة إدارية", "قطار", "حافلة", "سيارة خاصة", "طائرة"])
        self.region = QComboBox()
        self.region.addItems(["شمال", "جنوب"])

        self.dep_time = QDateTimeEdit(QDateTime.currentDateTime())
        self.dep_time.setDisplayFormat("dd-MM-yyyy HH:mm")
        self.ret_time = QDateTimeEdit(QDateTime.currentDateTime().addDays(1))
        self.ret_time.setDisplayFormat("dd-MM-yyyy HH:mm")

        form_layout.addRow("رقم الأمر بمهمة:", self.order_num)
        form_layout.addRow("تاريخ الأمر:", self.order_date)
        form_layout.addRow("سبب التنقل:", self.purpose)
        form_layout.addRow("المسار:", self.itinerary)
        form_layout.addRow("وسيلة النقل:", self.transport)
        form_layout.addRow("المنطقة:", self.region)
        form_layout.addRow("تاريخ وساعة الذهاب:", self.dep_time)
        form_layout.addRow("تاريخ وساعة الإياب:", self.ret_time)

        self.add_btn = QPushButton("حساب وإضافة المهمة")
        self.add_btn.clicked.connect(self.add_mission)
        form_layout.addRow(self.add_btn)

        form_group.setLayout(form_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["معرف المهمة", "رقم الأمر", "المنطقة", "الذهاب", "الإياب", "وجبات", "مبيت"])
        self.table.setColumnHidden(0, True) # Hide ID column
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        # Delete Button
        self.delete_btn = QPushButton("حذف المهمة المحددة")
        self.delete_btn.setStyleSheet("background-color: #d9534f; color: white;")
        self.delete_btn.clicked.connect(self.delete_mission)

        layout.addLayout(emp_layout)
        layout.addWidget(form_group)
        layout.addWidget(self.table)
        layout.addWidget(self.delete_btn)

        # Export Button
        self.export_btn = QPushButton("تصدير كشف المصاريف للموظف المحدد (Excel)")
        self.export_btn.setStyleSheet("background-color: #2E8B57; color: white; padding: 10px; font-weight: bold;")
        self.export_btn.clicked.connect(self.export_report)
        layout.addWidget(self.export_btn)

        self.setLayout(layout)

    def refresh_emp_combo(self):
        self.emp_combo.clear()
        emps = db.get_all_employees()
        for emp in emps:
            self.emp_combo.addItem(f"{emp[1]} ({emp[0]})", emp[0])

    def refresh_missions_table(self):
        self.table.setRowCount(0)
        emp_id = self.emp_combo.currentData()
        if not emp_id: return

        missions = db.get_missions_for_employee(emp_id)
        for i, m in enumerate(missions):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(m[0])))
            self.table.setItem(i, 1, QTableWidgetItem(m[2]))
            self.table.setItem(i, 2, QTableWidgetItem(m[9]))
            self.table.setItem(i, 3, QTableWidgetItem(m[7]))
            self.table.setItem(i, 4, QTableWidgetItem(m[8]))
            self.table.setItem(i, 5, QTableWidgetItem(str(m[10])))
            self.table.setItem(i, 6, QTableWidgetItem(str(m[11])))

    def delete_mission(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "تنبيه", "الرجاء تحديد مهمة للحذف.")
            return

        row = selected_rows[0].row()
        mission_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد من حذف هذه المهمة؟",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            db.delete_mission(mission_id)
            QMessageBox.information(self, "نجاح", "تم حذف المهمة بنجاح.")
            self.refresh_missions_table()

    def add_mission(self):
        emp_id = self.emp_combo.currentData()
        if not emp_id:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار موظف أولاً.")
            return

        dep_str = self.dep_time.dateTime().toString("dd-MM-yyyy HH:mm")
        ret_str = self.ret_time.dateTime().toString("dd-MM-yyyy HH:mm")
        reg = self.region.currentText()

        m_count, n_count, _, _ = calculate_mission_allowances(dep_str, ret_str, reg)

        data = {
            'order_number': self.order_num.text(),
            'order_date': self.order_date.text(),
            'purpose': self.purpose.text(),
            'itinerary': self.itinerary.text(),
            'transport_mode': self.transport.currentText(),
            'departure_datetime': dep_str,
            'return_datetime': ret_str,
            'region': reg,
            'meals_count': m_count,
            'nights_count': n_count
        }

        db.add_mission(emp_id, data)
        QMessageBox.information(self, "نجاح", f"تم حساب {m_count} وجبة و {n_count} ليلة. وتمت الإضافة بنجاح.")
        self.refresh_missions_table()

    def export_report(self):
        emp_id = self.emp_combo.currentData()
        if not emp_id:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار موظف.")
            return

        emp = db.get_employee(emp_id)
        missions = db.get_missions_for_employee(emp_id)

        if not missions:
            QMessageBox.warning(self, "تنبيه", "لا توجد مهمات مسجلة لهذا الموظف لتصديرها.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "حفظ الكشف", f"كشف_مصاريف_{emp[1].replace(' ', '_')}.xlsx", "Excel Files (*.xlsx)")
        if save_path:
            try:
                generate_report(emp, missions, save_path)
                QMessageBox.information(self, "نجاح", "تم تصدير الكشف بنجاح.")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام إدارة مصاريف التنقل")
        self.setMinimumSize(800, 600)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        db.init_db()

        main_widget = QWidget()
        layout = QVBoxLayout()

        # Author Header
        header_lbl = QLabel("نظام إدارة وحساب كشوف مصاريف التنقل ومهمات العمل\nتصميم وبرمجة: السيد مصباح مراد")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; padding: 10px;")
        layout.addWidget(header_lbl)

        # Tabs
        self.tabs = QTabWidget()
        self.emp_tab = EmployeesTab()
        self.mis_tab = MissionsTab()

        # Refresh mission tab's employee combo when changing tabs
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.tabs.addTab(self.emp_tab, "إدارة الموظفين")
        self.tabs.addTab(self.mis_tab, "المهمات وكشوف المصاريف")

        layout.addWidget(self.tabs)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.setStyleSheet("""
            QWidget {
                font-family: Arial, Tahoma;
                font-size: 14px;
            }
            QPushButton {
                padding: 5px 15px;
            }
        """)

    def on_tab_changed(self, index):
        if index == 1:
            self.mis_tab.refresh_emp_combo()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
