import ollama
import json
client = ollama.Client(host='http://localhost:11434')


def faustao_response(prompt):
    messages_input = [
        {
            'role': 'system', 
            'content': "Você sempre deve responder como o apresentador de TV Faustão"
        },
        {
            'role': 'system', 
            'content': f"utilize algumas das seguintes frases em suas respostas: {json.dumps(slogans_faustao(), ensure_ascii=False)}"
        },
        {
            'role': 'user', 
            'content': prompt
        }
        # {
        #     'role': 'system',
        #     'content': f'responda como o apresentador de tv conhecido por Faustão que utiliza as frases a seguir: {json.dumps(slogans_faustao())}'
        # }
    ]

    stream = client.chat(
        model='mistral',
        messages=messages_input,
        stream=True,
    )

    return stream

def slogans_faustao(): 
    return [
        "Oloco, bicho!",
        "Quem sabe faz ao vivo!",
        "Ô loco, meu!",
        "É brincadeira, meu!",
        "Cê é louco!",
        "Tá pegando fogo, bicho!",
        "Não é mole não!",
        "É uma fera, bicho!",
        "É agora que a onça bebe água!",
        "Vai pra casa, garoto!"
    ]
