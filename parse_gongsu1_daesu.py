import sys, io, re, fitz, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. 고쟁이 공통수학1 파싱
f_gong1 = r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형내신 고쟁이 공통수학1.pdf"
doc_g1 = fitz.open(f_gong1)

g1_ans_map = {}
for p in range(231, len(doc_g1)):
    t = doc_g1[p].get_text("text")
    matches = re.findall(r'(\d{3,4})\s+([①②③④⑤]|\d+|[가-힣\s/]+)', t)
    for qid, ans in matches:
        g1_ans_map[qid.zfill(4)] = ans.strip()

print(f"Gongsu1 quick answers: {len(g1_ans_map)} items (Sample: 0001: {g1_ans_map.get('0001')}, 0100: {g1_ans_map.get('0100')})")

# 2. 고쟁이 대수 파싱
f_daesu = r"C:\Users\Admin\Documents\카카오톡 받은 파일\고쟁이 대수.pdf"
doc_d = fitz.open(f_daesu)

daesu_ans_map = {}
for p in range(224, len(doc_d)):
    t = doc_d[p].get_text("text")
    matches = re.findall(r'(\d{3,4})\s+([①②③④⑤]|\d+|[가-힣\s/]+)', t)
    for qid, ans in matches:
        daesu_ans_map[qid.zfill(4)] = ans.strip()

print(f"Daesu quick answers: {len(daesu_ans_map)} items (Sample: 0001: {daesu_ans_map.get('0001')}, 0100: {daesu_ans_map.get('0100')})")
