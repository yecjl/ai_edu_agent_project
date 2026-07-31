"""
FastAPI入口

Author: danke
Date: 2026/7/26 16:46
"""
from fastapi import FastAPI

from backend.api.v1.resume import router as resume
from backend.api.v1.auth import router as auth

app = FastAPI(title="Auth Demo")

app.include_router(router= auth, prefix="/auth", tags=["auth"])
app.include_router(router= resume, prefix="/resume", tags=["resume"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)