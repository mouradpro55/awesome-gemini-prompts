package quran

import (
	"context"
	"database/sql"

	_ "modernc.org/sqlite"
)

type Repository struct {
	db *sql.DB
}

func NewRepository(dbPath string) (*Repository, error) {
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, err
	}

	// Optimize SQLite speed for bulk ingestion
	_, _ = db.Exec("PRAGMA synchronous = OFF;")
	_, _ = db.Exec("PRAGMA journal_mode = MEMORY;")
	_, _ = db.Exec("PRAGMA temp_store = MEMORY;")
	_, _ = db.Exec("PRAGMA cache_size = -64000;") // 64MB cache

	repo := &Repository{db: db}
	if err := repo.InitSchema(); err != nil {
		return nil, err
	}

	return repo, nil
}

func (r *Repository) InitSchema() error {
	schema := `
	CREATE TABLE IF NOT EXISTS surahs (
		id INTEGER PRIMARY KEY,
		name TEXT NOT NULL,
		total_ayahs INTEGER NOT NULL
	);

	CREATE TABLE IF NOT EXISTS ayahs (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		surah_id INTEGER NOT NULL,
		ayah_number INTEGER NOT NULL,
		text_tashkeel TEXT NOT NULL,
		clean_text TEXT NOT NULL,
		jummal_east INTEGER NOT NULL,
		jummal_west INTEGER NOT NULL,
		jummal_saghir INTEGER NOT NULL,
		dominant_element TEXT NOT NULL,
		fire_count INTEGER NOT NULL,
		earth_count INTEGER NOT NULL,
		air_count INTEGER NOT NULL,
		water_count INTEGER NOT NULL,
		FOREIGN KEY(surah_id) REFERENCES surahs(id)
	);

	CREATE INDEX IF NOT EXISTS idx_ayahs_jummal_east ON ayahs(jummal_east);
	CREATE INDEX IF NOT EXISTS idx_ayahs_jummal_west ON ayahs(jummal_west);
	CREATE INDEX IF NOT EXISTS idx_ayahs_surah_num ON ayahs(surah_id, ayah_number);
	`
	_, err := r.db.Exec(schema)
	return err
}

func (r *Repository) InsertSurah(ctx context.Context, s Surah) error {
	_, err := r.db.ExecContext(ctx, "INSERT OR IGNORE INTO surahs (id, name, total_ayahs) VALUES (?, ?, ?)", s.ID, s.Name, s.TotalAyahs)
	return err
}

func (r *Repository) InsertAyahs(ctx context.Context, ayahs []Ayah) error {
	tx, err := r.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	stmt, err := tx.PrepareContext(ctx, `INSERT INTO ayahs (
		surah_id, ayah_number, text_tashkeel, clean_text,
		jummal_east, jummal_west, jummal_saghir,
		dominant_element, fire_count, earth_count, air_count, water_count
	) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
	if err != nil {
		return err
	}
	defer stmt.Close()

	for _, a := range ayahs {
		_, err := stmt.ExecContext(ctx,
			a.SurahID, a.AyahNumber, a.TextTashkeel, a.CleanText,
			a.JummalEast, a.JummalWest, a.JummalSaghir,
			a.DominantElement, a.FireCount, a.EarthCount, a.AirCount, a.WaterCount,
		)
		if err != nil {
			return err
		}
	}

	return tx.Commit()
}

func (r *Repository) SearchByJummalEast(jummal int) ([]AyahSearchResult, error) {
	rows, err := r.db.Query(`
		SELECT s.name, a.ayah_number, a.text_tashkeel, a.jummal_east, a.dominant_element
		FROM ayahs a
		JOIN surahs s ON a.surah_id = s.id
		WHERE a.jummal_east = ?;
	`, jummal)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []AyahSearchResult
	for rows.Next() {
		var res AyahSearchResult
		if err := rows.Scan(&res.SurahName, &res.AyahNumber, &res.TextTashkeel, &res.JummalEast, &res.DominantElement); err != nil {
			return nil, err
		}
		results = append(results, res)
	}
	return results, nil
}

func (r *Repository) IsDBEmpty() (bool, error) {
	var count int
	err := r.db.QueryRow("SELECT COUNT(*) FROM ayahs").Scan(&count)
	if err != nil {
		return true, err
	}
	return count == 0, nil
}

func (r *Repository) Close() error {
	return r.db.Close()
}
