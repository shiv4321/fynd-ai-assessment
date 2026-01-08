"""
Data Models and Storage Module
Defines the data structures and in-memory storage for submissions.
"""

from datetime import datetime
from typing import List, Dict, Optional
import uuid
import json


class Submission:
    """
    Represents a single review submission with all associated data.
    """
    
    def __init__(self, rating: int, review: str, ai_response: str, 
                 summary: str, recommended_actions: str):
        """
        Initialize a new submission.
        
        Args:
            rating: Star rating (1-5)
            review: Review text from user
            ai_response: AI-generated response for user
            summary: AI-generated summary for admin
            recommended_actions: AI-generated recommendations for admin
        """
        self.id = str(uuid.uuid4())  # Generate unique ID
        self.rating = rating
        self.review = review
        self.ai_response = ai_response
        self.summary = summary
        self.recommended_actions = recommended_actions
        self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        """
        Convert submission to dictionary format.
        
        Returns:
            Dictionary representation of the submission
        """
        return {
            "id": self.id,
            "rating": self.rating,
            "review": self.review,
            "ai_response": self.ai_response,
            "summary": self.summary,
            "recommended_actions": self.recommended_actions,
            "timestamp": self.timestamp
        }


class SubmissionStore:
    """
    In-memory storage for submissions.
    
    Note: This uses in-memory storage which means data will be lost when the 
    server restarts. For production, you would use a database like PostgreSQL,
    MongoDB, or SQLite. However, for this assignment, in-memory storage is 
    acceptable and keeps deployment simple.
    """
    
    def __init__(self):
        """Initialize empty storage."""
        self.submissions: List[Submission] = []
    
    def add_submission(self, submission: Submission) -> str:
        """
        Add a new submission to storage.
        
        Args:
            submission: Submission object to store
            
        Returns:
            ID of the stored submission
        """
        self.submissions.append(submission)
        return submission.id
    
    def get_all_submissions(self) -> List[Dict]:
        """
        Retrieve all submissions.
        
        Returns:
            List of submission dictionaries, sorted by timestamp (newest first)
        """
        # Sort by timestamp in descending order (newest first)
        sorted_submissions = sorted(
            self.submissions, 
            key=lambda x: x.timestamp, 
            reverse=True
        )
        return [sub.to_dict() for sub in sorted_submissions]
    
    def get_submission_by_id(self, submission_id: str) -> Optional[Dict]:
        """
        Retrieve a specific submission by ID.
        
        Args:
            submission_id: The ID of the submission to retrieve
            
        Returns:
            Submission dictionary if found, None otherwise
        """
        for submission in self.submissions:
            if submission.id == submission_id:
                return submission.to_dict()
        return None
    
    def get_count(self) -> int:
        """
        Get total number of submissions.
        
        Returns:
            Count of submissions
        """
        return len(self.submissions)