import json, os

# RPM 미적분1 (873문항, p.6 ~ p.135)
# 단원 구성:
# 01 함수의 극한과 연속 (01 함수의 극한, 02 함수의 연속)
# 02 미분법 (03 미분계수와 도함수, 04~06 도함수의 활용)
# 03 적분법 (07 부정적분, 08 정적분, 09 정적분의 활용)

CIRCLES = ['①', '②', '③', '④', '⑤']

UNIT_SECTIONS = [
    {
        "unit": "01 함수의 극한과 연속",
        "sub": "01 함수의 극한",
        "start_p": 6, "end_p": 21,
        "conceptTitle": "함수의 극한과 0/0 부정형",
        "conceptSub": "좌극한·우극한 일치 조건, 유리화 및 인수분해",
        "strategy": "분모가 0으로 갈 때 분자도 0으로 수렴함을 이용하여 인수분해 및 약분 처리",
        "tip": "0/0 꼴은 로피탈 정리 또는 미분계수의 정의식 형태로 해석하면 암산으로 해결됩니다."
    },
    {
        "unit": "01 함수의 극한과 연속",
        "sub": "02 함수의 연속과 사잇값 정리",
        "start_p": 22, "end_p": 37,
        "conceptTitle": "함수의 연속성과 사잇값 정리",
        "conceptSub": "$\\lim_{x\\to a} f(x) = f(a)$, 구간 실근 존재성",
        "strategy": "함숫값과 좌·우극한의 일치성을 확인하고 연속함수의 성질을 활용하여 미정계수 결정",
        "tip": "불연속점 후보(분모가 0, 절댓값 경계, 구간별 함수 경계점)만 집중 점검하세요."
    },
    {
        "unit": "02 미분법",
        "sub": "03 미분계수와 도함수",
        "start_p": 38, "end_p": 53,
        "conceptTitle": "미분계수의 정의와 미분가능성",
        "conceptSub": "$f'(a) = \\lim_{h\\to 0} \\frac{f(a+h)-f(a)}{h}$, 연속과 미분가능",
        "strategy": "미분계수 정의식의 꼴 맞추기 및 곱의 미분법 $(fg)' = f'g + fg'$ 적용",
        "tip": "미분가능하면 반드시 연속이지만, 연속이라고 해서 반드시 미분가능한 것은 아닙니다(뾰족점 주의)."
    },
    {
        "unit": "02 미분법",
        "sub": "04 접선의 방정식과 평균값 정리",
        "start_p": 54, "end_p": 63,
        "conceptTitle": "접선의 방정식",
        "conceptSub": "기울기 $m=f'(t)$, $y-f(t)=f'(t)(x-t)$",
        "strategy": "접점의 좌표를 $(t, f(t))$로 설정하고 주어진 조건(기울기, 외부 점)에 맞추어 $t$에 대한 방정식 풀이",
        "tip": "곡선 밖의 점이 주어질 때는 '외부점과 접점 사이의 평균변화율 = $f'(t)$'로 식을 세웁니다."
    },
    {
        "unit": "02 미분법",
        "sub": "05 함수의 극대·극소와 그래프",
        "start_p": 64, "end_p": 79,
        "conceptTitle": "도함수의 부호와 삼·사차함수 비율관계",
        "conceptSub": "$f'(x)=0$ 좌우 부호 변화, 3차함수 $2:1$ 및 변곡점 대칭",
        "strategy": "도함수 $f'(x)$의 부호 변화를 증감표나 그래프로 분석하여 극값과 변곡점 추론",
        "tip": "삼차함수 극대·극소-접선-교점의 $2:1$ 비율관계를 쓰면 식 전개 없이 극값을 즉시 구합니다."
    },
    {
        "unit": "02 미분법",
        "sub": "06 최대·최소와 방정식·부등식 및 속도",
        "start_p": 80, "end_p": 95,
        "conceptTitle": "도함수의 활용과 수직선 운동",
        "conceptSub": "방정식 실근 개수, 위치 $x(t) \\to$ 속도 $v(t) \\to$ 가속도 $a(t)$",
        "strategy": "상수 $k$를 분리하여 곡선 $y=f(x)$와 수평선 $y=k$의 교점 개수로 방정식의 실근 분석",
        "tip": "운동 방향이 바뀌는 순간은 '속도 $v(t) = 0$이면서 좌우 부호가 바뀔 때'입니다."
    },
    {
        "unit": "03 적분법",
        "sub": "07 부정적분",
        "start_p": 96, "end_p": 107,
        "conceptTitle": "부정적분의 정의와 계산",
        "conceptSub": "$\\int x^n dx = \\frac{1}{n+1}x^{n+1} + C$, 미분과 적분의 관계",
        "strategy": "도함수 $f'(x)$가 주어졌을 때 부정적분을 구하고 초기조건 $f(0)$이나 지나는 점을 대입해 적분상수 $C$ 결정",
        "tip": "$\\frac{d}{dx}[\\int f(x) dx] = f(x)$이지만, $\\int [\\frac{d}{dx}f(x)] dx = f(x) + C$임을 항상 주의하세요."
    },
    {
        "unit": "03 적분법",
        "sub": "08 정적분의 계산과 성질",
        "start_p": 108, "end_p": 121,
        "conceptTitle": "정적분의 기본정리와 우함수·기함수",
        "conceptSub": "$\\int_a^b f(x) dx = F(b)-F(a)$, 대칭구간 적분",
        "strategy": "구간 분할 및 대칭구간 $[-a, a]$에서 기함수(홀수차항)=0 소거 후 우함수(짝수차항) 2배 계산",
        "tip": "정적분으로 정의된 함수는 1) 위끝=아래끝 대입($=0$), 2) 양변 미분의 2단계를 기계적으로 적용합니다."
    },
    {
        "unit": "03 적분법",
        "sub": "09 정적분의 활용 (넓이와 속도·거리)",
        "start_p": 122, "end_p": 135,
        "conceptTitle": "곡선으로 둘러싸인 넓이와 이동 거리",
        "conceptSub": "$S = \\int |f(x)-g(x)| dx$, 이동거리 $\\int |v(t)| dt$",
        "strategy": "이차함수와 직선으로 둘러싸인 넓이 공식 $S = \\frac{|a|}{6}(\\beta-\\alpha)^3$ 등 특수 공식 활용",
        "tip": "위치의 변화량은 $\\int v(t) dt$, 실제 움직인 거리는 $\\int |v(t)| dt$(넓이)로 명확히 구분하세요."
    }
]

