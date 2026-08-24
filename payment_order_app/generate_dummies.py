import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side, PatternFill
import json

def create_dummy_data():
    data = {
        "اسم المستفيد": ["أحمد محي", "محمد صالح", "فاطمة الزهراء", "مؤسسة النجاح"],
        "رقم الحوالة": [71, 72, 73, 74],
        "تاريخ الحوالة": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04"],
        "رقم بطاقة الالتزام": ["ENG-100", "ENG-101", "ENG-102", "ENG-103"],
        "RIP/RIB": ["RIB 0011223344", "RIP 99887766", "RIB 5544332211", "RIB 1122334455"],
        "المبلغ الخام": [10000.0, 15000.5, 20000.0, 50000.0],
        "المبلغ الصافي": [9000.0, 13500.0, 18000.0, 45000.0],
        "موضوع الدفع": ["شراء معدات", "صيانة دورية", "خدمات استشارية", "توريد أجهزة"],
        "تخصيص الميزانية": ["الباب الأول - المادة 3", "الباب الثاني - المادة 1", "الباب الثالث - المادة 2", "الباب الرابع - المادة 4"]
    }
    df = pd.DataFrame(data)
    df.to_excel("Data.xlsx", index=False)
    print("Created Data.xlsx")

def create_dummy_template():
    wb = Workbook()
    ws = wb.active
    ws.title = "حوالة"
    ws.sheet_view.rightToLeft = True

    # Just setting some dummy cells to match config
    ws['A1'] = "الجمهورية الجزائرية الديمقراطية الشعبية"
    ws.merge_cells('A1:J1')
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")

    # Add borders
    thin = Side(border_style="thin", color="000000")
    border = Border(top=thin, left=thin, right=thin, bottom=thin)

    # Some basic headers for visual effect
    ws['I4'] = "رقم الحوالة"
    ws['I5'] = "تاريخ الحوالة"
    ws['I3'] = "رقم بطاقة الالتزام"
    ws['F11'] = "تعيين المستفيد والاسم التجاري"
    ws['D11'] = "RIP/RIB"
    ws['J10'] = "المبلغ الخام"
    ws['J11'] = "المبلغ الصافي"
    ws['C11'] = "موضوع الدفع، المرفقات، ورقم الفاتورة"
    ws['K11'] = "تخصيص الميزانية"

    wb.save("Template.xlsx")
    print("Created Template.xlsx")

def create_default_config():
    config = {
        "sheet_name": "حوالة",
        "mapping": {
            "رقم الحوالة": "I4",
            "تاريخ الحوالة": "I5",
            "رقم بطاقة الالتزام": "I3",
            "اسم المستفيد": "F11",
            "RIP/RIB": "D11",
            "المبلغ الخام": "J10",
            "المبلغ الصافي": "J11",
            "موضوع الدفع": "C11",
            "تخصيص الميزانية": "K11"
        },
        "filename_columns": ["اسم المستفيد", "رقم الحوالة"]
    }
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print("Created config.json")

if __name__ == "__main__":
    create_dummy_data()
    create_dummy_template()
    create_default_config()
