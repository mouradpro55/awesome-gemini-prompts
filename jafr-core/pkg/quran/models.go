package quran

type Surah struct {
	ID         int
	Name       string
	TotalAyahs int
}

type Ayah struct {
	ID              int
	SurahID         int
	AyahNumber      int
	TextTashkeel    string
	CleanText       string
	JummalEast      int
	JummalWest      int
	JummalSaghir    int
	DominantElement string
	FireCount       int
	EarthCount      int
	AirCount        int
	WaterCount      int
}

type AyahSearchResult struct {
	SurahName       string
	AyahNumber      int
	TextTashkeel    string
	JummalEast      int
	DominantElement string
}
