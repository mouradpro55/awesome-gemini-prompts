package engine

import (
	"strings"
	"unicode"
)

type CalcType int

const (
	East CalcType = iota
	West
)

func MacroValue(text string, cType CalcType) int {
	val := 0
	table := EastTable
	if cType == West {
		table = WestTable
	}

	for _, r := range []rune(text) {
		if v, ok := table[r]; ok {
			val += v
		}
	}
	return val
}

func DigitalRoot(n int) int {
	if n == 0 {
		return 0
	}
	return 1 + ((n - 1) % 9)
}

func BastExtendedValue(text string, cType CalcType) int {
	var sb strings.Builder
	for _, r := range []rune(text) {
		if !unicode.IsSpace(r) {
			if expanded, ok := BastMapping[r]; ok {
				sb.WriteString(expanded)
			}
		}
	}
	return MacroValue(sb.String(), cType)
}
