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

def create_manual():
    output_path = "دليل_الاستخدام_MissionTrack.pdf"

    font_path = "Amiri.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Amiri', font_path))
        font_name = 'Amiri'
    else:
        font_name = 'Helvetica'

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 50
    right_margin = width - margin

    # Title
    c.setFont(font_name, 22)
    c.drawCentredString(width / 2.0, height - 80, render_arabic("دليل استخدام برنامج MissionTrack DZ"))
    c.setFont(font_name, 14)
    c.drawCentredString(width / 2.0, height - 110, render_arabic("نظام تسيير وحساب كشوف مصاريف التنقل"))

    start_y = height - 170

    # Section 1
    c.setFont(font_name, 16)
    c.drawRightString(right_margin, start_y, render_arabic("1. متطلبات التشغيل الأساسية:"))
    start_y -= 30
    c.setFont(font_name, 12)
    c.drawRightString(right_margin - 20, start_y, render_arabic("• يعمل البرنامج بشكل مباشر كملف تنفيذي (exe.) على نظام ويندوز 10 وويندوز 11."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("• لا يتطلب البرنامج أي تنصيب لخوادم أو برامج مساعدة، فهو يفتح عبر متصفحك الافتراضي."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("• هام جداً: يجب أن يكون ملف القالب الإداري الأصلي (Template.xlsx) موجوداً دائماً"))
    start_y -= 20
    c.drawRightString(right_margin - 20, start_y, render_arabic("  في نفس المجلد الذي يحتوي على البرنامج لكي تنجح عملية تصدير الكشوف."))

    # Section 2
    start_y -= 40
    c.setFont(font_name, 16)
    c.drawRightString(right_margin, start_y, render_arabic("2. كيفية تشغيل البرنامج:"))
    start_y -= 30
    c.setFont(font_name, 12)
    c.drawRightString(right_margin - 20, start_y, render_arabic("• انقر مرتين على أيقونة البرنامج (MissionTrack_DZ.exe)."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("• ستظهر نافذة سوداء صغيرة (مُخدّم محلي)، اتركها مفتوحة بالخلفية ولا تغلقها."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("• سيقوم البرنامج تلقائياً بفتح نافذة الواجهة في متصفحك (مثل جوجل كروم أو إيدج)."))

    # Section 3
    start_y -= 40
    c.setFont(font_name, 16)
    c.drawRightString(right_margin, start_y, render_arabic("3. دورة العمل وإدارة البيانات:"))
    start_y -= 30
    c.setFont(font_name, 12)
    c.drawRightString(right_margin - 20, start_y, render_arabic("أولاً: اذهب إلى تبويب (إدارة الموظفين) وقم بإضافة الموظفين وتفاصيل حساباتهم البريدية."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("ثانياً: اذهب إلى تبويب (المهمات والكشوفات) واختر موظفاً من القائمة."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("ثالثاً: قم بتعبئة تواريخ الذهاب والإياب بالصيغة المطلوبة (مثال: 01-05-2026 08:00)."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("رابعاً: اضغط على (معاينة الحساب) ليقوم النظام تلقائياً باستخراج عدد الوجبات والليالي والمبلغ."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("خامساً: احفظ المهمة في السجل لتنضم إلى قائمة مهام الموظف."))

    # Section 4
    start_y -= 40
    c.setFont(font_name, 16)
    c.drawRightString(right_margin, start_y, render_arabic("4. استخراج وطباعة الكشوف الرسمية:"))
    start_y -= 30
    c.setFont(font_name, 12)
    c.drawRightString(right_margin - 20, start_y, render_arabic("• بمجرد الانتهاء من إدخال كافة مهام الموظف خلال الشهر، اضغط على زر (تصدير Excel)."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("• سيقوم البرنامج بدمج جميع مهام هذا الموظف في القالب الرسمي وحساب المجاميع والتفقيط المالي."))
    start_y -= 25
    c.drawRightString(right_margin - 20, start_y, render_arabic("• الملف المصدّر (Excel) مُعد مسبقاً للطباعة بشكل عرضي (Landscape) على ورق A4."))

    # Footer
    c.setFont(font_name, 10)
    c.drawCentredString(width / 2.0, 55, render_arabic("تم تطوير وبناء هذا النظام بواسطة: السيد مصباح مراد - مديرية المواصلات السلكية واللاسلكية لولاية المنيعة"))
    c.drawCentredString(width / 2.0, 40, render_arabic("الهاتف: 0770112818 | البريد الإلكتروني: m.elgolea47@gmail.com"))
    c.drawCentredString(width / 2.0, 25, render_arabic("تحت إشراف: DTN بن طراري إبراهيم خليل | جميع الحقوق محفوظة للإدارة 2026"))

    c.showPage()
    c.save()
    print("User Guide PDF generated successfully.")

if __name__ == "__main__":
    create_manual()
