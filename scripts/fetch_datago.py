"""공공데이터포털(data.go.kr) 파일데이터 내려받기 + 카탈로그 기록.

사용:  python data_vault/scripts/fetch_datago.py 15060386 15044003 ...   (데이터셋 번호)
       python data_vault/scripts/fetch_datago.py --search "연간화재통계"   (검색만)
- 키 없이 받을 수 있는 '공공데이터포털에서 다운로드(원문파일등록)' 파일만 받음.
- 기관 사이트로 연결되는 자료(K-apt 등)는 catalog에 '외부'로 기록만 함.
- 받은 파일: data_vault/raw/<번호>/<파일명>, 목록: data_vault/catalog.csv
"""
import csv, hashlib, html, json, re, sys, time, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"; CAT = ROOT / "catalog.csv"
UA = {"User-Agent": "Mozilla/5.0"}
MAX_MB = 60  # 이보다 큰 파일은 저장소에 넣지 않고 기록만(필요 시 --big 으로 받기)
FIELDS = ["dataset_id", "title", "provider", "file_name", "status", "size_mb", "sha256", "fetched", "license", "provide_type", "source_url", "note"]

def get(url, data=None):
    req = urllib.request.Request(url, data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.headers

def page_info(pk):
    s = get(f"https://www.data.go.kr/data/{pk}/fileData.do")[0].decode("utf-8", "replace")
    def val(key):
        m = re.search(r'<strong class="key">\s*' + key + r'\s*</strong>\s*<div class="value">(.*?)</div>', s, re.S)
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else ""
    title = re.search(r"<title>(.*?)</title>", s, re.S)
    title = html.unescape(title.group(1)).split("|")[0].strip() if title else ""
    files = re.findall(r"fn_fileDataDown\('(\d+)',\s*'(uddi:[0-9a-f-]+)',\s*'([^']*)',\s*'(\d+)',\s*'(\d+)'\)", s)
    ext = re.search(r'<strong class="key">URL</strong>\s*<div class="value">\s*<a href="([^"]+)"', s)
    return dict(title=title, provider=val("제공기관") or val("기관명"), license=val("이용허락범위"),
                provide_type=val("제공형태"), files=list(dict.fromkeys(files)), ext=html.unescape(ext.group(1)) if ext else "")

def load_cat():
    if not CAT.exists(): return {}
    with CAT.open(encoding="utf-8-sig") as f:
        return {(r["dataset_id"], r["file_name"]): r for r in csv.DictReader(f)}

def save_cat(cat):
    with CAT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader()
        for k in sorted(cat): w.writerow({x: cat[k].get(x, "") for x in FIELDS})

def fetch(pk, cat, big=False):
    info = page_info(pk)
    base = dict(dataset_id=pk, title=info["title"], provider=info["provider"], license=info["license"],
                provide_type=info["provide_type"], fetched=str(date.today()), source_url=f"https://www.data.go.kr/data/{pk}/fileData.do")
    if not info["files"]:
        cat[(pk, "")] = {**base, "file_name": "", "status": "외부", "note": info["ext"] or "포털 파일 없음"}
        print(pk, "외부:", info["title"]); return
    for (_pk, uddi, atch, sn, hist) in info["files"][:1]:  # 최신 1건
        body = urllib.parse.urlencode(dict(publicDataDetailPk=uddi, publicDataPk=pk, atchFileId=atch, fileDetailSn=sn, publicDataTyCode="PR0051")).encode()
        j = json.loads(get("https://www.data.go.kr/tcs/dss/selectFileDataDownload.do", body)[0])
        if not j.get("status"):
            cat[(pk, "")] = {**base, "file_name": "", "status": "실패", "note": j.get("error", "")}; print(pk, "실패"); continue
        url = f"https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={j['atchFileId']}&fileDetailSn={j['fileDetailSn']}&insertDataPrcus=N"
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=600) as r:
            cd = r.headers.get("Content-Disposition", ""); size = int(r.headers.get("Content-Length") or 0)
            m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', cd)
            name = urllib.parse.unquote(m.group(1)) if m else f"{pk}.bin"
            try: name = name.encode("latin-1").decode("utf-8")
            except Exception: pass
            if size > MAX_MB * 1e6 and not big:
                cat[(pk, name)] = {**base, "file_name": name, "status": "대용량-미보관", "size_mb": f"{size/1e6:.1f}", "note": "--big 으로 받기"}
                print(pk, "대용량 건너뜀", name, f"{size/1e6:.0f}MB"); continue
            data = r.read()
        d = RAW / pk; d.mkdir(parents=True, exist_ok=True); (d / name).write_bytes(data)
        cat[(pk, name)] = {**base, "file_name": name, "status": "보관", "size_mb": f"{len(data)/1e6:.2f}", "sha256": hashlib.sha256(data).hexdigest()[:16]}
        print(pk, "받음", name, f"{len(data)/1e6:.1f}MB")

def search(kw):
    s = get("https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&perPage=10&keyword=" + urllib.parse.quote(kw))[0].decode("utf-8", "replace")
    for m in re.finditer(r'<a href="/data/(\d+)/fileData\.do">(.*?)</a>', s, re.S):
        print(m.group(1), re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip())

if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--search":
        for kw in a[1:]: print("##", kw); search(kw)
        sys.exit()
    big = "--big" in a; ids = [x for x in a if x.isdigit()]
    cat = load_cat()
    for pk in ids:
        try: fetch(pk, cat, big)
        except Exception as e: cat[(pk, "")] = {"dataset_id": pk, "status": "오류", "note": str(e)[:120], "fetched": str(date.today())}; print(pk, "오류", e)
        save_cat(cat); time.sleep(0.5)
