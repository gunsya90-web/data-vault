"""catalog.csv(보관) → 분야별 정리표(docs/분야별_정리표.md). 제목 키워드로 분류(한 자료는 첫 일치 분야 하나)."""
import csv,re,collections,os
D=[("소방·재난·안전",r"소방|화재|119|구조|구급|재난|재해|안전|사고|위험|대피|지진|홍수|침수|산불|응급|민방위"),
("복지·돌봄",r"복지|돌봄|노인|장애|수급|아동|보육|독거|요양|기초연금|사회보장|취약|자활|한부모|다문화|경로"),
("보건·의료",r"보건|의료|병원|의원|약국|건강|질병|감염|암|진료|사망|정신|자살|검진|백신"),
("기후·환경·에너지",r"기후|대기|미세먼지|기상|폭염|한파|온실|탄소|환경|에너지|전력|전기|가스|태양|수질|폐기물|녹지|공원|소음|열"),
("교통·도로",r"교통|도로|버스|지하철|철도|주차|차량|자동차|택시|고속|통행|신호|보행|자전거|횡단"),
("주거·건축·부동산",r"주택|아파트|건축|건물|주거|부동산|임대|공동주택|토지|빈집|재개발|노후"),
("인구·가구·행정",r"인구|가구|세대|주민|등록|행정|읍면동|통계|출생|전입|고령|1인"),
("경제·상권·일자리",r"시장|상가|상권|소상공인|사업체|고용|일자리|창업|기업|산업|매출|가격|지방세|세입|재정|예산"),
("교육·문화",r"학교|교육|도서관|문화|체육|관광|축제|학생|평생"),]
r=[x for x in csv.DictReader(open('catalog.csv',encoding='utf-8-sig')) if x['status']=='보관']
g=collections.defaultdict(list)
for x in r:
    t=x['title']; k=next((n for n,p in D if re.search(p,t)),"기타")
    g[k].append(x)
order=[n for n,_ in D]+["기타"]
L=["# 분야별 정리표","",f"`catalog.csv`의 보관 자료 {len(r)}건(파일 기준)을 제목 키워드로 분류. 한 자료는 첫 일치 분야 하나. 재생성: `python3 scripts/summarize_domains.py`","",
"| 분야 | 파일 수 | 데이터셋 수 | 용량(MB) | 대구 자료 |","|---|---:|---:|---:|---:|"]
for n in order:
    v=g.get(n,[]); 
    if not v: continue
    L.append(f"| {n} | {len(v)} | {len({x['dataset_id'] for x in v})} | {sum(float(x['size_mb'] or 0) for x in v):.0f} | {sum('대구' in x['title'] for x in v)} |")
for n in order:
    v=g.get(n,[])
    if not v: continue
    L+=["",f"## {n} ({len(v)})",""]
    seen=set()
    for x in sorted(v,key=lambda x:x['title']):
        if x['dataset_id'] in seen: continue
        seen.add(x['dataset_id'])
        L.append(f"- {x['title']} — `raw/{x['dataset_id']}/` ({x['provider']})")
open('docs/분야별_정리표.md','w').write("\n".join(L)+"\n")
print("\n".join(L[:20]))
