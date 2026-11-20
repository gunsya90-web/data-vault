"""관련 분야 키워드로 공공데이터포털 파일데이터를 넓게 찾아 후보 목록(candidates.csv)을 만든다.
사용: python scripts/discover_datago.py   → candidates.csv (dataset_id,title,keyword,keep)
"""
import csv, html, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0"}
KEYWORDS = ["소방", "화재", "119", "구급", "구조활동", "응급", "응급안전안심", "재난", "안전사고", "폭염", "한파", "온열질환",
            "미세먼지", "대기오염", "기상", "독거노인", "노인", "장애인", "기초생활", "수급자", "복지시설", "사회복지", "돌봄",
            "1인가구", "1인세대", "주민등록 인구", "공동주택", "아파트", "승강기", "전력사용량", "에너지 사용", "가스", "지역난방",
            "무더위쉼터", "한파쉼터", "응급의료", "병원", "전통시장", "고독사"]
NATIONAL = r"^(소방청|보건복지부|행정안전부|국토교통부|기상청|한국전력공사|한국사회보장정보원|한국승강기안전공단|한국가스안전공사|한국전기안전공사|한국지역난방공사|한국에너지공단|국립중앙의료원|질병관리청|한국부동산원|기후에너지환경부|환경부|한국환경공단|국가데이터처|통계청|한국소비자원|국민건강보험공단|건강보험심사평가원|한국노인인력개발원|한국보건사회연구원|한국사회복지협의회|국립재난안전연구원|한국토지주택공사|산림청|소상공인시장진흥공단|한국에너지기술연구원|한국가스공사)"
REGION = r"^(대구광역시|대구)"

def search(kw, page):
    u = ("https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&perPage=100&currentPage=%d&keyword=%s" % (page, urllib.parse.quote(kw)))
    s = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode("utf-8", "replace")
    out = []
    for m in re.finditer(r'<a href="/data/(\d+)/fileData\.do">(.*?)</a>', s, re.S):
        out.append((m.group(1), re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip()))
    return out

def main():
    seen = {}
    for kw in KEYWORDS:
        for page in (1, 2, 3):
            try: res = search(kw, page)
            except Exception as e: print(kw, page, "오류", e); res = []
            if not res: break
            for pk, t in res: seen.setdefault(pk, (t, kw))
            time.sleep(0.3)
        print(kw, len(seen))
    rows = []
    for pk, (t, kw) in seen.items():
        keep = bool(re.search(NATIONAL, t) or re.search(REGION, t))
        rows.append(dict(dataset_id=pk, title=t, keyword=kw, keep="Y" if keep else ""))
    with (ROOT / "candidates.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, ["dataset_id", "title", "keyword", "keep"]); w.writeheader(); w.writerows(rows)
    print("후보", len(rows), "선택", sum(r["keep"] == "Y" for r in rows))

if __name__ == "__main__": main()
