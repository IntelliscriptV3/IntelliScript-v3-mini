from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt, JWTError
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
# from ..db.models import User, Teacher, Student, Instructor
from .config import settings

bearer = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
#     token = creds.credentials
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
#         uid = int(payload["sub"])
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     user = db.query(User).filter(User.user_id == uid).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user

# def require_role(role: str):
#     def dep(user: User = Depends(get_current_user)):
#         if user.role != role:
#             raise HTTPException(status_code=403, detail=f"{role} role required")
#         return user
#     return dep

# def require_teacher(db: Session = Depends(get_db), user: User = Depends(require_role("teacher"))):
#     teacher = db.query(Teacher).filter(Teacher.user_id == user.user_id).first()
#     if not teacher:
#         raise HTTPException(status_code=403, detail="Teacher profile missing")
#     return teacher

# def require_student(db: Session = Depends(get_db), user: User = Depends(require_role("student"))):
#     s = db.query(Student).filter(Student.user_id == user.user_id).first()
#     if not s:
#         raise HTTPException(status_code=403, detail="Student profile missing")
#     return s

# def require_instructor(db: Session = Depends(get_db), user: User = Depends(require_role("instructor"))):
#     inst = db.query(Instructor).filter(Instructor.user_id == user.user_id).first()
#     if not inst:
#         raise HTTPException(status_code=403, detail="Instructor profile missing")
#     return inst
