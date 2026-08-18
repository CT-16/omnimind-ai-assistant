import os
import google.generativeai as genai
from typing import List, Dict

class AIEngine:
    """Core AI Integration wrapper for Google Gemini API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API Key missing! Set GEMINI_API_KEY in your .env file.")
        
        genai.configure(api_key=self.api_key)
        # Using Gemini 1.5 Flash for high performance, low latency, and long-context analysis
        # Using Gemini 2.5 Flash for high performance, low latency, and long-context analysis
        self.model = genai.GenerativeModel("gemini-3.6-flash")

    def summarize_text(self, text: str, mode: str = "Executive Brief") -> str:
        """Generates structured summaries based on requested mode."""
        prompts = {
            "Executive Brief": "Provide a high-level executive summary in 3-4 bullet points, followed by a 'Key Conclusion' sentence.",
            "Detailed Breakdown": "Provide a comprehensive structured breakdown with Section Headers, Core Concepts, and Detailed Bullet Points.",
            "Action Items": "Extract all actionable tasks, key deadlines, assigned roles, and decision points as a structured check-list."
        }
        
        prompt = f"""
        Role: You are an expert AI Executive Assistant.
        Task: {prompts.get(mode, prompts['Executive Brief'])}
        
        Document Content:
        \"\"\"
        {text[:20000]}  # Context limit safety check
        \"\"\"
        """
        response = self.model.generate_content(prompt)
        return response.text

    def answer_question(self, context: str, question: str) -> str:
        """Answers user questions grounding response in provided document context."""
        prompt = f"""
        Role: Professional Research Analyst.
        Task: Answer the user's question accurately based strictly on the provided context below.
        If the answer cannot be directly derived from the context, explicitly state: 'The provided document does not contain sufficient details to answer this.'

        Context:
        \"\"\"
        {context[:20000]}
        \"\"\"

        Question: {question}
        """
        response = self.model.generate_content(prompt)
        return response.text

    def generate_content(self, content_type: str, topic: str, tone: str) -> str:
        """Generates tailored creative and professional workplace content."""
        prompt = f"""
        Role: Professional Communications Specialist.
        Task: Draft a high-quality '{content_type}' on the topic: '{topic}'.
        Tone: {tone}.
        
        Ensure clean structure, professional formatting, and ready-to-publish quality.
        """
        response = self.model.generate_content(prompt)
        return response.text

    def get_smart_suggestions(self, text: str) -> str:
        """Analyzes content and automatically suggests next steps and improvement ideas."""
        prompt = f"""
        Analyze the following text and provide 3-4 intelligent productivity suggestions:
        1. Potential risk points or missing information.
        2. Recommended follow-up actions or communications.
        3. Strategic insights or improvement ideas.

        Text Content:
        \"\"\"
        {text[:15000]}
        \"\"\"
        """
        response = self.model.generate_content(prompt)
        return response.text