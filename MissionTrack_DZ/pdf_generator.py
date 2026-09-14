from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import os

def render_arabic(text):
    if not text: return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

def generate_pdf_report(employee, mission, output_path):
    # Register Font
    font_path = "Amiri.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Amiri', font_path))
        font_name = 'Amiri'
    else:
        font_name = 'Helvetica'

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # --- Header ---
    c.setFont(font_name, 14)
    c.drawCentredString(width / 2.0, height - 50, render_arabic("الجمهورية الجزائرية الديمقراطية الشعبية"))
    c.drawCentredString(width / 2.0, height - 70, render_arabic("وزارة البريد والمواصلات السلكية واللاسلكية"))

    c.setFont(font_name, 18)
    c.drawCentredString(width / 2.0, height - 120, render_arabic("كشف مصاريف التنقل"))

    # --- Employee Info ---
    c.setFont(font_name, 12)
    start_y = height - 160
    margin = 50
    right_margin = width - margin

    # Row 1
    c.drawRightString(right_margin, start_y, render_arabic(f"الاسم واللقب: {employee[1]}"))
    c.drawRightString(right_margin - 200, start_y, render_arabic(f"الرتبة / الوظيفة: {employee[2]} / {employee[3]}"))
    c.drawRightString(right_margin - 400, start_y, render_arabic(f"الرقم الاستدلالي: {employee[4]}"))

    # Row 2
    start_y -= 30
    c.drawRightString(right_margin, start_y, render_arabic(f"المقر الإداري: {employee[6]}"))
    c.drawRightString(right_margin - 200, start_y, render_arabic(f"طبيعة الحساب: {employee[7]}"))
    c.drawRightString(right_margin - 400, start_y, render_arabic(f"رقم الحساب: {employee[8]}"))

    # --- Mission Detail ---
    start_y -= 50
    c.setFont(font_name, 14)
    c.drawRightString(right_margin, start_y, render_arabic("تفاصيل المهمة:"))

    c.setFont(font_name, 12)
    start_y -= 30
    c.drawRightString(right_margin, start_y, render_arabic(f"رقم وتاريخ الأمر: {mission[5]} - {mission[6]}"))
    c.drawRightString(right_margin - 250, start_y, render_arabic(f"سبب التنقل: {mission[7]}"))

    start_y -= 30
    c.drawRightString(right_margin, start_y, render_arabic(f"المسار: {mission[8]}"))
    c.drawRightString(right_margin - 250, start_y, render_arabic(f"وسيلة النقل: {mission[9]}"))

    start_y -= 30
    c.drawRightString(right_margin, start_y, render_arabic(f"تاريخ الذهاب: {mission[10]}"))
    c.drawRightString(right_margin - 250, start_y, render_arabic(f"تاريخ الإياب: {mission[11]}"))

    start_y -= 30
    c.drawRightString(right_margin, start_y, render_arabic(f"المنطقة: {mission[12]}"))

    # --- Calculation Table ---
    start_y -= 50
    c.setFont(font_name, 12)

    col_widths = [100, 100, 100, 100]
    total_w = sum(col_widths)
    start_x = width/2 - total_w/2

    # Headers
    c.rect(start_x, start_y, col_widths[0], 25)
    c.rect(start_x+col_widths[0], start_y, col_widths[1], 25)
    c.rect(start_x+col_widths[0]*2, start_y, col_widths[2], 25)
    c.rect(start_x+col_widths[0]*3, start_y, col_widths[3], 25)

    c.drawCentredString(start_x + col_widths[0]*3.5, start_y + 8, render_arabic("عدد الوجبات"))
    c.drawCentredString(start_x + col_widths[0]*2.5, start_y + 8, render_arabic("المبلغ للوجبات"))
    c.drawCentredString(start_x + col_widths[0]*1.5, start_y + 8, render_arabic("عدد الليالي"))
    c.drawCentredString(start_x + col_widths[0]*0.5, start_y + 8, render_arabic("المبلغ لليالي"))

    # Values
    start_y -= 25
    rate = 800 if mission[12] == "شمال" else 1000
    n_rate = 3200 if mission[12] == "شمال" else 4000
    m_amt = mission[13] * rate
    n_amt = mission[14] * n_rate

    c.rect(start_x, start_y, col_widths[0], 25)
    c.rect(start_x+col_widths[0], start_y, col_widths[1], 25)
    c.rect(start_x+col_widths[0]*2, start_y, col_widths[2], 25)
    c.rect(start_x+col_widths[0]*3, start_y, col_widths[3], 25)

    c.drawCentredString(start_x + col_widths[0]*3.5, start_y + 8, render_arabic(str(mission[13])))
    c.drawCentredString(start_x + col_widths[0]*2.5, start_y + 8, render_arabic(f"{m_amt} دج"))
    c.drawCentredString(start_x + col_widths[0]*1.5, start_y + 8, render_arabic(str(mission[14])))
    c.drawCentredString(start_x + col_widths[0]*0.5, start_y + 8, render_arabic(f"{n_amt} دج"))

    # --- Footer Totals ---
    start_y -= 60
    c.setFont(font_name, 14)
    c.drawRightString(right_margin, start_y, render_arabic(f"المجموع العام: {mission[15]} دج"))
    start_y -= 30
    c.drawRightString(right_margin, start_y, render_arabic(f"المبلغ بالحروف: {mission[16]}"))

    # --- Signatures ---
    start_y -= 80
    c.drawRightString(right_margin, start_y, render_arabic("إمضاء المعني بالأمر"))
    c.drawString(margin + 50, start_y, render_arabic("تأشيرة السيد المدير الآمر بالصرف"))

    # --- Credits ---
    c.setFont(font_name, 10)
    c.drawCentredString(width / 2.0, 30, render_arabic("تم إعداد هذا البرنامج (MissionTrack DZ) من طرف السيد مصباح مراد"))

    c.showPage()
    c.save()
