"""
LLM Service Module
Handles all interactions with the Groq API for generating responses.
"""

from groq import Groq
from typing import Optional


class LLMService:
    """
    Service class for interacting with Groq LLM API.
    Provides methods for generating user responses, summaries, and recommendations.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the LLM service with Groq API key.
        
        Args:
            api_key: Groq API key for authentication
        """
        if not api_key:
            raise ValueError("Groq API key is required")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Fast and efficient model
        
    def _call_llm(self, prompt: str, temperature: float = 0.7, max_tokens: int = 300) -> str:
        """
        Internal method to call Groq LLM API.
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum length of response
            
        Returns:
            String response from the LLM
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")
    
    def generate_user_response(self, rating: int, review_text: str) -> str:
        """
        Generate an AI response to show to the user after they submit their review.
        The response should acknowledge their feedback and be appropriate to their rating.
        
        Args:
            rating: Star rating (1-5)
            review_text: The review text submitted by user
            
        Returns:
            AI-generated response string
        """
        prompt = f"""You are a friendly customer service representative. A user has submitted a review with a {rating}-star rating.

Review: {review_text}

Generate a brief, empathetic response (2-3 sentences) that:
- Thanks them for their feedback
- Acknowledges their experience
- Is appropriate for their rating level
- Sounds natural and human

Keep it concise and professional."""

        return self._call_llm(prompt, temperature=0.7, max_tokens=150)
    
    def generate_summary(self, review_text: str, rating: int) -> str:
        """
        Generate a concise summary of the review for the admin dashboard.
        
        Args:
            review_text: The review text to summarize
            rating: Star rating (1-5)
            
        Returns:
            Brief summary string
        """
        prompt = f"""Summarize this {rating}-star review in 1-2 sentences. Focus on the key points.

Review: {review_text}

Summary:"""

        return self._call_llm(prompt, temperature=0.5, max_tokens=150)
    
    def generate_recommendations(self, review_text: str, rating: int) -> str:
        """
        Generate recommended actions for the admin based on the review.
        
        Args:
            review_text: The review text
            rating: Star rating (1-5)
            
        Returns:
            Recommended actions string
        """
        prompt = f"""Based on this {rating}-star review, suggest 2-3 specific action items for the business to address.

Review: {review_text}

Provide clear, actionable recommendations:"""

        return self._call_llm(prompt, temperature=0.6, max_tokens=200)