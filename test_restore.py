import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import fitz

doc1 = fitz.open(r'C:\Users\Admin\.gemini\antigravity-ide\brain\b0f952ba-0320-493c-8d4e-9b48723e3c2d\.user_uploaded\media_1792448127372.pdf')
page187 = doc1[186]
txt = page187.get_text('text')

def restore_korean_math(s):
    # 1. 이상 문자 제거 (인쇄 헤더/푸터 등)
    s = s.replace('\x00', '').replace('\x1d', '')
    
    # 2. 선분 및 점 기호 복원
    # "#“ -> \overline{\mathrm{AB}}
    s = s.replace('\"#“', '$\\overline{\\mathrm{AB}}$')
    s = s.replace('\"#', '$\\overline{\\mathrm{AB}}$')
    # 단독 점 " -> A, # -> B, $ -> C
    s = re.sub(r'\"([라|를|와|의|\s|\)])', r'A\1', s)
    s = re.sub(r'#([라|를|와|의|\s|\)])', r'B\1', s)
    s = re.sub(r'\$([라|를|와|의|\s|\)])', r'C\1', s)
    s = s.replace('"', 'A').replace('#', 'B')
    
    # 3. 루트 기호 복원
    # 4'3 -> 4\sqrt{3}, 4'5 -> 4\sqrt{5}
    s = re.sub(r'(\d+)\'(\d+)', r'$\1\\sqrt{\2}$', s)
    s = re.sub(r'\'(\d+)', r'$\\sqrt{\1}$', s)
    s = re.sub(r'\'u([a-zA-Z0-9\+\-]+)', r'$\\sqrt{\1}$', s)
    
    # 4. 제곱/세제곱 기호 복원
    s = s.replace('Û`', '^2').replace('Ü`', '^3')
    
    # 5. 곱셈 점 복원
    s = re.sub(r'([a-zA-Z0-9])_([a-zA-Z0-9])', r'$\1 \\cdot \2$', s)
    
    # 6. 함수 기호 복원
    s = s.replace('G(x)', '$f(x)$').replace('H(x)', '$g(x)$')
    
    # 7. 분수 형태 복원
    s = re.sub(r'y=\s*(\d+)\s+(\d+)\s+x', r'$y=\\frac{\1}{\2}x$', s)
    s = re.sub(r'y=\s*(\d+)\s+x', r'$y=\\frac{\1}{x}$', s)
    s = re.sub(r'y=\s*(\d+)\s+x-(\d+)\s+\+\s*([a-zA-Z0-9]+)', r'$y=\\frac{\1}{x-\2}+\3$', s)
    
    # 8. 부등호 복원
    s = s.replace('(x 0)', '$(x > 0)$').replace('(x 4)', '$(x > 4)$').replace('(x 2)', '$(x > 2)$')
    s = s.replace('xy0', '$x \\ge 0$')
    s = s.replace('ƒ', '$\\le$').replace('≥', ' ')
    
    # 9. 공백 정리
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

lines = [l.strip() for l in txt.split('\n') if l.strip()]
print('=== Raw sample (0699) ===')
sample = ' '.join(lines[3:15])
print(sample)
print('\n=== Restored ===')
print(restore_korean_math(sample))
