from openai import OpenAI
import os
from typing import List, Dict
from app.utils.prompts import Prompts
import re 
import json

class ChatbotManager:
                
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
                temperature=self.temperature,
                stream=True  # Enable streaming
            )
            
            # Return the stream object directly
            return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
    def generate_final_analysis(self, conversation: List[Dict], final_code: str):
        try:
            new_convo = self.format_conversation(conversation)
            final_convo = [
                {"role": "system", "content": Prompts.FINAL_ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": Prompts.FINAL_ANALYSIS_PROMPT},
                {"role": "user", "content": new_convo},
                {"role": "user", "content": f"Final Code: {final_code}"}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=final_convo,
                max_tokens=500,
                temperature=self.temperature
            )
            final_analysis = response.choices[0].message.content 
            final_analysis = re.sub(r'```json|```', '', final_analysis).strip()
            return json.loads(final_analysis)
          
            
        except Exception as e:
            print(f"Error generating final analysis: {str(e)}")
    
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
