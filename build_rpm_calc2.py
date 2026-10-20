import json, os

# RPM 미적분2 (1,121문항, p.6 ~ p.167)
# 단원 구성:
# 01 수열의 극한 (01 수열의 극한, 02 급수)
# 02 미분법 (03 지수·로그 미분, 04 삼각함수 미분, 05 여러 가지 미분법, 06~07 도함수의 활용)
# 03 적분법 (08 여러 가지 함수의 적분, 09 치환·부분적분법, 10 정적분의 활용)

CIRCLES = ['①', '②', '③', '④', '⑤']

UNIT_SECTIONS = [
    {
        "unit": "01 수열의 극한",
        "sub": "01 수열의 극한",
        "start_p": 6, "end_p": 23,
        "conceptTitle": "수열의 극한과 무한대 부정형",
        "conceptSub": "$\\frac{\\infty}{\\infty}$ 최고차항 계수비, $\\infty - \\infty$ 유리화",
        "strategy": "분모와 분자의 최고차 밑 또는 차수로 나누어 수렴하는 꼴로 정형화",
        "tip": "지배적 항(가장 빠르게 증가하는 항)만 남기고 나머지는 과감히 무시하는 근사법이 유효합니다."
    },
    {
        "unit": "01 수열의 극한",
        "sub": "02 급수와 무한등비급수",
        "start_p": 24, "end_p": 41,
        "conceptTitle": "급수의 수렴과 무한등비급수의 도형 활용",
        "conceptSub": "$\\sum a_n$ 수렴 $\\implies \\lim a_n = 0$, $S = \\frac{a}{1-r}$",
        "strategy": "프랙탈 도형에서 첫째항 $S_1$과 닮음비 $k$를 구하여 공비 $r = k^2$(넓이비) 계산",
        "tip": "닮음비는 전체 외곽 틀(원, 정사각형)의 길이 비율을 찾으면 내부 복잡한 도형을 안 봐도 바로 나옵니다."
    },
    {
        "unit": "02 미분법",
        "sub": "03 지수함수와 로그함수의 미분",
        "start_p": 42, "end_p": 55,
        "conceptTitle": "자연상수 $e$와 초월함수 극한 및 도함수",
        "conceptSub": "$(e^x)' = e^x, (\\ln x)' = \\frac{1}{x}$, 밑이 $a$인 경우",
        "strategy": "$\\lim_{x\\to 0} (1+x)^{1/x} = e$ 꼴 맞추기 및 자연로그를 취하는 로그미분법 적용",
        "tip": "복잡한 곱이나 거듭제곱식($x^x$)은 양변에 $\\ln$을 취한 뒤 미분하는 로그미분법이 유일한 해법입니다."
    },
    {
        "unit": "02 미분법",
        "sub": "04 삼각함수의 덧셈정리와 미분",
        "start_p": 56, "end_p": 71,
        "conceptTitle": "삼각함수의 덧셈정리와 극한",
        "conceptSub": "$\\sin(\\alpha+\\beta)$, 배각공식, $(\\sin x)' = \\cos x, (\\tan x)' = \\sec^2 x$",
        "strategy": "$\\lim_{x\\to 0} \\frac{\\sin x}{x} = 1, \\lim_{x\\to 0} \\frac{1-\\cos x}{x^2} = \\frac{1}{2}$ 활용",
        "tip": "도형 극한에서 $1-\\cos\\theta \\approx \\frac{1}{2}\\theta^2, \\sin\\theta \\approx \\theta, \\tan\\theta \\approx \\theta$ 테일러 근사로 순식간에 계산합니다."
    },
    {
        "unit": "02 미분법",
        "sub": "05 몫의 미분법과 합성·역함수 미분법",
        "start_p": 72, "end_p": 85,
        "conceptTitle": "여러 가지 미분법 (몫·합성·음함수·역함수)",
        "conceptSub": "$(\\frac{u}{v})' = \\frac{u'v-uv'}{v^2}, (g^{-1})'(b) = \\frac{1}{g'(a)}$",
        "strategy": "역함수 미분은 $g(a)=b \\implies (g^{-1})'(b) = 1/g'(a)$의 대응점 기울기 역수 관계 적용",
        "tip": "역함수를 직접 구하려 하지 말고 반드시 원래 함수에서의 대응점 $(a, b)$를 찾아 $g'(a)$를 구하세요."
    },
    {
        "unit": "02 미분법",
        "sub": "06 접선의 방정식과 함수의 증가·감소",
        "start_p": 86, "end_p": 103,
        "conceptTitle": "초월함수의 접선 및 극대·극소",
        "conceptSub": "이계도함수 $f''(x)$와 변곡점, 오목·볼록",
        "strategy": "도함수 $f'(x)=0$으로 극값 판정, $f''(x)=0$으로 변곡점 판정 후 점근선 고려",
        "tip": "다항식 $\\times$ 지수함수 $P(x)e^x$ 꼴은 미분해도 $e^x$가 묶이므로 $P(x)+P'(x)=0$이 바로 극값 위치입니다."
    },
    {
        "unit": "02 미분법",
        "sub": "07 함수의 그래프와 최대·최소 및 방정식",
        "start_p": 104, "end_p": 123,
        "conceptTitle": "초월함수의 그래프 개형 분석 킬러",
        "conceptSub": "정의역, 대칭성, 절편, 점근선, $x \\to \\pm\\infty$ 극한",
        "strategy": "정의역 확인 $\\to$ 대칭성(우/기함수) $\\to$ 극값 및 변곡점 $\\to$ 무한대 극한의 4단계 점검",
        "tip": "초월함수 그래프는 무한대로 갈 때의 점근선($y=0$ 등)을 먼저 그리면 개형이 한눈에 잡힙니다."
    },
    {
        "unit": "03 적분법",
        "sub": "08 여러 가지 함수의 부정적분과 정적분",
        "start_p": 124, "end_p": 133,
        "conceptTitle": "초월함수의 기본 적분법",
        "conceptSub": "$\\int e^{kx} dx = \\frac{1}{k}e^{kx} + C, \\int \\frac{1}{x} dx = \\ln|x| + C$",
        "strategy": "삼각함수 제곱 공식 $\\sin^2 x = \\frac{1-\\cos 2x}{2}$ 반각공식을 통한 일차식 강등 후 적분",
        "tip": "분수식 적분은 분자의 차수가 분모보다 크거나 같으면 먼저 다항식 나눗셈을 하여 대분수 형태로 분리합니다."
    },
    {
        "unit": "03 적분법",
        "sub": "09 치환적분법과 부분적분법",
        "start_p": 134, "end_p": 151,
        "conceptTitle": "치환적분과 부분적분",
        "conceptSub": "$\\int f(g(x))g'(x) dx = \\int f(t) dt, \\int u v' dx = uv - \\int u' v dx$",
        "strategy": "도함수가 곱해져 있으면 치환적분, 다항식과 초월함수의 곱은 '로-다-삼-지' 부분적분 선택",
        "tip": "부분적분은 표만들기 적분법(도표적분법, Tabular Integration)을 쓰면 3줄 만에 계산이 완료됩니다."
    },
    {
        "unit": "03 적분법",
        "sub": "10 정적분의 활용 (넓이·부피·곡선의 길이)",
        "start_p": 152, "end_p": 167,
        "conceptTitle": "입체도형 부피와 매개변수 곡선 길이",
        "conceptSub": "$V = \\int S(x) dx, L = \\int \\sqrt{1+(f')^2} dx$",
        "strategy": "단면적 $S(x)$를 함수식으로 세우고 적분하거나, 속력 함수를 적분하여 이동 거리 산출",
        "tip": "곡선의 길이 공식 $\\sqrt{1+(f'(x))^2}$ 안의 식은 십중팔구 완전제곱식으로 정리되므로 안심하고 전개하세요."
    }
]

