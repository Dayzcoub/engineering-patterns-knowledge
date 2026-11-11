#!/usr/bin/env python3
"""Local keyword search across card fields; no network and no dependencies."""
import argparse, json, pathlib, re, sys

# Keep JSON and Russian descriptions intact when stdout is redirected on Windows.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
HERE=pathlib.Path(__file__).resolve().parent.parent

def tokenize(s):
    return [x for x in re.split(r"[^\w-]+",s.lower()) if x]

def main():
    ap=argparse.ArgumentParser(description='Search curated engineering pattern cards')
    ap.add_argument('query',nargs='?',default='',help='problem/symptom words')
    ap.add_argument('--project',choices=['KLIDAN','Audio Probe','STAYA'],help='project filter')
    ap.add_argument('--domain',help='filter by domain (e.g. audio, storage)')
    ap.add_argument('--limit',type=int,default=8)
    ap.add_argument('--json',action='store_true',help='print JSON')
    args=ap.parse_args()
    db=json.loads((HERE/'data'/'patterns.json').read_text(encoding='utf-8'))
    q=tokenize(args.query)
    scores=[]
    for p in db['cards']:
        if args.project and args.project not in p['projects']:continue
        if args.domain and p['domain'].lower()!=args.domain.lower():continue
        title=p['title'].lower()+' '+p['id'].lower()
        hay=' '.join(str(v) for k,v in p.items() if k not in ('source_urls',)).lower()
        score=sum(5 if w in title else 1 if w in hay else 0 for w in q)
        if q and not score:continue
        scores.append((score,p))
    scores.sort(key=lambda item:(-item[0],item[1]['priority'],item[1]['id']))
    found=[p for _,p in scores[:max(0,args.limit)]]
    if args.json:
        print(json.dumps(found,ensure_ascii=False,indent=2));return
    if not found:print('No matches. Try --domain or broader keywords.');return
    for p in found:
        print(f"[{p['priority']}] {p['id']} | {p['title']} | review={p['source_review']}")
        print('  Signal:',p['signals'])
        print('  Avoid:',p['avoid'])
        print('  Check:',p['verification'])
        print('  Source:',p['source_urls'][0])

if __name__=='__main__':main()
