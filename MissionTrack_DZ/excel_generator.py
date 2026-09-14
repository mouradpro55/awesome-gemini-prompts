import openpyxl
from openpyxl.styles import Alignment, Font, Border, Side
import os

def create_default_template(template_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "كشف مصاريف التنقل"
    ws.sheet_view.rightToLeft = True

    bold_font = Font(name="Arial", size=12, bold=True)
    normal_font = Font(name="Arial", size=11)
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    def set_cell(coord, value, font, merge=None):
        ws[coord] = value
        ws[coord].font = font
        ws[coord].alignment = center_align
        if merge:
            ws.merge_cells(merge)

    # Header
    set_cell("A1", "الجمهورية الجزائرية الديمقراطية الشعبية", bold_font, "A1:J1")
    set_cell("A2", "وزارة البريد والمواصلات السلكية واللاسلكية", bold_font, "A2:J2")
    set_cell("A3", "كشف مصاريف التنقل", Font(name="Arial", size=16, bold=True), "A3:J3")

    # Template labels (Static)
    set_cell("A5", "الاسم واللقب:", bold_font)
    set_cell("D5", "الرتبة / الوظيفة:", bold_font)
    set_cell("G5", "الرقم الاستدلالي:", bold_font)
    set_cell("A6", "المقر الإداري:", bold_font)
    set_cell("D6", "طبيعة الحساب:", bold_font)
    set_cell("G6", "رقم الحساب:", bold_font)

    set_cell("A8", "تفاصيل المهمة:", bold_font)
    set_cell("A9", "سبب التنقل:", bold_font)
    set_cell("D9", "المسار:", bold_font)

    set_cell("A11", "تاريخ الذهاب:", bold_font)
    set_cell("D11", "تاريخ الإياب:", bold_font)

    set_cell("A13", "الوجبات المستحقة:", bold_font)
    set_cell("D13", "الليالي المستحقة:", bold_font)

    set_cell("A15", "المجموع المالي:", bold_font)
    set_cell("D15", "المبلغ بالحروف:", bold_font)

    set_cell("A20", "تم إعداد هذا البرنامج من طرف السيد مصباح مراد", Font(name="Arial", size=10, italic=True), "A20:J20")

    wb.save(template_path)


def generate_excel_report(employee, mission, output_path):
    template_path = "Template.xlsx"
    if not os.path.exists(template_path):
        create_default_template(template_path)

    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Apply data onto the template
    normal_font = Font(name="Arial", size=11)

    ws['B5'] = employee[1]
    ws['B5'].font = normal_font

    ws['E5'] = f"{employee[2]} / {employee[3]}"
    ws['E5'].font = normal_font

    ws['H5'] = employee[4]
    ws['H5'].font = normal_font

    ws['B6'] = employee[6]
    ws['B6'].font = normal_font

    ws['E6'] = employee[7]
    ws['E6'].font = normal_font

    ws['H6'] = employee[8]
    ws['H6'].font = normal_font

    ws['B9'] = mission[7]
    ws['B9'].font = normal_font

    ws['E9'] = mission[8]
    ws['E9'].font = normal_font

    ws['B11'] = mission[10]
    ws['B11'].font = normal_font

    ws['E11'] = mission[11]
    ws['E11'].font = normal_font

    ws['B13'] = mission[13]
    ws['B13'].font = normal_font

    ws['E13'] = mission[14]
    ws['E13'].font = normal_font

    ws['B15'] = f"{mission[15]} دج"
    ws['B15'].font = normal_font

    ws['E15'] = mission[16]
    ws['E15'].font = normal_font
    # Avoid merging cells dynamically if template already has it, or merge if needed
    try:
        ws.merge_cells("E15:I15")
    except ValueError:
        pass # Already merged in customized template

    wb.save(output_path)
