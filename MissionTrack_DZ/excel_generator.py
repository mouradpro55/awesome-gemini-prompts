import openpyxl
import os
from tafqeet import tafqeet

def sanitize_sheet_title(title, existing_titles):
    invalid_chars = r'\/?*:][\''
    clean_title = "".join(c for c in title if c not in invalid_chars).strip()
    clean_title = clean_title[:28] if len(clean_title) > 28 else clean_title
    if not clean_title:
        clean_title = "موظف"

    unique_title = clean_title
    counter = 1
    while unique_title in existing_titles:
        unique_title = f"{clean_title}_{counter}"[:31]
        counter += 1
    existing_titles.add(unique_title)
    return unique_title

def populate_employee_sheet(ws, employee, missions, tafqeet_text):
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

    safe_write("C11", employee[1])

    # Month assumes we take the month of the first mission or leave blank
    safe_write("G11", missions[0][4] if missions and len(missions) > 0 else "")

    safe_write("C12", employee[2])

    safe_write("G12", f"=C12")

    safe_write("C14", employee[4])

    safe_write("G14", employee[5])

    safe_write("C15", employee[6])

    safe_write("G16", employee[8])

    # Track Totals
    total_n_meals = 0
    total_n_nights = 0
    total_s_meals = 0
    total_s_nights = 0

    # 2. Fill Missions (Row 9 to 28, max 10 missions since 2 rows per mission)
    start_row = 9
    for idx, m in enumerate(missions[:10]):
        row_dep = start_row + (idx * 2)
        row_ret = row_dep + 1

        # Determine regions
        n_meals, n_nights, s_meals, s_nights = 0, 0, 0, 0
        if m[12] == "شمال":
            n_meals = m[13]
            n_nights = m[14]
            total_n_meals += n_meals
            total_n_nights += n_nights
        else:
            s_meals = m[13]
            s_nights = m[14]
            total_s_meals += s_meals
            total_s_nights += s_nights

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

        safe_write(f"K{row_dep}", dep_date)
        safe_write(f"L{row_dep}", dep_time)

        safe_write(f"M{row_dep}", m[9]) # Transport

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

    # 3. Write hardcoded calculations
    safe_write("N29", total_n_meals if total_n_meals > 0 else "")
    safe_write("O29", total_n_nights if total_n_nights > 0 else "")
    safe_write("P29", total_s_meals if total_s_meals > 0 else "")
    safe_write("Q29", total_s_nights if total_s_nights > 0 else "")

    safe_write("D19", total_n_meals if total_n_meals > 0 else "")
    safe_write("D20", total_n_nights if total_n_nights > 0 else "")
    safe_write("D22", total_s_meals if total_s_meals > 0 else "")
    safe_write("D23", total_s_nights if total_s_nights > 0 else "")

    safe_write("G19", (total_n_meals * 800) if total_n_meals > 0 else "")
    safe_write("G20", (total_n_nights * 3200) if total_n_nights > 0 else "")
    safe_write("G22", (total_s_meals * 1000) if total_s_meals > 0 else "")
    safe_write("G23", (total_s_nights * 4000) if total_s_nights > 0 else "")

    grand_total = (total_n_meals * 800) + (total_n_nights * 3200) + (total_s_meals * 1000) + (total_s_nights * 4000)
    safe_write("G25", grand_total if grand_total > 0 else "")

    # 4. Tafqeet Text
    if grand_total > 0:
        if not tafqeet_text.endswith("دينار جزائري"):
            tafqeet_text += " دينار جزائري"
        safe_write("B29", f"أوقِف هذا الكشف عند مبلغ قدره: {tafqeet_text} تماماً")
    else:
        safe_write("B29", "")



def generate_excel_report(employee, missions, output_path, tafqeet_text):
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Template.xlsx")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"ملف القالب الأصلي غير موجود في المسار: {template_path}. يرجى وضع Template.xlsx بجانب البرنامج.")

    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    populate_employee_sheet(ws, employee, missions, tafqeet_text)

    wb.save(output_path)

def generate_consolidated_excel_report(employees_data, output_path, template_path="Template.xlsx"):
    if not os.path.isabs(template_path):
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), template_path)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"ملف القالب الأصلي غير موجود في المسار: {template_path}. يرجى وضع Template.xlsx بجانب البرنامج.")

    # Load master workbook using template as base
    wb = openpyxl.load_workbook(template_path)
    template_sheet = wb.active
    template_sheet.title = "__template__"

    used_sheet_titles = set()
    generated_sheets = []

    # Optional: Build Summary Sheet first
    summary_ws = wb.create_sheet(title="فهرس الكشف الإجمالي", index=0)
    summary_ws.views.sheetView[0].rightToLeft = True
    summary_ws.append(["ر/ت", "اسم ولقب الموظف", "الرتبة", "الحساب البريدي/البنكي", "عدد المهام", "المبلغ الإجمالي (دج)"])

    grand_all_total = 0
    total_missions_all = 0
    row_idx = 1

    for emp, missions in employees_data:
        if not missions:
            continue

        emp_name = emp[1] # full_name
        sheet_title = sanitize_sheet_title(emp_name, used_sheet_titles)

        # Copy the template sheet
        target_ws = wb.copy_worksheet(template_sheet)
        target_ws.title = sheet_title
        target_ws.views.sheetView[0].rightToLeft = True

        # Calculate Totals
        emp_total = sum(m[15] for m in missions)
        emp_tafqeet = tafqeet(emp_total)

        # Populate Employee Header & Info Cells (aligned with Template.xlsx)
        populate_employee_sheet(target_ws, emp, missions, emp_tafqeet)
        generated_sheets.append(target_ws)

        # Append to summary sheet
        summary_ws.append([
            row_idx,
            emp[1],              # full_name
            emp[2],              # rank
            f"{emp[7] or ''} {emp[8] or ''}", # bank / ccp
            len(missions),
            emp_total
        ])
        grand_all_total += emp_total
        total_missions_all += len(missions)
        row_idx += 1

    # Add Summary Total Row
    summary_ws.append([])
    summary_ws.append(["المجموع الكلي العام", "", "", "", total_missions_all, grand_all_total])

    # Remove the base template placeholder sheet
    wb.remove(wb["__template__"])

    wb.save(output_path)
