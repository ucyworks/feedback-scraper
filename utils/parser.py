"""
HTML Parser Utilities

This module provides functions for parsing HTML files and extracting review data.
"""
import re
from datetime import datetime
from typing import List, Optional
import locale
import sys
import os
from bs4 import BeautifulSoup

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from feedback_scraper.models.review import Review
from models.review import Review

# Set locale for date parsing (Turkish)
try:
    locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'tr_TR')
    except:
        print("Warning: Could not set Turkish locale. Date parsing may be incorrect.")

def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse a date string in Turkish format.
    
    Args:
        date_string: A date string like "24 Temmuz 2024"
    
    Returns:
        datetime object or None if parsing fails
    """
    try:
        # Handle Turkish month names
        months = {
            'Ocak': '01', 'Şubat': '02', 'Mart': '03', 'Nisan': '04',
            'Mayıs': '05', 'Haziran': '06', 'Temmuz': '07', 'Ağustos': '08',
            'Eylül': '09', 'Ekim': '10', 'Kasım': '11', 'Aralık': '12'
        }
        
        day, month_name, year = date_string.split()
        month = months.get(month_name, '01')
        
        return datetime.strptime(f"{day.zfill(2)}.{month}.{year}", "%d.%m.%Y")
    except Exception as e:
        print(f"Error parsing date '{date_string}': {str(e)}")
        return None

def count_stars(stars_div) -> int:
    """
    Count the number of filled stars in a rating.
    
    Args:
        stars_div: The div containing the star ratings
    
    Returns:
        An integer representing the number of stars (1-5)
    """
    count = 0
    for star in stars_div.find_all("div", class_="star-w"):
        full_div = star.find("div", class_="full")
        if full_div and full_div.get('style') and 'width: 100%' in full_div.get('style'):
            count += 1
    return count

def extract_reviews_from_html(input_source: str, is_file_path: bool = True) -> List[Review]:
    """
    Extract reviews from an HTML file or HTML content.
    
    Args:
        input_source: Path to the HTML file or HTML content string
        is_file_path: Whether input_source is a file path (True) or HTML content (False)
    
    Returns:
        A list of Review objects
    """
    # Read the HTML file or use HTML content directly
    if is_file_path:
        with open(input_source, 'r', encoding='utf-8') as file:
            html_content = file.read()
    else:
        html_content = input_source
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all review containers
    review_containers = soup.find_all("article", class_="review-card-container")
    
    reviews = []
    for container in review_containers:
        # Extract rating
        stars_div = container.find("div", class_="review-card-stars")
        rating = count_stars(stars_div) if stars_div else 0
        
        # Extract owner name
        owner_elem = container.find("p", class_="review-card-owner")
        owner = owner_elem.text.strip() if owner_elem else "Unknown"
        
        # Extract date
        date_elem = container.find("div", class_="review-card-date")
        date_str = date_elem.text.strip() if date_elem else None
        date = parse_date(date_str) if date_str else None
        
        # Extract comment
        comment_elem = container.find("span", class_="review-card-comment-text")
        comment = comment_elem.text.strip() if comment_elem else ""
        
        # Extract user info (height, weight, size)
        height = None
        weight = None
        size = None
        
        info_list = container.find("ul", class_="review-card-b-info-list")
        if info_list:
            for info_item in info_list.find_all("li", class_="review-card-b-info"):
                info_text = info_item.text.strip()
                if "Boy:" in info_text:
                    try:
                        height = int(re.search(r'Boy:\s*(\d+)', info_text).group(1))
                    except:
                        pass
                elif "Kilo:" in info_text:
                    try:
                        weight = int(re.search(r'Kilo:\s*(\d+)', info_text).group(1))
                    except:
                        pass
                elif "Beden:" in info_text:
                    size = info_text.replace("Beden:", "").strip()
        
        # Extract seller
        seller_elem = container.find("p", class_="review-card-seller")
        seller = None
        if seller_elem:
            inner_p = seller_elem.find("p")
            seller = inner_p.text.strip() if inner_p else None
        
        # Extract likes
        likes = 0
        like_span = container.find("span", class_="reviews-like-button")
        if like_span:
            likes_text = like_span.text.strip().replace('(', '').replace(')', '')
            try:
                likes = int(likes_text) if likes_text else 0
            except:
                pass
        
        # Create Review object
        review = Review(
            rating=rating,
            owner=owner,
            date=date,
            comment=comment,
            size=size,
            height=height,
            weight=weight,
            seller=seller,
            likes=likes
        )
        
        reviews.append(review)
    
    return reviews
