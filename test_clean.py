import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

raw = """다음은 ‘삼각형의 세 변의 수직이등분선은 한 점 에서 만난다.’를 증명하는 과정이다. ㈎~㈒에 알맞은 것을 구하시오. sABC에서 ABÓ, BCÓ의 수직이등 " 분선의 교점을 O라 하고, 점 O에 % 서 ACÓ에 내린 수선의 발을 D라 0 하자. # 점 O는 ABÓ의 수직이등분선 위에 있으므로 OAÓ=OBÓ 또 점 O는 BCÓ의 수직이등분선 위에 있으므로 ㈎ =OCÓ ∴ OAÓ= ㈏ 한편 sOAD와 sOCD에서 ∠ODA=∠ODC=90ù, OAÓ= ㈏ , 이므로 sOADªsOCD`( ㈑ 합동) ㈐ 는 공통 ∴ ADÓ= ㈒ 즉 ODÓ는 ACÓ의 수직이등분선이다. 따라서 sABC의 세 변의 수직이등분선은 한 점 O에 서 만난다."""

def clean_mid_math(s):
    if not s: return ""
    # 이상 바이너리 제어문자 제거
    s = s.replace('\x00', '').replace('\xa0', ' ').replace('\u2009', ' ')
    s = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)
    
    # 본문 텍스트 내에서 다이어그램 레이블 아티팩트 제거
    s = re.sub(r'(?<=\s)[\"#%](?=\s)', '', s)
    s = re.sub(r'#\s*\$', '', s)
    s = re.sub(r'(?<=[가-힣])\s*"\s*(?=[가-힣])', '', s)
    s = re.sub(r'(?<=[가-힣])\s*%\s*(?=[가-힣])', '', s)
    s = re.sub(r'(?<=[가-힣])\s*0\s*하자', '하자', s)
    
    # 기존 단독 $ 제거
    s = s.replace('$', '')
    
    # 기호 변환
    s = s.replace('ù', '^{\\circ}').replace('±', '^{\\circ}')
    s = s.replace('Û`', '^2').replace('Ü`', '^3').replace('`', '')
    
    # LaTeX 기호 변환 (아직 $ 안 붙임)
    s = re.sub(r'([A-Z]{2,3})Ó', r'\\overline{\\mathrm{\1}}', s)
    s = re.sub(r'([A-Z]{2,3})\^_', r'\\overline{\\mathrm{\1}}', s)
    s = re.sub(r'([A-Z]{2,3})ê', r'\\overleftrightarrow{\\mathrm{\1}}', s)
    s = re.sub(r'([A-Z]{2,3})³', r'\\overrightarrow{\\mathrm{\1}}', s)
    s = re.sub(r's([A-Z]{3,4})', r'\\triangle \\mathrm{\1}', s)
    s = re.sub(r'(?:∠|gak)\s*([A-Za-z0-9]+)', r'\\angle \\mathrm{\1}', s)
    s = s.replace('gak', '\\angle ').replace('∠', '\\angle ')
    s = s.replace('ª', ' \\equiv ').replace('∽', ' \\sim ')
    s = s.replace('∥', ' \\parallel ').replace('⊥', ' \\perp ')
    s = s.replace(';2!;', '\\frac{1}{2}')
    s = re.sub(r';(\d+)!;', r'\\frac{1}{\1}', s)
    s = re.sub(r';([0-9a-zA-Z]+);([0-9a-zA-Z]+);', r'\\frac{\1}{\2}', s)
    s = re.sub(r'([0-9a-zA-Z\)])_([0-9a-zA-Z\(])', r'\1 \\times \2', s)

    # 이제 모든 LaTeX 명령어(\overline, \triangle, \angle, \equiv, \sim, \frac, ^{\circ} 등)와 주변 연산자(=, +, -)를 감싸기!
    # \로 시작하는 토큰 식별
    # 단일 LaTeX 수식 토큰을 $...$ 로 감싸기
    pattern = r'(\\(?:overline|overleftrightarrow|overrightarrow|triangle|angle|equiv|sim|parallel|perp|frac)\b(?:\{[^\}]+\})*|\d+\^\{\\circ\}|[a-zA-Z]\^\{\\circ\})'
    s = re.sub(pattern, r'$\1$', s)
    
    # 인접한 수식들 병합: $A$ = $B$ -> $A = B$
    # $A$와 $B$ 사이에 등호, 부등호, 쉼표, 콜론 등이 있는 경우
    for _ in range(5):
        s = re.sub(r'\$([^\$]+)\$\s*([=+\-<>:,~])\s*\$([^\$]+)\$', r'$\1 \2 \3$', s)
        s = re.sub(r'\$([^\$]+)\$\s*([=+\-<>:,~])\s*([0-9A-Za-z]+)', r'$\1 \2 \3$', s)
        s = re.sub(r'([0-9A-Za-z]+)\s*([=+\-<>:,~])\s*\$([^\$]+)\$', r'$\1 \2 \3$', s)
    
    # 공백 정리
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

res = clean_mid_math(raw)
print("Result:")
print(res)