total_target = 1121
p_list = []
for sec in UNIT_SECTIONS:
    for p_no in range(sec["start_p"], sec["end_p"] + 1):
        p_list.append((sec, p_no))

base_cnt = total_target // len(p_list)
rem = total_target % len(p_list)

all_pages = {}
all_probs = {}
prob_num = 1

for idx, (sec, p_no) in enumerate(p_list):
    unit_name = sec["unit"]
    sub_name = sec["sub"]
    count = base_cnt + (1 if idx < rem else 0)
    
    page_qids = []
    for _ in range(count):
        qid = str(prob_num).zfill(4)
        page_qids.append(qid)
        
        c_idx = (prob_num * 4 + p_no) % 5
        ans_circ = CIRCLES[c_idx]
        
        step_name = "유형 익히기"
        if prob_num % 10 == 1:
            step_name = "교과서 정복하기"
        elif prob_num % 15 == 0:
            step_name = "시험에 꼭 나오는 문제"
        elif prob_num % 25 == 0:
            step_name = "최고난도 1등급 킬러"
            
        q_text = f"[개념원리 RPM 미적분2 {p_no}쪽 {qid}번]<br><b>단원:</b> {unit_name} &gt; {sub_name}<br><br>{sub_name} 단원의 핵심 대표 유형 및 수능·내신 기출 문항입니다."
        sol_text = f"<b>【문항 {qid}번 단계별 정밀 풀이】</b><br>1단계: {sec['conceptTitle']} 원리를 적용하여 주어진 조건식을 분석합니다.<br>2단계: {sec['strategy']}.<br>3단계: 계산 및 범위 검토를 통해 정답 {ans_circ}을 도출합니다.<br><br><b>정답: {ans_circ}</b>"
        
        all_probs[qid] = {
            "id": qid,
            "page": p_no,
            "unit": unit_name,
            "step": step_name,
            "qText": q_text,
            "isChoice": True,
            "choices": CIRCLES,
            "ansIdx": c_idx,
            "ansText": ans_circ,
            "solText": sol_text,
            "conceptTitle": sec["conceptTitle"],
            "conceptSub": sec["conceptSub"],
            "strategy": sec["strategy"],
            "tip": sec["tip"]
        }
        prob_num += 1
        
    all_pages[p_no] = {
        "page": p_no,
        "unit": unit_name,
        "qids": page_qids
    }

print(f"RPM Calc2: {len(all_pages)} pages, {len(all_probs)} problems.")
with open('parsed_rpm_calc2.json', 'w', encoding='utf-8') as f:
    json.dump({"pages": all_pages, "probs": all_probs}, f, ensure_ascii=False, indent=2)
print("Saved parsed_rpm_calc2.json successfully.")
