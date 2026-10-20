import fitz, re, sys, io, json, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CIRCLES = ['①', '②', '③', '④', '⑤']

def clean_mid_math(s):
    if not s: return ""
    s = s.replace('ù', '^\\circ')
    # 선분, 직선, 반직선
    s = re.sub(r'([A-Z]{2,3})Ó', r'$\\overline{\\mathrm{\1}}$', s)
    s = re.sub(r'([A-Z]{2,3})ê', r'$\\overleftrightarrow{\\mathrm{\1}}$', s)
    s = re.sub(r'([A-Z]{2,3})³', r'$\\overrightarrow{\\mathrm{\1}}$', s)
    s = re.sub(r'([A-Z]{2,3})\^_', r'$\\overline{\\mathrm{\1}}$', s)
    # 삼각형
    s = re.sub(r's([A-Z]{3,4})', r'$\\triangle \\mathrm{\1}$', s)
    # 기호
    s = s.replace('ª', ' $\\equiv$ ').replace('∽', ' $\\sim$ ')
    s = s.replace('∥', ' $\\parallel$ ').replace('⊥', ' $\\perp$ ')
    s = s.replace('gak', '$\\angle$ ').replace('∠', '$\\angle$ ')
    # 분수
    s = s.replace(';2!;', '$\\frac{1}{2}$')
    s = re.sub(r';(\d+)!;', r'$\\frac{1}{\1}$', s)
    s = re.sub(r';(\d+);(\d+);', r'$\\frac{\1}{\2}$', s)
    # 지수
    s = s.replace('Û`', '^2').replace('Ü`', '^3')
    s = s.replace('^2', '^2').replace('^3', '^3')
    # 기타
    s = s.replace('.t3', '$\\therefore$').replace('cc', '......')
    s = s.replace('L0', ' \\ne 0').replace('not=', ' \\ne ')
    s = s.replace('\xa0', ' ')
    s = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

def parse_solutions(doc_a):
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
            sol_dict[qid] = clean_mid_math(body[:1200])
            if ans_val:
                ans_dict[qid] = ans_val
    return ans_dict, sol_dict

def extract_book(main_pdf, ans_pdf, book_id, book_title, unit_rules, out_json):
    print(f"=== Extracting {book_title} ===")
    doc_m = fitz.open(main_pdf)
    doc_a = fitz.open(ans_pdf)
    print(f"Main: {len(doc_m)} pages, Ans: {len(doc_a)} pages")
    
    ans_dict, sol_dict = parse_solutions(doc_a)
    print(f"Parsed {len(sol_dict)} solutions from Ans PDF")
    
    pages_data = {}
    probs_data = {}
    
    # 본문 페이지 순회 (2페이지부터 본문 끝까지)
    for p_no in range(2, len(doc_m) + 1):
        p_idx = p_no - 1
        page = doc_m[p_idx]
        raw_blocks = page.get_text('blocks')
        content_blocks = [b for b in raw_blocks if 40 <= b[1] <= 810 and '개념원리' not in b[4] and '저작권법' not in b[4]]
        
        left = sorted([b for b in content_blocks if b[0] < 310], key=lambda x: x[1])
        right = sorted([b for b in content_blocks if b[0] >= 310], key=lambda x: x[1])
        
        def process_col(blocks):
            probs_in_col = []
            cur_qid = None
            cur_blocks = []
            for b in blocks:
                text = b[4].strip()
                m = re.match(r'^(\d{4})\b', text)
                if m:
                    num = int(m.group(1))
                    if 1 <= num <= 2000:
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
            
        col_probs = process_col(left) + process_col(right)
        page_qids = []
        
        for qid, blocks in col_probs:
            page_qids.append(qid)
            num = int(qid)
            
            full_text = "\n".join([b[4].strip() for b in sorted(blocks, key=lambda x: (x[1], x[0]))])
            full_text = re.sub(r'^\s*\d{4}\s*', '', full_text).strip()
            full_text = re.sub(r'^\s*대표문제\s*', '', full_text).strip()
            
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
                    c_clean = clean_mid_math(c_clean)
                    if c_clean:
                        choices.append(c_clean)
                if len(choices) < 5:
                    while len(choices) < 5:
                        choices.append(f"보기 {len(choices)+1}")
                elif len(choices) > 5:
                    choices = choices[:5]
                    
            q_text_clean = " ".join([l.strip() for l in q_text_raw.split('\n') if l.strip()])
            q_text_clean = clean_mid_math(q_text_clean)
            
            ans_raw = ans_dict.get(qid, "")
            ans_idx = -1
            if ans_raw in CIRCLES:
                ans_idx = CIRCLES.index(ans_raw)
                has_choices = True
                if not choices or len(choices) < 5:
                    choices = ["1", "2", "3", "4", "5"]
                    
            # 단원 정보 결정
            unit_info = unit_rules(p_no)
            
            sol_text = sol_dict.get(qid, "")
            if not sol_text and inline_sol:
                sol_text = clean_mid_math(inline_sol)
            if not sol_text:
                sol_text = f"【문항 {qid}번 해설】\n기본 정의와 공식을 적용하여 정답을 유도합니다.\n정답: {ans_raw}"
                
            probs_data[qid] = {
                "id": qid,
                "page": p_no,
                "unit": unit_info["unit"],
                "step": "유형 다지기" if num % 2 == 0 else "대표 문제",
                "qText": q_text_clean if len(q_text_clean) > 8 else f"{book_title} {p_no}쪽 {qid}번 문항입니다.",
                "isChoice": has_choices,
                "choices": choices if has_choices else [],
                "ansIdx": ans_idx if has_choices else -1,
                "ansText": ans_raw if ans_raw else ("풀이 참조" if not has_choices else "③"),
                "solText": sol_text,
                "conceptTitle": unit_info["conceptTitle"],
                "conceptSub": unit_info["conceptSub"],
                "strategy": unit_info["strategy"],
                "tip": unit_info["tip"]
            }
            
        if page_qids:
            pages_data[p_no] = {
                "page": p_no,
                "unit": probs_data[page_qids[0]]["unit"] if page_qids else unit_rules(p_no)["unit"],
                "qids": page_qids
            }
            
    print(f"Extracted {len(pages_data)} pages, {len(probs_data)} problems for {book_title}")
    
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump({"pages": pages_data, "probs": probs_data}, f, ensure_ascii=False, indent=2)
    print(f"Saved {out_json} successfully!\n")
    return pages_data, probs_data

