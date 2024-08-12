
import ollama
import json

client = ollama.Client()

def llm_response(prompt):
    messages_input = [
        {
            'role': 'user', 
            'content': prompt
        }
    ]

    stream = client.chat(
        model='phi3',
    
        messages=messages_input,
        stream=True,
    )

    return stream