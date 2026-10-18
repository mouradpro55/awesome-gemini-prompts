package quran

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"

	"jafr-core/pkg/engine"
	"jafr-core/pkg/nlp"
)

var (
	surahRegex = regexp.MustCompile(`^\*2\*\s+(\d+)\s+([^{]+)\s+{(\d+)}$`)
	ayahRegex  = regexp.MustCompile(`^([^\{]+)\{(\d+)\}$`)
)

func ParseAndIngestQuran(filePath string, repo *Repository) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var currentSurahID int
	var ayahsBatch []Ayah
	batchSize := 1000

	ctx := context.Background()

	for scanner.Scan() {
		line := scanner.Text()
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}

		// Check for surah header
		if strings.HasPrefix(line, "*2*") {
			matches := surahRegex.FindStringSubmatch(line)
			if len(matches) == 4 {
				surahID, _ := strconv.Atoi(matches[1])
				surahName := strings.TrimSpace(matches[2])
				totalAyahs, _ := strconv.Atoi(matches[3])

				currentSurahID = surahID
				repo.InsertSurah(ctx, Surah{
					ID:         surahID,
					Name:       surahName,
					TotalAyahs: totalAyahs,
				})
			}
			continue
		}

		// It's an ayah line
		// Remove leading '@' if present
		line = strings.TrimPrefix(line, "@")
		line = strings.TrimSpace(line)

		matches := ayahRegex.FindStringSubmatch(line)
		if len(matches) == 3 {
			ayahTextTashkeel := strings.TrimSpace(matches[1])
			ayahNumber, _ := strconv.Atoi(matches[2])

			opts := nlp.ProcessOptions{UnifyHamzat: true, ExpandShaddah: false}
			cleanText := nlp.CleanAndNormalize(ayahTextTashkeel, opts)

			jummalEast := engine.MacroValue(cleanText, engine.East)
			jummalWest := engine.MacroValue(cleanText, engine.West)
			jummalSaghir := engine.DigitalRoot(jummalEast) // Using East for saghir as default

			elemCounts, dominant := engine.CalculateElements(cleanText)

			ayah := Ayah{
				SurahID:         currentSurahID,
				AyahNumber:      ayahNumber,
				TextTashkeel:    ayahTextTashkeel,
				CleanText:       cleanText,
				JummalEast:      jummalEast,
				JummalWest:      jummalWest,
				JummalSaghir:    jummalSaghir,
				DominantElement: dominant,
				FireCount:       elemCounts.Fire,
				EarthCount:      elemCounts.Earth,
				AirCount:        elemCounts.Air,
				WaterCount:      elemCounts.Water,
			}

			ayahsBatch = append(ayahsBatch, ayah)

			if len(ayahsBatch) >= batchSize {
				if err := repo.InsertAyahs(ctx, ayahsBatch); err != nil {
					return fmt.Errorf("failed to insert batch: %w", err)
				}
				ayahsBatch = ayahsBatch[:0]
			}
		}
	}

	if err := scanner.Err(); err != nil {
		return err
	}

	// Insert remaining ayahs
	if len(ayahsBatch) > 0 {
		if err := repo.InsertAyahs(ctx, ayahsBatch); err != nil {
			return fmt.Errorf("failed to insert final batch: %w", err)
		}
	}

	return nil
}
