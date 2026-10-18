package ui

import (
	"fmt"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"

	"jafr-core/pkg/engine"
	"jafr-core/pkg/nlp"
)

func CreateElementsTab() fyne.CanvasObject {
	input := widget.NewMultiLineEntry()
	input.SetPlaceHolder(ShapeArabic("أدخل النص لتحليل الطبائع..."))
	input.Wrapping = fyne.TextWrapWord

	fireBar := widget.NewProgressBar()
	earthBar := widget.NewProgressBar()
	airBar := widget.NewProgressBar()
	waterBar := widget.NewProgressBar()

	dominantLabel := widget.NewLabel(ShapeArabic("الطبع الغالب: غير محدد"))

	calcBtn := widget.NewButton(ShapeArabic("تحليل التوازن"), func() {
		text := input.Text
		opts := nlp.ProcessOptions{UnifyHamzat: true, ExpandShaddah: false}
		cleanText := nlp.CleanAndNormalize(text, opts)

		counts, dominant := engine.CalculateElements(cleanText)
		total := float64(counts.Fire + counts.Earth + counts.Air + counts.Water)

		if total > 0 {
			fireBar.SetValue(float64(counts.Fire) / total)
			earthBar.SetValue(float64(counts.Earth) / total)
			airBar.SetValue(float64(counts.Air) / total)
			waterBar.SetValue(float64(counts.Water) / total)
		} else {
			fireBar.SetValue(0)
			earthBar.SetValue(0)
			airBar.SetValue(0)
			waterBar.SetValue(0)
		}

		domAr := ""
		switch dominant {
		case "fire": domAr = ShapeArabic("ناري")
		case "earth": domAr = ShapeArabic("ترابي")
		case "air": domAr = ShapeArabic("هوائي")
		case "water": domAr = ShapeArabic("مائي")
		}
		dominantLabel.SetText(fmt.Sprintf("%s: %s", ShapeArabic("الطبع الغالب"), domAr))
	})

	resultsContainer := container.NewVBox(
		container.NewHBox(widget.NewLabel(ShapeArabic("ناري:")), fireBar),
		container.NewHBox(widget.NewLabel(ShapeArabic("ترابي:")), earthBar),
		container.NewHBox(widget.NewLabel(ShapeArabic("هوائي:")), airBar),
		container.NewHBox(widget.NewLabel(ShapeArabic("مائي:")), waterBar),
		dominantLabel,
	)

	return container.NewBorder(
		nil,
		container.NewVBox(calcBtn, resultsContainer),
		nil,
		nil,
		input,
	)
}
