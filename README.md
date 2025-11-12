# Affinity Answers Assignment

This repository contains solutions to three technical assignment questions covering web scraping, database queries, and shell scripting.

## 📋 Table of Contents

- [Overview](#overview)
- [Setup Instructions](#setup-instructions)
- [Question 1: OLX Web Scraper](#question-1-olx-web-scraper)
- [Question 2: Database Queries](#question-2-database-queries)
- [Question 3: Shell Script](#question-3-shell-script)
- [Requirements](#requirements)

---

## Overview

This project contains solutions to the following questions:

1. **OLX Web Scraper** - Extract search results (title, description, price) for "Car Cover" from OLX
2. **Database Queries** - SQL queries on the Rfam public database (tigers taxonomy, rice DNA sequences, pagination)
3. **Shell Script** - Extract Scheme Name and Asset Value from AMFI India NAV data

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/asimchoudhary/affinity-answers-assignment.git
cd affinity-answers-assignment
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

**On Linux/macOS:**

```bash
source .venv/bin/activate
```

**On Windows:**

```bash
.venv\Scripts\activate
```

### 4. Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## Question 1: OLX Web Scraper

**Objective:** Scrape search results for "Car Cover" from OLX and display title, description, and price in table format.

### Running the Script

```bash
cd q1.Scrap-olx
python olx_scrapy.py
```

### Output

- Displays results in a formatted table in the terminal
- Saves results to `olx_car cover_results.csv`

### Features

- Fetches all pages of search results
- Extracts title, description, price, location, and URL
- Handles pagination automatically
- Rate limiting to avoid blocking
- Exports to CSV format

---

## Question 2: Database Queries

**Objective:** Query the Rfam public database to answer questions about taxonomy, table relationships, and DNA sequences.

### Running the Script

```bash
cd q2.Db-queries
python db_queries.py
```

### Questions Answered

**a) Tiger Taxonomy:**

- Count of tiger types in the taxonomy table
- NCBI ID of Sumatran Tiger (Panthera tigris sumatrae)

**b) Table Relationships:**

- Lists all foreign key columns that connect tables in the database

**c) Rice DNA Sequence:**

- Identifies the type of rice (Oryza) with the longest DNA sequence

**d) Pagination Query:**

- Returns page 9 (15 results per page) of family names with DNA sequences > 1,000,000 bp
- Results sorted by length in descending order

### Database Connection Details

- **Host:** mysql-rfam-public.ebi.ac.uk
- **Port:** 4497
- **User:** rfamro
- **Database:** Rfam

---

## Question 3: Shell Script

**Objective:** Extract Scheme Name and Net Asset Value from AMFI India NAV data and save as TSV.

### Running the Script

```bash
cd q3.Shell-script
chmod +x shell_script.sh
./shell_script.sh
```

### Output

- Creates `nav_data.tsv` with scheme names and asset values
- Tab-separated format
- Displays total records extracted

### Features

- Downloads latest NAV data from AMFI India
- Filters valid records (6 fields with numeric NAV values)
- Extracts only Scheme Name and Net Asset Value
- Outputs in TSV format for easy data processing

---

## Project Structure

```
affinity-answers-assignment/
├── README.md
├── requirements.txt
├── q1.Scrap-olx/
│   ├── olx_scrapy.py
│   └── olx_car cover_results.csv (generated)
├── q2.Db-queries/
│   └── db_queries.py
└── q3.Shell-script/
    ├── shell_script.sh
    ├── nav_data.tsv (generated)
    └── nav_input.txt (temporary file)
```

---

## Notes

- **Question 3:** The shell script downloads the latest NAV data each time it runs.

---

## Author

**Asim Choudhary**  
GitHub: [@asimchoudhary](https://github.com/asimchoudhary)

---

## License

This project is for assignment purposes.
