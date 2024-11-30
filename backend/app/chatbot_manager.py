from openai import OpenAI
import os

'''''''''
conversation should be in this form: 
[
    {
    "role": "system", 
    "content": [{"type": "text", "text": "You are an interviewer helping users prepare for technical interviews. Ask questions and provide feedback based on their responses. Do not give answers but just hints where needed. Analyze code"}]
    },
    {
    "role": "assistant", 
    "content": [{"type": "text", "text": "Let's dive in, what is blah blah blah question" }]
    }
    {
    "role": "user", 
    "content": [{"type": "text", "text": "User response" }]
    },
    {
    "role": "assistant", 
    "content": [{"type": "text", "text": "Bot reply" }]
    }
    
    //FOR CODE:
    {
    "role": "user", 
    "content": [
        {"type": "text", "text": "User response" },
        {"type": "text", "text": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\ndef reverse_linked_list(head):\n    prev = None\n    current = head\n    while current:\n        next_node = current.next\n        current.next = prev\n        prev = current\n        current = next_node\n    return prev"}
    ]
    },
    ...
]

'''''''''


class ChatbotManager:
    def __init__(self):
        self.model = "gpt-4o-mini" 
        self.temperature = 0.5
        self.client = OpenAI()

    def generate_response(self, conversation):
        # Given the convo history, generate response with openai api
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
        

    def generate_final_analysis(self, conversation):
        # Create a new prompt to get structured final analysis
        prompt = """
                Evaluate the following interview conversation and provide the results in the following JSON format:
                {{
                    "qualitative_score": "No Hire | Lean Hire | Hire | Strong Hire",
                    "ratings": {{
                        "technical_ability": "Numeric value out of 10",
                        "problem_solving_skills": "Numeric value out of 10"
                    }},
                    "summary": "Short justification for the scores and qualitative rating."
                }}

                """
        new_convo = ""
        for m in conversation:
        # for everything but system, push the convo into a new String
            if m["role"] == "assistant" or m["role"] == "user":
                for content in m["content"]:
                    new_convo += f"{'Interviewer' if m['role'] == 'assistant' else 'Candidate'}: {content['text']}\n"
            print("NEW CONVERSATION STRING: " + new_convo)

        
        # new system prompt as interview analyzer
        # new user prompt requesting structured analysis
        # final convo as a single transcript string
        final_convo = []
        final_convo.append({"role": "system", "content": "You are an interview evaluator. Analyze interview conversations and provide structured feedback. If the candidate doesnt provide anything technical, then give them a no hire and 0 for all scores. Only increase their rating from 0 when they show understanding of technical concepts."},)
        final_convo.append({"role": "user", "content": prompt})
        final_convo.append({"role": "user", "content": new_convo})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=final_convo,
                max_tokens=500,
                temperature=self.temperature
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

