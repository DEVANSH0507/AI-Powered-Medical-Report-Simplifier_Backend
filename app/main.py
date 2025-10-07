from fastapi import FastAPI
from app.api import upload
from app.api import summary
from typing import Optional
app = FastAPI()

#we declare routes
app.include_router(upload.router, prefix="/upload")
app.include_router(summary.router, prefix="/analyze")


@app.get("/")
def root():
    return {"Working "}

