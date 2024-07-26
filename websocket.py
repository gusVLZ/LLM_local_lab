import asyncio
import ollama
import json
from websockets.server import serve
from faustaoIA import faustao_response

async def echo(websocket):
    async for message in websocket:

        stream = faustao_response(message)

        first = True
        for chunk in stream:
            #print(chunk['message']['content'], end='', flush=True)
            if first:
                print(chunk)
                first = False
            await websocket.send(chunk['message']['content'])

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())