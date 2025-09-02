import os, sys, argparse, pathlib, re
from openai import OpenAI

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path", required=True, help="파일 경로(리포 상대)")
    p.add_argument("--instruction", required=True, help="무엇을 바꿀지 지시문")
    args = p.parse_args()

    ws = os.environ.get("GITHUB_WORKSPACE", ".")
    target = pathlib.Path(ws) / args.path
    target.parent.mkdir(parents=True, exist_ok=True)

    before = target.read_text(encoding="utf-8") if target.exists() else ""
    prompt = f"""You are a code generator. Update the *single* file below.
- Return only the final file content between tags <FILE> ... </FILE>.
- Do not include backticks or explanations.

[INSTRUCTION]
{args.instruction}

[CURRENT FILE PATH]
{args.path}

[CURRENT CONTENT]
{before}
"""

    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
    )
    text = resp.choices[0].message.content
    m = re.search(r"<FILE>\n?(.*)\n?</FILE>", text, re.DOTALL)
    new = m.group(1) if m else text

    target.write_text(new, encoding="utf-8")
    print(f"wrote: {args.path} ({len(new)} bytes)")

if __name__ == "__main__":
    main()
