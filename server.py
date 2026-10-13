from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# --- Load variables from .env ---
load_dotenv()

# --- Read variables from .env ---
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "cs3720db")
PORT = int(os.getenv("PORT", "8000"))

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing. Check your .env file.")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB]

collection1 = db["robotsexamples"]
collection2 = db["robotsexamplessvg"]

# --- FastAPI app setup ---
app = FastAPI()

# Optional: enable CORS if you’ll connect from React/React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Root endpoint ---
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + MongoDB Atlas backend!"}


# --- Get all robots examples ---
@app.get("/robotsexamples")
def get_robots():
    robots = list(collection1.find())      # Retrieve all documents
    for r in robots:
        r["_id"] = str(r["_id"])          # Convert ObjectId to string
    return robots

# --- Get all robots examples SVG ---
@app.get("/robotsexamplessvg")
def get_robots():
    robots = list(collection2.find())      # Retrieve all documents
    for r in robots:
        r["_id"] = str(r["_id"])          # Convert ObjectId to string
    return robots