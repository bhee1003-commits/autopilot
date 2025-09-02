from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping():
    # 테스트 호환을 위해 가장 보편적인 응답 스키마 사용
    return {"ping": "pong"}
