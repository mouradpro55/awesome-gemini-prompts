package ui

import (
	"strings"
	"unicode"
)

// Arabic Presentation Forms-B mapping: [isolated, final, initial, medial]
var arabicForms = map[rune][4]rune{
	'ا': {0xFE8D, 0xFE8E, 0xFE8D, 0xFE8E},
	'أ': {0xFE83, 0xFE84, 0xFE83, 0xFE84},
	'إ': {0xFE87, 0xFE88, 0xFE87, 0xFE88},
	'آ': {0xFE81, 0xFE82, 0xFE81, 0xFE82},
	'ب': {0xFE8F, 0xFE90, 0xFE91, 0xFE92},
	'ت': {0xFE95, 0xFE96, 0xFE97, 0xFE98},
	'ث': {0xFE99, 0xFE9A, 0xFE9B, 0xFE9C},
	'ج': {0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0},
	'ح': {0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4},
	'خ': {0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8},
	'د': {0xFEA9, 0xFEAA, 0xFEA9, 0xFEAA},
	'ذ': {0xFEAB, 0xFEAC, 0xFEAB, 0xFEAC},
	'ر': {0xFEAD, 0xFEAE, 0xFEAD, 0xFEAE},
	'ز': {0xFEAF, 0xFEB0, 0xFEAF, 0xFEB0},
	'س': {0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4},
	'ش': {0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8},
	'ص': {0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC},
	'ض': {0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0},
	'ط': {0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4},
	'ظ': {0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8},
	'ع': {0xFEC9, 0xFECA, 0xFECB, 0xFECC},
	'غ': {0xFECD, 0xFECE, 0xFECF, 0xFED0},
	'ف': {0xFED1, 0xFED2, 0xFED3, 0xFED4},
	'ق': {0xFED5, 0xFED6, 0xFED7, 0xFED8},
	'ك': {0xFED9, 0xFEDA, 0xFEDB, 0xFEDC},
	'ل': {0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0},
	'م': {0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4},
	'ن': {0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8},
	'ه': {0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC},
	'و': {0xFEED, 0xFEEE, 0xFEED, 0xFEEE},
	'ي': {0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4},
	'ى': {0xFEEF, 0xFEF0, 0xFEEF, 0xFEF0},
	'ة': {0xFE93, 0xFE94, 0xFE93, 0xFE94},
	'ء': {0xFE80, 0xFE80, 0xFE80, 0xFE80},
	'ئ': {0xFE89, 0xFE8A, 0xFE8B, 0xFE8C},
	'ؤ': {0xFE85, 0xFE86, 0xFE85, 0xFE86},
}

func isNonConnector(r rune) bool {
	switch r {
	case 'ا', 'أ', 'إ', 'آ', 'د', 'ذ', 'ر', 'ز', 'و', 'ؤ', 'ى':
		return true
	}
	return false
}

func isArabic(r rune) bool {
	_, ok := arabicForms[r]
	return ok
}

// ShapeArabic connects letters according to contextual position and reverses order for BiDi LTR renderers
func ShapeArabic(text string) string {
	if text == "" {
		return ""
	}

	lines := strings.Split(text, "\n")
	var reshapedLines []string

	for _, line := range lines {
		words := strings.FieldsFunc(line, func(c rune) bool {
			return unicode.IsSpace(c)
		})

		if len(words) == 0 {
			reshapedLines = append(reshapedLines, "")
			continue
		}

		var shapedWords []string
		for _, w := range words {
			runes := []rune(w)
			n := len(runes)
			shaped := make([]rune, n)

			for i := 0; i < n; i++ {
				r := runes[i]
				forms, ok := arabicForms[r]
				if !ok {
					shaped[i] = r
					continue
				}

				prevConnects := i > 0 && isArabic(runes[i-1]) && !isNonConnector(runes[i-1])
				nextConnects := i < n-1 && isArabic(runes[i+1])

				if prevConnects && nextConnects {
					shaped[i] = forms[3] // medial
				} else if prevConnects {
					shaped[i] = forms[1] // final
				} else if nextConnects {
					shaped[i] = forms[2] // initial
				} else {
					shaped[i] = forms[0] // isolated
				}
			}

			// Reverse character order inside word for RTL display
			for i, j := 0, n-1; i < j; i, j = i+1, j-1 {
				shaped[i], shaped[j] = shaped[j], shaped[i]
			}
			shapedWords = append(shapedWords, string(shaped))
		}

		// Reverse word order in the line
		for i, j := 0, len(shapedWords)-1; i < j; i, j = i+1, j-1 {
			shapedWords[i], shapedWords[j] = shapedWords[j], shapedWords[i]
		}

		// Join with space
		reshapedLines = append(reshapedLines, strings.Join(shapedWords, " "))
	}

	return strings.Join(reshapedLines, "\n")
}
