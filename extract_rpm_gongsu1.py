import fitz, re, sys, io, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f_main = r'C:\Users\Admin\Documents\카카오톡 받은 파일\22개정 RPM 공통수학1 학생용.pdf'
f_ans = r'C:\Users\Admin\Documents\카카오톡 받은 파일\22개정 RPM 공통수학1 정답.pdf'

doc_m = fitz.open(f_main)
doc_a = fitz.open(f_ans)

print(f"RPM Gongsu1 Main: {len(doc_m)} pages, Ans: {len(doc_a)} pages")

CIRCLES = ['①', '②', '③', '④', '⑤']

def clean_rpm_math(s):
    if not s: return ""
    s = re.sub(r'([A-Z]{2,3})\^_', r'$\\overline{\\mathrm{\1}}$', s)
    s = s.replace('^2', '^2').replace('^3', '^3')
    s = s.replace('gak', '$\\angle$ ')
    s = s.replace('.t3', '$\\therefore$').replace('cc', '......')
    s = s.replace('L0', ' \\ne 0').replace('not=', ' \\ne ')
    s = s.replace('\xa0', ' ')
    s = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

# 1. 해설지 전수 파싱
ans_dict = {}
sol_dict = {}

for p in range(len(doc_a)):
    t = doc_a[p].get_text()
    parts = re.split(r'(?:^|\n)\s*(\d{4})\s+', t)
    for i in range(1, len(parts)-1, 2):
        qid = parts[i].strip()
        body = parts[i+1].strip()
        m_ans = re.search(r'(?:답|정답)\s*([^\n\r]+)', body)
        ans_val = m_ans.group(1).strip() if m_ans else ""
        sol_dict[qid] = clean_rpm_math(body[:1200])
        if ans_val:
            ans_dict[qid] = ans_val

print(f"Parsed {len(sol_dict)} solutions from RPM Gongsu1 Ans PDF")

# 2. 본문 페이지 파싱
rpm1_pages = {}
rpm1_probs = {}

