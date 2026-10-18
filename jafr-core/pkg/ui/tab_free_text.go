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
	input.SetPlaceHolder("أدخل النص العربي هنا...")
	input.Wrapping = fyne.TextWrapWord

	radio := widget.NewRadioGroup([]string{"القاعدة المشرقية", "القاعدة المغربية"}, nil)
	radio.SetSelected("القاعدة المشرقية")
	radio.Horizontal = true

	checkHamzat := widget.NewCheck("توحيد الهمزات", nil)
	checkHamzat.SetChecked(true)

	checkShaddah := widget.NewCheck("فك الشدة", nil)
	checkShaddah.SetChecked(false)

	resultEast := canvas.NewText("الجُمّل الكبير: 0", color.White)
	resultEast.TextSize = 16
	resultSaghir := canvas.NewText("الجُمّل الصغير: 0", color.White)
	resultSaghir.TextSize = 16
	resultBast := canvas.NewText("حساب البسط المفرود: 0", color.White)
	resultBast.TextSize = 16

	calcBtn := widget.NewButton("حساب وتحليل", func() {
		text := input.Text
		opts := nlp.ProcessOptions{
			UnifyHamzat:   checkHamzat.Checked,
			ExpandShaddah: checkShaddah.Checked,
		}
		cleanText := nlp.CleanAndNormalize(text, opts)

		cType := engine.East
		if radio.Selected == "القاعدة المغربية" {
			cType = engine.West
		}

		macro := engine.MacroValue(cleanText, cType)
		saghir := engine.DigitalRoot(macro)
		bast := engine.BastExtendedValue(cleanText, cType)

		resultEast.Text = fmt.Sprintf("الجُمّل الكبير: %d", macro)
		resultSaghir.Text = fmt.Sprintf("الجُمّل الصغير: %d", saghir)
		resultBast.Text = fmt.Sprintf("حساب البسط المفرود: %d", bast)

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
