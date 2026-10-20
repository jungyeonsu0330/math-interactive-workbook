import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('c:/Users/Admin/Desktop/문제집작업/index.html', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const BOOKS_DATA = (\{.*?\});\s*\n\s*let curBookKey', html, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print(f"Total books configured in web portal: {len(data)}")
    total_probs = 0
    for k, v in data.items():
        cnt = len(v['probs'])
        pgs = len(v['pages'])
        total_probs += cnt
        print(f"  • {v['title']} ({k}): {cnt}문항 / {pgs}쪽 수록")
    print(f"\n==========================================")
    print(f"★ 총 수록 문항 수: {total_probs}문항 전수 등록 완료!")
    print(f"==========================================")
else:
    print("BOOKS_DATA not found!")
