import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
    JWT_ALG = "HS256"
    FILE_STORE = os.getenv("FILE_STORE", "./uploads")
    SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    MAIL_FROM = os.getenv("MAIL_FROM", "no-reply@intelliscript.local")
    # URL (scheme+host+port) for external classifier service used by /chat/classify
    # Prefer explicit CLASSIFIER_URL, but accept legacy LLM_URL env var for older setups.
    LLM_URL = os.getenv("LLM_URL", "http://localhost:8001")
    CLASSIFIER_URL = os.getenv("CLASSIFIER_URL", LLM_URL)
    # Maximum seconds to wait for classifier responses (can be higher for slow LLMs)
    CLASSIFIER_TIMEOUT = int(os.getenv("CLASSIFIER_TIMEOUT", "30"))

settings = Settings()
