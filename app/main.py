from fastapi import FastAPI
from app.api.ping import router as ping_router

def create_app() -> FastAPI:
    app = FastAPI(title="UST Autopilot App")
    # Legacy: /ping
    @app.get("/ping")
    def legacy_ping():
        return {"ping": "pong"}
    # New: /api/ping
    app.include_router(ping_router, prefix="/api")
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
