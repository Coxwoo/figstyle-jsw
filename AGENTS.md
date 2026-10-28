# AGENTS.md — Codex 용 안내

이 저장소는 Claude Code 를 기준으로 쓴 그래프 스타일이다. Codex 도 같은 파일을 정본으로 삼아 같은 그림을 그린다.

- 할 일의 순서는 `SKILL.md` 다 — 준비 (설치 확인) → 규칙 읽기 → 주장 한 문장 → 데이터 종류 확인 → 그리기 → 그림 확인 → README 한 줄.
- 규칙은 `rules/graph-style.md`, 값은 `figstyle.py` 한 곳에 있으니 바꾸지 않는다. 예시는 `examples/make_examples.py`.
- 처음에는 `python check_setup.py` 로 설치를 확인한다. 빠진 Python 패키지는 `--install`, 글꼴은 안내를 보여 주고 사용자 확인 뒤 설치를 돕는다.
- Claude Code 에만 있는 것 — skill 폴더 (`~/.claude/skills/…`), `CLAUDE.md`, "이 skill 폴더 (Base directory)" 같은 말, Claude 의 도구 이름 — 은 Codex 환경에 맞게 스스로 판단해 같은 일을 한다 (예: skill 폴더 = 이 저장소 폴더).
- 판단이 갈리는 곳 (설치 권한, 네트워크, 글꼴이 없을 때) 은 사용자에게 알리고 정한다.
