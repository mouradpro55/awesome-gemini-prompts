package main

import (
	"fmt"
	"strings"

	"github.com/abdullahdiaa/garabic"
	"github.com/go-pdf/fpdf"
)

// prepareArabic يعالج النص العربي بضمه وعكسه ليتوافق مع fpdf
func prepareArabic(text string) string {
	// 1. تشكيل الحروف العربية لتكون متصلة
	shaped := garabic.Shape(text)

	// 2. لأن go-pdf/fpdf يرسم الحروف من اليسار لليمين، يجب عكس السلسلة
	// لكن يجب عكس الحروف وليس الكلمات فقط، ومكتبات مثل fpdf تحتاج عكس الأحرف.
	// سنقوم بعكس الـ runes بشكل كامل ليدعم العرض بشكل صحيح في الـ PDF.
	runes := []rune(shaped)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func GeneratePDF(ref, date, recipient, subject, body string) error {
	pdf := fpdf.New("P", "mm", "A4", "")
	pdf.AddPage()

	// إضافة الخط العربي
	// ملاحظة: لاستخدام خطوط TTF مع go-pdf/fpdf يجب تحديد مسار ملف ttf مباشرة في AddUTF8Font
	pdf.AddUTF8Font("Amiri", "", "Amiri-Regular.ttf")
	pdf.SetFont("Amiri", "", 14)

	// إضافة الترويسة
	pdf.CellFormat(190, 10, prepareArabic("الجمهورية الجزائرية الديمقراطية الشعبية"), "", 1, "C", false, 0, "")
	pdf.CellFormat(190, 10, prepareArabic("وزارة البريد والمواصلات السلكية واللاسلكية"), "", 1, "C", false, 0, "")
	pdf.CellFormat(190, 10, prepareArabic("مديرية المواصلات السلكية واللاسلكية الوطنية"), "", 1, "C", false, 0, "")

	pdf.Ln(10) // سطر فارغ

	// المعلومات الأساسية
	pdf.SetFont("Amiri", "", 12)
	pdf.CellFormat(95, 10, prepareArabic(fmt.Sprintf("التاريخ: %s", date)), "", 0, "R", false, 0, "")
	pdf.CellFormat(95, 10, prepareArabic(fmt.Sprintf("رقم المراسلة: %s", ref)), "", 1, "L", false, 0, "")

	pdf.Ln(5)

	pdf.SetFont("Amiri", "", 14)
	// المرسل إليه
	pdf.CellFormat(190, 10, prepareArabic(fmt.Sprintf("إلى السيد(ة): %s", recipient)), "", 1, "R", false, 0, "")

	pdf.Ln(5)

	// الموضوع
	pdf.SetFont("Amiri", "", 14)
	pdf.CellFormat(190, 10, prepareArabic(fmt.Sprintf("الموضوع: %s", subject)), "", 1, "R", false, 0, "")

	pdf.Ln(10)

	// نص المراسلة
	pdf.SetFont("Amiri", "", 12)

	// لمعالجة النص الطويل بشكل أفضل، نقسمه لأسطر ونطبق prepareArabic
	lines := strings.Split(body, "\n")
	for _, line := range lines {
		pdf.MultiCell(190, 8, prepareArabic(line), "", "R", false)
	}

	pdf.Ln(20)

	// الإمضاء (أسفل اليسار)
	pdf.CellFormat(190, 10, prepareArabic("المدير الولائي"), "", 1, "L", false, 0, "")

	// حفظ الملف
	fileName := fmt.Sprintf("correspondence_%s.pdf", strings.ReplaceAll(ref, "/", "-"))
	err := pdf.OutputFileAndClose(fileName)
	if err != nil {
		return err
	}

	return nil
}
