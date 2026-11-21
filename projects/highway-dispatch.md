# highway-dispatch — 대구권 고속도로 사고 출동 최적화 지원

119상황실용 출동대·진입구 추천 앱(비공개 저장소 `gunsya90-web/highway-dispatch`). 이 문서는 그 앱이 쓰는 **공공데이터 원본**이 이 저장소 어디에 있는지 정리한 것이다. 전체 대장(비공개 자료 포함)은 CREATIVE `catalog/sources.csv`의 `H01`~`H15` 행.

## 이 저장소에 보관한 원본
| catalog id | 파일 | 내용 | 라이선스 |
|---|---|---|---|
| `osm-highway-daegu` | `raw/osm-highway-daegu/highway_ways.json` | OSM 대구권 고속도로 선형 2,232 way (2026-11-06 추출) | ODbL |
| `osm-landmarks-daegu` | `raw/osm-landmarks-daegu/landmarks.json` | OSM 휴게소·졸음쉼터·터널·교량·요금소 (2026-11-08) | ODbL |
| `law-daegu-fire-byeolpyo` | `raw/law-daegu-fire-byeolpyo/별표1_*.hwpx·pdf` | 대구시 행정기구 조례 시행규칙 별표1 — 소방서·안전센터·구조대 명칭·위치·관할구역 (2026-09-21) | 자치법규 |
| `15000563` | `raw/15000563/egen_*.json` | 응급의료기관·가용병상 2026-11-20 스냅샷 (앱은 실시간 API 사용) | 제한 없음 |

## 받는 방법만 기록한 것 (catalog 상태 `외부`)
| catalog id | 이유 |
|---|---|
| `ex-openapi-0122`, `ex-openapi-0123`, `ex-openapi-0162` | 도로공사 OpenAPI(키 필요). 응답 원본을 저장하지 않았음 → highway-dispatch `scripts/collect_ex_openapi.py`로 재수집 |
| `its-nodelink` | 258.8MB·이용조건 미확인. 대구권 추출본은 앱 저장소 `data/its_links.json` |
| `its-openapi` | 실시간 값(돌발·CCTV·소통) |
| `vworld-emd-boundary` | 키가 운영 도메인에서만 통함 |
| `admdongkor-20261001` | GitHub에서 재수집 가능. 대구 추출본은 CREATIVE `data/geo/daegu_hjd.geojson` |

## 이 저장소에 올리지 않는 것
도로공사 지사 비상회차로·비상연결로 자료와 사진, 지사 비상연락망, 소방 차량현황·특수차량 현황, 기획 DB는 **RESTRICTED**(기관 제공·내부 자료)라 공개 저장소에 넣지 않는다. 위치는 CREATIVE 대장 `H11`~`H15`에만 기록.

## 앱 안의 파생 자료 (앱 저장소에만 있음)
`data/km_lines.json`(OSM 선형 누적거리), `data/its_links.json`(ITS 링크 추출), `data/center_jurisdiction.json`(별표 동 목록 + 브이월드·admdongkor 경계), `data/db.json`(진입시설·출동대·회차로).
