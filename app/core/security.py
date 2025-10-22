# from datetime import datetime, timedelta
# from jose import jwt
# from passlib.context import CryptContext
# from .config import settings

# pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(p: str) -> str:
#     return pwd_ctx.hash(p)

# def verify_password(p: str, h: str) -> bool:
#     return pwd_ctx.verify(p, h)

# def create_access_token(sub: str, role: str, extra: dict | None = None, minutes: int = 120) -> str:
#     data = {"sub": sub, "role": role, "exp": datetime.utcnow() + timedelta(minutes=minutes)}
#     if extra: data.update(extra)
#     return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