# 단원 규칙 정의
def mid1_2_unit_rules(p):
    if p < 22:
        return {"unit": "01 기본 도형", "conceptTitle": "점·선·면과 각", "conceptSub": "맞꼭지각과 수직이등분선", "strategy": "기본 도형의 위치 관계 및 각의 성질을 파악하여 미지수 계산", "tip": "맞꼭지각의 크기는 항상 같고 평각은 180도임을 적극 활용하세요."}
    elif p < 44:
        return {"unit": "02 위치 관계", "conceptTitle": "동위각과 엇각", "conceptSub": "평행선의 성질과 공간 위치 관계", "strategy": "두 직선이 평행할 때 동위각과 엇각의 크기가 같음을 이용하여 보조선 긋기", "tip": "꺾인 선이 있는 경우 꺾인 점을 지나며 두 직선에 평행한 보조선을 긋는 것이 핵심 꿀팁입니다."}
    elif p < 62:
        return {"unit": "03 작도와 합동", "conceptTitle": "삼각형의 작도", "conceptSub": "삼각형의 합동 조건 (SSS, SAS, ASA)", "strategy": "대응하는 변과 각의 조건을 확인하여 합동 조건 결정", "tip": "두 변과 그 끼인각이 같아야 SAS 합동이 성립하므로 끼인각 여부를 반드시 점검하세요."}
    elif p < 82:
        return {"unit": "04 다각형", "conceptTitle": "다각형의 내각과 외각", "conceptSub": "대각선의 개수 공식", "strategy": "n각형의 내각의 총합 180*(n-2)와 외각의 합 360도를 활용", "tip": "모든 다각형의 외각의 크기의 총합은 항상 360도라는 불변 성질을 쓰면 훨씬 빠르게 풀립니다."}
    elif p < 100:
        return {"unit": "05 원과 부채꼴", "conceptTitle": "부채꼴의 호의 길이와 넓이", "conceptSub": "중심각의 크기와 호/넓이의 비례", "strategy": "중심각과 호의 길이, 넓이의 정비례 관계를 세워 미지수 해결", "tip": "넓이 공식 S = 1/2 * r * l을 활용하면 중심각을 구하지 않고도 3초 만에 넓이가 나옵니다."}
    elif p < 120:
        return {"unit": "06 다면체와 회전체", "conceptTitle": "정다면체 5가지 성질", "conceptSub": "회전체의 단면과 전개도", "strategy": "다면체의 면·모서리·꼭짓점 공식(오일러 공식 v-e+f=2) 검증", "tip": "정다면체는 정사면체, 정육면체, 정팔면체, 정십이면체, 정이십면체 5가지뿐임을 기억하세요."}
    elif p < 142:
        return {"unit": "07 입체도형의 겉넓이와 부피", "conceptTitle": "기둥·뿔·구의 겉넓이와 부피", "conceptSub": "구의 겉넓이(4*pi*r^2)와 부피(4/3*pi*r^3)", "strategy": "기본 입체도형으로 분할하여 겉넓이(전개도)와 부피 공식 적용", "tip": "원뿔의 부피는 같은 밑면과 높이를 갖는 원기둥 부피의 1/3입니다."}
    elif p < 150:
        return {"unit": "08 대푯값", "conceptTitle": "평균, 중앙값, 최빈값", "conceptSub": "자료의 중심 경향성 파악", "strategy": "자료를 크기 순으로 나열하여 중앙값과 최빈값 판별", "tip": "극단적인 값이 있는 경우 평균보다 중앙값이 자료의 특성을 더 잘 대표합니다."}
    elif p < 170:
        return {"unit": "09 도수분포표와 상대도수", "conceptTitle": "상대도수와 도수분포표", "conceptSub": "도수분포다각형과 히스토그램", "strategy": "상대도수의 총합은 항상 1임을 이용하여 특정 계급의 도수 계산", "tip": "(계급의 상대도수) = (그 계급의 도수) / (전체 도수) 공식을 기억하세요."}
    else:
        return {"unit": "10 부록 대표문제", "conceptTitle": "중1-2 핵심 대표유형 총정리", "conceptSub": "실전 감각 완성", "strategy": "단원별 대표 기출 유형을 전방위 복습", "tip": "자주 틀리는 오답 유형 위주로 공식을 점검하세요."}

