#!/usr/bin/env python
"""
Customer Review Scraper

This script extracts customer reviews from HTML files or URLs containing product feedback.
"""
import os
import sys
import argparse
from datetime import datetime

# Fix the import paths by adjusting the directory structure
# Instead of using feedback_scraper, use relative imports since we're inside the feedback-scraper directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.review import Review
from utils.parser import extract_reviews_from_html
from utils.scraper import fetch_html_from_url
from utils.exporter import export_reviews_to_json, export_reviews_to_csv, export_reviews_to_excel

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Scrape customer reviews from HTML files or URLs')
    source_group = parser.add_mutually_exclusive_group(required=False)
    source_group.add_argument('--input', '-i', type=str, default='feedback.html',
                        help='Path to HTML file containing reviews (default: feedback.html)')
    source_group.add_argument('--url', '-u', type=str,
                        help='URL to scrape reviews from (e.g., Trendyol product page)')
    parser.add_argument('--output', '-o', type=str, default='reviews',
                        help='Output filename without extension (default: reviews)')
    parser.add_argument('--format', '-f', type=str, choices=['json', 'csv', 'excel', 'all'], default='json',
                        help='Output format (default: json)')
    return parser.parse_args()

def main():
    """Main function to run the scraper."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Print start message
    print(f"Starting review scraper at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    html_content = None
    
    # Handle URL or file input
    if args.url:
        print(f"Fetching reviews from URL: {args.url}")
        try:
            html_content = fetch_html_from_url(args.url)
            if not html_content:
                print("Error: Could not fetch content from URL")
                sys.exit(1)
        except Exception as e:
            print(f"Error fetching URL: {str(e)}")
            sys.exit(1)
    else:
        print(f"Processing local file: {args.input}")
        # Check if input file exists
        if not os.path.exists(args.input):
            print(f"Error: Input file {args.input} not found")
            sys.exit(1)
            
        # Read the input file
        try:
            with open(args.input, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except Exception as e:
            print(f"Error reading input file: {str(e)}")
            sys.exit(1)
    
    # Extract reviews from HTML
    try:
        reviews = extract_reviews_from_html(html_content, is_file_path=False)
        print(f"Found {len(reviews)} reviews")
    except Exception as e:
        print(f"Error extracting reviews: {str(e)}")
        sys.exit(1)
    
    # Export reviews in the specified format
    try:
        if args.format == 'json' or args.format == 'all':
            output_file = export_reviews_to_json(reviews, f"{args.output}.json")
            print(f"Exported reviews to {output_file}")
        
        if args.format == 'csv' or args.format == 'all':
            output_file = export_reviews_to_csv(reviews, f"{args.output}.csv")
            print(f"Exported reviews to {output_file}")
        
        if args.format == 'excel' or args.format == 'all':
            output_file = export_reviews_to_excel(reviews, f"{args.output}.xlsx")
            print(f"Exported reviews to {output_file}")
    except Exception as e:
        print(f"Error exporting reviews: {str(e)}")
        sys.exit(1)
    
    print(f"Review scraping completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
