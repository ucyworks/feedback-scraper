"""
Exporter Utilities

This module provides functions for exporting reviews to various formats.
"""
import os
import json
import csv
from typing import List

from models.review import Review

def ensure_directory_exists(file_path: str) -> None:
    """
    Ensure that the directory for the given file path exists.
    
    Args:
        file_path: Path to the file
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def export_reviews_to_json(reviews: List[Review], output_file: str) -> str:
    """
    Export reviews to a JSON file.
    
    Args:
        reviews: List of Review objects
        output_file: Path to the output file
    
    Returns:
        Path to the created file
    """
    ensure_directory_exists(output_file)
    
    # Convert reviews to dictionaries
    reviews_data = [review.to_dict() for review in reviews]
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(reviews_data, file, ensure_ascii=False, indent=2)
    
    return output_file

def export_reviews_to_csv(reviews: List[Review], output_file: str) -> str:
    """
    Export reviews to a CSV file.
    
    Args:
        reviews: List of Review objects
        output_file: Path to the output file
    
    Returns:
        Path to the created file
    """
    ensure_directory_exists(output_file)
    
    # Convert reviews to dictionaries
    reviews_data = [review.to_dict() for review in reviews]
    
    if not reviews_data:
        with open(output_file, 'w', encoding='utf-8', newline='') as file:
            file.write('')
        return output_file
    
    # Get fieldnames from the first review
    fieldnames = list(reviews_data[0].keys())
    
    # Write to CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews_data)
    
    return output_file

def export_reviews_to_excel(reviews: List[Review], output_file: str) -> str:
    """
    Export reviews to an Excel file.
    
    Args:
        reviews: List of Review objects
        output_file: Path to the output file
    
    Returns:
        Path to the created file
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for Excel export. Install it with 'pip install pandas openpyxl'")
    
    ensure_directory_exists(output_file)
    
    # Convert reviews to dictionaries
    reviews_data = [review.to_dict() for review in reviews]
    
    # Create DataFrame
    df = pd.DataFrame(reviews_data)
    
    # Write to Excel file
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    return output_file
