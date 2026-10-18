package main

import (
	"fmt"
	"log"
	"os"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"

	"jafr-core/pkg/quran"
	"jafr-core/pkg/ui"
)

func main() {
	// Setup DB Path
	dbPath := "jafr_quran.db"
	repo, err := quran.NewRepository(dbPath)
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}
	defer repo.Close()

	// Ingest Quran data if empty
	isEmpty, err := repo.IsDBEmpty()
	if err != nil {
		log.Fatalf("Failed to check if DB is empty: %v", err)
	}

	if isEmpty {
		fmt.Println("Initializing database from ARQURAN.TXT...")
		quranDataPath := "assets/data/ARQURAN.TXT"
		if _, err := os.Stat(quranDataPath); err == nil {
			err = quran.ParseAndIngestQuran(quranDataPath, repo)
			if err != nil {
				log.Printf("Failed to ingest Quran data: %v", err)
			} else {
				fmt.Println("Quran data ingested successfully.")
			}
		} else {
			fmt.Printf("ARQURAN.TXT not found at %s. Quran DB will be empty.\n", quranDataPath)
		}
	}

	a := app.New()
	a.Settings().SetTheme(&ui.JafrTheme{})

	w := a.NewWindow("محرك حساب الجفر والتحليل القرآني - JafrCore Engine")
	w.Resize(fyne.NewSize(800, 600))

	tabs := container.NewAppTabs(
		container.NewTabItem("حاسبة النصوص", ui.CreateFreeTextTab()),
		container.NewTabItem("ميزان الطبائع", ui.CreateElementsTab()),
		container.NewTabItem("البحث القرآني العكسي", ui.CreateQuranTab(repo)),
	)

	w.SetContent(tabs)
	w.ShowAndRun()
}
