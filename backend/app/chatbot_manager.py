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
        self.model = "gpt-4" 
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
