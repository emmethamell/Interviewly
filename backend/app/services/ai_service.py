from openai import OpenAI
import os
from typing import List, Dict

class ChatbotManager:
    SYSTEM_PROMPT="You are an interview evaluator. Analyze interview conversations and provide structured feedback. If the candidate doesnt provide anything technical, then give them a no hire and 0 for all scores. Only increase their rating from 0 when they show understanding of technical concepts."
    FINAL_ANALYSIS_PROMPT="""
        Evaluate the following interview conversation and provide the results in the following JSON format:
        {
            "qualitative_score": "No Hire | Lean Hire | Hire | Strong Hire",
            "ratings": {
                "technical_ability": "Numeric value out of 10",
                "problem_solving_skills": "Numeric value out of 10"
            },
            "summary": "Short justification for the scores and qualitative rating."
        }
        """
                
    def __init__(self):
        self.model = "gpt-4o-mini" 
        self.temperature = 0.5
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, conversation: List[Dict]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
                max_tokens=500,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
    def generate_final_analysis(self, conversation: List[Dict], final_code: str):
        new_convo = self.format_conversation(conversation)
        final_convo = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": self.FINAL_ANALYSIS_PROMPT},
            {"role": "user", "content": new_convo},
            {"role": "user", "content": f"Final Code: {final_code}"}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=final_convo,
                max_tokens=500,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def format_conversation(self, conversation: List[Dict]) -> str:
        return "\n".join(
            f"{'Interviewer' if m['role'] == 'assistant' else 'Candidate'}: {content['text']}"
            for m in conversation for content in m["content"]
        )
    
"""
Conversation format
[
    {
    "role": "system" OR "assistant" OR "user", 
    "content": [{"type": "text", "text": user_reponse OR bot_reply}]
    },
    ...
]

"""
