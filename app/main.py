from fastapi import FastAPI
from app.api.ping import router as ping_router

app = FastAPI(title="UST Autopilot App")

# 레거시 호환: /ping 도 열어둔다 (테스트가 둘 중 무엇을 쓰든 대응)
@app.get("/ping")
def legacy_ping():
    return {"ping": "pong"}

# 신규 엔드포인트: /api/ping
app.include_router(ping_router, prefix="/api")

if __name__ == "__main__":
    # 로컬 실행용 (테스트에는 영향 없음)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
