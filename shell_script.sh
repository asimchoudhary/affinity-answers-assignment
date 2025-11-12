#!/bin/bash

INPUT_URL="https://portal.amfiindia.com/spages/NAVAll.txt"
OUTPUT_FILE="nav_data.tsv"

# Download the NAV data using the provided URL and save to a temporary file
curl -L -s "$INPUT_URL" -o nav_input.txt

# Check if download was successful
if [ ! -s nav_input.txt ]; then
    echo "Error: Failed to download NAV data"
    exit 1
fi

# Main extraction logic using awk
awk -F';' '
BEGIN {
    # OFS = Output Field Separator (tab character)
    OFS="\t"
    # Print header
    print "Scheme Name", "Net Asset Value"
}
NF == 6 && $5 ~ /^[0-9]+\.[0-9]+$/ {
    # NF == 6: Only process lines with exactly 6 fields
    # $5 ~ /^[0-9]+\.[0-9]+$/: Ensure field 5 is a valid number
    print $4, $5
}
' nav_input.txt > "$OUTPUT_FILE"

echo "Data extracted successfully to $OUTPUT_FILE"
echo "Total records extracted: $(tail -n +2 $OUTPUT_FILE | wc -l)"