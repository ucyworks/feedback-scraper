#!/usr/bin/env python
"""
Customer Review Scraper

This script extracts customer reviews from HTML files containing product feedback.
"""
import os
import sys
import argparse
from datetime import datetime

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feedback_scraper.models.review import Review
from feedback_scraper.utils.parser import extract_reviews_from_html
from feedback_scraper.utils.exporter import export_reviews_to_json, export_reviews_to_csv, export_reviews_to_excel

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Scrape customer reviews from HTML files')
    parser.add_argument('--input', '-i', type=str, default='feedback.html',
                        help='Path to HTML file containing reviews (default: feedback.html)')
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
    print(f"Processing {args.input}...")
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found")
        sys.exit(1)
    
    # Extract reviews from HTML
    try:
        reviews = extract_reviews_from_html(args.input)
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
