
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Sentiment(BaseModel):
    sentiment_score: float
    sentiment_magnitude: float

sentiments = [Sentiment(sentiment_score=0.0, sentiment_magnitude=0.0)]

@app.post("/api/v1/sentiment")
async def create_sentiment(sentiment: Sentiment):
    sentiments.append(sentiment)
    return sentiment

@app.get("/api/v1/sentiment", response_model=Sentiment)
async def get_sentiment():
    if len(sentiments) > 0:
        return sentiments[-1]
    else:
        return None

