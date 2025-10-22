# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from ...db.session import SessionLocal
# from ...db.models import User, Teacher, Student, Instructor
# from ...core.security import verify_password, create_access_token
# from ...core.deps import get_db
# from ...schemas.auth import LoginIn, TokenOut

# router = APIRouter(prefix="/auth", tags=["auth"])

# @router.post("/login", response_model=TokenOut)
# def login(payload: LoginIn, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == payload.username).first()
#     if not user or not verify_password(payload.password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"access_token": create_access_token(str(user.user_id), user.role)}
