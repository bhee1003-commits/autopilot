from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def root():
    return "OK: root", 200

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    # 로컬 실행용 (Cloud Run에서는 gunicorn이 사용됨)
    import os
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
