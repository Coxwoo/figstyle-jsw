# 예시 그림 — 가상의 증폭기 "Demo Amp"

모두 `examples/make_examples.py` 가 만든 **가짜 데이터**다 (실제 측정·sim 이 아니다).

- [가짜 데이터] `gain_vs_freq` — 이번 대 이전 설계의 이득, UGF 한 점 (곡선 둘 + 0 dB 선 + 차이 화살표)
- [가짜 데이터] `noise_spectrum` — 입력 환산 잡음 스펙트럼, 1 MHz 한 점 (로그·로그 + 목표선)
- [가짜 데이터] `noise_budget` — 잡음 몫 막대, 증폭기만 빨강
- [가짜 데이터] `noise_vs_current` — 잡음 대 입력단 전류, 고른 동작점 (목표선 + 한계 밖 띠)
- [가짜 데이터] `gain_vs_temp` — 이득 대 온도, 가장 나쁜 곳 (최소선)
- [가짜 데이터] `noise_by_corner` — corner 별 잡음 막대, 가장 나쁜 곳만 빨강
- [가짜 데이터] `pm_vs_load` — phase margin 대 부하 cap, 기본 부하 한 점
- [가짜 데이터] `step_settling` — 계단 응답, ±1 % 띠에 들어간 시각
