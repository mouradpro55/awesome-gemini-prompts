package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"
	"time"
)

func CreateFormUI(w fyne.Window) fyne.CanvasObject {
	refEntry := widget.NewEntry()
	refEntry.SetPlaceHolder("رقم المراسلة")

	dateEntry := widget.NewEntry()
	dateEntry.SetText(time.Now().Format("2006/01/02"))

	recipientEntry := widget.NewEntry()
	recipientEntry.SetPlaceHolder("المرسل إليه")

	subjectEntry := widget.NewEntry()
	subjectEntry.SetPlaceHolder("الموضوع")

	bodyEntry := widget.NewMultiLineEntry()
	bodyEntry.SetPlaceHolder("نص المراسلة...")
	bodyEntry.SetMinRowsVisible(15)

	submitBtn := widget.NewButton("حفظ وتصدير إلى PDF", func() {
		ref := refEntry.Text
		date := dateEntry.Text
		recipient := recipientEntry.Text
		subject := subjectEntry.Text
		body := bodyEntry.Text

		if ref == "" || recipient == "" || subject == "" || body == "" {
			dialog.ShowInformation("خطأ", "الرجاء ملء جميع الحقول", w)
			return
		}

		err := GeneratePDF(ref, date, recipient, subject, body)
		if err != nil {
			dialog.ShowError(err, w)
		} else {
			dialog.ShowInformation("نجاح", "تم حفظ المراسلة بصيغة PDF بنجاح في مجلد البرنامج", w)
			// Clear fields after successful generation
			refEntry.SetText("")
			recipientEntry.SetText("")
			subjectEntry.SetText("")
			bodyEntry.SetText("")
		}
	})

	form := container.NewVBox(
		widget.NewLabel("الرقم المرجعي:"),
		refEntry,
		widget.NewLabel("التاريخ:"),
		dateEntry,
		widget.NewLabel("المرسل إليه:"),
		recipientEntry,
		widget.NewLabel("الموضوع:"),
		subjectEntry,
		widget.NewLabel("النص:"),
		bodyEntry,
		submitBtn,
	)

	return container.NewScroll(form)
}
