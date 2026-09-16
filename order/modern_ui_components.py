import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
                             QDateTimeEdit, QMessageBox, QFileDialog, QHeaderView, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont

import database
from calculator import calculate_allowances
from tafqeet import tafqeet
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report

class EmployeesPage(QWidget):
    def __init__(self, refresh_missions_callback):
        super().__init__()
        self.refresh_missions_callback = refresh_missions_callback
        layout = QVBoxLayout(self)

        # Form
        form_group = QGroupBox("إضافة موظف جديد")
        form_group.setStyleSheet("QGroupBox { border: 1px solid #313244; border-radius: 5px; margin-top: 10px; padding: 15px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; color: #89B4FA; font-weight: bold; }")
        form_layout = QFormLayout(form_group)

        self.name_input = QLineEdit()
        self.rank_input = QLineEdit()
        self.job_input = QLineEdit()
        self.index_input = QLineEdit()
        self.cat_input = QLineEdit()
        self.loc_input = QLineEdit()
        self.bank_type = QComboBox()
        self.bank_type.addItems(["CCP", "BNA", "BEA", "CPA", "BADR"])
        self.bank_acc_input = QLineEdit()

        inputs = [self.name_input, self.rank_input, self.job_input, self.index_input,
                  self.cat_input, self.loc_input, self.bank_type, self.bank_acc_input]

        for w in inputs:
            w.setStyleSheet("padding: 8px; border: 1px solid #313244; border-radius: 4px; background-color: #11111B;")
            w.setFont(QFont("Arial", 11))

        form_layout.addRow("الاسم واللقب:", self.name_input)
        form_layout.addRow("الرتبة:", self.rank_input)
        form_layout.addRow("الوظيفة:", self.job_input)
        form_layout.addRow("الرقم الاستدلالي:", self.index_input)
        form_layout.addRow("الصنف:", self.cat_input)
        form_layout.addRow("المقر الإداري:", self.loc_input)
        form_layout.addRow("طبيعة الحساب:", self.bank_type)
        form_layout.addRow("رقم الحساب:", self.bank_acc_input)

        self.add_btn = QPushButton("حفظ الموظف")
        self.add_btn.setStyleSheet("background-color: #89B4FA; color: #11111B; padding: 10px; border-radius: 4px; font-weight: bold;")
        self.add_btn.clicked.connect(self.add_employee)
        form_layout.addRow(self.add_btn)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("QTableWidget { background-color: #181825; border: 1px solid #313244; alternate-background-color: #1E1E2E; } QHeaderView::section { background-color: #313244; padding: 4px; font-weight: bold; border: 1px solid #1E1E2E; }")
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الرقم", "الاسم واللقب", "الرتبة", "المقر"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        self.delete_btn = QPushButton("حذف الموظف المحدد")
        self.delete_btn.setStyleSheet("background-color: #F38BA8; color: #11111B; padding: 10px; border-radius: 4px; font-weight: bold;")
        self.delete_btn.clicked.connect(self.delete_employee)

        layout.addWidget(form_group)
        layout.addWidget(self.table)
        layout.addWidget(self.delete_btn)

        self.refresh_table()

    def add_employee(self):
        data = {
            'full_name': self.name_input.text().strip(),
            'rank': self.rank_input.text().strip(),
            'job_title': self.job_input.text().strip(),
            'index_number': self.index_input.text().strip(),
            'category': self.cat_input.text().strip(),
            'workplace': self.loc_input.text().strip(),
            'bank_type': self.bank_type.currentText(),
            'bank_account': self.bank_acc_input.text().strip()
        }
        if not data['full_name']:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال الاسم واللقب.")
            return

        database.add_employee(data)
        QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح.")
        self.clear_fields()
        self.refresh_table()
        self.refresh_missions_callback()

    def delete_employee(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "تنبيه", "الرجاء تحديد موظف للحذف.")
            return
        row = selected_rows[0].row()
        emp_id = int(self.table.item(row, 0).text())
        emp_name = self.table.item(row, 1).text()

        reply = QMessageBox.question(self, "تأكيد", f"هل أنت متأكد من حذف الموظف: {emp_name} وكافة مهماته؟",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            database.delete_employee(emp_id)
            QMessageBox.information(self, "نجاح", "تم الحذف.")
            self.refresh_table()
            self.refresh_missions_callback()

    def refresh_table(self):
        self.table.setRowCount(0)
        emps = database.get_all_employees()
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

class MissionsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        emp_layout = QHBoxLayout()
        self.emp_combo = QComboBox()
        self.emp_combo.setStyleSheet("padding: 5px; border: 1px solid #313244; background-color: #11111B;")
        self.refresh_emp_combo()
        self.emp_combo.currentIndexChanged.connect(self.refresh_missions_table)
        emp_label = QLabel("اختر الموظف:")
        emp_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        emp_layout.addWidget(emp_label)
        emp_layout.addWidget(self.emp_combo)
        layout.addLayout(emp_layout)

        # Form
        form_group = QGroupBox("حساب وإضافة مهمة جديدة")
        form_group.setStyleSheet("QGroupBox { border: 1px solid #313244; border-radius: 5px; margin-top: 10px; padding: 15px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; color: #A6E3A1; font-weight: bold; }")
        form_layout = QFormLayout(form_group)

        self.order_num = QLineEdit()
        self.order_date = QLineEdit()
        self.purpose = QLineEdit()
        self.itinerary = QLineEdit()
        self.transport = QLineEdit()
        self.region = QComboBox()
        self.region.addItems(["شمال", "جنوب"])

        self.chap = QLineEdit()
        self.art = QLineEdit()
        self.month = QLineEdit()

        self.dep_time = QDateTimeEdit(QDateTime.currentDateTime())
        self.dep_time.setDisplayFormat("dd-MM-yyyy HH:mm")
        self.dep_time.setCalendarPopup(True)
        self.ret_time = QDateTimeEdit(QDateTime.currentDateTime().addDays(1))
        self.ret_time.setDisplayFormat("dd-MM-yyyy HH:mm")
        self.ret_time.setCalendarPopup(True)

        inputs = [self.order_num, self.order_date, self.purpose, self.itinerary, self.transport,
                  self.region, self.chap, self.art, self.month, self.dep_time, self.ret_time]

        for w in inputs:
            w.setStyleSheet("padding: 8px; border: 1px solid #313244; border-radius: 4px; background-color: #11111B;")
            w.setFont(QFont("Arial", 11))

        form_layout.addRow("المنطقة:", self.region)
        form_layout.addRow("تاريخ وساعة الذهاب:", self.dep_time)
        form_layout.addRow("تاريخ وساعة الإياب:", self.ret_time)

        self.calc_btn = QPushButton("احسب آلياً")
        self.calc_btn.setStyleSheet("background-color: #F9E2AF; color: #11111B; padding: 8px; border-radius: 4px; font-weight: bold;")
        self.calc_btn.clicked.connect(self.calc_mission)
        form_layout.addRow(self.calc_btn)

        calc_res_layout = QHBoxLayout()
        self.meals_res = QLineEdit()
        self.meals_res.setPlaceholderText("عدد الوجبات")
        self.nights_res = QLineEdit()
        self.nights_res.setPlaceholderText("عدد الليالي")
        self.meals_res.setStyleSheet("padding: 5px; background-color: #11111B; border: 1px solid #313244;")
        self.nights_res.setStyleSheet("padding: 5px; background-color: #11111B; border: 1px solid #313244;")
        calc_res_layout.addWidget(QLabel("الوجبات:"))
        calc_res_layout.addWidget(self.meals_res)
        calc_res_layout.addWidget(QLabel("الليالي:"))
        calc_res_layout.addWidget(self.nights_res)
        form_layout.addRow(calc_res_layout)

        form_layout.addRow("رقم الأمر بمهمة:", self.order_num)
        form_layout.addRow("تاريخ الأمر:", self.order_date)
        form_layout.addRow("سبب التنقل:", self.purpose)
        form_layout.addRow("المسار:", self.itinerary)
        form_layout.addRow("وسيلة النقل:", self.transport)
        form_layout.addRow("الباب المالي:", self.chap)
        form_layout.addRow("المادة المالية:", self.art)
        form_layout.addRow("شهر التقرير:", self.month)

        self.add_btn = QPushButton("حفظ الكشف")
        self.add_btn.setStyleSheet("background-color: #A6E3A1; color: #11111B; padding: 10px; border-radius: 4px; font-weight: bold;")
        self.add_btn.clicked.connect(self.add_mission)
        form_layout.addRow(self.add_btn)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("QTableWidget { background-color: #181825; border: 1px solid #313244; alternate-background-color: #1E1E2E; } QHeaderView::section { background-color: #313244; padding: 4px; font-weight: bold; border: 1px solid #1E1E2E; }")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "المنطقة", "الذهاب", "الإياب", "الإجمالي"])
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        self.delete_btn = QPushButton("حذف المهمة المحددة")
        self.delete_btn.setStyleSheet("background-color: #F38BA8; color: #11111B; padding: 8px; border-radius: 4px; font-weight: bold;")
        self.delete_btn.clicked.connect(self.delete_mission)

        layout.addWidget(form_group)
        layout.addWidget(self.table)
        layout.addWidget(self.delete_btn)

        # Export Actions
        export_layout = QHBoxLayout()
        self.export_pdf_btn = QPushButton("تصدير إلى PDF")
        self.export_pdf_btn.setStyleSheet("background-color: #F38BA8; color: #11111B; padding: 10px; border-radius: 4px; font-weight: bold; font-size: 11pt;")
        self.export_pdf_btn.clicked.connect(self.export_pdf)

        self.export_excel_btn = QPushButton("تصدير إلى Excel")
        self.export_excel_btn.setStyleSheet("background-color: #A6E3A1; color: #11111B; padding: 10px; border-radius: 4px; font-weight: bold; font-size: 11pt;")
        self.export_excel_btn.clicked.connect(self.export_excel)

        export_layout.addWidget(self.export_pdf_btn)
        export_layout.addWidget(self.export_excel_btn)
        layout.addLayout(export_layout)

    def refresh_emp_combo(self):
        current_data = self.emp_combo.currentData()
        self.emp_combo.clear()
        emps = database.get_all_employees()
        for emp in emps:
            self.emp_combo.addItem(f"{emp[1]} ({emp[0]})", emp[0])
            if current_data and current_data == emp[0]:
                self.emp_combo.setCurrentIndex(self.emp_combo.count() - 1)

    def refresh_missions_table(self):
        self.table.setRowCount(0)
        emp_id = self.emp_combo.currentData()
        if not emp_id: return

        missions = database.get_missions_for_employee(emp_id)
        for i, m in enumerate(missions):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(m[0])))
            self.table.setItem(i, 1, QTableWidgetItem(m[12]))
            self.table.setItem(i, 2, QTableWidgetItem(m[10]))
            self.table.setItem(i, 3, QTableWidgetItem(m[11]))
            self.table.setItem(i, 4, QTableWidgetItem(f"{m[15]} دج"))

    def calc_mission(self):
        dep_str = self.dep_time.dateTime().toString("dd-MM-yyyy HH:mm")
        ret_str = self.ret_time.dateTime().toString("dd-MM-yyyy HH:mm")
        reg = self.region.currentText()

        m_count, n_count, tot = calculate_allowances(dep_str, ret_str, reg)

        self.meals_res.setText(str(m_count))
        self.nights_res.setText(str(n_count))
        txt = tafqeet(tot)
        QMessageBox.information(self, "النتيجة", f"الإجمالي: {tot} دج\n{txt}")

    def add_mission(self):
        emp_id = self.emp_combo.currentData()
        if not emp_id:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار موظف.")
            return

        try:
            m_c = int(self.meals_res.text())
            n_c = int(self.nights_res.text())
        except ValueError:
            QMessageBox.warning(self, "تنبيه", "الرجاء حساب الوجبات والليالي أولاً.")
            return

        reg = self.region.currentText()
        rate = 800 if reg == "شمال" else 1000
        n_rate = 3200 if reg == "شمال" else 4000
        tot = (m_c * rate) + (n_c * n_rate)
        t_txt = tafqeet(tot)

        dep_str = self.dep_time.dateTime().toString("dd-MM-yyyy HH:mm")
        ret_str = self.ret_time.dateTime().toString("dd-MM-yyyy HH:mm")

        data = {
            'budget_chapter': self.chap.text().strip(),
            'budget_article': self.art.text().strip(),
            'report_month_year': self.month.text().strip(),
            'order_number': self.order_num.text().strip(),
            'order_date': self.order_date.text().strip(),
            'purpose': self.purpose.text().strip(),
            'itinerary': self.itinerary.text().strip(),
            'transport_mode': self.transport.text().strip(),
            'departure_datetime': dep_str,
            'return_datetime': ret_str,
            'region': reg,
            'meals_count': m_c,
            'nights_count': n_c,
            'total_amount': tot,
            'amount_text': t_txt
        }
        database.add_mission(emp_id, data)
        QMessageBox.information(self, "نجاح", "تم حفظ الكشف بنجاح.")
        self.refresh_missions_table()

    def delete_mission(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "تنبيه", "الرجاء تحديد مهمة للحذف.")
            return

        row = selected_rows[0].row()
        mission_id = int(self.table.item(row, 0).text())

        reply = QMessageBox.question(self, "تأكيد", "هل أنت متأكد من الحذف؟",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            database.delete_mission(mission_id)
            QMessageBox.information(self, "نجاح", "تم الحذف.")
            self.refresh_missions_table()

    def _get_selected_mission(self):
        emp_id = self.emp_combo.currentData()
        if not emp_id: return None, None

        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "تنبيه", "الرجاء تحديد مهمة من الجدول للتصدير.")
            return None, None

        row = selected_rows[0].row()
        mission_id = int(self.table.item(row, 0).text())

        emp = database.get_employee(emp_id)
        missions = database.get_missions_for_employee(emp_id)
        mission = next((m for m in missions if m[0] == mission_id), None)
        return emp, mission

    def export_pdf(self):
        emp, mission = self._get_selected_mission()
        if not mission: return

        path, _ = QFileDialog.getSaveFileName(self, "حفظ PDF", f"كشف_{emp[1]}.pdf", "PDF Files (*.pdf)")
        if path:
            generate_pdf_report(emp, [mission], path, mission[16]) # Pass mission in list to match pdf_generator logic if it expects list, actually let's check pdf_generator logic
            QMessageBox.information(self, "نجاح", "تم التصدير بنجاح.")

    def export_excel(self):
        emp, mission = self._get_selected_mission()
        if not mission: return

        path, _ = QFileDialog.getSaveFileName(self, "حفظ Excel", f"كشف_{emp[1]}.xlsx", "Excel Files (*.xlsx)")
        if path:
            generate_excel_report(emp, [mission], path, mission[16]) # Same here
            QMessageBox.information(self, "نجاح", "تم التصدير بنجاح.")
