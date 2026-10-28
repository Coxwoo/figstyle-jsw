"""figstyle — 그래프를 늘 같은 모양으로 그리는 matplotlib 스타일.

누가 어느 컴퓨터에서 그려도 같은 모양이 되게 한다. 규칙과 이유는 rules/graph-style.md.

쓰는 법:
    import figstyle as fs                          # import 하면 matplotlib rcParams 가 이 스타일로 바뀐다
    fig, ax = fs.plt.subplots(figsize=fs.SIZE, layout="constrained")
    ax.plot(x, y, **fs.MAIN)                       # 주 결과 — 검정 실선
    ax.plot(x2, y2, **fs.COMP)                     # 비교 (sim·이전 설계) — 파랑 점선
    ax.plot(xk, yk, **fs.KEY_DOT)                  # 핵심 한 곳 — 빨강 점
    fs.key_text(ax, xk, yk, "9.5 MHz", xytext=(12, -4), va="center")   # 그 점의 빨강 굵은 숫자
    fs.save(fig, "gain_vs_freq")                   # figures/gain_vs_freq.png, figures/svg/, figures/pdf/
예시 전부: examples/make_examples.py.

규칙 (요약 — 자세히는 rules/graph-style.md):
    - 그림 하나에 축 하나 (subplot·이중 y 축 없음), 곡선은 1–2 개. 기준선·한계 띠·강조하지 않는 것은 회색.
    - 검정 실선 = 주 결과, 파랑 점선 = 비교, 빨강 = 그림마다 핵심 한 곳 (굵은 숫자와 그 점).
    - 정보 밀도: 위에 더해 그 주장을 받치는 회색 표시 1–3 개 (기준선, 차이 화살표, 짧은 숫자 글).
    - 범례는 곡선이 둘일 때만, 상자 없이. 조건 문장은 그림에 넣지 않는다 (슬라이드 글로).
    - 글꼴: 축 제목·눈금 Arial, 그림 안 글자 Arial Narrow. 없으면 비슷한 글꼴로 바뀐다 (SANS·NARROW).
    - 크기 6.0 × 4.0 in, 300 dpi — PowerPoint 에 원래 크기로 넣으면 그림 글자가 12–15 pt.
    - 저장: PNG 는 figures/, SVG (PPT 용 — 글자는 윤곽선) 는 figures/svg/, PDF (논문용 — 글꼴 포함) 는 figures/pdf/.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.ticker import LogLocator, NullFormatter  # noqa: E402


def _first_font(*names):
    """설치된 글꼴 중 처음 것 — 하나도 없으면 matplotlib 에 늘 있는 DejaVu Sans."""
    have = {f.name for f in font_manager.fontManager.ttflist}
    return next((n for n in names if n in have), "DejaVu Sans")


def _has_regular(name):
    """보통 굵기 (400) 판이 설치돼 있나 — 가변 글꼴 (VF) 만 있으면 matplotlib 이 Thin 으로 그려서 쓰지 않는다."""
    return any(f.name == name and f.weight in (400, "normal", "regular") for f in font_manager.fontManager.ttflist)


SANS = _first_font("Arial", "Liberation Sans", "Helvetica")
NARROW = _first_font("Arial Narrow", "Liberation Sans Narrow", SANS)
KR = [n for n in ("Noto Sans KR", "Malgun Gothic", "AppleGothic", "NanumGothic") if _has_regular(n)][:1]   # 한글 대체 (있을 때만)

INK, INK2, MUTED, GRID, BAND = "#111111", "#4A4A4A", "#767676", "#E5E5E3", "#EDEEE9"
GRAY = "#A8A8A8"                             # 강조하지 않는 막대·곡선
RED, BLUE = "#B4161E", "#1F5FD6"            # 핵심 한 곳, 비교
SIZE, DPI = (6.0, 4.0), 300
MAIN = {"color": INK, "lw": 2.0, "ls": "-"}
COMP = {"color": BLUE, "lw": 2.0, "ls": (0, (4, 2))}
REF = {"color": GRAY, "lw": 1.2, "ls": (0, (3, 2))}         # 기준선·목표선
KEY_DOT = {"marker": "o", "ms": 8, "mfc": RED, "mec": "white", "mew": 1.5, "ls": "none", "zorder": 5, "clip_on": False}
DOT = {"marker": "o", "ms": 7, "mfc": INK, "mec": "white", "mew": 1.3, "ls": "none", "zorder": 5, "clip_on": False}

plt.rcParams.update({
    "font.family": [SANS] + KR, "font.size": 12,
    "axes.labelsize": 13, "axes.labelcolor": INK, "axes.edgecolor": INK2, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "axes.axisbelow": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "xtick.color": INK2, "ytick.color": INK2,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8, "xtick.major.size": 4, "ytick.major.size": 4,
    "xtick.minor.width": 0.6, "xtick.minor.size": 2,
    "lines.solid_capstyle": "round", "lines.dash_capstyle": "round", "lines.solid_joinstyle": "round",
    "legend.frameon": False, "legend.handlelength": 2.6,
    "mathtext.fontset": "custom", "mathtext.rm": SANS, "mathtext.it": f"{SANS}:italic", "mathtext.bf": f"{SANS}:bold",
    "svg.fonttype": "path", "svg.hashsalt": "figstyle", "pdf.fonttype": 42,
    "savefig.facecolor": "white",
})


def minus(s):
    """글자 속 하이픈을 마이너스 기호로 — 축 눈금 (unicode_minus) 과 같게."""
    return s.replace("-", "−")


def text(ax, x, y, s, size=13, color=INK, weight="normal", **kw):
    """그림 안 글자 — Arial Narrow."""
    return ax.annotate(s, (x, y), family=[NARROW] + KR, fontsize=size, color=color, fontweight=weight, **kw)


def key_text(ax, x, y, s, **kw):
    """그림의 핵심 숫자 — 빨강 굵게. 위치는 점에서 띄운 거리 (xytext, points)."""
    return text(ax, x, y, minus(s), size=15, color=RED, weight="bold", textcoords="offset points", **kw)


def note(ax, x, y, s, **kw):
    """주장을 받치는 짧은 회색 글 (기준선 이름, 차이 숫자)."""
    return text(ax, x, y, minus(s), size=12, color=MUTED, **kw)


def legend(ax, handles, **kw):
    """범례 — 곡선이 둘일 때만, 상자 없이."""
    return ax.legend(handles=handles, prop={"family": [NARROW] + KR, "size": 13}, labelcolor=INK, **kw)


def ref_hline(ax, y, label=None, x=None, **kw):
    """회색 가로 기준선 (목표·한계). label 은 선 위 왼쪽 (x 를 주면 그 자리) 에 회색 글로."""
    ax.axhline(y, **REF)
    if label:
        xs = x if x is not None else ax.get_xlim()[0]
        note(ax, xs, y, label, xytext=(4, 4), textcoords="offset points", va="bottom", **kw)


def bars(ax, labels, values, key=None, fmt="{:g}"):
    """막대 — 강조하지 않는 막대는 회색, key (번호) 하나만 빨강. 막대 위에 값."""
    colors = [RED if i == key else GRAY for i in range(len(values))]
    ax.bar(labels, values, color=colors, width=0.6, zorder=3)
    ax.grid(axis="x", visible=False)
    for i, v in enumerate(values):
        style = {"color": RED, "weight": "bold", "size": 14} if i == key else {"color": INK2, "weight": "normal", "size": 12}
        text(ax, i, v, minus(fmt.format(v)), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
             size=style["size"], color=style["color"], weight=style["weight"],
             bbox={"boxstyle": "square,pad=0.15", "fc": "white", "ec": "none"})   # 기준선이 숫자를 가르지 않게


def hz(f):
    """decade 눈금 글자 — 1 kHz, 10 MHz, 1 GHz …"""
    for unit, scale in (("GHz", 1e9), ("MHz", 1e6), ("kHz", 1e3), ("Hz", 1.0)):
        if f >= scale:
            return f"{f / scale:g} {unit}"


def freq_log_axis(ax, lo, hi):
    """로그 주파수 축 — 격자는 decade 마다, 그 사이는 작은 눈금만.
    눈금 글자도 decade 마다지만, 7 decade 가 넘으면 글자가 겹치지 않게 하나 걸러 단다."""
    ax.set_xscale("log")
    ax.set_xlim(lo, hi)
    decades = [10.0 ** k for k in range(round(math.log10(lo)), round(math.log10(hi)) + 1)]
    step = 1 if len(decades) <= 7 else 2
    ax.set_xticks(decades, [hz(f) if i % step == 0 else "" for i, f in enumerate(decades)])
    ax.xaxis.set_minor_locator(LogLocator(subs=range(2, 10)))
    ax.xaxis.set_minor_formatter(NullFormatter())


def save(fig, name, out="figures"):
    """<out>/<이름>.png (300 dpi), <out>/svg/<이름>.svg, <out>/pdf/<이름>.pdf.
    날짜·프로그램 이름을 파일에 넣지 않아, 다시 그려도 같은 파일이 된다."""
    out = Path(out)
    for sub in ("svg", "pdf"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.png", dpi=DPI, metadata={"Software": None})
    fig.savefig(out / "svg" / f"{name}.svg", metadata={"Date": None, "Creator": None})
    fig.savefig(out / "pdf" / f"{name}.pdf", metadata={"CreationDate": None, "Creator": None, "Producer": None})
    plt.close(fig)
    print(f"  → {out.as_posix()}/{name}.png, svg/, pdf/")
