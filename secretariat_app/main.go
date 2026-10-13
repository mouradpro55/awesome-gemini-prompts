package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

func main() {
	a := app.New()
	a.Settings().SetTheme(&customTheme{})

	w := a.NewWindow("برنامج المراسلات - سكرتارية")

	tabs := container.NewAppTabs(
		container.NewTabItem("مراسلة جديدة", CreateFormUI(w)),
		container.NewTabItem("معلومات البرنامج", widget.NewLabel("برنامج لكتابة المراسلات يخص سكرتارية مديرية المواصلات السلكية واللاسلكية الوطنية.")),
	)

	w.SetContent(tabs)
	w.Resize(fyne.NewSize(600, 700))
	w.ShowAndRun()
}
