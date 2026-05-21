import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# 데이터를 저장할 JSON 파일 경로
DATA_FILE = "courses.json"

# 수강기록 데이터 구조 정의 (Pydantic을 통한 자동 검증)
class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

# JSON 파일에서 데이터를 읽어오는 함수
def load_courses():
    # 파일이 존재하지 않으면 빈 리스트 반환
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # 파일 형식이 깨져있어도 서버가 종료되지 않도록 예외 처리
        return []

# JSON 파일에 데이터를 덮어쓰는 함수
def save_courses(courses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # ensure_ascii=False로 한글 깨짐 방지, indent=2로 가독성 확보
        json.dump(courses, f, ensure_ascii=False, indent=2)

# (1) GET /courses : 전체 수강기록 리턴
@app.get("/courses")
def get_all_courses():
    courses = load_courses()
    return courses

# (2) POST /courses : 새로운 수강기록 추가
@app.post("/courses")
def add_new_course(course: Course):
    # 기존 데이터 읽기
    courses = load_courses()
    
    # 새로운 데이터 추가 (Pydantic 모델을 딕셔너리로 변환하여 추가)
    new_course_dict = course.model_dump()
    courses.append(new_course_dict)
    
    # 변경된 전체 리스트를 파일에 저장
    save_courses(courses)
    
    return {"message": "수강기록이 성공적으로 추가되었습니다.", "data": new_course_dict}