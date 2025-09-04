import os, yaml, re, sys, subprocess
from pathlib import Path

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_KEY:
    print("OPENAI_API_KEY not set", file=sys.stderr); sys.exit(78)

try:
    # openai>=1.x
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    def gen_code(system, user):
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}],
            temperature=0.2,
        )
        return r.choices[0].message.content
except Exception:
    # 구버전 fallback
    import openai as oai
    oai.api_key = OPENAI_KEY
    def gen_code(system, user):
        r = oai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system},
                      {"role":"user","content":user}],
            temperature=0.2,
        )
        return r.choices[0].message["content"]

ROOT = Path(__file__).resolve().parents[1]
roadmap = ROOT/".multiverse/roadmap.yaml"
data = yaml.safe_load(roadmap.read_text())

made_any = False
for t in data.get("tasks", []):
    if t.get("status") != "todo": continue
    if t.get("target") not in {"exp","beta","main"}: continue
    out_path = ROOT / t["path"]
    out_path.parent.mkdir(parents=True, exist_ok=True)

    system = (
        "You are generating safe, minimal Flask modules for Cloud Run.\n"
        "Rules:\n"
        "- Output ONLY Python code for a single file.\n"
        "- Provide a function def register(app): and register a Blueprint if routes are needed.\n"
        "- No external libs besides Flask std usage.\n"
        "- Must not modify other files.\n"
    )
    user = f"""Repository root has app/main.py that auto-loads app.experiments.* modules by calling register(app) if present.

Write code for: {t['path']}
Task ID: {t['id']}
Requirements:
{t['prompt']}
"""

    content = gen_code(system, user)
    # 코드 블록 제거(markdown fence → 순수 파이썬)
    content = re.sub(r"^```(?:python)?\s*|```$", "", content.strip(), flags=re.MULTILINE)

    out_path.write_text(content.strip() + "\n")
    print(f"[GENERATED] {out_path}")
    t["status"] = "done"
    made_any = True

# 로드맵 저장
if made_any:
    roadmap.write_text(yaml.safe_dump(data, sort_keys=False))
else:
    print("No tasks generated.")

sys.exit(0 if made_any else 0)