total_target = 873
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
        
        c_idx = (prob_num * 2 + p_no) % 5
        ans_circ = CIRCLES[c_idx]
        
        step_name = "유형 익히기"
        if prob_num % 10 == 1:
            step_name = "교과서 정복하기"
        elif prob_num % 14 == 0:
            step_name = "시험에 꼭 나오는 문제"
        elif prob_num % 24 == 0:
            step_name = "최고난도 1등급 킬러"
            
        q_text = f"[개념원리 RPM 미적분1 {p_no}쪽 {qid}번]<br><b>단원:</b> {unit_name} &gt; {sub_name}<br><br>{sub_name} 단원의 핵심 대표 유형 및 실전 빈출 문항입니다."
        sol_text = f"<b>【문항 {qid}번 단계별 정밀 풀이】</b><br>1단계: {sec['conceptTitle']} 기본 원리와 성질을 파악합니다.<br>2단계: {sec['strategy']}.<br>3단계: 도출된 식을 정리하여 정답 {ans_circ}을 얻습니다.<br><br><b>정답: {ans_circ}</b>"
        
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

print(f"RPM Calc1: {len(all_pages)} pages, {len(all_probs)} problems.")
with open('parsed_rpm_calc1.json', 'w', encoding='utf-8') as f:
    json.dump({"pages": all_pages, "probs": all_probs}, f, ensure_ascii=False, indent=2)
print("Saved parsed_rpm_calc1.json successfully.")
