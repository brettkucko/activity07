import os
import traceback

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient

# --- Load variables from .env ---
load_dotenv()

# --- Read variables from .env ---
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "cs3720db")
PORT = int(os.getenv("PORT", "8000"))

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing. Check your .env file.")

# Connect to MongoDB (lazy: no real connection until the first query)
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client[MONGODB_DB]

collection1 = db["robotsexamples"]
collection2 = db["robotsexamplessvg"]

# --- FastAPI app setup ---
app = FastAPI()

# Optional: enable CORS if you'll connect from React/React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetch_all(collection):
    """Return every document in a collection with _id converted to a string."""
    docs = list(collection.find())
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs


# --- Root endpoint ---
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + MongoDB Atlas backend!"}


# --- Get all robots examples ---
@app.get("/robotsexamples")
def get_robots():
    try:
        return fetch_all(collection1)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            {"error": type(e).__name__, "detail": str(e)}, status_code=500
        )


# --- Get all robots examples SVG ---
@app.get("/robotsexamplessvg")
def get_robots_svg():
    try:
        return fetch_all(collection2)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            {"error": type(e).__name__, "detail": str(e)}, status_code=500
        )


# --- Health check that actually touches the database ---
@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return {"status": "ok", "database": MONGODB_DB}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            {"error": type(e).__name__, "detail": str(e)}, status_code=500
        )