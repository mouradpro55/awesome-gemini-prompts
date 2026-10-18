package ui

import (
	"fmt"
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"

	"jafr-core/pkg/engine"
	"jafr-core/pkg/nlp"
)

func CreateFreeTextTab() fyne.CanvasObject {
	input := widget.NewMultiLineEntry()
	input.SetPlaceHolder(ShapeArabic("أدخل النص العربي هنا..."))
	input.Wrapping = fyne.TextWrapWord

	radioChoices := []string{ShapeArabic("القاعدة المشرقية"), ShapeArabic("القاعدة المغربية")}
	radio := widget.NewRadioGroup(radioChoices, nil)
	radio.SetSelected(radioChoices[0])
	radio.Horizontal = true

	checkHamzat := widget.NewCheck(ShapeArabic("توحيد الهمزات"), nil)
	checkHamzat.SetChecked(true)

	checkShaddah := widget.NewCheck(ShapeArabic("فك الشدة"), nil)
	checkShaddah.SetChecked(false)

	resultEast := canvas.NewText(ShapeArabic("الجُمّل الكبير: 0"), color.White)
	resultEast.TextSize = 20
	resultSaghir := canvas.NewText(ShapeArabic("الجُمّل الصغير: 0"), color.White)
	resultSaghir.TextSize = 20
	resultBast := canvas.NewText(ShapeArabic("حساب البسط المفرود: 0"), color.White)
	resultBast.TextSize = 20

	calcBtn := widget.NewButton(ShapeArabic("حساب وتحليل"), func() {
		text := input.Text
		opts := nlp.ProcessOptions{
			UnifyHamzat:   checkHamzat.Checked,
			ExpandShaddah: checkShaddah.Checked,
		}
		cleanText := nlp.CleanAndNormalize(text, opts)

		cType := engine.East
		if radio.Selected == ShapeArabic("القاعدة المغربية") {
			cType = engine.West
		}

		macro := engine.MacroValue(cleanText, cType)
		saghir := engine.DigitalRoot(macro)
		bast := engine.BastExtendedValue(cleanText, cType)

		resultEast.Text = fmt.Sprintf("%s: %d", ShapeArabic("الجُمّل الكبير"), macro)
		resultSaghir.Text = fmt.Sprintf("%s: %d", ShapeArabic("الجُمّل الصغير"), saghir)
		resultBast.Text = fmt.Sprintf("%s: %d", ShapeArabic("حساب البسط المفرود"), bast)

		resultEast.Refresh()
		resultSaghir.Refresh()
		resultBast.Refresh()
	})

	optionsContainer := container.NewHBox(radio, checkHamzat, checkShaddah)
	resultsContainer := container.NewHBox(resultEast, widget.NewLabel(" | "), resultSaghir, widget.NewLabel(" | "), resultBast)

	return container.NewBorder(
		nil,
		container.NewVBox(optionsContainer, calcBtn, resultsContainer),
		nil,
		nil,
		input,
	)
}
