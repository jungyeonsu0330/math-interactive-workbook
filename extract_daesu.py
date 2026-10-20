import sys, io, re, json, fitz
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f_main = r"C:\Users\Admin\Documents\카카오톡 받은 파일\고쟁이 대수.pdf"
f_ans = r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형,내신 고쟁이 대수 정답과 해설-1.pdf"

doc_m = fitz.open(f_main)
doc_a = fitz.open(f_ans)

print(f"Daesu Main pages: {len(doc_m)}, Ans pages: {len(doc_a)}")

# 1. 빠른 정답 추출 (224~229)
CIRCLES = ['①', '②', '③', '④', '⑤']
ans_map = {}
for p in range(223, len(doc_m)):
    t = doc_m[p].get_text("text")
    matches = re.findall(r'(\d{3,4})\s+([①②③④⑤]|\d+|[가-힣\s/]+)', t)
    for qid, ans in matches:
        ans_map[qid.zfill(4)] = ans.strip()

print(f"Quick answers mapped: {len(ans_map)} items")

# 2. 해설지에서 주관식 정답 보강
for p in range(len(doc_a)):
    t = doc_a[p].get_text("text")
    m_list = re.findall(r'(?:^|\n)\s*(\d{3,4})\s*[\s\S]{0,120}?(?:답|)\s*([^\n]+)', t)
    for qid, ans in m_list:
        qid_norm = qid.zfill(4)
        if qid_norm not in ans_map or ans_map[qid_norm] in ['풀이 참조', '']:
            ans_clean = ans.strip()
            if ans_clean:
                ans_map[qid_norm] = ans_clean

def clean_and_format_math(s):
    if not s:
        return ""
    # 선분 및 점
    s = s.replace('\"#\x93', '$\\overline{\\mathrm{AB}}$').replace('\"#“', '$\\overline{\\mathrm{AB}}$').replace('\"#', '$\\overline{\\mathrm{AB}}$')
    s = s.replace('\"', ' A ').replace('#', ' B ')
    s = re.sub(r'[\x00-\x1f\x7f-\x9f\u201c\u201d\u2018\u2019“”]', '', s)
    s = s.replace('\xa0', ' ')
    
    # 루트
    s = s.replace(" '5", " 8'5").replace(" '2", " 8'2").replace(" '3", " 8'3")
    s = re.sub(r'\'u([0-9a-zA-Z\+\-]+)', r'\\sqrt{\1}', s)
    s = re.sub(r'(\d+)\'(\d+)', r'\1\\sqrt{\2}', s)
    s = re.sub(r'\'(\d+)', r'\\sqrt{\1}', s)
    
    # 거듭제곱 및 지수/로그
    s = s.replace('Û`', '^2').replace('Ü`', '^3').replace('Ý`', '^4')
    s = s.replace('log`', 'log_{').replace('ln`', 'ln ')
    
    # 곱셈 점 및 함수
    s = re.sub(r'([a-zA-Z0-9])_([a-zA-Z0-9])', r'$\1 \\cdot \2$', s)
    s = s.replace('G(x)', 'f(x)').replace('H(x)', 'g(x)')
    
    # 분수
    s = re.sub(r'y=\s*(\d+)\s+(\d+)\s+x\s*\+\s*([a-zA-Z0-9]+)', r'$y=\\frac{\g<1>}{\g<2>}x+\g<3>$', s)
    s = re.sub(r'y=\s*(\d+)\s+(\d+)\s+x', r'$y=\\frac{\g<1>}{\g<2>}x$', s)
    s = re.sub(r'y=\s*(\d+)\s+x-(\d+)\s*\+\s*([a-zA-Z0-9]+)', r'$y=\\frac{\g<1>}{x-\g<2>}+\g<3>$', s)
    s = re.sub(r'y=-\s*(\d+)\s+x\+(\d+)', r'$y=-\\frac{\g<1>}{x+\g<2>}$', s)
    s = re.sub(r'y=\s*(\d+)\s+x(?:\s|$)', r'$y=\\frac{\g<1>}{x}$ ', s)
    
    # 부등호 및 기호
    s = s.replace('ƒ', '\\le ')
    s = s.replace(']x]', '|x|').replace('\\(x, y)]', '{(x, y) | ').replace('^', '}')
    s = s.replace('Ó', '').replace('Ô', '').replace('Õ', '')
    s = s.replace('≥', ' ')
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

def format_choice(c):
    if not c:
        return ""
    c = clean_and_format_math(c)
    if c == "\\sqrt{5}" or c == "'5":
        c = "8\\sqrt{5}"
    if any(k in c for k in ['\\sqrt', '^', '\\frac', '\\cdot', '/', '+', '-']):
        if not c.startswith('$'):
            m = re.match(r'^(\d+)/(\d+)$', c.strip())
            if m:
                c = f"\\frac{{{m.group(1)}}}{{{m.group(2)}}}"
            return f"${c}$"
    return c

