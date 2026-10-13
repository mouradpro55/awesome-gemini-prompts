package main

import (
	"os"
	"strings"
	"testing"
)

func TestGeneratePDF(t *testing.T) {
	ref := "123/2023"
	err := GeneratePDF(ref, "2023/10/25", "المدير العام", "طلب عطلة", "أرجو من سيادتكم الموافقة على طلب العطلة الخاصة بي.")
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	fileName := "correspondence_" + strings.ReplaceAll(ref, "/", "-") + ".pdf"
	if _, err := os.Stat(fileName); os.IsNotExist(err) {
		t.Fatalf("Expected file %s to be created, but it was not.", fileName)
	}

	// Clean up after test
	os.Remove(fileName)
}
