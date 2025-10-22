from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Date, DateTime, Text, DECIMAL, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time, datetime
from decimal import Decimal
from passlib.context import CryptContext
import secrets
import string 

# Database setup
DATABASE_URL = "postgresql://postgres:kisal123@localhost/intelliscript2"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="School Management API", version="1.0.0")

# Database Models

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(150), unique=True)
    role = Column(String)  # stored as enum in DB; keep string here
    password_hash = Column(String(255))
    created_at = Column(DateTime)

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    fname = Column(String(100))
    mname = Column(String(100))
    lname = Column(String(100))
    contact_no = Column(String(100))
    email = Column(String(150))
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    address_line3 = Column(String(100))
    age = Column(Integer)
    stream = Column(String)
    grade = Column(String)

class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    fname = Column(String(100))
    mname = Column(String(100))
    lname = Column(String(100))
    contact_no = Column(String(100))
    email = Column(String(150))
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    address_line3 = Column(String(100))
    age = Column(Integer)

class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'))
    course_code = Column(String(20))
    subject = Column(String(100))
    grade = Column(String)
    stream = Column(String)
    day_of_week = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)
    class_room = Column(String(100))

class Enrollment(Base):
    __tablename__ = 'enrollments'
    enrollment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))

class Assessment(Base):
    __tablename__ = 'assessments'
    assessment_id = Column(Integer, primary_key=True)
    course_id = Column(Integer)
    title = Column(String(150))
    description = Column(Text)
    max_marks = Column(Integer)
    assessment_date = Column(Date)

class Attendance(Base):
    __tablename__ = 'attendance'
    attendance_id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    course_id = Column(Integer)
    attendance_date = Column(Date)
    status = Column(String)
    remarks = Column(Text)
    created_at = Column(DateTime)

class Fee(Base):
    __tablename__ = 'fees'
    fee_id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    course_id = Column(Integer)
    month_year = Column(Date)
    amount = Column(DECIMAL(10,2))
    paid = Column(Boolean)
    paid_at = Column(DateTime)
    payment_method = Column(String(50))

# Response Models
class StudentResponse(BaseModel):
    student_id: int
    user_id: Optional[int] = None
    fname: Optional[str] = None
    mname: Optional[str] = None
    lname: Optional[str] = None
    contact_no: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    age: Optional[int] = None
    stream: Optional[str] = None
    grade: Optional[str] = None

    class Config:
        from_attributes = True

class TeacherResponse(BaseModel):
    teacher_id: int
    user_id: Optional[int] = None
    fname: Optional[str] = None
    mname: Optional[str] = None
    lname: Optional[str] = None
    contact_no: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    age: Optional[int] = None

    class Config:
        from_attributes = True

class CourseResponse(BaseModel):
    course_id: int
    teacher_id: Optional[int] = None
    course_code: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    stream: Optional[str] = None
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    class_room: Optional[str] = None

    class Config:
        from_attributes = True

class EnrollmentResponse(BaseModel):
    enrollment_id: int
    student_id: Optional[int] = None
    course_id: Optional[int] = None

    class Config:
        from_attributes = True

class AssessmentResponse(BaseModel):
    assessment_id: int
    course_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    max_marks: Optional[int] = None
    assessment_date: Optional[date] = None

    class Config:
        from_attributes = True

class AttendanceResponse(BaseModel):
    attendance_id: int
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    attendance_date: Optional[date] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FeeResponse(BaseModel):
    fee_id: int
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    month_year: Optional[date] = None
    amount: Optional[Decimal] = None
    paid: Optional[bool] = None
    paid_at: Optional[datetime] = None
    payment_method: Optional[str] = None

    class Config:
        from_attributes = True

# Create/Update Models
class StudentCreate(BaseModel):
    fname: str
    mname: Optional[str] = None
    lname: str
    contact_no: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    age: Optional[int] = None
    stream: Optional[str] = None
    grade: Optional[str] = None

class StudentUpdate(BaseModel):
    fname: Optional[str] = None
    mname: Optional[str] = None
    lname: Optional[str] = None
    contact_no: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    age: Optional[int] = None
    stream: Optional[str] = None
    grade: Optional[str] = None

class TeacherCreate(BaseModel):
    fname: str
    mname: Optional[str] = None
    lname: str
    contact_no: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    age: Optional[int] = None

class TeacherUpdate(BaseModel):
    fname: Optional[str] = None
    mname: Optional[str] = None
    lname: Optional[str] = None
    contact_no: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    age: Optional[int] = None

