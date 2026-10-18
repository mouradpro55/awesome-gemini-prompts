package ui

// Contextual glyph map: [isolated, final, initial, medial]
var arabicForms = map[rune][4]rune{
	'\u0622': {0xFE81, 0xFE82, 0xFE81, 0xFE82}, // آ
	'\u0623': {0xFE83, 0xFE84, 0xFE83, 0xFE84}, // أ
	'\u0624': {0xFE85, 0xFE86, 0xFE85, 0xFE86}, // ؤ
	'\u0625': {0xFE87, 0xFE88, 0xFE87, 0xFE88}, // إ
	'\u0626': {0xFE89, 0xFE8A, 0xFE8B, 0xFE8C}, // ئ
	'\u0627': {0xFE8D, 0xFE8E, 0xFE8D, 0xFE8E}, // ا
	'\u0628': {0xFE8F, 0xFE90, 0xFE91, 0xFE92}, // ب
	'\u0629': {0xFE93, 0xFE94, 0xFE93, 0xFE94}, // ة
	'\u062A': {0xFE95, 0xFE96, 0xFE97, 0xFE98}, // ت
	'\u062B': {0xFE99, 0xFE9A, 0xFE9B, 0xFE9C}, // ث
	'\u062C': {0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0}, // ج
	'\u062D': {0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4}, // ح
	'\u062E': {0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8}, // خ
	'\u062F': {0xFEA9, 0xFEAA, 0xFEA9, 0xFEAA}, // د
	'\u0630': {0xFEAB, 0xFEAC, 0xFEAB, 0xFEAC}, // ذ
	'\u0631': {0xFEAD, 0xFEAE, 0xFEAD, 0xFEAE}, // ر
	'\u0632': {0xFEAF, 0xFEB0, 0xFEAF, 0xFEB0}, // ز
	'\u0633': {0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4}, // س
	'\u0634': {0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8}, // ش
	'\u0635': {0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC}, // ص
	'\u0636': {0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0}, // ض
	'\u0637': {0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4}, // ط
	'\u0638': {0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8}, // ظ
	'\u0639': {0xFEC9, 0xFECA, 0xFECB, 0xFECC}, // ع
	'\u063A': {0xFECD, 0xFECE, 0xFECF, 0xFED0}, // غ
	'\u0641': {0xFED1, 0xFED2, 0xFED3, 0xFED4}, // ف
	'\u0642': {0xFED5, 0xFED6, 0xFED7, 0xFED8}, // ق
	'\u0643': {0xFED9, 0xFEDA, 0xFEDB, 0xFEDC}, // ك
	'\u0644': {0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0}, // ل
	'\u0645': {0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4}, // م
	'\u0646': {0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8}, // ن
	'\u0647': {0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC}, // ه
	'\u0648': {0xFEED, 0xFEEE, 0xFEED, 0xFEEE}, // و
	'\u0649': {0xFEEF, 0xFEF0, 0xFEEF, 0xFEF0}, // ى
	'\u064A': {0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4}, // ي
	'\u0621': {0xFE80, 0xFE80, 0xFE80, 0xFE80}, // ء
}

func isNonConnector(r rune) bool {
	switch r {
	case '\u0627', '\u0622', '\u0623', '\u0625', '\u062F', '\u0630', '\u0631', '\u0632', '\u0648', '\u0624', '\u0649':
		return true
	}
	return false
}

func isArabic(r rune) bool {
	_, ok := arabicForms[r]
	return ok
}

// ShapeArabic contextually connects Arabic glyphs without reversing text
func ShapeArabic(text string) string {
	if text == "" {
		return ""
	}

	runes := []rune(text)
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

	return string(shaped)
}
