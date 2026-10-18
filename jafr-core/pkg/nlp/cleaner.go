package nlp

import (
	"regexp"
	"strings"
	"unicode"
)

var (
	tashkeelRegex  = regexp.MustCompile("[\u064B-\u0652\u0640\u0653-\u065F]")
	nonArabicRegex = regexp.MustCompile("[^\u0621-\u064A\\s]")
)

type ProcessOptions struct {
	UnifyHamzat   bool
	ExpandShaddah bool
}

func CleanAndNormalize(input string, opts ProcessOptions) string {
	var cleaned string

	if opts.ExpandShaddah {
		// Replace shaddah with the preceding character repeated
		// The shaddah character is \u0651
		// We need to iterate over runes to find shaddah and repeat the previous char
		var sb strings.Builder
		runes := []rune(input)
		for i, r := range runes {
			if r == '\u0651' {
				// Find the last actual Arabic letter before the shaddah
				// skipping any other tashkeel (vowels) that might be between the letter and shaddah
				for j := i - 1; j >= 0; j-- {
					if runes[j] >= '\u0621' && runes[j] <= '\u064A' {
						sb.WriteRune(runes[j])
						break
					}
				}
			} else {
				sb.WriteRune(r)
			}
		}
		cleaned = sb.String()
	} else {
		cleaned = input
	}

	cleaned = tashkeelRegex.ReplaceAllString(cleaned, "")
	cleaned = nonArabicRegex.ReplaceAllString(cleaned, "")

	var sb strings.Builder
	runes := []rune(cleaned)

	for _, r := range runes {
		if opts.UnifyHamzat {
			switch r {
			case 'أ', 'إ', 'آ', 'ء', 'ئ', 'ؤ':
				r = 'ا'
			case 'ة':
				r = 'ه'
			case 'ى':
				r = 'ي'
			}
		}
		if !unicode.IsSpace(r) && (r < '\u0621' || r > '\u064A') {
			continue
		}
		sb.WriteRune(r)
	}
	return strings.TrimSpace(sb.String())
}
