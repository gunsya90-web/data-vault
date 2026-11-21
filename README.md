# data-vault — 공공데이터 원본 보관소

대회·프로젝트에 쓰는 공공데이터 **원본**을 한곳에 쌓아 두는 저장소입니다. 가공 결과는 각 프로젝트 저장소에 둡니다.

## 구조
```
catalog.csv              전체 목록(데이터셋 번호·이름·기관·파일·상태·크기·지문값·받은 날·라이선스·출처)
raw/<데이터셋번호>/       원본 파일(고치지 않음). 100MB 미만만 보관
scripts/fetch_datago.py  공공데이터포털(data.go.kr) 파일데이터 자동 수집
projects/                대회·프로젝트별로 어떤 데이터를 쓰는지 연결
```

## 저장소 3개의 역할 (2026-11-21)
| 저장소 | 공개 | 담는 것 |
|---|---|---|
| **data-vault** (여기) | 공개 | 공공데이터 **원본**과 원본 목록(`catalog.csv`). 공개 라이선스 자료만 |
| **CREATIVE** | 비공개 | **통합 데이터 대장** `catalog/sources.csv`(모든 프로젝트·모든 출처, 보안 등급·위치·data-vault 경로), 가공본, 대회 자료 |
| **highway-dispatch** | 비공개 | 출동 앱이 실제로 읽는 운영 데이터(`data/`, `db/`) — RESTRICTED 자료 포함 |

- 새 데이터를 받으면: 원본은 여기 `raw/` + `catalog.csv`, 대장 한 줄은 CREATIVE `catalog/sources.csv`(`vault` 칸에 이 저장소 경로).
- **RESTRICTED·CONFIDENTIAL**(기관 제공 자료, 소방 내부 차량현황, 연락처, 비상출입구 사진 등)은 이 저장소에 절대 올리지 않는다.

## dataset_id 규칙
| 형태 | 출처 |
|---|---|
| 숫자(예: `15000563`) | 공공데이터포털 data.go.kr 데이터셋 번호 |
| `OA-xxxxx` | 서울 열린데이터광장 |
| `bokjiro-<번호>` | 복지로 사회보장통계 |
| `bigdata119-<번호>` | 소방안전 빅데이터 플랫폼 |
| `osm-…`, `law-…`, `ex-openapi-…`, `its-…`, `vworld-…`, `admdongkor-…` | OpenStreetMap 추출, 자치법규 원문, 도로공사·ITS·브이월드 API, 행정동 경계 |

## 상태 값(catalog.csv)
| 상태 | 뜻 |
|---|---|
| 보관 | raw/ 에 원본 있음 |
| 외부 | 포털이 기관 사이트로 연결(K-apt·한전·서울 열린데이터광장 등) — 직접 받아야 함, note에 주소 |
| 대용량-미보관 | 60MB 초과라 저장소에 넣지 않음. `--big` 으로 받기 |
| 빈 파일 / 오류 | 포털 파일 문제 또는 접속 오류 — 다시 시도 |

## 사용법
```bash
python scripts/fetch_datago.py --search "연간화재통계"      # 번호 찾기
python scripts/fetch_datago.py 15060386 15044003          # 받기 + catalog 갱신
python scripts/fetch_datago.py 15112639 --big             # 대용량도 받기(LFS 용량 주의)
```

## 용량 원칙
- 파일 1개 100MB 제한(50MB부터 경고), 저장소 일반 파일은 1GB 안쪽 유지. 클라우드 세션에서는 LFS 서버(lfs.github.com) 접속이 막혀 있어 지금은 LFS 없이 100MB 미만 파일만 보관(PC에서는 LFS 사용 가능).
- 공공데이터는 다시 받을 수 있으므로 아주 큰 파일은 보관하지 않고 catalog에 받는 방법만 기록.

## 라이선스 주의
- 공공누리 4유형(예: 서울 홈에너지 시간별, 서울 가로수 위치)은 상업적 이용·변경 금지 → 사업화 결과물에는 쓰지 않음.
- 각 파일의 이용허락범위는 catalog.csv `license` 칸 확인.
