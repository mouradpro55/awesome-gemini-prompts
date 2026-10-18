package ui

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/widget"

	"jafr-core/pkg/quran"
)

func CreateQuranTab(repo *quran.Repository) fyne.CanvasObject {
	input := widget.NewEntry()
	input.SetPlaceHolder("أدخل الوزن العددي (مثال: 110)...")

	var resultsData []quran.AyahSearchResult

	list := widget.NewTable(
		func() (int, int) {
			return len(resultsData), 4
		},
		func() fyne.CanvasObject {
			label := widget.NewLabel("Template")
			label.Wrapping = fyne.TextTruncate
			return label
		},
		func(i widget.TableCellID, o fyne.CanvasObject) {
			label := o.(*widget.Label)
			ayah := resultsData[i.Row]
			switch i.Col {
			case 0:
				label.SetText(ayah.SurahName)
			case 1:
				label.SetText(fmt.Sprintf("%d", ayah.AyahNumber))
			case 2:
				label.SetText(ayah.TextTashkeel)
			case 3:
				domAr := ""
				switch ayah.DominantElement {
				case "fire": domAr = "ناري"
				case "earth": domAr = "ترابي"
				case "air": domAr = "هوائي"
				case "water": domAr = "مائي"
				}
				label.SetText(domAr)
			}
		},
	)
	list.SetColumnWidth(0, 100)
	list.SetColumnWidth(1, 50)
	list.SetColumnWidth(2, 400)
	list.SetColumnWidth(3, 80)

	headers := container.NewGridWithColumns(4,
		widget.NewLabelWithStyle("السورة", fyne.TextAlignCenter, fyne.TextStyle{Bold: true}),
		widget.NewLabelWithStyle("الآية", fyne.TextAlignCenter, fyne.TextStyle{Bold: true}),
		widget.NewLabelWithStyle("النص", fyne.TextAlignCenter, fyne.TextStyle{Bold: true}),
		widget.NewLabelWithStyle("الطبع", fyne.TextAlignCenter, fyne.TextStyle{Bold: true}),
	)

	searchBtn := widget.NewButton("بحث عكسي", func() {
		val, err := strconv.Atoi(input.Text)
		if err == nil {
			res, err := repo.SearchByJummalEast(val)
			if err == nil {
				resultsData = res
				list.Refresh()
			}
		}
	})

	exportBtn := widget.NewButton("تصدير النتائج (CSV/JSON)", func() {
		if len(resultsData) == 0 {
			dialog.ShowInformation("تنبيه", "لا توجد نتائج لتصديرها", fyne.CurrentApp().Driver().AllWindows()[0])
			return
		}

		userHome, _ := os.UserHomeDir()
		downloadsDir := filepath.Join(userHome, "Downloads")

		timestamp := time.Now().Format("20060102_150405")
		csvPath := filepath.Join(downloadsDir, fmt.Sprintf("quran_results_%s.csv", timestamp))
		jsonPath := filepath.Join(downloadsDir, fmt.Sprintf("quran_results_%s.json", timestamp))

		// Export CSV
		csvFile, err := os.Create(csvPath)
		if err == nil {
			defer csvFile.Close()
			writer := csv.NewWriter(csvFile)
			writer.Write([]string{"السورة", "الآية", "النص", "الطبع الغالب", "الجُمّل"})
			for _, r := range resultsData {
				domAr := ""
				switch r.DominantElement {
				case "fire": domAr = "ناري"
				case "earth": domAr = "ترابي"
				case "air": domAr = "هوائي"
				case "water": domAr = "مائي"
				}
				writer.Write([]string{r.SurahName, strconv.Itoa(r.AyahNumber), r.TextTashkeel, domAr, strconv.Itoa(r.JummalEast)})
			}
			writer.Flush()
		}

		// Export JSON
		jsonFile, err := os.Create(jsonPath)
		if err == nil {
			defer jsonFile.Close()
			encoder := json.NewEncoder(jsonFile)
			encoder.SetIndent("", "  ")
			encoder.Encode(resultsData)
		}

		dialog.ShowInformation("تم التصدير", fmt.Sprintf("تم تصدير النتائج بنجاح إلى:\n%s\n%s", csvPath, jsonPath), fyne.CurrentApp().Driver().AllWindows()[0])
	})

	topContainer := container.NewVBox(input, container.NewHBox(searchBtn, exportBtn), headers)

	return container.NewBorder(
		topContainer,
		nil,
		nil,
		nil,
		list,
	)
}