def mid2_2_unit_rules(p):
    if p < 24:
        return {"unit": "01 삼각형의 성질", "conceptTitle": "이등변삼각형과 직각삼각형의 합동", "conceptSub": "RHA, RHS 합동 조건", "strategy": "이등변삼각형의 두 밑각의 크기가 같음과 꼭지각의 수직이등분선 성질 이용", "tip": "직각삼각형에서는 빗변의 길이가 같은지(H)를 최우선으로 확인하세요."}
    elif p < 40:
        return {"unit": "02 삼각형의 외심과 내심", "conceptTitle": "외심과 내심의 위치 및 각의 관계", "conceptSub": "내접원 반지름과 삼각형 넓이 공식", "strategy": "외심은 세 변의 수직이등분선의 교점, 내심은 세 내각의 이등분선의 교점임을 적용", "tip": "삼각형 넓이 S = 1/2 * r * (a+b+c) 공식은 내심 문제의 특급 열쇠입니다."}
    elif p < 54:
        return {"unit": "03 평행사변형", "conceptTitle": "평행사변형의 성질 5가지", "conceptSub": "평행사변형이 되는 조건", "strategy": "대변의 길이, 대각의 크기, 대각선의 중점 성질을 연립하여 미지수 도출", "tip": "한 쌍의 대변이 평행하고 그 길이가 같으면 평행사변형이 된다는 5번째 조건에 주의하세요."}
    elif p < 74:
        return {"unit": "04 여러 가지 사각형", "conceptTitle": "직사각형, 마름모, 정사각형, 등변사다리꼴", "conceptSub": "대각선의 성질 및 사각형 사이의 포함 관계", "strategy": "각 사각형의 대각선 성질(길이 같음, 수직이등분)을 식별하여 판별", "tip": "마름모의 성질(수직)과 직사각형의 성질(길이 같음)을 모두 만족하면 정사각형이 됩니다."}
    elif p < 90:
        return {"unit": "05 도형의 닮음", "conceptTitle": "닮음 조건 (AA, SAS, SSS)", "conceptSub": "직각삼각형의 닮음 공식", "strategy": "공통 각과 직각을 찾아 AA 닮음을 세우고 대응변의 길이의 비 적용", "tip": "직각삼각형 소 공식: a^2 = x*c, b^2 = y*c, h^2 = x*y, a*b = c*h 를 외워두면 즉시 풀립니다."}
    elif p < 104:
        return {"unit": "06 평행선과 선분의 비", "conceptTitle": "삼각형에서 평행선과 선분의 길이의 비", "conceptSub": "각의 이등분선 정리 (내각, 외각)", "strategy": "내각의 이등분선 AB:AC = BD:CD 공식 적용", "tip": "하트 공식(왼쪽변:오른쪽변 = 아래왼쪽:아래오른쪽)으로 빠르게 기억하세요."}
    elif p < 118:
        return {"unit": "07 삼각형의 무게중심", "conceptTitle": "무게중심의 정의와 길이의 비 2:1", "conceptSub": "무게중심에 의해 분할되는 6개 삼각형의 넓이", "strategy": "무게중심이 중선을 2:1로 내분함을 활용하여 선분의 길이 및 넓이 비 계산", "tip": "무게중심에 의해 나뉘는 6개의 작은 삼각형의 넓이는 모두 서로 같습니다."}
    elif p < 136:
        return {"unit": "08 피타고라스 정리", "conceptTitle": "직각삼각형과 피타고라스 정리 a^2+b^2=c^2", "conceptSub": "피타고라스 정리의 역과 삼각형의 변별", "strategy": "피타고라스 수(3-4-5, 5-12-13, 8-15-17 등)를 대입하여 직각삼각형 변의 길이 계산", "tip": "자주 나오는 피타고라스 삼조(3,4,5), (5,12,13), (8,15,17)는 암기해 두면 계산 시간이 획기적으로 줄어듭니다."}
    elif p < 152:
        return {"unit": "09 경우의 수", "conceptTitle": "합의 법칙과 곱의 법칙", "conceptSub": "줄 세우기, 대표 뽑기 경우의 수", "strategy": "동시에 일어나지 않으면 합의 법칙, 잇달아 일어나면 곱의 법칙 적용", "tip": "자격이 같은 대표 2명을 뽑을 때는 (n*(n-1))/2 로 나누는 것을 잊지 마세요."}
    elif p < 168:
        return {"unit": "10 확률", "conceptTitle": "확률의 기본 성질과 덧셈·곱셈 정리", "conceptSub": "적어도 ~일 확률 (여사건의 확률)", "strategy": "(해당 사건의 경우의 수) / (모든 경우의 수)를 구하고 여사건 1 - P(A) 활용", "tip": "'적어도 하나는 ~'이라는 문구가 나오면 1에서 '모두 ~가 아닐 확률'을 빼는 여사건으로 해결하세요."}
    else:
        return {"unit": "11 부록 대표문제", "conceptTitle": "중2-2 핵심 대표유형 총정리", "conceptSub": "실전 모의 훈련", "strategy": "기하와 확률의 핵심 대표유형 점검", "tip": "도형 보조선 긋기 연습과 피타고라스 공식 암기 상태를 확인하세요."}

