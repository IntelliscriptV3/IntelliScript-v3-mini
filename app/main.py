import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .api.v1.auth import router as auth_router
from .api.v1.chat import router as chat_router
from .api.v1.admin import router as admin_router

app = FastAPI(title="IntelliScript Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(admin_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)