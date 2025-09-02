# 혹시 작업 디렉터리가 리포 루트일 때도 대비 (중복 추가 방지)
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
