package ui

import (
	_ "embed"
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/theme"
)

//go:embed assets/fonts/Cairo-Regular.ttf
var arabicFontRegular []byte

//go:embed assets/fonts/Cairo-Bold.ttf
var arabicFontBold []byte

type JafrTheme struct{}

func (m JafrTheme) Font(style fyne.TextStyle) fyne.Resource {
	if style.Bold {
		return &fyne.StaticResource{
			StaticName:    "Cairo-Bold.ttf",
			StaticContent: arabicFontBold,
		}
	}
	return &fyne.StaticResource{
		StaticName:    "Cairo-Regular.ttf",
		StaticContent: arabicFontRegular,
	}
}

// Modern Dark Palette
func (m JafrTheme) Color(name fyne.ThemeColorName, variant fyne.ThemeVariant) color.Color {
	switch name {
	case theme.ColorNameBackground:
		return color.NRGBA{R: 13, G: 15, B: 24, A: 255} // #0D0F18
	case theme.ColorNameInputBackground:
		return color.NRGBA{R: 22, G: 27, B: 46, A: 220}
	case theme.ColorNamePrimary:
		return color.NRGBA{R: 255, G: 184, B: 0, A: 255} // #FFB800
	case theme.ColorNameForeground:
		return color.NRGBA{R: 240, G: 243, B: 246, A: 255}
	case theme.ColorNameSeparator:
		return color.NRGBA{R: 38, G: 45, B: 71, A: 255}
	default:
		return theme.DefaultTheme().Color(name, theme.VariantDark)
	}
}

func (m JafrTheme) Icon(name fyne.ThemeIconName) fyne.Resource {
	return theme.DefaultTheme().Icon(name)
}

func (m JafrTheme) Size(name fyne.ThemeSizeName) float32 {
	switch name {
	case theme.SizeNameText:
		return 18.0 // Increased from 14.0 for crystal clear Arabic readability
	case theme.SizeNameHeadingText:
		return 24.0 // Prominent section titles
	case theme.SizeNameSubHeadingText:
		return 20.0
	case theme.SizeNameCaptionText:
		return 15.0
	case theme.SizeNamePadding:
		return 8.0
	default:
		return theme.DefaultTheme().Size(name)
	}
}
