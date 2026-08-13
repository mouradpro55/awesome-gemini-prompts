package main

import (
	"encoding/json"
	"os"
	"strings"
	"text/template"
	"time"

	"github.com/fatih/color"
)

// ReportData holds the data to be injected into the report template
type ReportData struct {
	TargetURL       string
	ScanTime        string
	TotalURLs       int
	TotalVulns      int
	Vulnerabilities []Vulnerability
}

// GenerateJSONReport saves the vulnerabilities to a JSON file
func GenerateJSONReport(data ReportData, filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(data)
}

// GenerateHTMLReport creates a simple HTML report
func GenerateHTMLReport(data ReportData, filename string) error {
	htmlTemplate := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vulnerability Scan Report - {{.TargetURL}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
        h1, h2 { color: #2c3e50; }
        .summary { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .summary p { margin: 5px 0; font-size: 16px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #2c3e50; color: white; }
        tr:hover { background-color: #f1f1f1; }
        .severity-high { color: #e74c3c; font-weight: bold; }
        .severity-medium { color: #f39c12; font-weight: bold; }
        .severity-low { color: #3498db; font-weight: bold; }
    </style>
</head>
<body>

    <h1>Vulnerability Scan Report</h1>

    <div class="summary">
        <h2>Scan Summary</h2>
        <p><strong>Target:</strong> {{.TargetURL}}</p>
        <p><strong>Scan Time:</strong> {{.ScanTime}}</p>
        <p><strong>URLs Scanned:</strong> {{.TotalURLs}}</p>
        <p><strong>Vulnerabilities Found:</strong> {{.TotalVulns}}</p>
    </div>

    <h2>Details</h2>
    {{if eq .TotalVulns 0}}
        <p>No vulnerabilities found.</p>
    {{else}}
        <table>
            <thead>
                <tr>
                    <th>Type</th>
                    <th>URL</th>
                    <th>Severity</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {{range .Vulnerabilities}}
                <tr>
                    <td>{{.Type}}</td>
                    <td><a href="{{.URL}}" target="_blank">{{.URL}}</a></td>
                    <td class="severity-{{.Severity | ToLower}}">{{.Severity}}</td>
                    <td>{{.Details}}</td>
                </tr>
                {{end}}
            </tbody>
        </table>
    {{end}}

</body>
</html>
`

	// Register a custom function to help with CSS classes based on severity
	funcMap := template.FuncMap{
		"ToLower": func(s string) string {
			// Extract just the severity word, handle cases like "Low/Medium"
			lower := strings.ToLower(s)
			if strings.Contains(lower, "high") { return "high" }
			if strings.Contains(lower, "medium") { return "medium" }
			return "low"
		},
	}

	tmpl, err := template.New("report").Funcs(funcMap).Parse(htmlTemplate)
	if err != nil {
		return err
	}

	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	return tmpl.Execute(file, data)
}

// ExportResults handles generating requested reports
func ExportResults(scanner *Scanner) {
	if len(scanner.Vulnerabilities) == 0 {
		color.Cyan("[*] No vulnerabilities found to report.")
		return
	}

	data := ReportData{
		TargetURL:       scanner.BaseURL,
		ScanTime:        time.Now().Format(time.RFC1123),
		TotalURLs:       len(scanner.Visited),
		TotalVulns:      len(scanner.Vulnerabilities),
		Vulnerabilities: scanner.Vulnerabilities,
	}

	jsonFilename := "report.json"
	htmlFilename := "report.html"

	color.Cyan("\n[*] Generating reports...")

	if err := GenerateJSONReport(data, jsonFilename); err != nil {
		color.Red("[-] Error generating JSON report: %v", err)
	} else {
		color.Green("[+] JSON report saved to %s", jsonFilename)
	}

	if err := GenerateHTMLReport(data, htmlFilename); err != nil {
		color.Red("[-] Error generating HTML report: %v", err)
	} else {
		color.Green("[+] HTML report saved to %s", htmlFilename)
	}
}
