import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from resource_utils import resource_path

def ar(text):
    if text is None or text == "":
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def generate_pdf_report(employee, missions, output_path, tafqeet_text, settings=None):
    font_path = resource_path("Amiri.ttf")
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('AmiriFont', font_path))
        font_name = 'AmiriFont'
    else:
        font_name = 'Helvetica'

    rep_title = settings[1] if settings else "الجمهورية الجزائرية الديمقراطية الشعبية"
    state_title = settings[3] if settings else "ولايـــــــــــــــــة المنيعــــــــــــــــــــــة"
    inst_title = settings[4] if settings else "مديرية المواصلات السلكية واللاسلكية الوطنية"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        rightMargin=25,
        leftMargin=25,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', fontName=font_name, fontSize=11, leading=14, alignment=1)
    header_style = ParagraphStyle('Header', fontName=font_name, fontSize=13, leading=16, alignment=1)
    cell_style = ParagraphStyle('Cell', fontName=font_name, fontSize=9, leading=11, alignment=1)
    cell_bold = ParagraphStyle('CellB', fontName=font_name, fontSize=9, leading=11, alignment=1)

    elements = []

    # 1. الترويسة وبيانات الموظف والمؤسسة
    header_data = [
        [
            Paragraph(f"<b>{ar(rep_title)}</b><br/>{ar(state_title)}<br/>{ar(inst_title)}", title_style),
            Paragraph(f"<b><font size=14>{ar('كشف مصاريف التنقل')}</font></b><br/>{ar('لشهر: ' + (missions[0][4] if missions else ''))}", header_style),
            Paragraph(
                f"<b>{ar('السيد:')}</b> {ar(employee[1])} &nbsp;&nbsp; <b>{ar('الرتبة:')}</b> {ar(employee[2])}<br/>"
                f"<b>{ar('الرقم الاستدلالي:')}</b> {employee[4]} &nbsp;&nbsp; <b>{ar('الصنف:')}</b> {employee[5]}<br/>"
                f"<b>{ar('الحساب:')}</b> {employee[8]} ({ar(employee[7])})",
                title_style
            )
        ]
    ]
    t_header = Table(header_data, colWidths=[240, 220, 300])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_header)
    elements.append(Spacer(1, 10))

    # 2. جدول المأموريات
    cols = [ar('المبلغ'), ar('النوع'), ar('ليالي'), ar('وجبات'), ar('وسيلة النقل'), ar('تاريخ وساعة الإياب'), ar('تاريخ وساعة الذهاب'), ar('المسار'), ar('سبب التنقل'), ar('أمر بمهمة')]
    table_rows = [cols]

    total_meals_n = total_nights_n = 0
    total_meals_s = total_nights_s = 0
    grand_total = 0

    for m in missions:
        is_training = (len(m) > 18 and m[18] == 'تكوين') or ('تكوين' in str(m[7]))
        m_type_txt = ar("تكوين (25%)") if is_training else ar("عادية")

        reg = m[12]
        meals = m[13] or 0
        nights = m[14] or 0
        amt = m[15] or 0
        grand_total += amt

        if reg == "جنوب":
            total_meals_s += meals
            total_nights_s += nights
        else:
            total_meals_n += meals
            total_nights_n += nights

        order_info = f"{m[5]}<br/>{m[6]}"
        table_rows.append([
            f"{amt:,.2f}",
            m_type_txt,
            str(nights),
            str(meals),
            ar(m[9]),
            m[11],
            m[10],
            ar(m[8]),
            ar(m[7]),
            order_info
        ])

    table_rows.append([
        f"<b>{grand_total:,.2f}</b>",
        "",
        str(total_nights_n + total_nights_s),
        str(total_meals_n + total_meals_s),
        "", "", "", "",
        f"<b>{ar('المجموع الإجمالي')}</b>",
        ""
    ])

    formatted_rows = []
    for r_idx, row in enumerate(table_rows):
        formatted_row = []
        for c_idx, cell in enumerate(row):
            st = cell_bold if (r_idx == 0 or r_idx == len(table_rows)-1) else cell_style
            formatted_row.append(Paragraph(str(cell), st))
        formatted_rows.append(formatted_row)

    col_widths = [75, 75, 40, 40, 75, 95, 95, 115, 110, 70]
    m_table = Table(formatted_rows, colWidths=col_widths, repeatRows=1)
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#f8fafc")),
    ]))
    elements.append(m_table)
    elements.append(Spacer(1, 10))

    # 3. التفقيط والتوقيعات
    fin_text = (
        f"<b>{ar('أوقف هذا الكشف عند مبلغ قدره:')}</b> {ar(tafqeet_text)}.<br/>"
        f"<b>{ar('تفاصيل التعويض:')}</b> {ar('شمال')} ({total_meals_n} {ar('وجبة')} / {total_nights_n} {ar('ليلة')}) &nbsp;|&nbsp; "
        f"{ar('جنوب')} ({total_meals_s} {ar('وجبة')} / {total_nights_s} {ar('ليلة')})"
    )

    footer_data = [
        [Paragraph(fin_text, title_style)],
        [
            Paragraph(f"<br/><br/><b>{ar('إمضاء المعني')}</b>", title_style),
            Paragraph(f"<br/><br/><b>{ar('تأشيرة رئيس المصلحة')}</b>", title_style),
            Paragraph(f"<br/><br/><b>{ar('تأشيرة الآمر بالصرف')}</b>", title_style)
        ]
    ]
    t_footer = Table(footer_data, colWidths=[790])
    t_footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(t_footer)

    doc.build(elements)
