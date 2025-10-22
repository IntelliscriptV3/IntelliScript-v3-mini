import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .api.v1.auth import router as auth_router
from .api.v1.chat import router as chat_router
from .api.v1.admin import router as admin_router

app = FastAPI(title="IntelliScript Backend")

# disable automatic redirects when trailing slash is missing/present
# this prevents 307 Temporary Redirect responses when frontend hits paths
# without the exact trailing-slash form
app.router.redirect_slashes = False

# Configure CORS origins explicitly. When credentials are sent from the
# frontend (fetch with credentials: 'include'), Access-Control-Allow-Origin
# must NOT be '*'. Use the FRONTEND_ORIGINS env var (comma-separated)
# or default to http://localhost:8080 for local development.
frontend_origins = os.getenv("FRONTEND_ORIGINS", "http://localhost:8080")
if isinstance(frontend_origins, str):
    allow_origins = [o.strip() for o in frontend_origins.split(",") if o.strip()]
else:
    allow_origins = list(frontend_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(admin_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)