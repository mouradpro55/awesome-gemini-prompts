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
	input.SetPlaceHolder("أدخل النص لتحليل الطبائع...")
	input.Wrapping = fyne.TextWrapWord

	fireBar := widget.NewProgressBar()
	earthBar := widget.NewProgressBar()
	airBar := widget.NewProgressBar()
	waterBar := widget.NewProgressBar()

	dominantLabel := widget.NewLabel("الطبع الغالب: غير محدد")

	calcBtn := widget.NewButton("تحليل التوازن", func() {
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
		case "fire": domAr = "ناري"
		case "earth": domAr = "ترابي"
		case "air": domAr = "هوائي"
		case "water": domAr = "مائي"
		}
		dominantLabel.SetText(fmt.Sprintf("الطبع الغالب: %s", domAr))
	})

	resultsContainer := container.NewVBox(
		container.NewHBox(widget.NewLabel("ناري:"), fireBar),
		container.NewHBox(widget.NewLabel("ترابي:"), earthBar),
		container.NewHBox(widget.NewLabel("هوائي:"), airBar),
		container.NewHBox(widget.NewLabel("مائي:"), waterBar),
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
