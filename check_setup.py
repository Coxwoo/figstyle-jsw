"""처음 쓰는 PC 에서 figstyle 에 필요한 것을 확인한다 — Python 패키지와 글꼴.

    python check_setup.py              # 확인만 한다
    python check_setup.py --install    # 빠진 Python 패키지를 설치하고 (requirements.txt) matplotlib 글꼴 목록을 새로 만든다

글꼴은 자동으로 설치하지 않는다 — 아래 안내 (공식 배포처) 대로 설치한 뒤 --install 로 글꼴 목록을 새로 만들고 다시 확인한다.
끝 코드: 꼭 필요한 것이 모두 있으면 0, 아니면 1.
"""
import argparse
import importlib
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGES = [  # (import 이름, pip 이름, 최소 판, 쓰는 곳)
    ("matplotlib", "matplotlib", "3.7", "그래프"),
    ("numpy", "numpy", "1.24", "예시 데이터"),
]
FONTS = [  # (글꼴, 꼭 필요한가, 쓰는 곳, 없을 때)
    ("Arial", True, "축 제목·눈금", "비슷한 글꼴 (Liberation Sans → DejaVu Sans) 로 바뀐다"),
    ("Arial Narrow", False, "그림 안 글자 (범례·주석)", "Arial 로 대신 — 그림 안 글자가 조금 넓어진다"),
    ("Noto Sans KR", False, "그림에 한글을 쓸 때만", "맑은 고딕 등 다른 한글 글꼴로"),
]
FONT_HELP = {
    "Arial": "Windows·macOS 에 기본으로 있다. Linux 는 같은 폭의 대체 글꼴: sudo apt install fonts-liberation",
    "Arial Narrow": "Microsoft Office 와 함께 설치된다. Linux 는 fonts-liberation 의 Liberation Sans Narrow",
    "Noto Sans KR": ("https://fonts.google.com/noto/specimen/Noto+Sans+KR → Get font → Download all → "
                     "압축 속 static/ 의 NotoSansKR-Regular.ttf·NotoSansKR-Bold.ttf 를 설치 "
                     "(Windows: 오른쪽 클릭 → 설치, macOS: 서체 관리자, Linux: ~/.local/share/fonts 에 복사 후 fc-cache -f)"),
}
OK, NO, SOSO = "✓", "✗", "△"


def _version_ok(have, need):
    def nums(v):
        out = []
        for part in str(v).split("."):
            digits = "".join(ch for ch in part if ch.isdigit())
            if not digits:
                break
            out.append(int(digits))
        return out
    return nums(have) >= nums(need)


def check_packages():
    rows, missing = [], []
    for mod, pip_name, need, use in PACKAGES:
        try:
            ver = getattr(importlib.import_module(mod), "__version__", "?")
            good = ver == "?" or _version_ok(ver, need)
            rows.append((OK if good else NO, f"{pip_name} {ver}", use + ("" if good else f" — {need} 이상 필요")))
            if not good:
                missing.append(pip_name)
        except ImportError:
            rows.append((NO, pip_name, f"{use} — 없음"))
            missing.append(pip_name)
    return rows, missing


def check_fonts():
    """설치된 글꼴을 새로 읽어 본다 (matplotlib 글꼴 목록과도 비교)."""
    try:
        from matplotlib import font_manager as fm
    except ImportError:
        return [(NO, "글꼴", "matplotlib 을 설치한 뒤 다시 확인")], [], False
    files = {}
    for entry in fm.FontManager().ttflist:                     # 지금 설치된 글꼴 (캐시에는 쓰지 않는다)
        files.setdefault(entry.name, []).append(Path(entry.fname).name)
    cached = {f.name for f in fm.fontManager.ttflist}
    rows, missing_required, stale = [], [], False
    for name, required, use, fallback in FONTS:
        found = files.get(name, [])
        if not found:
            rows.append((NO if required else SOSO, name, f"{use} — 없음 ({fallback})"))
            if required:
                missing_required.append(name)
            continue
        if all("VF" in fn or "[" in fn for fn in found):
            rows.append((SOSO, name, f"{use} — 가변 판 (VF) 만 있음: 그림에서 가늘게 나옴 → static 판 설치 권장"))
        else:
            rows.append((OK, name, use))
        if name not in cached:
            stale = True
    return rows, missing_required, stale


def refresh_font_cache():
    try:
        from matplotlib import font_manager as fm
        fm._load_fontmanager(try_read_cache=False)
        print("  matplotlib 글꼴 목록을 새로 만들었다")
    except Exception as e:
        print(f"  matplotlib 글꼴 목록을 새로 만들지 못함 ({e}) — matplotlib 캐시 폴더의 fontlist-*.json 을 지운다")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="figstyle 에 필요한 것을 확인한다")
    parser.add_argument("--install", action="store_true", help="빠진 Python 패키지를 설치하고 글꼴 목록을 새로 만든다")
    args = parser.parse_args()

    print(f"Python {platform.python_version()} ({platform.system()})")
    rows, missing = check_packages()
    if args.install and missing:
        print(f"\n설치: {', '.join(missing)}")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(HERE / "requirements.txt")], check=False)
        importlib.invalidate_caches()
        rows, missing = check_packages()
    font_rows, missing_fonts, stale = check_fonts()
    if args.install and stale:
        refresh_font_cache()
        font_rows, missing_fonts, stale = check_fonts()

    print("\n[Python 패키지]")
    for mark, what, note in rows:
        print(f"  {mark} {what:<22} {note}")
    print("\n[글꼴]")
    for mark, what, note in font_rows:
        print(f"  {mark} {what:<22} {note}")

    todo = []
    if missing:
        todo.append("python check_setup.py --install   # Python 패키지 설치")
    for name in missing_fonts + [r[1] for r in font_rows if r[0] == SOSO and r[1] in FONT_HELP]:
        todo.append(f"{name}: {FONT_HELP[name]}")
    if stale:
        todo.append("글꼴을 설치했으면: python check_setup.py --install   # matplotlib 글꼴 목록 새로 만들기")
    print("\n" + ("할 일:\n  - " + "\n  - ".join(dict.fromkeys(todo)) if todo else "모두 준비됨"))
    sys.exit(1 if (missing or missing_fonts) else 0)


if __name__ == "__main__":
    main()
