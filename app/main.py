from flask import Flask, jsonify
import os

def create_app() -> "Flask":
    app = Flask(__name__)

    @app.get("/")
    def root():
        return "OK: root", 200

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app

# Cloud Run의 빌드팩 Procfile에서 app.main:app 또는 app.main:create_app 둘 다 대응
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
