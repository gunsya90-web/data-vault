# 프로젝트별 데이터 연결
- svc_seoul_ai_hackathon_2026.md — 2026 SVC Seoul AI 해커톤(현대건설)
- 사회보장 경진대회(우리동네 안심채움 지도)·기후환경 대회(폭염 119 내일지도) 자료는 highway-dispatch 저장소 `docs/contest_ssis/data`, `docs/contest/data`에 있음 — 필요 시 이곳으로 옮겨 통합

## 사회보장·기후환경·로컬AI(전통시장) 원본 (2026-11-20 통합)
- 세 데이터 채팅창(사회보장공공데이터 수집 / 기후환경공공데이터 수집 및 관리 / 공공데이터 수집 및 관리)의 대장
  (CREATIVE `catalog/sources.csv`, `contest_ssis_2026/catalog/sources.csv`)에 있는 data.go.kr 파일 55건을 이 저장소 raw/로 다시 받아 보관.
- 가공본은 이미 GitHub에 있음: CREATIVE `data/processed/`, `contest_ssis_2026/processed/` / highway-dispatch 브랜치 `claude/adoring-shannon-zuxh0q`의 `contest_ssis_2026/processed/`.
- 포털 밖 원본(소방안전 빅데이터 파일·MCP 원자료, 기상청, 대구 대기측정망, 브이월드 SHP, 행안부 주민등록, 전통시장 기사)은 각 채팅창에서 올려야 함.
