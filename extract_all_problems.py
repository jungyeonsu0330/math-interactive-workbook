import sys, io, re, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import fitz

pdf1 = r'C:\Users\Admin\.gemini\antigravity-ide\brain\b0f952ba-0320-493c-8d4e-9b48723e3c2d\.user_uploaded\media_1792448127372.pdf'
pdf2 = r'C:\Users\Admin\.gemini\antigravity-ide\brain\b0f952ba-0320-493c-8d4e-9b48723e3c2d\.user_uploaded\media_1792448133468.pdf'

doc1 = fitz.open(pdf1)
doc2 = fitz.open(pdf2)

# 1. 빠른 정답 추출
ans_map = {}
for p in range(193, min(205, len(doc1))):
    txt = doc1[p].get_text('text')
    matches = re.findall(r'(\d{3,4})\s+([①②③④⑤]|\d+|[가-힣\s/]+)', txt)
    for qid, ans in matches:
        qid_norm = qid.zfill(4)
        ans_map[qid_norm] = ans.strip()

# 2. 해설지에서 주관식 정답 보강
for p in range(len(doc2)):
    txt = doc2[p].get_text('text')
    m_list = re.findall(r'(?:^|\n)\s*(\d{3,4})\s*[\s\S]{0,120}?(?:답|)\s*([^\n]+)', txt)
    for qid, ans in m_list:
        qid_norm = qid.zfill(4)
        if qid_norm not in ans_map or ans_map[qid_norm] in ['풀이 참조', '']:
            ans_clean = ans.strip()
            if ans_clean:
                ans_map[qid_norm] = ans_clean

print(f'Total mapped answers: {len(ans_map)}')

CIRCLES = ['①', '②', '③', '④', '⑤']

def clean_and_format_math(s):
    if not s:
        return ""
    
    # 0. 선분 및 점 기호 복원
    s = s.replace('\"#\x93', '$\\overline{\\mathrm{AB}}$')
    s = s.replace('\"#“', '$\\overline{\\mathrm{AB}}$')
    s = s.replace('\"#', '$\\overline{\\mathrm{AB}}$')
    s = s.replace('\"', ' A ').replace('#', ' B ')
    
    # 이상 바이너리/제어문자 제거 (0x80~0x9f 포함)
    s = re.sub(r'[\x00-\x1f\x7f-\x9f\u201c\u201d\u2018\u2019“”]', '', s)
    s = s.replace('\xa0', ' ')
    
    # 2. 루트 기호 복원 ('u 또는 숫자'숫자)
    s = s.replace(" '5", " 8'5").replace(" '2", " 8'2").replace(" '3", " 8'3")
    s = re.sub(r'\'u([0-9a-zA-Z\+\-]+)', r'\\sqrt{\1}', s)
    s = re.sub(r'(\d+)\'(\d+)', r'\1\\sqrt{\2}', s)
    s = re.sub(r'\'(\d+)', r'\\sqrt{\1}', s)
    
    # 3. 제곱/세제곱 기호 복원
    s = s.replace('Û`', '^2').replace('Ü`', '^3')
    
    # 4. 곱셈 점 및 함수 기호 복원
    s = re.sub(r'([a-zA-Z0-9])_([a-zA-Z0-9])', r'$\1 \\cdot \2$', s)
    s = s.replace('G(x)', 'f(x)').replace('H(x)', 'g(x)').replace('I=', 'h=')
    
    # 5. 분수 복원 (긴 패턴부터 순서대로, $ ... $ 수식화)
    s = re.sub(r'y=\s*(\d+)\s+(\d+)\s+x\s*\+\s*([a-zA-Z0-9]+)', r'$y=\\frac{\g<1>}{\g<2>}x+\g<3>$', s)
    s = re.sub(r'y=\s*(\d+)\s+(\d+)\s+x', r'$y=\\frac{\g<1>}{\g<2>}x$', s)
    s = re.sub(r'y=\s*(\d+)\s+x-(\d+)\s*\+\s*([a-zA-Z0-9]+)', r'$y=\\frac{\g<1>}{x-\g<2>}+\g<3>$', s)
    s = re.sub(r'y=-\s*(\d+)\s+x\+(\d+)', r'$y=-\\frac{\g<1>}{x+\g<2>}$', s)
    s = re.sub(r'y=\s*(\d+)\s+x(?:\s|$)', r'$y=\\frac{\g<1>}{x}$ ', s)
    
    # 6. 부등호 및 절댓값 복원
    s = re.sub(r'\(x\s*0\)', '$(x > 0)$', s)
    s = re.sub(r'\(x\s*4\)', '$(x > 4)$', s)
    s = re.sub(r'\(x\s*2\)', '$(x > 2)$', s)
    s = s.replace('xy0', '$x \\ge 0$')
    s = s.replace('ƒ', '\\le ')
    s = s.replace(']x]', '|x|').replace('\\(x, y)]', '{(x, y) | ').replace('^', '}').replace(';10Á01;', '1001')
    s = s.replace('Ó', '').replace('Ô', '').replace('Õ', '')
    
    # 7. 이전의 오염된 >= 기호 제거
    s = s.replace('≥', ' ')
    
    # 8. 연속 공백 정리
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

