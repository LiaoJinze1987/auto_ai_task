from fastapi import FastAPI
from pydantic import BaseModel
from openclaw_client import OpenClawClient
from intent_dispatcher import IntentDispatcher
import uvicorn

app = FastAPI()
#
class ChatRequest(BaseModel):
    message: str
#
client = OpenClawClient()
dispatcher = IntentDispatcher()

@app.post("/chat")
def chat(request: ChatRequest):
    intent = client.analyze(request.message)
    result = dispatcher.dispatch(intent)
    return {
        "code": 200,
        "intent": intent,
        "result": result
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