class CourseCreate(BaseModel):
    teacher_id: int
    course_code: str
    subject: str
    grade: Optional[str] = None
    stream: Optional[str] = None
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    class_room: Optional[str] = None

class CourseUpdate(BaseModel):
    teacher_id: Optional[int] = None
    course_code: Optional[str] = None
    subject: Optional[str] = None
    grade: Optional[str] = None
    stream: Optional[str] = None
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    class_room: Optional[str] = None

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class AssessmentCreate(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    max_marks: int
    assessment_date: date

class AssessmentUpdate(BaseModel):
    course_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    max_marks: Optional[int] = None
    assessment_date: Optional[date] = None

class AttendanceCreate(BaseModel):
    student_id: int
    course_id: int
    attendance_date: date
    status: str
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None

class AttendanceUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    attendance_date: Optional[date] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None

class FeeCreate(BaseModel):
    student_id: int
    course_id: int
    month_year: date
    amount: Decimal
    paid: bool = False
    paid_at: Optional[datetime] = None
    payment_method: Optional[str] = None

class FeeUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    month_year: Optional[date] = None
    amount: Optional[Decimal] = None
    paid: Optional[bool] = None
    paid_at: Optional[datetime] = None
    payment_method: Optional[str] = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Add password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_username(fname: str, lname: str, db: Session) -> str:
    """Create a unique username based on first and last name"""
    base_username = (fname[0] + lname).lower().replace(" ", "")
    
    # Check if base username exists
    existing_user = db.query(User).filter(User.username == base_username).first()
    if not existing_user:
        return base_username
    
    # If exists, add numbers until we find a unique one
    counter = 1
    while True:
        new_username = f"{base_username}{counter}"
        existing_user = db.query(User).filter(User.username == new_username).first()
        if not existing_user:
            return new_username
        counter += 1

def generate_random_password(length: int = 8) -> str:
    """Generate a random password"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def create_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


# Student CRUD Operations
@app.post("/students/", response_model=dict)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    try:
        username = create_username(student.fname, student.lname, db)
        password_hash = generate_random_password()
        role = 'student'
        email = student.email if student.email else None
        created_at = datetime.now()
        db_user = User(username=username, email=email, role=role, password_hash=password_hash, created_at=created_at)
        db.add(db_user)
        db.flush()  # Flush to get user_id
        
        user_id = db_user.user_id
        student_data = student.model_dump()
        student_data['user_id'] = user_id
        
        db_student = Student(**student_data)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        return JSONResponse(status_code=200, content={"message": "Student created successfully", "student_id": db_student.student_id})
    
    except Exception as e:
        db.rollback()
        print("Error creating student:", e)
        return JSONResponse(status_code=500, content={"message": "Student creation failed", "error": str(e)})
        

@app.get("/students/", response_model=List[StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        students = db.query(Student).offset(skip).limit(limit).all()
        return students
    except Exception as e:
        print("Error reading students:", e)
        return JSONResponse(status_code=500, content={"message": "Failed to read students", "error": str(e)})

@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        print("Error reading student:", e)
        return JSONResponse(status_code=500, content={"message": "Failed to read student", "error": str(e)})

@app.put("/students/{student_id}", response_model=dict)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    try:
        db_student = db.query(Student).filter(Student.student_id == student_id).first()
        if db_student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        
        update_data = student.model_dump(exclude_unset=True)
        email = update_data.get('email')
        if email:
            db_user = db.query(User).filter(User.user_id == db_student.user_id).first()
            if db_user:
                db_user.email = email
                db.add(db_user)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Student updated successfully"})
    except Exception as e:
        db.rollback()
        print("Error updating student:", e)
        return JSONResponse(status_code=500, content={"message": "Student update failed", "error": str(e)})

@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    try:
        db_student = db.query(Student).filter(Student.student_id == student_id).first()
        if db_student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        user_id = db_student.user_id
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            db.delete(db_user)
        db.delete(db_student)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Student deleted successfully"})
    except Exception as e:
        db.rollback()
        print("Error deleting student:", e)
        return JSONResponse(status_code=500, content={"message": "Student deletion failed", "error": str(e)})

# Teacher CRUD Operations
@app.post("/teachers/", response_model=dict)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    try:
        username = create_username(teacher.fname, teacher.lname, db)
        password = generate_random_password()
        email = teacher.email if teacher.email else None
        role = 'teacher'
        created_at = datetime.now()
        
        # Create user first
        db_user = User(
            username=username, 
            email=email,
            role=role, 
            password_hash=password,
            created_at=created_at
        )
        db.add(db_user)
        db.flush()

        teacher_data = teacher.model_dump()
        teacher_data['user_id'] = db_user.user_id

        db_teacher = Teacher(**teacher_data)
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
        return JSONResponse(status_code=200, content={"message": "Teacher created successfully", "teacher_id": db_teacher.teacher_id})
    except Exception as e:
        db.rollback()
        print("Error creating teacher:", e)
        return JSONResponse(status_code=500, content={"message": "Teacher creation failed", "error": str(e)})

@app.get("/teachers/", response_model=List[TeacherResponse])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        teachers = db.query(Teacher).offset(skip).limit(limit).all()
        return teachers
    except Exception as e:
        print("Error reading teachers:", e)
        return JSONResponse(status_code=500, content={"message": "Teacher retrieval failed", "error": str(e)})

@app.get("/teachers/{teacher_id}", response_model=TeacherResponse)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return teacher
    except Exception as e:
        print("Error reading teacher:", e)
        return JSONResponse(status_code=500, content={"message": "Teacher retrieval failed", "error": str(e)})
        

@app.put("/teachers/{teacher_id}", response_model=dict)
def update_teacher(teacher_id: int, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    try:
        db_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
        if db_teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        update_data = teacher.model_dump(exclude_unset=True)
        email = update_data.get('email')
        if email:
            db_user = db.query(User).filter(User.user_id == db_teacher.user_id).first()
            if db_user:
                db_user.email = email
                db.add(db_user)
                
        for field, value in update_data.items():
            setattr(db_teacher, field, value)
        
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Teacher updated successfully"})
    except Exception as e:
        db.rollback()
        print("Error updating teacher:", e)
        return JSONResponse(status_code=500, content={"message": "Teacher update failed", "error": str(e)})

@app.delete("/teachers/{teacher_id}", response_model=dict)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        db_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
        if db_teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        user_id = db_teacher.user_id
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if db_user:
            db.delete(db_user)
        db.delete(db_teacher)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Teacher deleted successfully"})
    except Exception as e:
        db.rollback()
        print("Error deleting teacher:", e)
        return JSONResponse(status_code=500, content={"message": "Teacher deletion failed", "error": str(e)})

# Course CRUD Operations
@app.post("/courses", response_model=dict)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    try:
        db_course = Course(**course.model_dump())
        db.add(db_course)
        db.commit()
        db.refresh(db_course)
        return JSONResponse(status_code=201, content={"message": "Course created successfully", "course_id": db_course.course_id})
    except Exception as e:
        db.rollback()
        print("Error creating course:", e)
        return JSONResponse(status_code=500, content={"message": "Course creation failed", "error": str(e)})

@app.get("/courses/", response_model=List[CourseResponse])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        courses = db.query(Course).offset(skip).limit(limit).all()
        return courses
    except Exception as e:
        print("Error reading courses:", e)
        return JSONResponse(status_code=500, content={"message": "Course retrieval failed", "error": str(e)})

@app.get("/courses/{course_id}", response_model=CourseResponse)
def read_course(course_id: int, db: Session = Depends(get_db)):
    try:
        course = db.query(Course).filter(Course.course_id == course_id).first()
        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    except Exception as e:
        print("Error reading course:", e)
        return JSONResponse(status_code=500, content={"message": "Course retrieval failed", "error": str(e)})
        

@app.put("/courses/{course_id}", response_model=dict)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.course_id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")
        
        update_data = course.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_course, field, value)
        
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Course updated successfully"})
    except Exception as e:
        db.rollback()
        print("Error updating course:", e)
        return JSONResponse(status_code=500, content={"message": "Course update failed", "error": str(e)})

@app.delete("/courses/{course_id}", response_model=dict)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        db_course = db.query(Course).filter(Course.course_id == course_id).first()
        if db_course is None:
            raise HTTPException(status_code=404, detail="Course not found")

        db.delete(db_course)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Course deleted successfully"})
    except Exception as e:
        db.rollback()
        print("Error deleting course:", e)
        return JSONResponse(status_code=500, content={"message": "Course deletion failed", "error": str(e)})


# Enrollment CRUD Operations
@app.post("/enrollments", response_model=dict)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        db_enrollment = Enrollment(**enrollment.model_dump())
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return JSONResponse(status_code=200, content={"message": "Enrollment created successfully", "enrollment_id": db_enrollment.enrollment_id})
    except Exception as e:
        db.rollback()
        print("Error creating enrollment:", e)
        return JSONResponse(status_code=500, content={"message": "Enrollment creation failed", "error": str(e)})

@app.get("/enrollments/", response_model=List[EnrollmentResponse])
def read_enrollments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        enrollments = db.query(Enrollment).offset(skip).limit(limit).all()
        return enrollments
    except Exception as e:
        print("Error reading enrollments:", e)
        return JSONResponse(status_code=500, content={"message": "Enrollment retrieval failed", "error": str(e)})

@app.get("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def read_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        enrollment = db.query(Enrollment).filter(Enrollment.enrollment_id == enrollment_id).first()
        if enrollment is None:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        return enrollment
    except Exception as e:
        print("Error reading enrollment:", e)
        return JSONResponse(status_code=500, content={"message": "Enrollment retrieval failed", "error": str(e)})

@app.delete("/enrollments/{enrollment_id}", response_model=dict)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        db_enrollment = db.query(Enrollment).filter(Enrollment.enrollment_id == enrollment_id).first()
        if db_enrollment is None:
            raise HTTPException(status_code=404, detail="Enrollment not found")

        db.delete(db_enrollment)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Enrollment deleted successfully"})
    except Exception as e:
        db.rollback()
        print("Error deleting enrollment:", e)
        return JSONResponse(status_code=500, content={"message": "Enrollment deletion failed", "error": str(e)})

@app.get("/enrollments_by_student/{student_id}", response_model=List[EnrollmentResponse])
def read_enrollments_by_student(student_id: int, db: Session = Depends(get_db)):
    try:
        enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
        return enrollments
    except Exception as e:
        print("Error reading enrollments by student:", e)
        return JSONResponse(status_code=500, content={"message": "Enrollment retrieval failed", "error": str(e)})
    
@app.get("/courses_by_teacher/{teacher_id}", response_model=List[CourseResponse])
def read_courses_by_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        courses = db.query(Course).filter(Course.teacher_id == teacher_id).all()
        return courses
    except Exception as e:
        print("Error reading courses by teacher:", e)
        return JSONResponse(status_code=500, content={"message": "Course retrieval failed", "error": str(e)})

# Assessment CRUD Operations
# @app.post("/assessments/", response_model=dict)
# def create_assessment(assessment: AssessmentCreate, db: Session = Depends(get_db)):
#     try:
#         db_assessment = Assessment(**assessment.model_dump())
#         db.add(db_assessment)
#         db.commit()
#         db.refresh(db_assessment)
#         return JSONResponse(status_code=200, content={"message": "Assessment created successfully", "assessment_id": db_assessment.assessment_id})
#     except Exception as e:
#         db.rollback()
#         print("Error creating assessment:", e)
#         return JSONResponse(status_code=500, content={"message": "Assessment creation failed", "error": str(e)})

@app.get("/assessments/", response_model=List[AssessmentResponse])
def read_assessments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        assessments = db.query(Assessment).offset(skip).limit(limit).all()
        return assessments
    except Exception as e:
        print("Error reading assessments:", e)
        return JSONResponse(status_code=500, content={"message": "Assessment retrieval failed", "error": str(e)})

@app.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
def read_assessment(assessment_id: int, db: Session = Depends(get_db)):
    try:
        assessment = db.query(Assessment).filter(Assessment.assessment_id == assessment_id).first()
        if assessment is None:
            raise HTTPException(status_code=404, detail="Assessment not found")
        return assessment
    except Exception as e:
        print("Error reading assessment:", e)
        return JSONResponse(status_code=500, content={"message": "Assessment retrieval failed", "error": str(e)})

@app.get("/assessments_by_course/{course_id}", response_model=List[AssessmentResponse])
def read_assessments_by_course(course_id: int, db: Session = Depends(get_db)):
    try:
        assessments = db.query(Assessment).filter(Assessment.course_id == course_id).all()
        return assessments
    except Exception as e:
        print("Error reading assessments by course:", e)
        return JSONResponse(status_code=500, content={"message": "Assessment retrieval failed", "error": str(e)})

# @app.put("/assessments/{assessment_id}", response_model=dict)
# def update_assessment(assessment_id: int, assessment: AssessmentUpdate, db: Session = Depends(get_db)):
#     try:
#         db_assessment = db.query(Assessment).filter(Assessment.assessment_id == assessment_id).first()
#         if db_assessment is None:
#             raise HTTPException(status_code=404, detail="Assessment not found")

#         update_data = assessment.dict(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(db_assessment, field, value)

#         db.commit()
#         return JSONResponse(status_code=200, content={"message": "Assessment updated successfully"})
#     except Exception as e:
#         db.rollback()
#         print("Error updating assessment:", e)
#         return JSONResponse(status_code=500, content={"message": "Assessment update failed", "error": str(e)})

@app.delete("/assessments/{assessment_id}", response_model=dict)
def delete_assessment(assessment_id: int, db: Session = Depends(get_db)):
    try:
        db_assessment = db.query(Assessment).filter(Assessment.assessment_id == assessment_id).first()
        if db_assessment is None:
            raise HTTPException(status_code=404, detail="Assessment not found")

        db.delete(db_assessment)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Assessment deleted successfully"})
    except Exception as e:
        db.rollback()
        print("Error deleting assessment:", e)
        return JSONResponse(status_code=500, content={"message": "Assessment deletion failed", "error": str(e)})



# Attendance CRUD Operations
@app.post("/attendance/", response_model=dict)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    attendance_data = attendance.model_dump()
    if attendance_data.get('created_at') is None:
        attendance_data['created_at'] = datetime.now()
    
    db_attendance = Attendance(**attendance_data)
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return {"message": "Attendance created successfully", "attendance_id": db_attendance.attendance_id}

@app.get("/attendance/", response_model=List[AttendanceResponse])
def read_attendance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).offset(skip).limit(limit).all()
    return attendance

@app.get("/attendance/{attendance_id}", response_model=AttendanceResponse)
def read_attendance_record(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return attendance

@app.put("/attendance/{attendance_id}", response_model=dict)
def update_attendance(attendance_id: int, attendance: AttendanceUpdate, db: Session = Depends(get_db)):
    db_attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    update_data = attendance.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_attendance, field, value)
    
    db.commit()
    return {"message": "Attendance updated successfully"}

@app.delete("/attendance/{attendance_id}", response_model=dict)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    db_attendance = db.query(Attendance).filter(Attendance.attendance_id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    db.delete(db_attendance)
    db.commit()
    return {"message": "Attendance deleted successfully"}

@app.get("/attendance_by_course/{course_id}", response_model=List[AttendanceResponse])
def read_attendance_by_course(course_id: int, db: Session = Depends(get_db)):
    try:
        attendance = db.query(Attendance).filter(Attendance.course_id == course_id).all()
        return attendance
    except Exception as e:
        print("Error reading attendance by course:", e)
        return JSONResponse(status_code=500, content={"message": "Attendance retrieval failed", "error": str(e)})

# Fee CRUD Operations
@app.post("/fees/", response_model=dict)
def create_fee(fee: FeeCreate, db: Session = Depends(get_db)):
    db_fee = Fee(**fee.model_dump())
    db.add(db_fee)
    db.commit()
    db.refresh(db_fee)
    return {"message": "Fee record created successfully", "fee_id": db_fee.fee_id}

@app.get("/fees/", response_model=List[FeeResponse])
def read_fees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fees = db.query(Fee).offset(skip).limit(limit).all()
    return fees

@app.get("/fees/{fee_id}", response_model=FeeResponse)
def read_fee(fee_id: int, db: Session = Depends(get_db)):
    fee = db.query(Fee).filter(Fee.fee_id == fee_id).first()
    if fee is None:
        raise HTTPException(status_code=404, detail="Fee record not found")
    return fee

@app.put("/fees/{fee_id}", response_model=dict)
def update_fee(fee_id: int, fee: FeeUpdate, db: Session = Depends(get_db)):
    db_fee = db.query(Fee).filter(Fee.fee_id == fee_id).first()
    if db_fee is None:
        raise HTTPException(status_code=404, detail="Fee record not found")
    
    update_data = fee.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fee, field, value)
    
    db.commit()
    return {"message": "Fee updated successfully"}

@app.delete("/fees/{fee_id}", response_model=dict)
def delete_fee(fee_id: int, db: Session = Depends(get_db)):
    db_fee = db.query(Fee).filter(Fee.fee_id == fee_id).first()
    if db_fee is None:
        raise HTTPException(status_code=404, detail="Fee record not found")
    
    db.delete(db_fee)
    db.commit()
    return {"message": "Fee deleted successfully"}

@app.get("/fees_by_course/{course_id}", response_model=List[FeeResponse])
def read_fees_by_course(course_id: int, db: Session = Depends(get_db)):
    try:
        fees = db.query(Fee).filter(Fee.course_id == course_id).all()
        return fees
    except Exception as e:
        print("Error reading fees by course:", e)
        return JSONResponse(status_code=500, content={"message": "Fee retrieval failed", "error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)