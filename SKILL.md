---
name: figstyle
description: 그래프 (matplotlib) 를 figstyle 스타일로 그린다 — 축 하나·곡선 1–2 개, 검정 실선 주 결과·파랑 점선 비교·빨강 핵심 한 곳, 6 × 4 in, PNG·SVG·PDF. "그래프 그려줘", "figure 만들어줘", "PT 에 넣을 그림", "이 데이터 plot 해줘" 같은 요청에 쓴다.
---

# figstyle — 같은 모양의 그래프

이 skill 폴더 (Base directory) 에 스타일 `figstyle.py`, 규칙 `rules/graph-style.md`, 예시 `examples/make_examples.py` 가 있다.

## 순서

1. 그리기 전에 `rules/graph-style.md` 를 읽는다.
2. 그림이 보일 주장을 한 문장으로 정한다. 모르면 사용자에게 묻는다.
   새 그림을 여러 개 만들 때는 후보 (무엇을 보이나·데이터·수고) 와 추천을 먼저 내고, 합의한 뒤에 그린다.
3. 데이터 종류를 확인한다 — 측정, sim (pre/post-layout), 계산. 한 그림에 섞지 않는다.
4. 코드를 쓴다 (예시 8 개는 `examples/make_examples.py`):

   ```python
   import sys
   sys.path.insert(0, r"<이 skill 폴더>")
   import figstyle as fs

   fig, ax = fs.plt.subplots(figsize=fs.SIZE, layout="constrained")
   ax.plot(x, y, **fs.MAIN)                          # 주 결과
   ax.plot(x2, y2, **fs.COMP)                        # 비교 — 있을 때만
   fs.ref_hline(ax, target, "Target …")              # 회색 기준선
   ax.plot(xk, yk, **fs.KEY_DOT)                     # 핵심 한 곳
   fs.key_text(ax, xk, yk, "…", xytext=(10, 6))
   fs.save(fig, "<내용_이름>", out="figures")        # figures/<이름>.png, svg/, pdf/
   ```

5. 그린 PNG 를 열어 본다 — 글자 겹침, 잘린 점·글, 빨강이 한 곳인지.
6. `figures/README.md` 에 한 줄 더한다 — 맨 앞에 [측정]·[post-layout sim]·[pre-layout sim]·[계산].

## 꼭 지킬 것

- 축 하나, 곡선 1–2 개, 빨강 한 곳, 회색 보조 1–3 개.
- 범례는 곡선이 둘일 때만. 조건 문장은 그림 밖 (슬라이드 캡션) 에.
- 크기는 그대로 (6 × 4 in, 300 dpi). 다른 판은 원본을 두고 새 이름으로.
- 회로도·블럭도·사진에는 이 스타일을 쓰지 않는다.