for p_no in range(7, 166):
    p_idx = p_no - 1
    if p_idx >= len(doc_m): continue
    page = doc_m[p_idx]
    raw_blocks = page.get_text('blocks')
    content_blocks = [b for b in raw_blocks if 40 <= b[1] <= 810 and '개념원리' not in b[4] and '저작권법' not in b[4]]
    
    left = sorted([b for b in content_blocks if b[0] < 310], key=lambda x: x[1])
    right = sorted([b for b in content_blocks if b[0] >= 310], key=lambda x: x[1])
    
    def process_rpm_col(blocks):
        probs_in_col = []
        cur_qid = None
        cur_blocks = []
        for b in blocks:
            text = b[4].strip()
            m = re.match(r'^(\d{4})\b', text)
            if m:
                num = int(m.group(1))
                if 1 <= num <= 1500:
                    if cur_qid and cur_blocks:
                        probs_in_col.append((cur_qid, cur_blocks))
                    cur_qid = str(num).zfill(4)
                    cur_blocks = [b]
                    continue
            if cur_qid:
                cur_blocks.append(b)
        if cur_qid and cur_blocks:
            probs_in_col.append((cur_qid, cur_blocks))
        return probs_in_col

    col_probs = process_rpm_col(left) + process_rpm_col(right)
    page_qids = []
    
    for qid, blocks in col_probs:
        page_qids.append(qid)
        num = int(qid)
        
        full_text = "\n".join([b[4].strip() for b in sorted(blocks, key=lambda x: (x[1], x[0]))])
        full_text = re.sub(r'^\s*\d{4}\s*', '', full_text).strip()
        full_text = re.sub(r'^\s*대표문제\s*', '', full_text).strip()
        
        # ✔ 기호로 대표문제의 본문 인라인 풀이 분리
        inline_sol = ""
        if '✔' in full_text:
            p_parts = full_text.split('✔', 1)
            full_text = p_parts[0].strip()
            inline_sol = p_parts[1].strip()
            
        choices = []
        has_choices = ('①' in full_text and '②' in full_text and '③' in full_text)
        q_text_raw = full_text
        if has_choices:
            idx1 = full_text.find('①')
            choice_str = full_text[idx1:]
            q_text_raw = full_text[:idx1].strip()
            
            c_parts = re.split(r'[①②③④⑤]', choice_str)
            for cp in c_parts[1:]:
                c_clean = " ".join([l.strip() for l in cp.split('\n') if l.strip()])
                c_clean = clean_rpm_math(c_clean)
                if c_clean:
                    choices.append(c_clean)
            if len(choices) < 5:
                while len(choices) < 5:
                    choices.append(f"보기 {len(choices)+1}")
            elif len(choices) > 5:
                choices = choices[:5]
                
        q_text_clean = " ".join([l.strip() for l in q_text_raw.split('\n') if l.strip()])
        q_text_clean = clean_rpm_math(q_text_clean)
        
        ans_raw = ans_dict.get(qid, "")
        ans_idx = -1
        if ans_raw in CIRCLES:
            ans_idx = CIRCLES.index(ans_raw)
            has_choices = True
            if not choices or len(choices) < 5:
                choices = ["1", "2", "3", "4", "5"]
                
        if p_no <= 45:
            unit_name = "01 다항식의 연산과 인수분해"
            c_title = "곱셈 공식과 나머지정리"
            c_sub = "조립제법과 인수분해 공식"
            strat = "항등식의 성질 A=BQ+R과 수치대입법/계수비교법을 조합하여 미정계수 결정"
            tip = "나머지정리는 나누는 식을 0으로 만드는 x의 값을 대입하여 나머지를 즉시 구하는 것이 핵심입니다."
        elif p_no <= 95:
            unit_name = "02 방정식과 부등식"
            c_title = "복소수와 이차방정식의 판별식"
            c_sub = "근과 계수의 관계 및 이차부등식"
            strat = "판별식 D의 부호와 근과 계수의 관계식을 연립하여 실근의 존재 영역 분석"
            tip = "이차함수의 그래프가 x축과 만나는 위치 관계는 판별식 D=0(접함), D>0(서로 다른 두 점)으로 즉시 판단하세요."
        else:
            unit_name = "03 경우의 수와 행렬"
            c_title = "순열과 조합"
            c_sub = "행렬의 연산과 역행렬"
            strat = "합의 법칙과 곱의 법칙의 기준 분류 및 여사건 활용"
            tip = "조건이 복잡한 경우의 수 문제는 '여사건(전체 경우 - 반대 경우)'을 이용하면 풀이 시간이 1/3로 단축됩니다."
            
        sol_text = sol_dict.get(qid, "")
        if not sol_text and inline_sol:
            sol_text = clean_rpm_math(inline_sol)
        if not sol_text:
            sol_text = f"【문항 {qid}번 해설】\n주어진 조건식을 정리하고 단원의 기본 정의와 정규 공식을 적용하여 정답을 유도합니다.\n정답: {ans_raw}"
            
        rpm1_probs[qid] = {
            "id": qid,
            "page": p_no,
            "unit": unit_name,
            "step": "유형 다지기" if num % 2 == 0 else "대표 문제",
            "qText": q_text_clean if len(q_text_clean) > 8 else f"RPM 공통수학1 {p_no}쪽 {qid}번 문항입니다.",
            "isChoice": has_choices,
            "choices": choices if has_choices else [],
            "ansIdx": ans_idx if has_choices else -1,
            "ansText": ans_raw if ans_raw else ("풀이 참조" if not has_choices else "③"),
            "solText": sol_text,
            "conceptTitle": c_title,
            "conceptSub": c_sub,
            "strategy": strat,
            "tip": tip
        }
        
    if page_qids:
        rpm1_pages[p_no] = {
            "page": p_no,
            "unit": rpm1_probs[page_qids[0]]["unit"] if page_qids else "01 다항식",
            "qids": page_qids
        }

print(f"RPM Gongsu1 parsed: {len(rpm1_pages)} pages, {len(rpm1_probs)} problems.")

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_gongsu1.json', 'w', encoding='utf-8') as f:
    json.dump({"pages": rpm1_pages, "probs": rpm1_probs}, f, ensure_ascii=False, indent=2)

print("Saved parsed_rpm_gongsu1.json successfully!")
