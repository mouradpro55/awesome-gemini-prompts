package main

import (
	"flag"
	"fmt"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/fatih/color"
)

// Scanner struct holds the configuration and state of our scanner
type Scanner struct {
	BaseURL        string
	Domain         string
	Visited        map[string]bool
	VisitedMu      sync.Mutex
	Client         *http.Client
	MaxDepth       int
	Concurrency    int
	Vulnerabilities []Vulnerability
	VulnMu         sync.Mutex
}

// NewScanner creates a new instance of the Scanner
func NewScanner(targetURL string, maxDepth, concurrency int) (*Scanner, error) {
	u, err := url.Parse(targetURL)
	if err != nil {
		return nil, err
	}

	return &Scanner{
		BaseURL: targetURL,
		Domain:  u.Hostname(),
		Visited: make(map[string]bool),
		Client: &http.Client{
			Timeout: 10 * time.Second, // Timeout for requests
		},
		MaxDepth:        maxDepth,
		Concurrency:     concurrency,
		Vulnerabilities: make([]Vulnerability, 0),
	}, nil
}

// Crawl starts the scanning process from the base URL
func (s *Scanner) Crawl() {
	color.Cyan("[*] Starting crawler and scanner on %s", s.BaseURL)

	urlsToScan := make(chan string, 1000)
	vulnResults := make(chan Vulnerability, 100)
	var wg sync.WaitGroup

	// Goroutine to collect vulnerabilities
	go func() {
		for vuln := range vulnResults {
			s.VulnMu.Lock()
			s.Vulnerabilities = append(s.Vulnerabilities, vuln)
			s.VulnMu.Unlock()
			color.Red("[!] VULNERABILITY FOUND: [%s] %s", vuln.Type, vuln.URL)
		}
	}()

	// Start worker pool
	for i := 0; i < s.Concurrency; i++ {
		wg.Add(1)
		go s.worker(urlsToScan, &wg, vulnResults)
	}

	// Send the initial URL to start
	urlsToScan <- s.BaseURL

	time.Sleep(5 * time.Second) // Increased sleep to allow modules to run
	close(urlsToScan)
	wg.Wait()
	close(vulnResults)

	color.Green("\n[*] Scanning finished. Found %d unique URLs and %d vulnerabilities.", len(s.Visited), len(s.Vulnerabilities))

	// Export results after scanning
	ExportResults(s)
}

func (s *Scanner) worker(urls <-chan string, wg *sync.WaitGroup, results chan Vulnerability) {
	defer wg.Done()
	for currentURL := range urls {
		s.VisitedMu.Lock()
		if s.Visited[currentURL] {
			s.VisitedMu.Unlock()
			continue
		}
		s.Visited[currentURL] = true
		s.VisitedMu.Unlock()

		color.HiYellow("[Crawler] Scanning: %s", currentURL)

		// Run vulnerability checks on the discovered URL
		RunModules(currentURL, s.Client, results)

		newURLs, err := s.extractURLs(currentURL)
		if err != nil {
			continue
		}

		// Basic mechanism to queue new URLs (without depth tracking yet for simplicity)
		for _, u := range newURLs {
			s.VisitedMu.Lock()
			if !s.Visited[u] {
				s.Visited[u] = true
				// For now, we collect them without re-pushing to avoid infinite loop
			}
			s.VisitedMu.Unlock()
		}
	}
}

// extractURLs fetches the page and extracts all links
func (s *Scanner) extractURLs(pageURL string) ([]string, error) {
	resp, err := s.Client.Get(pageURL)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("bad status: %d", resp.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil, err
	}

	var foundURLs []string
	doc.Find("a").Each(func(i int, selection *goquery.Selection) {
		href, exists := selection.Attr("href")
		if exists {
			absoluteURL := s.resolveURL(pageURL, href)
			if absoluteURL != "" && s.isSameDomain(absoluteURL) {
				foundURLs = append(foundURLs, absoluteURL)
			}
		}
	})

	return foundURLs, nil
}

// resolveURL converts relative URLs to absolute URLs
func (s *Scanner) resolveURL(base, href string) string {
	baseURL, err := url.Parse(base)
	if err != nil {
		return ""
	}
	hrefURL, err := url.Parse(href)
	if err != nil {
		return ""
	}

	// Ignore mailto, javascript, etc.
	if hrefURL.Scheme != "" && hrefURL.Scheme != "http" && hrefURL.Scheme != "https" {
		return ""
	}

	resolvedURL := baseURL.ResolveReference(hrefURL)

	// Remove fragments (e.g., #section) to avoid duplicate crawling
	resolvedURL.Fragment = ""

	return resolvedURL.String()
}

// isSameDomain ensures we don't crawl out of the target domain
func (s *Scanner) isSameDomain(link string) bool {
	u, err := url.Parse(link)
	if err != nil {
		return false
	}
	// Simple check, can be improved for subdomains
	return strings.HasSuffix(u.Hostname(), s.Domain)
}

func main() {
	var target string
	flag.StringVar(&target, "u", "http://example.com", "Target URL to scan")
	flag.Parse()

	fmt.Println("=======================================")
	color.HiMagenta("    Go Scanner - Web Vulnerability Engine")
	fmt.Println("=======================================")

	scanner, err := NewScanner(target, 2, 5)
	if err != nil {
		color.Red("[-] Error initializing scanner: %v", err)
		return
	}

	scanner.Crawl()
}
