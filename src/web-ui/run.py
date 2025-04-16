import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

sio = socketio.AsyncServer(async_mode='asgi')

app = FastAPI()

app.mount('/ws', socketio.ASGIApp(sio))

@app.get("/")
async def homepage():
    return PlainTextResponse('Hello, world!')

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=3000)

