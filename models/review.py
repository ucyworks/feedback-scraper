"""
Review Model

This module defines the Review class that represents a customer review.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Review:
    """Class for representing a customer review."""
    rating: int
    owner: str
    date: datetime
    comment: str
    size: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    seller: Optional[str] = None
    likes: int = 0
    
    def to_dict(self) -> dict:
        """Convert review to dictionary for export purposes."""
        return {
            'rating': self.rating,
            'owner': self.owner,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'comment': self.comment,
            'size': self.size,
            'height': self.height,
            'weight': self.weight,
            'seller': self.seller,
            'likes': self.likes
        }
    
    def __str__(self) -> str:
        """String representation of a review."""
        return (f"Review by {self.owner} on {self.date.strftime('%Y-%m-%d')}: "
                f"{self.rating}★ - {self.comment[:50]}{'...' if len(self.comment) > 50 else ''}")