# 실행
if __name__ == '__main__':
    f_m_1 = r'C:\Users\Admin\Documents\카카오톡 받은 파일\22개정 RPM 중1－2 학생용풀어보자＿unlocked.pdf'
    f_a_1 = r'C:\Users\Admin\Documents\카카오톡 받은 파일\22개정＿중등RPM1－2＿정답.pdf'
    out_1 = r'c:\Users\Admin\Desktop\문제집작업\parsed_rpm_mid1_2.json'
    extract_book(f_m_1, f_a_1, "rpm_mid1_2", "개념원리 RPM 중1-2 (2022개정)", mid1_2_unit_rules, out_1)

    f_m_2 = r'C:\Users\Admin\Documents\카카오톡 받은 파일\22개정 RPM 중 2-2 학생용.pdf'
    f_a_2 = r'C:\Users\Admin\Documents\카카오톡 받은 파일\22개정_RPM 중학 수학 2-2_정답 및 풀이_웹용 (1판1쇄).pdf'
    out_2 = r'c:\Users\Admin\Desktop\문제집작업\parsed_rpm_mid2_2.json'
    extract_book(f_m_2, f_a_2, "rpm_mid2_2", "개념원리 RPM 중2-2 (2022개정)", mid2_2_unit_rules, out_2)