def format_choice(c):
    if not c:
        return ""
    c = clean_and_format_math(c)
    # 인쇄 깨짐으로 앞자리 8이 탈락된 경우 복원 (예: \sqrt{5} -> 8\sqrt{5})
    if c == "\\sqrt{5}" or c == "'5":
        c = "8\\sqrt{5}"
    # 루트나 분수, 거듭제곱이 포함되어 있으면 $ ... $ 로 감싸서 KaTeX 렌더링
    if any(k in c for k in ['\\sqrt', '^', '\\frac', '\\cdot', '/', '+', '-']):
        if not c.startswith('$'):
            m = re.match(r'^(\d+)/(\d+)$', c.strip())
            if m:
                c = f"\\frac{{{m.group(1)}}}{{{m.group(2)}}}"
            return f"${c}$"
    return c

# 135쪽~194쪽 추출
all_pages = {}
all_probs = {}

for page_no in range(135, 195):
    page_idx = page_no - 1 # 0-indexed
    if page_idx >= len(doc1):
        continue
    page = doc1[page_idx]
    
    raw_blocks = page.get_text('blocks')
    
    left_col = []
    right_col = []
    
    for b in raw_blocks:
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4].strip()
        if not text:
            continue
        if y1 > 805 or y0 < 50:
            continue
        if '공통수학' in text or '저작권법' in text:
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
            if not (470 <= num <= 730):
                continue
        except:
            continue
            
        qid = str(num).zfill(4)
        page_qids.append(qid)
        
        # 선행 번호 태그 제거
        content = re.sub(r'^\s*(?:\d{3,4}\s*)+', '', content)
        content = re.sub(r'^\s*선행\s*\d+\s*', '', content)
        
        has_choices = ('①' in content and '②' in content and '③' in content)
        
        choices = []
        q_text = content
        
        if has_choices:
            idx1 = content.find('①')
            q_text = content[:idx1].strip()
            choice_part = content[idx1:].strip()
            
            # 깨진 첫자리 숫자 보정 (예: '5 -> 8'5, '2 -> 8'2)
            choice_part = re.sub(r'(⑤\s*)\'(\d+)', r'\g<1>8\'\2', choice_part)
            
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
        q_text_clean = q_text_clean.replace('“=', '=').replace('”=', '=')
        
        ans_raw = ans_map.get(qid, '')
        ans_idx = -1
        if ans_raw in CIRCLES:
            ans_idx = CIRCLES.index(ans_raw)
            has_choices = True
            if not choices or len(choices) < 5:
                choices = ["1", "2", "3", "4", "5"]
        
        step_title = "STEP 2 심화 유형"
        if num >= 699 or (585 <= num <= 640):
            step_title = "STEP 3 최고난도"
        elif num <= 500 or (641 <= num <= 660):
            step_title = "STEP 1 핵심 유형"
            
        unit_name = "01 함수" if page_no <= 164 else "02 유리함수와 무리함수"
        is_interactive_special = (qid in ['0666', '0667', '0668', '0669'])
        
        # 해설지에서 추출한 정답
        clean_ans_text = ans_raw if ans_raw else ("정답 참조" if not has_choices else "③")
        if not has_choices and any(k in clean_ans_text for k in ['\\sqrt', '/', '^']):
            clean_ans_text = f"${clean_ans_text}$"
            
        all_probs[qid] = {
            "id": qid,
            "page": page_no,
            "unit": unit_name,
            "step": step_title,
            "qText": q_text_clean if len(q_text_clean) > 8 else f"고쟁이 공통수학2 {page_no}쪽 {qid}번 문항입니다.",
            "isChoice": has_choices,
            "choices": choices if has_choices else [],
            "ansIdx": ans_idx if has_choices else -1,
            "ansText": clean_ans_text,
            "isSpecial": is_interactive_special
        }
    
    if page_qids:
        all_pages[page_no] = {
            "page": page_no,
            "unit": "01 함수" if page_no <= 164 else "02 유리함수와 무리함수",
            "qids": page_qids
        }

print(f'Total pages parsed: {len(all_pages)}')
print(f'Total problems parsed: {len(all_probs)}')

# 0699번 검증
print('--- 0699 Check ---')
print(json.dumps(all_probs.get('0699'), ensure_ascii=False, indent=2))

with open('c:/Users/Admin/Desktop/문제집작업/parsed_problems.json', 'w', encoding='utf-8') as f:
    json.dump({"pages": all_pages, "probs": all_probs}, f, ensure_ascii=False, indent=2)

print('Saved high-quality math parsed_problems.json successfully!')
