"""서울 열린데이터광장 파일데이터(F) 내려받기 + catalog 기록.
사용: python scripts/fetch_seoul.py OA-22835 OA-23040 ...   (95MB 넘는 파일은 기록만, --big 이면 받음)
"""
import csv, hashlib, html, re, sys, urllib.parse, urllib.request
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from fetch_datago import load_cat, save_cat, RAW
UA = {"User-Agent": "Mozilla/5.0"}
MAX_MB = 95

def fetch(oa, cat, big=False):
    url = f"https://data.seoul.go.kr/dataList/{oa}/F/1/datasetView.do"
    s = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "replace")
    title = re.search(r"<title>(.*?)</title>", s, re.S); title = html.unescape(title.group(1)).split("|")[0].strip() if title else oa
    lic = re.search(r"공공누리\s*(?:제)?\s*\d\s*유형|공공누리\s*\d유형|KOGL[^<]{0,10}", s)
    files = dict(re.findall(r"""<span title="([^"]+)" onclick="javascript:downloadFile\('(\d+)'\);""", s))
    base = dict(dataset_id=oa, title=title, provider="서울특별시", license=lic.group(0).strip() if lic else "", provide_type="서울 열린데이터광장 파일",
                fetched=str(date.today()), source_url=url)
    if not files:
        cat[(oa, "")] = {**base, "file_name": "", "status": "외부", "note": "파일 목록 없음(시트·API형일 수 있음)"}; print(oa, "파일 없음"); return
    for name, seq in files.items():
        body = urllib.parse.urlencode(dict(infId=oa, seqNo="", seq=seq, infSeq="1")).encode()
        req = urllib.request.Request("https://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false", data=body, headers=UA)
        with urllib.request.urlopen(req, timeout=900) as r:
            size = int(r.headers.get("Content-Length") or 0)
            if size > MAX_MB * 1e6 and not big:
                cat[(oa, name)] = {**base, "file_name": name, "status": "대용량-미보관", "size_mb": f"{size/1e6:.1f}", "note": "--big"}
                print(oa, "대용량 건너뜀", name, f"{size/1e6:.0f}MB"); continue
            data = r.read()
        if data[:200].lstrip().lower().startswith(b"<html"):
            cat[(oa, name)] = {**base, "file_name": name, "status": "실패", "note": "파일 대신 오류 페이지 응답(시트형 자료일 수 있음)"}
            print(oa, "실패(오류 페이지)", name); continue
        d = RAW / oa; d.mkdir(parents=True, exist_ok=True); (d / name).write_bytes(data)
        cat[(oa, name)] = {**base, "file_name": name, "status": "보관", "size_mb": f"{len(data)/1e6:.2f}", "sha256": hashlib.sha256(data).hexdigest()[:16]}
        print(oa, "받음", name, f"{len(data)/1e6:.1f}MB")

if __name__ == "__main__":
    a = sys.argv[1:]; big = "--big" in a; cat = load_cat()
    for oa in [x for x in a if x.startswith("OA-")]:
        try: fetch(oa, cat, big)
        except Exception as e: cat[(oa, "")] = {"dataset_id": oa, "status": "오류", "note": str(e)[:120], "fetched": str(date.today())}; print(oa, "오류", e)
        save_cat(cat)
