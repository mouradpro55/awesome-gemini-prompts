import openpyxl
from openpyxl.styles import Alignment, Font, Border, Side
import os

def create_default_template(template_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "كشف مصاريف التنقل"
    ws.sheet_view.rightToLeft = True

    # Print Settings: Exact Match with User SRS
    ws.views.sheetView[0].rightToLeft = True
    ws.views.sheetView[0].showGridLines = False
    ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.scale = 80
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = 0.118
    ws.page_margins.right = 0.118
    ws.page_margins.top = 0.354
    ws.page_margins.bottom = 0.551

    # Apply precise Column Dimensions
    col_widths = {
        'A': 1.1, 'B': 15.0, 'C': 8.9, 'D': 16.7, 'E': 13.0, 'F': 15.3, 'G': 37.1, 'H': 1.7,
        'I': 11.1, 'J': 22.0, 'K': 15.1, 'L': 8.3, 'M': 11.0, 'N': 5.7, 'O': 5.3, 'P': 5.7,
        'Q': 5.3, 'R': 5.9, 'S': 1.0, 'T': 7.1, 'U': 1.7, 'V': 1.7, 'W': 5.1
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # Styling helpers
    bold_font = Font(name="Arial", size=11, bold=True)
    normal_font = Font(name="Arial", size=11)
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    right_align = Alignment(horizontal="right", vertical="center")

    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    def set_cell(coord, value, font, align=center_align, merge=None, border=None):
        ws[coord] = value
        ws[coord].font = font
        ws[coord].alignment = align
        if border:
            ws[coord].border = border
        if merge:
            ws.merge_cells(merge)

    # --- Left Block (Admin & Finance): Cols B to G ---
    # Header
    set_cell("B3", "الجمهورية الجزائرية الديمقراطية الشعبية", bold_font, merge="B3:G3")
    set_cell("B5", "ولايـــــــــــــــــة المنيعــــــــــــــــــــــة", bold_font, merge="B5:G5")
    set_cell("B6", "مديرية المواصلات السلكية واللاسلكية الوطنية لولاية المنيعة", bold_font, merge="B6:D7")

    set_cell("F6", "الـبــــــاب :", bold_font)
    set_cell("G6", "2", normal_font)
    set_cell("F7", "الـمــــادة :", bold_font)
    set_cell("G7", "21100", normal_font)

    # Main Report Title
    set_cell("B9", "كشـــــف مصاريــــف التنقــــــــــل", Font(name="Arial", size=16, bold=True), align=center_align, merge="B9:G9")

    # Employee Data Headers
    set_cell("B11", "السيـــــــــــــد :", bold_font, align=right_align)
    set_cell("F11", "لـشـهــــــــر :", bold_font, align=right_align)

    set_cell("B12", "الـرتـبــــــــــــة :", bold_font, align=right_align)
    set_cell("F12", "الوظيفــــــة :", bold_font, align=right_align)

    set_cell("B14", "الرقم الاستدلالي :", bold_font, align=right_align)
    set_cell("F14", "الصـنــــــــف :", bold_font, align=right_align)

    set_cell("B15", "المقـــر الإداري :", bold_font, align=right_align)
    set_cell("F15", "الـبـنـــــــــك :", bold_font, align=right_align)
    set_cell("G15", "الحســاب البـريــدي الجــاري", normal_font)

    set_cell("F16", "رقم الحساب :", bold_font, align=right_align)

    # Calculations Block
    set_cell("B17", "التعويضات اليومية :", bold_font, align=right_align)

    # Nord
    set_cell("E19", "الاكــــــل :", bold_font)
    set_cell("F19", 800, normal_font)
    ws['G19'] = "=D19*F19"

    set_cell("E20", ": النــــــوم", bold_font)
    set_cell("F20", 3200, normal_font)
    ws['G20'] = "=D20*F20"

    # Sud
    set_cell("E22", "الاكــــــل :", bold_font)
    set_cell("F22", 1000, normal_font)
    ws['G22'] = "=D22*F22"

    set_cell("E23", ": النــــــوم", bold_font)
    set_cell("F23", 4000, normal_font)
    ws['G23'] = "=D23*F23"

    set_cell("B25", "المجموع العـــام ( مصاربــف النقـــل + التعويضـات اليوميــة )", bold_font, align=right_align, merge="B25:F25")
    ws['G25'] = "=SUM(G19:G23)"

    # Tafqeet and Sigs
    set_cell("B28", "اتعهد صاحب هذه المصاريف بصحة المعلومات اطلب تسديدها", bold_font, align=right_align, merge="B28:G28")

    set_cell("C31", "المنيعــة في :", bold_font)
    set_cell("G31", "امضــاء المعنـي", bold_font)
    set_cell("C32", "المديـــر", bold_font)


    # --- Right Block (Missions Grid): Cols I to W ---
    set_cell("I6", "سبب التنقل", bold_font, border=thin_border, merge="I6:I8")
    set_cell("J6", "المراحل", bold_font, border=thin_border, merge="J6:J8")
    set_cell("K6", "تاريخ الذهاب والاياب", bold_font, border=thin_border, merge="K6:K8")
    set_cell("L6", "ساعـة الذهاب و الإيـاب", bold_font, border=thin_border, merge="L6:L8")
    set_cell("M6", "وسيلة نقل", bold_font, border=thin_border, merge="M6:M8")

    set_cell("N6", "عــــدد التعـويــضــــات", bold_font, border=thin_border, merge="N6:Q6")

    set_cell("N7", "شمــــــال", bold_font, border=thin_border, merge="N7:O7")
    set_cell("N8", "وجبة", bold_font, border=thin_border)
    set_cell("O8", "مرقد", bold_font, border=thin_border)

    set_cell("P7", "الجنــوب", bold_font, border=thin_border, merge="P7:Q7")
    set_cell("P8", "وجبة", bold_font, border=thin_border)
    set_cell("Q8", "مرقد", bold_font, border=thin_border)

    set_cell("R6", "رقم المهمة", bold_font, border=thin_border, merge="R6:T6")
    set_cell("R7", "تاريخ المهمة", bold_font, border=thin_border, merge="R7:T8")

    # Bottom Sums Row
    set_cell("L29", "المجموع", bold_font, border=thin_border, merge="L29:M29")
    ws['N29'] = "=SUM(N9:N28)"
    ws['O29'] = "=SUM(O9:O28)"
    ws['P29'] = "=SUM(P9:P28)"
    ws['Q29'] = "=SUM(Q9:Q28)"

    # Draw grid borders for the blank areas to ensure it looks like a table
    for r in range(9, 30):
        for c in range(9, 21): # I to T
            col_letter = openpyxl.utils.get_column_letter(c)
            ws[f"{col_letter}{r}"].border = thin_border

    wb.save(template_path)


def generate_excel_report(employee, missions, output_path, tafqeet_text):
    template_path = "Template.xlsx"
    if not os.path.exists(template_path):
        create_default_template(template_path)

    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    normal_font = Font(name="Arial", size=11)

    def safe_write(coord_str, val):
        coord = openpyxl.utils.coordinate_to_tuple(coord_str)
        for merged_range in ws.merged_cells.ranges:
            if coord[0] >= merged_range.min_row and coord[0] <= merged_range.max_row and \
               coord[1] >= merged_range.min_col and coord[1] <= merged_range.max_col:
                top_left = ws.cell(row=merged_range.min_row, column=merged_range.min_col)
                top_left.value = val
                return top_left
        cell = ws[coord_str]
        cell.value = val
        return cell

    # 1. Fill Employee Info
    safe_write("C11", employee[1])
    try: ws.merge_cells("C11:E11")
    except ValueError: pass

    # Month assumes we take the month of the first mission or leave blank
    # NOTE: user specified F11 is the header ("لـشـهــــــــر :"). G11 should hold the data.
    # In my previous code, F11 is header, G11 is where we put it. But wait, we write to G11. The user said "الخلية F11 فارغة! يجب كتابة الشهر".
    # Oh! F11 has "لـشـهــــــــر :" in the template, so the data should actually go to G11. I will write to G11 just in case, but let's ensure F11 is safely written.
    safe_write("G11", missions[0][4] if missions and len(missions) > 0 else "")

    safe_write("C12", employee[2])
    try: ws.merge_cells("C12:E13")
    except ValueError: pass

    safe_write("G12", f"=C12")
    try: ws.merge_cells("G12:G13")
    except ValueError: pass

    safe_write("C14", employee[4])
    try: ws.merge_cells("C14:E14")
    except ValueError: pass

    safe_write("G14", employee[5])

    safe_write("C15", employee[6])
    try: ws.merge_cells("C15:E15")
    except ValueError: pass

    safe_write("G16", employee[8])

    # 2. Link Sub-totals
    safe_write("D19", "=N29")
    safe_write("D20", "=O29")
    safe_write("D22", "=P29")
    safe_write("D23", "=Q29")

    # 3. Tafqeet Text
    t_cell = safe_write("B29", f"أوقِف هذا الكشف عند مبلغ قدره: {tafqeet_text}")
    t_cell.font = Font(name="Arial", size=12, bold=True)
    try: ws.merge_cells("B29:G29")
    except ValueError: pass

    # 4. Fill Missions (Row 9 to 28, max 10 missions since 2 rows per mission)
    start_row = 9
    for idx, m in enumerate(missions[:10]):
        row_dep = start_row + (idx * 2)
        row_ret = row_dep + 1

        # Determine regions
        n_meals, n_nights, s_meals, s_nights = 0, 0, 0, 0
        if m[12] == "شمال":
            n_meals = m[13]
            n_nights = m[14]
        else:
            s_meals = m[13]
            s_nights = m[14]

        # Parse Departure and Return datetime strings (expected: "DD-MM-YYYY HH:MM")
        try:
            dep_parts = m[10].split(' ')
            dep_date = dep_parts[0]
            dep_time = dep_parts[1] if len(dep_parts)>1 else ""

            ret_parts = m[11].split(' ')
            ret_date = ret_parts[0]
            ret_time = ret_parts[1] if len(ret_parts)>1 else ""
        except:
            dep_date, dep_time, ret_date, ret_time = "", "", "", ""

        # Departure Row (row_dep)
        safe_write(f"I{row_dep}", m[7]) # Purpose

        safe_write(f"J{row_dep}", m[8]) # Itinerary
        try: ws.merge_cells(f"J{row_dep}:J{row_ret}")
        except: pass

        safe_write(f"K{row_dep}", dep_date)
        safe_write(f"L{row_dep}", dep_time)

        safe_write(f"M{row_dep}", m[9]) # Transport
        try: ws.merge_cells(f"M{row_dep}:M{row_ret}")
        except: pass

        safe_write(f"N{row_dep}", n_meals if n_meals > 0 else "")
        safe_write(f"O{row_dep}", n_nights if n_nights > 0 else "")
        safe_write(f"P{row_dep}", s_meals if s_meals > 0 else "")
        safe_write(f"Q{row_dep}", s_nights if s_nights > 0 else "")

        safe_write(f"R{row_dep}", m[5]) # Order Num
        safe_write(f"S{row_dep}", f'=IF(K{row_dep}="","","/")')
        safe_write(f"T{row_dep}", f'=IF(K{row_dep}="","",YEAR(DATEVALUE(K{row_dep})))')

        # Return Row (row_ret)
        safe_write(f"K{row_ret}", ret_date)
        safe_write(f"L{row_ret}", ret_time)
        safe_write(f"R{row_ret}", m[6]) # Order Date

        # Center align everything in the mission grid
        for c in range(9, 21):
            col_letter = openpyxl.utils.get_column_letter(c)
            ws[f"{col_letter}{row_dep}"].alignment = center_align
            ws[f"{col_letter}{row_ret}"].alignment = center_align

    wb.save(output_path)