# 3. 본문 페이지 파싱 (페이지 7 ~ 223)
all_pages = {}
all_probs = {}

for p_no in range(7, 224):
    p_idx = p_no - 1
    if p_idx >= len(doc_m):
        continue
    page = doc_m[p_idx]
    
    raw_blocks = page.get_text('blocks')
    left_col = []
    right_col = []
    
    for b in raw_blocks:
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4].strip()
        if not text or y1 > 805 or y0 < 50:
            continue
        if '대수' in text or '저작권법' in text:
            continue
        if x0 < 310:
            left_col.append((y0, x0, text))
        else:
            right_col.append((y0, x0, text))
            
    left_col.sort(key=lambda item: item[0])
    right_col.sort(key=lambda item: item[0])
    
    ordered_items = left_col + right_col
    page_text = "\n".join([item[2] for item in ordered_items])
    
    prob_splits = re.split(r'(?:^|\n)\s*(\d{3,4})\s*(?:\n|선행|\b)', page_text)
    page_qids = []
    
    i = 1
    while i < len(prob_splits) - 1:
        qid_raw = prob_splits[i].strip()
        content = prob_splits[i+1].strip()
        i += 2
        
        try:
            num = int(qid_raw)
            if not (1 <= num <= 900):
                continue
        except:
            continue
            
        qid = str(num).zfill(4)
        page_qids.append(qid)
        
        content = re.sub(r'^\s*(?:\d{3,4}\s*)+', '', content)
        content = re.sub(r'^\s*선행\s*\d+\s*', '', content)
        
        has_choices = ('①' in content and '②' in content and '③' in content)
        choices = []
        q_text = content
        
        if has_choices:
            idx1 = content.find('①')
            q_text = content[:idx1].strip()
            choice_part = content[idx1:].strip()
            
            parts = re.split(r'[①②③④⑤]', choice_part)
            for p in parts[1:]:
                c_clean = " ".join([l.strip() for l in p.split('\n') if l.strip()])
                c_clean = re.sub(r'(\d+)\s+(\d+)', r'\1/\2', c_clean)
                c_clean = re.sub(r'^\s*\'(\d+)', r'8\'\1', c_clean)
                formatted = format_choice(c_clean)
                if formatted:
                    choices.append(formatted)
            
            if len(choices) < 5:
                while len(choices) < 5:
                    choices.append(f"보기 {len(choices)+1}")
            elif len(choices) > 5:
                choices = choices[:5]
        
        q_text_clean = " ".join([l.strip() for l in q_text.split('\n') if l.strip()])
        q_text_clean = clean_and_format_math(q_text_clean)
        
        ans_raw = ans_map.get(qid, '')
        ans_idx = -1
        if ans_raw in CIRCLES:
            ans_idx = CIRCLES.index(ans_raw)
            has_choices = True
            if not choices or len(choices) < 5:
                choices = ["1", "2", "3", "4", "5"]
                
        # 대수 단원 추정
        if p_no <= 75:
            unit_name = "01 지수함수와 로그함수"
        elif p_no <= 150:
            unit_name = "02 삼각함수"
        else:
            unit_name = "03 수열"
            
        step_title = "STEP 2 심화 유형"
        if "최고난도" in content or num % 10 in [8, 9, 0]:
            step_title = "STEP 3 최고난도"
        elif num % 10 in [1, 2, 3]:
            step_title = "STEP 1 핵심 유형"
            
        all_probs[qid] = {
            "id": qid,
            "page": p_no,
            "unit": unit_name,
            "step": step_title,
            "qText": q_text_clean if len(q_text_clean) > 8 else f"고쟁이 대수 {p_no}쪽 {qid}번 문항입니다.",
            "isChoice": has_choices,
            "choices": choices if has_choices else [],
            "ansIdx": ans_idx if has_choices else -1,
            "ansText": ans_raw if ans_raw else ("정답 참조" if not has_choices else "③"),
        }
        
    if page_qids:
        all_pages[p_no] = {
            "page": p_no,
            "unit": all_probs[page_qids[0]]["unit"] if page_qids else "01 지수와 로그",
            "qids": page_qids
        }

print(f"Daesu parsed: {len(all_pages)} pages, {len(all_probs)} problems.")
with open('c:/Users/Admin/Desktop/문제집작업/parsed_daesu.json', 'w', encoding='utf-8') as f:
    json.dump({"pages": all_pages, "probs": all_probs}, f, ensure_ascii=False, indent=2)

print("Saved parsed_daesu.json successfully.")
