from .database import create_db_and_tables
from fastapi import FastAPI
from .routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware

create_db_and_tables()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "welcome!!"}
