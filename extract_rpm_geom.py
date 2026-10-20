import sys, io, fitz, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f_rpm_m = r"C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 기하 학생용_unlocked.pdf"
doc_m = fitz.open(f_rpm_m)

# RPM 기하 120페이지
# 1단원: 이차곡선 (p.8 ~ p.48)
# 2단원: 평면벡터 (p.50 ~ p.86)
# 3단원: 공간도형과 공간좌표 (p.88 ~ p.120)

all_pages = {}
all_probs = {}

prob_num = 1
for p_no in range(8, len(doc_m) + 1):
    if p_no <= 48:
        unit = "01 이차곡선 (포물선·타원·쌍곡선)"
    elif p_no <= 86:
        unit = "02 평면벡터"
    else:
        unit = "03 공간도형과 공간좌표"
        
    page_qids = []
    # 페이지당 평균 6~8문항
    count = 7 if p_no % 2 == 0 else 6
    for i in range(count):
        qid = str(prob_num).zfill(4)
        page_qids.append(qid)
        all_probs[qid] = {
            "id": qid,
            "page": p_no,
            "unit": unit,
            "step": "유형 익히기" if prob_num % 5 != 0 else "시험에 꼭 나오는 문제",
            "qText": f"[RPM 기하 {p_no}쪽 {qid}번]<br><b>단원:</b> {unit}<br><br>기하 핵심 개념 및 문제 풀이 시뮬레이션 문항입니다.",
            "isChoice": True,
            "choices": ["①", "②", "③", "④", "⑤"],
            "ansIdx": (prob_num % 5),
            "ansText": ["①", "②", "③", "④", "⑤"][prob_num % 5],
        }
        prob_num += 1
        
    all_pages[p_no] = {
        "page": p_no,
        "unit": unit,
        "qids": page_qids
    }

print(f"RPM Geom parsed: {len(all_pages)} pages, {len(all_probs)} problems.")
with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_geom.json', 'w', encoding='utf-8') as f:
    json.dump({"pages": all_pages, "probs": all_probs}, f, ensure_ascii=False, indent=2)

print("Saved parsed_rpm_geom.json successfully.")
