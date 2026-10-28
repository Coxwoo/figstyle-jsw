# figstyle — 같은 모양의 그래프

- matplotlib 그래프를 누가 그려도 같은 모양으로 만든다 — `import figstyle` 한 줄이면 색·선·글꼴·크기가 맞춰진다.
- 철학은 "Simple is best": 그림 하나에 주장 하나, 축 하나, 곡선 1–2 개, 빨강은 핵심 한 곳.
- Claude Code 를 기준으로 썼다 (skill). Codex 는 `AGENTS.md` 를 읽고 같은 파일을 따른다. 발표 자료 양식은 함께 쓰는 저장소 [simple-pt](https://github.com/Coxwoo/simple-pt-jsw).

![예시 — 곡선 하나, 목표선, 한계 밖 띠, 고른 동작점 (가짜 데이터)](examples/figures/noise_vs_current.png)

## 목차

1. 파일 — 무엇이 어디에
2. 설치 — 처음 한 번
3. Claude Code 에서
4. Codex 에서
5. 직접 — Python
6. 규칙 한눈에
7. 라이선스

---

## 1. 파일

| 파일 | 내용 |
|---|---|
| `figstyle.py` | 스타일의 정본 — 색·선·크기 상수, rcParams, 도우미 (`key_text`, `ref_hline`, `note`, `bars`, `freq_log_axis`, `save`) |
| `rules/graph-style.md` | 규칙과 이유 |
| `SKILL.md` | Claude Code skill — 준비, 그리는 순서, 꼭 지킬 것 |
| `CLAUDE.md` | 이 저장소를 Claude Code 로 열었을 때 |
| `AGENTS.md` | Codex 용 안내 — 같은 파일을 따르고, Claude Code 전용인 부분은 Codex 가 판단 |
| `check_setup.py`, `requirements.txt` | 설치 확인 — Python 패키지와 글꼴 |
| `examples/` | 가짜 데이터 예시 8 개 — `make_examples.py`, 그림 `figures/` (한 줄 설명 `figures/README.md`) |

## 2. 설치 — 처음 한 번

```bash
python check_setup.py              # 무엇이 있고 무엇이 빠졌는지
python check_setup.py --install    # 빠진 Python 패키지 설치 + matplotlib 글꼴 목록 새로 만들기
```

- 패키지는 `requirements.txt` (matplotlib, numpy).
- 글꼴: Arial (축), Arial Narrow (그림 안 글자 — Office 와 함께), 한글을 쓸 때 Noto Sans KR ([Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+KR) 의 static 판). 없으면 비슷한 글꼴 (Liberation Sans → DejaVu Sans) 로 바뀐다.

## 3. Claude Code 에서

```bash
git clone https://github.com/Coxwoo/figstyle-jsw.git ~/.claude/skills/figstyle
```

- 그 뒤 어느 프로젝트에서든 "figstyle 로 이 데이터 그래프 그려줘". 처음이면 Claude 가 `check_setup.py` 로 설치부터 확인한다.
- 이 저장소 폴더를 Claude Code 로 열면 `CLAUDE.md` 가 `SKILL.md` 를 가리킨다.

## 4. Codex 에서

- 이 저장소를 받아 그 폴더에서 Codex 를 열고 "figstyle 로 그래프 그려줘".
- Codex 는 `AGENTS.md` 를 읽고 `SKILL.md`·`rules/graph-style.md` 를 그대로 따른다. Claude Code 에만 있는 부분은 Codex 가 환경에 맞게 판단한다.

## 5. 직접 — Python

```bash
python examples/make_examples.py
```

```python
import figstyle as fs

fig, ax = fs.plt.subplots(figsize=fs.SIZE, layout="constrained")
ax.plot(x, y, **fs.MAIN)                         # 주 결과 — 검정 실선
ax.plot(x2, y2, **fs.COMP)                       # 비교 — 파랑 점선
fs.ref_hline(ax, 10, "Target 10")                # 회색 기준선
ax.plot(xk, yk, **fs.KEY_DOT)                    # 핵심 한 곳 — 빨강 점
fs.key_text(ax, xk, yk, "8.5 @ 150", xytext=(0, -22), ha="center")
fs.save(fig, "noise_vs_current")                 # figures/noise_vs_current.png, svg/, pdf/
```

## 6. 규칙 한눈에

| 역할 | 모양 |
|---|---|
| 주 결과 | 검정 실선 (`fs.MAIN`) |
| 비교 | 파랑 점선 (`fs.COMP`) |
| 핵심 한 곳 | 빨강 점과 굵은 숫자 (`fs.KEY_DOT`, `fs.key_text`) |
| 기준선·한계 | 회색 (`fs.ref_hline`, `fs.note`, `fs.BAND`) |

- 축 하나, 곡선 1–2 개, 회색 보조 1–3 개. 범례는 곡선이 둘일 때만. 조건 문장은 그림 밖. 6 × 4 in, 300 dpi.
- 자세히는 `rules/graph-style.md`.

## 7. 라이선스

MIT — `LICENSE`.
