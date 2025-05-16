'''
Handles the FastAPI integration & middleware
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import reddit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(reddit.router)