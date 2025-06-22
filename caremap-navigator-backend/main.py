from fastapi import FastAPI, Query, HTTPException, Request
from pydantic import BaseModel
import httpx
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from dotenv import load_dotenv
import os
from typing import List
import json
import anthropic

# to run this file, seperately run on terminal: uvicorn main:app --reload 

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
df = pd.read_csv("final_with_preferences.csv")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    zipCode: str
    serviceTypes: List[str] #list of preferences
    languagePreference: str
    accessibilityNeeds: List[str]
    familySize: str
    specialRequirements: List[str]
    notificationPreference: str

class ChatMessage(BaseModel): #input
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel): #output response model
    messages: List[ChatMessage]


@app.post("/ask")
def search_services(query: Query):
    # Step 1: Filter by zip code directly
    filtered = df[df["zip_code"].astype(str) == query.zipCode]

    # Step 2: Further filter based on serviceTypes (which match column names like "lgbtq_friendly", etc.)
    for pref in query.serviceTypes:
        if pref in df.columns:
            filtered = filtered[filtered[pref].astype(str).str.lower() == "true"]

    # Step 3: Convert top 10 results to records
    records = filtered.to_dict(orient="records")[:10]  # or more if needed


    # Step 4: Format the input for Claude
    input_text = "\n\n".join([
        f"Name: {r.get('name')}, Address: {r.get('address')}, ZIP: {r.get('zip_code')}, Matching Preferences: {', '.join([k for k in query.serviceTypes if str(r.get(k, '')).lower() == 'true'])}"
        for r in records
    ])

    # Step 5: Build Claude prompt
    prompt = f"""
A user is looking for community services near ZIP code {query.zipCode}.
Here are their preferences:

- Service types: {', '.join(query.serviceTypes)}
- Language preference: {query.languagePreference}
- Accessibility needs: {', '.join(query.accessibilityNeeds) if query.accessibilityNeeds else 'None'}
- Family size: {query.familySize}
- Special requirements: {', '.join(query.specialRequirements) if query.specialRequirements else 'None'}
- Notification preference: {query.notificationPreference}

Based on these preferences, here are some service matches from our dataset:

{input_text}

Please summarize the key options that best meet the user's needs. Include names, addresses, zip codes, and note which preferences they match.
"""


    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "summary": message.content[0].text,
        "matches": records
    }

@app.post("/chat")
def chat_with_claude(chat: ChatRequest):
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        temperature=0.3,
        messages=chat.messages
    )
    return {"reply": response.content[0].text}
