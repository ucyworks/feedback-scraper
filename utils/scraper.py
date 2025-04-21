"""
Web Scraper Utilities

This module provides functions for scraping web content from URLs.
"""
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# User agent list to rotate and avoid detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
]

def get_random_user_agent():
    """Get a random user agent from the list."""
    return random.choice(USER_AGENTS)

def fetch_html_from_url(url, max_retries=3, delay=2):
    """
    Fetch HTML content from a URL.
    
    Args:
        url: The URL to fetch content from
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    
    Returns:
        HTML content as string or None if failed
    """
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # If successful, return the HTML content
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Request failed (attempt {retries + 1}/{max_retries}): {str(e)}")
            retries += 1
            
            if retries < max_retries:
                # Add jitter to delay to avoid detection
                jitter = random.uniform(0.5, 1.5)
                sleep_time = delay * jitter
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
    
    return None

def extract_product_id_from_trendyol_url(url):
    """
    Extract the product ID from a Trendyol product URL.
    
    Args:
        url: Trendyol product URL
    
    Returns:
        Product ID as string or None if not found
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        
        # Extract the product ID from the path
        path_parts = parsed_url.path.split('-p-')
        if len(path_parts) > 1:
            product_id = path_parts[1]
            return product_id
        
        # If not found in path, check query parameters
        query_params = parse_qs(parsed_url.query)
        if 'boutiqueId' in query_params:
            return query_params['boutiqueId'][0]
        
        return None
    except Exception as e:
        print(f"Error extracting product ID: {str(e)}")
        return None

def fetch_trendyol_reviews(product_id, page=1):
    """
    Fetch reviews for a Trendyol product.
    
    Args:
        product_id: The product ID
        page: The page number of reviews to fetch
    
    Returns:
        HTML content containing reviews
    """
    # Construct API URL for reviews
    api_url = f"https://public-mdc.trendyol.com/discovery-web-socialgw-service/api/review/{product_id}?page={page}"
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'application/json',
        'Referer': f'https://www.trendyol.com/product-p-{product_id}',
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Return JSON data
        return response.json()
    except Exception as e:
        print(f"Error fetching Trendyol reviews: {str(e)}")
        return None
