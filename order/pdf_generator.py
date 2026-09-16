from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import arabic_reshaper
from bidi.algorithm import get_display
import os

def render_arabic(text):
    if not text: return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

def generate_pdf_report(employee, missions, output_path, tafqeet_text):
    font_path = "Amiri.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Amiri', font_path))
        font_name = 'Amiri'
    else:
        font_name = 'Helvetica'

    # Switch to Landscape A4 for wide table
    c = canvas.Canvas(output_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Margins and layout
    margin = 30
    grid_start_x = width - margin - 450 # Right side for Mission Grid (450px wide)
    admin_start_x = width - margin      # Extreme right for Admin block (but draws leftwards)

    # --- Left Block (Admin & Finance) ---
    c.setFont(font_name, 12)
    start_y = height - 40

    c.drawRightString(admin_start_x, start_y, render_arabic("الجمهورية الجزائرية الديمقراطية الشعبية"))
    start_y -= 20
    c.drawRightString(admin_start_x, start_y, render_arabic("ولايـــــــــــــــــة المنيعــــــــــــــــــــــة"))
    start_y -= 20
    c.drawRightString(admin_start_x, start_y, render_arabic("مديرية المواصلات السلكية واللاسلكية الوطنية لولاية المنيعة"))

    start_y -= 30
    c.setFont(font_name, 14)
    c.drawRightString(admin_start_x - 50, start_y, render_arabic("كشف مصاريف التنقل"))

    # Employee Details
    c.setFont(font_name, 11)
    start_y -= 40
    c.drawRightString(admin_start_x, start_y, render_arabic(f"السيـــــــــــــد : {employee[1]}"))
    start_y -= 20
    c.drawRightString(admin_start_x, start_y, render_arabic(f"الـرتـبــــــــــــة : {employee[2]}"))
    start_y -= 20
    c.drawRightString(admin_start_x, start_y, render_arabic(f"الرقم الاستدلالي : {employee[4]}"))
    start_y -= 20
    c.drawRightString(admin_start_x, start_y, render_arabic(f"المقـــر الإداري : {employee[6]}"))
    start_y -= 20
    c.drawRightString(admin_start_x, start_y, render_arabic(f"رقم الحساب : {employee[8]}"))

    # --- Right Block (Missions Grid) ---
    # Draw Table Headers
    table_y = height - 50
    c.setFont(font_name, 10)

    col_w = [60, 100, 60, 50, 60, 30, 30, 30, 30]
    headers = ["سبب التنقل", "المراحل", "تاريخ", "ساعة", "وسيلة النقل", "وجبة(ش)", "نوم(ش)", "وجبة(ج)", "نوم(ج)"]

    cur_x = grid_start_x
    for i, h in enumerate(headers):
        c.rect(cur_x, table_y, col_w[i], 30)
        c.drawCentredString(cur_x + (col_w[i]/2), table_y + 10, render_arabic(h))
        cur_x += col_w[i]

    # Draw Mission Rows
    table_y -= 20

    total_n_m = total_n_n = total_s_m = total_s_n = 0

    for m in missions[:10]: # Max 10 missions
        try:
            d_date, d_time = m[10].split(' ')[0], m[10].split(' ')[1]
            r_date, r_time = m[11].split(' ')[0], m[11].split(' ')[1]
        except:
            d_date = d_time = r_date = r_time = ""

        n_meals = m[13] if m[12] == "شمال" else 0
        n_nights = m[14] if m[12] == "شمال" else 0
        s_meals = m[13] if m[12] == "جنوب" else 0
        s_nights = m[14] if m[12] == "جنوب" else 0

        total_n_m += n_meals
        total_n_n += n_nights
        total_s_m += s_meals
        total_s_n += s_nights

        # Departure Row
        cur_x = grid_start_x
        row_data_dep = [m[7], m[8], d_date, d_time, m[9], str(n_meals or ""), str(n_nights or ""), str(s_meals or ""), str(s_nights or "")]
        for i, val in enumerate(row_data_dep):
            c.rect(cur_x, table_y, col_w[i], 20)
            c.drawCentredString(cur_x + (col_w[i]/2), table_y + 6, render_arabic(val))
            cur_x += col_w[i]

        table_y -= 20

        # Return Row
        cur_x = grid_start_x
        row_data_ret = ["", "", r_date, r_time, "", "", "", "", ""]
        for i, val in enumerate(row_data_ret):
            c.rect(cur_x, table_y, col_w[i], 20)
            c.drawCentredString(cur_x + (col_w[i]/2), table_y + 6, render_arabic(val))
            cur_x += col_w[i]

        table_y -= 20

    # Draw Totals Row
    cur_x = grid_start_x + sum(col_w[:5])
    c.rect(grid_start_x, table_y, sum(col_w[:5]), 20)
    c.drawCentredString(grid_start_x + sum(col_w[:5])/2, table_y + 6, render_arabic("المجموع"))

    totals = [str(total_n_m), str(total_n_n), str(total_s_m), str(total_s_n)]
    for i, val in enumerate(totals):
        c.rect(cur_x, table_y, col_w[5+i], 20)
        c.drawCentredString(cur_x + (col_w[5+i]/2), table_y + 6, render_arabic(val))
        cur_x += col_w[5+i]

    # --- Financial Calculation Box (Bottom Left) ---
    c.setFont(font_name, 11)
    fin_y = start_y - 40
    c.drawRightString(admin_start_x, fin_y, render_arabic("التعويضات اليومية:"))

    grand_total = (total_n_m * 800) + (total_n_n * 3200) + (total_s_m * 1000) + (total_s_n * 4000)

    fin_y -= 20
    c.drawRightString(admin_start_x, fin_y, render_arabic(f"الشمال: أكل ({total_n_m}) = {total_n_m * 800} دج | نوم ({total_n_n}) = {total_n_n * 3200} دج"))
    fin_y -= 20
    c.drawRightString(admin_start_x, fin_y, render_arabic(f"الجنوب: أكل ({total_s_m}) = {total_s_m * 1000} دج | نوم ({total_s_n}) = {total_s_n * 4000} دج"))

    fin_y -= 30
    c.setFont(font_name, 12)
    c.drawRightString(admin_start_x, fin_y, render_arabic(f"المجموع العام: {grand_total} دج"))
    fin_y -= 25
    c.drawRightString(admin_start_x, fin_y, render_arabic(f"أوقِف هذا الكشف عند مبلغ قدره: {tafqeet_text}"))

    # Signatures
    fin_y -= 50
    c.drawRightString(admin_start_x, fin_y, render_arabic("امضــاء المعنـي"))
    c.drawString(admin_start_x - 300, fin_y, render_arabic("تأشيرة السيد المدير الآمر بالصرف"))

    c.showPage()
    c.save()
