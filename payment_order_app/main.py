import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from logic import process_orders

class Worker(QThread):
    progress = pyqtSignal(int, int)
    log = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, template_path, data_path, output_dir, config_path):
        super().__init__()
        self.template_path = template_path
        self.data_path = data_path
        self.output_dir = output_dir
        self.config_path = config_path

    def run(self):
        def progress_cb(curr, tot):
            self.progress.emit(curr, tot)

        def log_cb(msg):
            self.log.emit(msg)

        success, msg = process_orders(
            self.template_path, self.data_path, self.output_dir, self.config_path,
            progress_callback=progress_cb, log_callback=log_cb
        )
        self.finished.emit(success, msg)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مولد الحوالات الإدارية الآلي")
        self.setMinimumSize(700, 500)

        # Set RTL Layout for the whole app
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        # Main Widget and Layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # UI Elements
        # 1. Template Selector
        template_layout = QHBoxLayout()
        self.template_input = QLineEdit()
        self.template_input.setPlaceholderText("اختر ملف القالب (Template.xlsx)")
        template_btn = QPushButton("استعراض...")
        template_btn.clicked.connect(self.select_template)
        template_layout.addWidget(QLabel("ملف القالب:"))
        template_layout.addWidget(self.template_input)
        template_layout.addWidget(template_btn)

        # 2. Data Source Selector
        data_layout = QHBoxLayout()
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("اختر ملف البيانات (Data.xlsx)")
        data_btn = QPushButton("استعراض...")
        data_btn.clicked.connect(self.select_data)
        data_layout.addWidget(QLabel("ملف البيانات:"))
        data_layout.addWidget(self.data_input)
        data_layout.addWidget(data_btn)

        # 3. Output Directory Selector
        out_layout = QHBoxLayout()
        self.out_input = QLineEdit()
        self.out_input.setPlaceholderText("اختر مجلد حفظ الحوالات")
        out_btn = QPushButton("استعراض...")
        out_btn.clicked.connect(self.select_output_dir)
        out_layout.addWidget(QLabel("مجلد الحفظ:"))
        out_layout.addWidget(self.out_input)
        out_layout.addWidget(out_btn)

        # 4. Config Selector (optional, default to config.json)
        config_layout = QHBoxLayout()
        self.config_input = QLineEdit()
        self.config_input.setText("config.json")
        self.config_input.setPlaceholderText("مسار ملف الإعدادات (config.json)")
        config_btn = QPushButton("استعراض...")
        config_btn.clicked.connect(self.select_config)
        config_layout.addWidget(QLabel("ملف الإعدادات:"))
        config_layout.addWidget(self.config_input)
        config_layout.addWidget(config_btn)

        # 5. Target Sheet selector (Optional override)
        sheet_layout = QHBoxLayout()
        self.sheet_input = QLineEdit()
        self.sheet_input.setPlaceholderText("اسم ورقة العمل المستهدفة (اختياري، يترك فارغاً لاستخدام الإعدادات)")
        sheet_layout.addWidget(QLabel("ورقة العمل:"))
        sheet_layout.addWidget(self.sheet_input)

        # Generate Button
        self.generate_btn = QPushButton("توليد الحوالات")
        self.generate_btn.setStyleSheet("background-color: #2E8B57; color: white; font-weight: bold; padding: 10px; font-size: 14px;")
        self.generate_btn.clicked.connect(self.start_generation)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Log Box
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText("سجل الأحداث...")

        # Add to main layout
        main_layout.addLayout(template_layout)
        main_layout.addLayout(data_layout)
        main_layout.addLayout(out_layout)
        main_layout.addLayout(config_layout)
        main_layout.addLayout(sheet_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.generate_btn)
        main_layout.addWidget(QLabel("نسبة التقدم:"))
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(QLabel("سجل الأحداث:"))
        main_layout.addWidget(self.log_box)

        # Default styling
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, Tahoma;
                font-size: 14px;
            }
            QPushButton {
                padding: 5px 15px;
            }
        """)

    def select_template(self):
        file, _ = QFileDialog.getOpenFileName(self, "اختر ملف القالب", "", "Excel Files (*.xlsx)")
        if file:
            self.template_input.setText(file)

    def select_data(self):
        file, _ = QFileDialog.getOpenFileName(self, "اختر ملف البيانات", "", "Excel Files (*.xlsx *.xls)")
        if file:
            self.data_input.setText(file)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "اختر مجلد الحفظ")
        if dir_path:
            self.out_input.setText(dir_path)

    def select_config(self):
        file, _ = QFileDialog.getOpenFileName(self, "اختر ملف الإعدادات", "", "JSON Files (*.json)")
        if file:
            self.config_input.setText(file)

    def append_log(self, msg):
        self.log_box.append(msg)

    def update_progress(self, current, total):
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)

    def on_generation_finished(self, success, msg):
        self.generate_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "اكتمل", msg)
            self.append_log(f"--- {msg} ---")
            self.progress_bar.setValue(100)
        else:
            QMessageBox.warning(self, "خطأ", msg)
            self.append_log(f"--- حدث خطأ: {msg} ---")

    def start_generation(self):
        template_path = self.template_input.text().strip()
        data_path = self.data_input.text().strip()
        output_dir = self.out_input.text().strip()
        config_path = self.config_input.text().strip()

        if not template_path or not data_path or not output_dir or not config_path:
            QMessageBox.warning(self, "تنبيه", "يرجى تعبئة جميع الحقول أولاً.")
            return

        if not os.path.exists(template_path):
            QMessageBox.warning(self, "تنبيه", "ملف القالب غير موجود.")
            return

        if not os.path.exists(data_path):
            QMessageBox.warning(self, "تنبيه", "ملف البيانات غير موجود.")
            return

        if not os.path.exists(config_path):
            QMessageBox.warning(self, "تنبيه", "ملف الإعدادات غير موجود.")
            return

        self.generate_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_box.clear()
        self.append_log("جاري بدء المعالجة...")

        sheet_name = self.sheet_input.text().strip()

        # Write the sheet override to config if provided, logic handles it from config
        import json
        if sheet_name:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                config['sheet_name'] = sheet_name
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
            except Exception as e:
                self.append_log(f"فشل تحديث اسم ورقة العمل في ملف الإعدادات: {e}")

        self.worker = Worker(template_path, data_path, output_dir, config_path, sheet_name=sheet_name)
        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.append_log)
        self.worker.finished.connect(self.on_generation_finished)
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Ensure RTL for the application level too
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
