"""figstyle 예시 그림 — 가상의 증폭기 "Demo Amp" 의 가짜 데이터 (실제 측정·sim 이 아니다).

    python examples/make_examples.py              # examples/figures/ 에 PNG, svg/, pdf/

그림마다 주장 하나, 축 하나, 곡선 1–2 개, 빨강은 핵심 한 곳. 그림 목록은 examples/figures/README.md.
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import figstyle as fs  # noqa: E402

OUT = Path(__file__).resolve().parent / "figures"


def new_fig():
    return fs.plt.subplots(figsize=fs.SIZE, layout="constrained")


def gain_vs_freq():
    """두 곡선 (이번·이전 설계) + 핵심 점 (UGF) + 회색 기준선·차이 화살표."""
    f = np.logspace(1, 9, 1600)

    def gain_db(a0_db, p1, p2):
        h = 10 ** (a0_db / 20) / ((1 + 1j * f / p1) * (1 + 1j * f / p2))
        return 20 * np.log10(np.abs(h))

    new, old = gain_db(76, 1.5e3, 60e6), gain_db(62, 2.6e3, 30e6)
    ugf = np.interp(0, new[::-1], f[::-1])           # 0 dB 를 지나는 주파수
    fig, ax = new_fig()
    l1, = ax.plot(f, new, **fs.MAIN, label="This design")
    l2, = ax.plot(f, old, **fs.COMP, label="Previous")
    fs.freq_log_axis(ax, 1e1, 1e9)
    ax.set_ylim(-40, 90)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Open-loop gain (dB)")
    fs.ref_hline(ax, 0, "0 dB")
    ax.annotate("", xy=(60, 76), xytext=(60, 62), arrowprops={"arrowstyle": "<->", "color": fs.GRAY, "lw": 1.2})
    fs.note(ax, 60, 69, "+14 dB", xytext=(6, 0), textcoords="offset points", va="center")
    ax.plot(ugf, 0, **fs.KEY_DOT)
    fs.key_text(ax, ugf, 0, f"UGF {ugf / 1e6:.1f} MHz", xytext=(10, 10), va="bottom")
    fs.legend(ax, [l1, l2], loc="upper right")
    fs.save(fig, "gain_vs_freq", OUT)
    return {"UGF (MHz)": round(ugf / 1e6, 2)}


def noise_spectrum():
    """두 곡선 (로그·로그) + 목표선 + 핵심 점."""
    f = np.logspace(1, 7, 600)
    new = 8.5 * np.sqrt(1 + 2e3 / f)
    old = 13.0 * np.sqrt(1 + 5e3 / f)
    fig, ax = new_fig()
    l1, = ax.plot(f, new, **fs.MAIN, label="This design")
    l2, = ax.plot(f, old, **fs.COMP, label="Previous")
    fs.freq_log_axis(ax, 1e1, 1e7)
    ax.set_yscale("log")
    ax.set_ylim(3, 400)                              # 핵심 숫자가 눈금 글자와 겹치지 않게 아래를 비운다
    ax.set_yticks([5, 10, 20, 50, 100, 200], ["5", "10", "20", "50", "100", "200"])
    ax.yaxis.set_minor_formatter(fs.NullFormatter())
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Input-referred noise (nV/√Hz)")
    fs.ref_hline(ax, 10, "Target 10 nV/√Hz")
    fk = 1e6
    vk = 8.5 * np.sqrt(1 + 2e3 / fk)
    ax.plot(fk, vk, **fs.KEY_DOT)
    fs.key_text(ax, fk, vk, f"{vk:.1f} nV/√Hz", xytext=(0, -24), ha="center", va="top")
    fs.legend(ax, [l1, l2], loc="upper right")
    fs.save(fig, "noise_spectrum", OUT)
    return {"noise @ 1 MHz": round(vk, 2)}


def noise_budget():
    """막대 — 핵심 막대 하나만 빨강."""
    fig, ax = new_fig()
    fs.bars(ax, ["Amplifier", "Sensor", "ADC", "Other"], [64, 21, 10, 5], key=0, fmt="{:g} %")
    ax.set_ylim(0, 75)
    ax.set_ylabel("Share of total noise (%)")
    fs.save(fig, "noise_budget", OUT)
    return {}


def noise_vs_current():
    """곡선 하나 + 목표선 + 한계 밖 회색 띠 + 핵심 점 (고른 동작점)."""
    i = np.linspace(20, 250, 400)
    vn = 70 / np.sqrt(i) + 2.8
    fig, ax = new_fig()
    ax.axvspan(170, 250, color=fs.BAND, zorder=0, lw=0)
    ax.plot(i, vn, **fs.MAIN)
    ax.set_xlim(20, 250)
    ax.set_ylim(0, 20)
    ax.set_xlabel("Input-stage current (µA)")
    ax.set_ylabel("Input-referred noise (nV/√Hz)")
    fs.ref_hline(ax, 10, "Target 10 nV/√Hz")
    fs.note(ax, 174, 19.4, "Over 200 µW", va="top")
    ik = 150
    vk = 70 / np.sqrt(ik) + 2.8
    ax.plot(ik, vk, **fs.KEY_DOT)
    fs.key_text(ax, ik, vk, f"{vk:.1f} nV/√Hz @ {ik} µA", xytext=(0, -22), ha="center", va="top")
    fs.save(fig, "noise_vs_current", OUT)
    return {"noise @ 150 uA": round(vk, 2)}


def gain_vs_temp():
    """곡선 하나 + 최소선 + 핵심 점 (가장 나쁜 곳)."""
    t = np.linspace(-20, 100, 300)
    g = 76 - 0.03 * (t - 27) - 0.0002 * (t - 27) ** 2
    fig, ax = new_fig()
    ax.plot(t, g, **fs.MAIN)
    ax.set_xlim(-20, 100)
    ax.set_ylim(66, 80)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("DC gain (dB)")
    fs.ref_hline(ax, 70, "Min 70 dB")
    ax.plot(t[-1], g[-1], **fs.KEY_DOT)
    fs.key_text(ax, t[-1], g[-1], f"{g[-1]:.1f} dB", xytext=(0, 12), ha="right", va="bottom")
    fs.save(fig, "gain_vs_temp", OUT)
    return {"gain @ 100 C": round(float(g[-1]), 2)}


def noise_by_corner():
    """막대 — 가장 나쁜 corner 만 빨강, 목표선 회색."""
    fig, ax = new_fig()
    fs.bars(ax, ["TT", "FF", "SS", "FS", "SF"], [8.5, 8.1, 9.6, 8.8, 9.2], key=2)
    ax.set_ylim(0, 12)
    ax.set_xlabel("Process corner")
    ax.set_ylabel("Input-referred noise (nV/√Hz)")
    fs.ref_hline(ax, 10, "Target 10", x=3.6)
    fs.save(fig, "noise_by_corner", OUT)
    return {}


def pm_vs_load():
    """곡선 하나 + 최소선 + 핵심 점 (기본 부하) + 끝 값 회색 글."""
    c = np.linspace(0.5, 20, 300)
    pm = 82 - 12 * np.log(1 + c / 1.5)
    fig, ax = new_fig()
    ax.plot(c, pm, **fs.MAIN)
    ax.set_xlim(0, 20)
    ax.set_ylim(30, 90)
    ax.set_xlabel("Load capacitance (pF)")
    ax.set_ylabel("Phase margin (°)")
    fs.ref_hline(ax, 45, "Min 45°")
    ck = 2.0
    pk = 82 - 12 * np.log(1 + ck / 1.5)
    ax.plot(ck, pk, **fs.KEY_DOT)
    fs.key_text(ax, ck, pk, f"{pk:.0f}° @ {ck:g} pF", xytext=(10, 6), va="bottom")
    fs.note(ax, c[-1], pm[-1], f"{pm[-1]:.0f}°", xytext=(0, 8), textcoords="offset points", ha="right", va="bottom")
    fs.save(fig, "pm_vs_load", OUT)
    return {"PM @ 2 pF": round(pk, 1), "PM @ 20 pF": round(float(pm[-1]), 1)}


def step_settling():
    """시간 축 곡선 하나 + 허용 띠 (회색) + 핵심 점 (들어간 시각)."""
    t = np.linspace(0, 1e-6, 4000)
    zeta, wn = 0.6, 2 * np.pi * 3e6
    wd = wn * np.sqrt(1 - zeta ** 2)
    y = 1 - np.exp(-zeta * wn * t) / np.sqrt(1 - zeta ** 2) * np.sin(wd * t + np.arccos(zeta))
    v = 0.5 * y
    out = np.nonzero(np.abs(y - 1) > 0.01)[0]
    k = out[-1] + 1                                  # 마지막으로 ±1 % 밖이던 곳 다음
    fig, ax = new_fig()
    ax.axhspan(0.5 * 0.99, 0.5 * 1.01, color=fs.BAND, zorder=0, lw=0)
    ax.plot(t * 1e6, v, **fs.MAIN)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.65)
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Output (V)")
    fs.note(ax, 0.98, 0.5 * 1.01, "±1 %", xytext=(0, 4), textcoords="offset points", ha="right", va="bottom")
    ax.plot(t[k] * 1e6, v[k], **fs.KEY_DOT)
    fs.key_text(ax, t[k] * 1e6, v[k], f"{t[k] * 1e9:.0f} ns", xytext=(0, -16), ha="center", va="top")
    fs.save(fig, "step_settling", OUT)
    return {"settling (ns)": round(t[k] * 1e9, 1)}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"fonts: {fs.SANS} / {fs.NARROW} / KR {fs.KR}")
    values = {}
    for make in (gain_vs_freq, noise_spectrum, noise_budget, noise_vs_current,
                 gain_vs_temp, noise_by_corner, pm_vs_load, step_settling):
        values.update(make())
    print("key values:", values)
