package engine

import "unicode"

type ElementCounts struct {
	Fire  int
	Earth int
	Air   int
	Water int
}

var ElementsMap = map[rune]string{
	'ا': "fire", 'ه': "fire", 'ط': "fire", 'م': "fire", 'ف': "fire", 'ش': "fire", 'ذ': "fire",
	'ب': "earth", 'و': "earth", 'ي': "earth", 'ن': "earth", 'ص': "earth", 'ت': "earth", 'ض': "earth",
	'ج': "air", 'ز': "air", 'ك': "air", 'س': "air", 'ق': "air", 'ث': "air", 'ظ': "air",
	'د': "water", 'ح': "water", 'ل': "water", 'ع': "water", 'ر': "water", 'خ': "water", 'غ': "water",
}

func CalculateElements(text string) (ElementCounts, string) {
	counts := ElementCounts{}
	for _, r := range []rune(text) {
		if !unicode.IsSpace(r) {
			if elem, ok := ElementsMap[r]; ok {
				switch elem {
				case "fire":
					counts.Fire++
				case "earth":
					counts.Earth++
				case "air":
					counts.Air++
				case "water":
					counts.Water++
				}
			}
		}
	}

	dominant := "fire"
	maxVal := counts.Fire

	if counts.Earth > maxVal {
		maxVal = counts.Earth
		dominant = "earth"
	}
	if counts.Air > maxVal {
		maxVal = counts.Air
		dominant = "air"
	}
	if counts.Water > maxVal {
		maxVal = counts.Water
		dominant = "water"
	}

	// Tie breaker: standard order (fire, earth, air, water)

	return counts, dominant
}
