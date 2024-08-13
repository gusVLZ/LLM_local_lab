
import ollama
import json

client = ollama.Client()

def filter_documents(prompt, documents):
    filtered_documents = []
    for d in documents:
        messages_input = [
            {
                'role': 'user', 
                'content': f"""answer with a single word (yes or no), if the next text can be used to answer the user question
                TEXT: {d}
                QUESTION: {prompt}
                """
            }
        ]
        response = client.chat(
            model='gemma2:2b',
        
            messages=messages_input,
        )
        print(response["message"]["content"])

        if "yes" in response["message"]["content"].lower():
            filtered_documents.append(d)
        
    return filtered_documents


def llm_response(prompt, documents):

    messages_input = [
        {
            'role': 'system', 
            'content': f"""Based on the texts below:
{"\n\n".join(documents)}

answer this question in brazilian portuguese:
{prompt}"""
        }
    ]

    stream = client.chat(
        model='gemma2:2b',
    
        messages=messages_input,
        stream=True,
    )

    return stream