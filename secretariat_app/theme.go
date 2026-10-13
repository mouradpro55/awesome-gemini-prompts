package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/theme"
	"image/color"
)

type customTheme struct{}

func (c customTheme) Color(n fyne.ThemeColorName, v fyne.ThemeVariant) color.Color {
	return theme.DefaultTheme().Color(n, v)
}

func (c customTheme) Icon(n fyne.ThemeIconName) fyne.Resource {
	return theme.DefaultTheme().Icon(n)
}

var cachedFont fyne.Resource

func (c customTheme) Font(s fyne.TextStyle) fyne.Resource {
	// تحميل الخط العربي مرة واحدة فقط لتجنب استهلاك الموارد بشكل مفرط (I/O exhaustion)
	if cachedFont == nil {
		fontData, err := fyne.LoadResourceFromPath("Amiri-Regular.ttf")
		if err == nil {
			cachedFont = fontData
		} else {
			return theme.DefaultTheme().Font(s)
		}
	}
	return cachedFont
}

func (c customTheme) Size(n fyne.ThemeSizeName) float32 {
	return theme.DefaultTheme().Size(n)
}
