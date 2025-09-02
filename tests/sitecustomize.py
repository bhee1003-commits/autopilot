import sys, pathlib
# tests/의 부모(= 리포 루트)를 sys.path 맨 앞에 추가
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
