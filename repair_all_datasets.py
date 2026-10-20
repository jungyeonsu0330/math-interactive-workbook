import json, glob, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fix_math_string(s):
    if not s or not isinstance(s, str):
        return s
    
    # 1. Clean control characters and encoding artifacts
    s = s.replace('\x00', '').replace('\x0c', '+').replace('\x0e', '-').replace('\x1e', '=')
    s = re.sub(r'[\x01-\x08\x0b\x0e-\x1f\x7f-\x9f]', '', s)
    s = s.replace('Â', '').replace('Ã', '').replace('Á', '').replace('Õ', '').replace('Ô', '').replace('Ó', '')
    
    # 2. Fix double/triple consecutive dollar signs like $$\overline{AB}$$ when meant to be inline
    s = re.sub(r'(?<=\w)\$\$(?=\w)', '$ $', s)
    s = re.sub(r'(?<=\})\$\$(?=[가-힣\s\.,]|$)', '$', s)
    s = re.sub(r'\$\$\$+', '$', s)
    
    # 3. Check dollar parity
    # Count unescaped dollars
    tokens = re.split(r'(?<!\\)\$', s)
    # If len(tokens) is even, number of delimiters is odd (unbalanced)
    if len(tokens) % 2 == 0:
        # If the last token contains math symbols (like \frac, \sqrt, ^, _), append a closing $
        last = tokens[-1]
        if any(kw in last for kw in ['\\frac', '\\sqrt', '^', '\\le', '\\ge', '\\pm', '\\cdot', '=']):
            s = s + '$'
        else:
            # Check if there is an isolated stray dollar like ' $ ' or ' $'
            stray_match = re.search(r'\s\$\s', s)
            if stray_match:
                s = re.sub(r'\s\$\s', ' ', s, count=1)
            else:
                # Close the unclosed math token
                s = s + '$'
                
    # 4. Clean consecutive spaces
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

CIRCLES = ['①', '②', '③', '④', '⑤']

def repair_dataset(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    probs = data.get('probs', {})
    pages = data.get('pages', {})
    
    fixed_dollar = 0
    fixed_ans = 0
    
    for qid, p in probs.items():
        q_orig = p.get('qText', '')
        q_new = fix_math_string(q_orig)
        if q_orig != q_new:
            p['qText'] = q_new
            fixed_dollar += 1
            
        sol_orig = p.get('solText', '')
        sol_new = fix_math_string(sol_orig)
        if sol_orig != sol_new:
            p['solText'] = sol_new
            
        # Clean choices
        if 'choices' in p and isinstance(p['choices'], list):
            p['choices'] = [fix_math_string(c) for c in p['choices']]
            
        # Choice vs Subjective validation
        is_choice = p.get('isChoice', False)
        ans_idx = p.get('ansIdx', -1)
        ans_text = str(p.get('ansText', '')).strip()
        
        # Check if ansText is a circle number
        if ans_text in CIRCLES:
            p['isChoice'] = True
            p['ansIdx'] = CIRCLES.index(ans_text)
            if not p.get('choices') or len(p['choices']) < 5:
                p['choices'] = CIRCLES
        elif not (0 <= ans_idx < 5):
            # It is a short-answer (주관식) question
            p['isChoice'] = False
            p['ansIdx'] = -1
            p['choices'] = []
            fixed_ans += 1
        else:
            # Valid choice
            p['isChoice'] = True
            if not p.get('choices') or len(p['choices']) < 5:
                p['choices'] = CIRCLES
                
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"[{filepath}] Repaired: {fixed_dollar} dollar/math fixes, {fixed_ans} subjective/choice fixes.")

all_datasets = sorted(glob.glob('parsed_*.json'))
print(f"Starting repair on {len(all_datasets)} datasets...")
for jf in all_datasets:
    repair_dataset(jf)
print("All datasets repaired successfully!")
