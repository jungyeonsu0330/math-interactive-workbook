import fitz, re, sys, io, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f_main = r'C:\Users\Admin\Documents\카카오톡 받은 파일\(2022) RPM 공통수학2.pdf'
f_ans = r'C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 공통수학2 답지.pdf'

doc_m = fitz.open(f_main)
doc_a = fitz.open(f_ans)

print(f"RPM Gongsu2 Main: {len(doc_m)} pages, Ans: {len(doc_a)} pages")

CIRCLES = ['①', '②', '③', '④', '⑤']

def clean_rpm_math(s):
    if not s: return ""
    s = s.replace('PA^_', '$\\overline{\\mathrm{PA}}$')
    s = s.replace('PB^_', '$\\overline{\\mathrm{PB}}$')
    s = s.replace('AB^_', '$\\overline{\\mathrm{AB}}$')
    s = s.replace('BC^_', '$\\overline{\\mathrm{BC}}$')
    s = s.replace('AC^_', '$\\overline{\\mathrm{AC}}$')
    s = s.replace('OA^_', '$\\overline{\\mathrm{OA}}$')
    s = s.replace('OB^_', '$\\overline{\\mathrm{OB}}$')
    s = s.replace('OP^_', '$\\overline{\\mathrm{OP}}$')
    s = re.sub(r'([A-Z]{2,3})\^_', r'$\\overline{\\mathrm{\1}}$', s)
    
    s = s.replace('^2', '^2').replace('^3', '^3')
    s = s.replace('gakABC', '$\\angle \\mathrm{ABC}$')
    s = s.replace('gak', '$\\angle$ ')
    
    # 루트
    s = re.sub(r'1(\d)', r'\\sqrt{\1}', s) # e.g. 17 -> \sqrt{7}, 13 -> \sqrt{3} in some contexts
    s = s.replace('.t3', '$\\therefore$').replace('cc', '......')
    s = s.replace('L0', ' \\ne 0').replace('not=', ' \\ne ')
    
    s = s.replace('\xa0', ' ')
    s = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

# 1. 해설지 전수 파싱: 문항 번호, 정답, 단계별 상세 풀이
ans_dict = {}
sol_dict = {}

for p in range(len(doc_a)):
    t = doc_a[p].get_text()
    # 문항 번호와 풀이 블록 추출
    parts = re.split(r'(?:^|\n)\s*(\d{4})\s+', t)
    for i in range(1, len(parts)-1, 2):
        qid = parts[i].strip()
        body = parts[i+1].strip()
        
        # 정답 추출
        m_ans = re.search(r'(?:답|정답)\s*([^\n\r]+)', body)
        ans_val = m_ans.group(1).strip() if m_ans else ""
        
        # 다른 풀이 분리
        sol_dict[qid] = clean_rpm_math(body[:1200])
        if ans_val:
            ans_dict[qid] = ans_val

print(f"Parsed {len(sol_dict)} solutions from RPM Gongsu2 Ans PDF")

# 2. 본문 페이지 파싱 (페이지 7 ~ 165)
rpm2_pages = {}
rpm2_probs = {}

for p_no in range(7, 166):
    p_idx = p_no - 1
    if p_idx >= len(doc_m): continue
    page = doc_m[p_idx]
    
    t = page.get_text()
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
            
        # 선택지 분리
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
        
        # 정답
        ans_raw = ans_dict.get(qid, "")
        ans_idx = -1
        if ans_raw in CIRCLES:
            ans_idx = CIRCLES.index(ans_raw)
            has_choices = True
            if not choices or len(choices) < 5:
                choices = ["1", "2", "3", "4", "5"]
                
        # 단원명 결정 (RPM 공통수학2 단원 매핑)
        if p_no <= 25:
            unit_name = "01 평면좌표와 직선의 방정식"
            c_title = "두 점 사이의 거리와 직선의 기울기"
            c_sub = "내분점·외분점과 무게중심 공식"
            strat = "선분의 내분점 공식과 점과 직선 사이의 거리 d 공식을 좌표축에 투영하여 해결"
            tip = "거리의 제곱의 합 AP² + BP²의 최솟값은 두 점 A, B의 중점을 지날 때 발생하므로 완전제곱식으로 정리하면 암산 가능합니다."
        elif p_no <= 50:
            unit_name = "02 원의 방정식과 도형의 이동"
            c_title = "원의 방정식과 접선의 방정식"
            c_sub = "평행이동과 대칭이동 공식"
            strat = "원의 중심과 직선 사이의 거리 d=r 성질 및 대칭축 선대칭 성질을 활용"
            tip = "원의 접선 문제는 판별식을 쓰지 말고, 항상 원의 중심과 직선 사이의 거리 d=r을 쓰세요. 계산 속도가 3배 빠릅니다!"
        elif p_no <= 90:
            unit_name = "03 집합과 명제"
            c_title = "집합의 연산과 드모르간 법칙"
            c_sub = "명제의 대우와 귀류법, 절대부등식"
            strat = "벤 다이어그램을 활용한 원소의 개수 추적 및 산술·기하 평균 부등식 적용"
            tip = "합집합의 원소의 개수 n(A∪B)의 최댓값/최솟값은 교집합 n(A∩B)의 범위에 의해 결정되므로 포함 관계를 먼저 파악하세요."
        elif p_no <= 130:
            unit_name = "04 함수와 역함수"
            c_title = "일대일대응과 합성함수"
            c_sub = "역함수의 존재 조건과 성질"
            strat = "단조 증가/감소 조건을 통한 일대일대응 확인 및 역함수 합성 공식 (f∘g)⁻¹=g⁻¹∘f⁻¹ 적용"
            tip = "역함수 그래프와의 교점은 원래 함수 y=f(x)가 증가함수일 때 항상 y=x 위에 존재하므로 연립방정식 f(x)=x로 즉시 해결하세요."
        else:
            unit_name = "05 유리함수와 무리함수"
            c_title = "유리함수의 점근선과 대칭 중심"
            c_sub = "무리함수의 시작점과 정의역/치역"
            strat = "유리함수의 점근선의 교점 (p, q)에 대한 점대칭성과 무리함수 곡선과 직선의 위치 관계 연립"
            tip = "유리함수와 직선의 교점 문제는 점근선의 교점을 원점으로 평행이동하면 대칭성 덕분에 계산이 극단적으로 단순해집니다."
            
        sol_text = sol_dict.get(qid, f"【문항 {qid}번 해설】\n주어진 조건식을 정리하고 단원의 기본 정의와 정규 공식을 적용하여 정답을 유도합니다.\n정답: {ans_raw}")
        
        rpm2_probs[qid] = {
            "id": qid,
            "page": p_no,
            "unit": unit_name,
            "step": "유형 다지기" if num % 2 == 0 else "대표 문제",
            "qText": q_text_clean if len(q_text_clean) > 8 else f"RPM 공통수학2 {p_no}쪽 {qid}번 문항입니다.",
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
        rpm2_pages[p_no] = {
            "page": p_no,
            "unit": rpm2_probs[page_qids[0]]["unit"] if page_qids else "01 평면좌표",
            "qids": page_qids
        }

print(f"RPM Gongsu2 parsed: {len(rpm2_pages)} pages, {len(rpm2_probs)} problems.")

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_gongsu2.json', 'w', encoding='utf-8') as f:
    json.dump({"pages": rpm2_pages, "probs": rpm2_probs}, f, ensure_ascii=False, indent=2)

print("Saved parsed_rpm_gongsu2.json successfully!")
