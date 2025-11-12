# OLX Web Scraper - Car Cover Search

## 📌 Task

Scrape OLX search results for "Car Cover" and extract:

- Title of the ad
- Description
- Price

Display the results in table format.

## 🎯 Approach & Solution

### Problem Analysis

When scraping OLX, there were multiple approaches to consider:

1. **BeautifulSoup (HTML Parsing)** ❌

   - OLX uses lazy loading/infinite scroll
   - Would only extract ~40 results (initial HTML document)
   - Misses dynamically loaded content

2. **Selenium (Browser Automation)** ⚠️

   - Would work but introduces unnecessary complexity
   - Requires browser driver setup
   - Slower execution
   - Overkill for this task

3. **API Reverse Engineering** ✅ **[CHOSEN APPROACH]**
   - Inspected network requests from OLX frontend
   - Identified the internal API endpoint: `/api/relevance/v4/search`
   - Mimics browser behavior by setting proper headers
   - Direct JSON response - no HTML parsing needed
   - Can fetch all pages of results
   - Fast and efficient

### Why This Approach?

By reverse engineering the API that the OLX frontend uses, we can:

- Get structured JSON data directly
- Avoid HTML parsing complexity
- Handle pagination easily
- Fetch all search results (not just initial 40)
- More reliable and maintainable solution

## 📊 Features

- ✅ Fetches all pages of search results automatically
- ✅ Extracts title, description, price, location, and URL
- ✅ Handles pagination with proper rate limiting (1.5s delay)
- ✅ Error handling for network issues and API changes
- ✅ Exports results to CSV format
- ✅ Clean table output using `tabulate`

## 🔧 Technical Details

**API Endpoint:** `https://www.olx.in/api/relevance/v4/search`

**Headers Used:**

- User-Agent (mimics browser)
- Accept (JSON)
- Referer (OLX search page)
- Origin (OLX domain)

**Rate Limiting:** 1.5 seconds between requests to avoid blocking
