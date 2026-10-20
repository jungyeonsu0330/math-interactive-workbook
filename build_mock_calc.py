import json, os

# 261020 수능&모의 미적분 15문항 정보
# Answers from verified answer marks:
# Q01: ③ (idx 2) - 로그함수의 극한(1) : lim{x->0} ln(1+x)/x 꼴의 극한
# Q02: ② (idx 1) - 매개변수로 나타낸 함수의 미분법
# Q03: ④ (idx 3) - 치환적분을 이용한 정적분(2) : 유리함수
# Q04: ③ (idx 2) - 입체도형의 부피; 단면이 밑면과 수직인 경우(1)
# Q05: ① (idx 0) - 접선의 방정식(4) : 곡선 밖의 점이 주어진 경우
# Q06: ③ (idx 2) - 정적분과 급수의 관계
# Q07: ⑤ (idx 4) - 등비수열의 극한을 이용한 미정계수의 결정
# Q08: ④ (idx 3) - 입체도형의 부피; 단면이 밑면과 수직인 경우(1)
# Q09: ⑤ (idx 4) - 수열의 극한에 대한 기본 성질
# Q10: ④ (idx 3) - 합성함수의 미분법(5) : 지수함수
# Q11: ② (idx 1) - 합이 주어진 등비급수
# Q12: ③ (idx 2) - 정적분과 급수의 관계
# Q13: ④ (idx 3) - 정적분과 급수의 관계
# Q14: ① (idx 0) - 좌표평면 위에서 움직인 거리
# Q15: ② (idx 1) - 좌표평면 위에서 움직인 거리

CIRCLES = ['①', '②', '③', '④', '⑤']

meta_list = [
    {
        "id": "0001", "page": 1, "unit": "02 미분법",
        "sub": "로그함수의 극한(1) : lim{x->0} ln(1+x)/x 꼴의 극한",
        "ansIdx": 2, "ansText": "③",
        "conceptTitle": "로그함수의 극한 기본 공식",
        "conceptSub": "자연로그 밑 e의 정의와 치환 극한",
        "strategy": "lim_{x->0} ln(1+kx)/x = k 공식을 적용하여 분자·분모의 계수비를 즉시 비교합니다.",
        "tip": "x -> 0일 때 ln(1+ax) ~ ax의 무한소 근사를 사용하면 3초 만에 답을 도출할 수 있습니다."
    },
    {
        "id": "0002", "page": 1, "unit": "02 미분법",
        "sub": "매개변수로 나타낸 함수의 미분법",
        "ansIdx": 1, "ansText": "②",
        "conceptTitle": "매개변수 미분법",
        "conceptSub": "dy/dx = (dy/dt) / (dx/dt)",
        "strategy": "x와 y를 각각 매개변수 t에 대해 미분한 후, dy/dt를 dx/dt로 나누어 접선의 기울기를 구합니다.",
        "tip": "t의 값이 주어지면 각각의 도함수 값 dy/dt, dx/dt를 먼저 계산한 후 비율을 구하는 것이 실수를 방지합니다."
    },
    {
        "id": "0003", "page": 1, "unit": "03 적분법",
        "sub": "치환적분을 이용한 정적분(2) : 유리함수",
        "ansIdx": 3, "ansText": "④",
        "conceptTitle": "치환적분법",
        "conceptSub": "f'(x)/f(x) 형태의 적분 및 분수식 치환",
        "strategy": "분모의 미분이 분자에 곱해진 형태를 찾아 t로 치환하고 적분 구간을 새 변수 t의 범위로 반드시 변경합니다.",
        "tip": "인테그럴 f'(x)/f(x) dx = ln|f(x)| + C 공식을 기억하면 치환 과정 없이 암산으로 바로 풀립니다."
    },
    {
        "id": "0004", "page": 1, "unit": "03 적분법",
        "sub": "입체도형의 부피; 단면이 밑면과 수직인 경우(1)",
        "ansIdx": 2, "ansText": "③",
        "conceptTitle": "입체도형의 부피와 정적분",
        "conceptSub": "단면적 S(x)의 정적분 V = int S(x) dx",
        "strategy": "x축에 수직인 평면으로 자른 단면의 한 변의 길이를 함수식으로 나타내고, 단면의 넓이 S(x)를 구한 뒤 구간 적분합니다.",
        "tip": "단면이 정사각형이면 S(x)=[y(x)]^2, 정삼각형이면 S(x)=sqrt(3)/4 * [y(x)]^2을 적용합니다."
    },
    {
        "id": "0005", "page": 1, "unit": "02 미분법",
        "sub": "접선의 방정식(4) : 곡선 밖의 점이 주어진 경우",
        "ansIdx": 0, "ansText": "①",
        "conceptTitle": "곡선 밖의 점에서 그은 접선",
        "conceptSub": "접점의 좌표 (t, f(t)) 설정 및 방정식 수립",
        "strategy": "접점을 (t, f(t))로 두고 접선의 방정식 y - f(t) = f'(t)(x - t)을 세운 후 곡선 밖의 점의 좌표를 대입하여 t를 구합니다.",
        "tip": "외부 점과 접점 사이의 평균변화율 (f(t)-y1)/(t-x1) = f'(t) 형태로 식을 세우면 식 전개가 훨씬 깔끔해집니다."
    },
    {
        "id": "0006", "page": 2, "unit": "03 적분법",
        "sub": "정적분과 급수의 관계",
        "ansIdx": 2, "ansText": "③",
        "conceptTitle": "구분구적법과 정적분 변환",
        "conceptSub": "lim sum f(a + k*p/n) * p/n = int_a^{a+p} f(x) dx",
        "strategy": "k/n을 x로 치환하고, 1/n을 dx로 대응시켜 정적분 식으로 변환한 후 미적분학의 기본정리로 계산합니다.",
        "tip": "식 안에 있는 a + b*k/n 전체를 x로 두면 적분 구간은 [a, a+b], dx = (b/n)이 되어 피적분함수가 간단해집니다."
    },
    {
        "id": "0007", "page": 2, "unit": "01 수열의 극한과 급수",
        "sub": "등비수열의 극한을 이용한 미정계수의 결정",
        "ansIdx": 4, "ansText": "⑤",
        "conceptTitle": "등비수열의 극한 r^n",
        "conceptSub": "|r| > 1, |r| < 1, r = 1, r = -1 구간 분류",
        "strategy": "공비의 크기에 따라 최고차항(절댓값이 가장 큰 밑)으로 분모·분자를 나누어 극한값을 계산합니다.",
        "tip": "밑의 절댓값이 가장 큰 항만 남기고 나머지는 0으로 수렴하므로 지배적 항만 취해 최고차 계수비를 구합니다."
    },
    {
        "id": "0008", "page": 2, "unit": "03 적분법",
        "sub": "입체도형의 부피; 단면이 밑면과 수직인 경우(1)",
        "ansIdx": 3, "ansText": "④",
        "conceptTitle": "입체도형 부피의 정적분",
        "conceptSub": "단면적 함수 S(x)의 정적분",
        "strategy": "단면의 기하학적 형태에 맞춘 넓이 식 S(x)를 작성하고 주어진 적분 구간 [a, b]에서 치환 또는 부분적분을 적용합니다.",
        "tip": "단면의 한 변이 곡선 y=f(x)와 밑면 경계선 사이의 거리이므로 선분의 길이식을 명확히 세우는 것이 출발점입니다."
    },
    {
        "id": "0009", "page": 2, "unit": "01 수열의 극한과 급수",
        "sub": "수열의 극한에 대한 기본 성질",
        "ansIdx": 4, "ansText": "⑤",
        "conceptTitle": "수열의 극한의 기본 성질 및 대소 관계",
        "conceptSub": "수렴하는 수열의 사칙연산과 샌드위치 정리",
        "strategy": "수렴하는 수열의 성질을 이용하여 구하고자 하는 수열을 수렴성이 보장된 수열들의 선형 결합 형태로 변형합니다.",
        "tip": "수렴한다는 전제조건이 있을 때만 lim(an * bn) = lim(an) * lim(bn)이 성립함을 항상 유의하세요."
    },
    {
        "id": "0010", "page": 2, "unit": "02 미분법",
        "sub": "합성함수의 미분법(5) : 지수함수",
        "ansIdx": 3, "ansText": "④",
        "conceptTitle": "합성함수 미분법",
        "conceptSub": "d/dx [e^{g(x)}] = g'(x) e^{g(x)}",
        "strategy": "지수함수와 다항·삼각함수의 합성 형태에서 연쇄법칙(Chain Rule)을 적용하여 도함수를 구합니다.",
        "tip": "지수함수 e^u는 미분해도 자기 자신 e^u가 그대로 남고 속미분 u'만 곱해진다는 점을 활용해 빠르게 전개합니다."
    },
    {
        "id": "0011", "page": 2, "unit": "01 수열의 극한과 급수",
        "sub": "합이 주어진 등비급수",
        "ansIdx": 1, "ansText": "②",
        "conceptTitle": "무한등비급수의 수렴과 합",
        "conceptSub": "S = a / (1 - r) (|r| < 1)",
        "strategy": "초항 a와 공비 r (|r| < 1)의 관계식을 세워 연립방정식을 풀고 무한급수의 합 공식에 대입합니다.",
        "tip": "등비급수 문제에서 짝수 번째 항들의 합, 홀수 번째 항들의 합은 공비가 r^2이 된다는 점을 이용하면 즉시 해결됩니다."
    },
    {
        "id": "0012", "page": 3, "unit": "03 적분법",
        "sub": "정적분과 급수의 관계",
        "ansIdx": 2, "ansText": "③",
        "conceptTitle": "정적분과 급수의 응용",
        "conceptSub": "k/n 항의 치환과 적분 구간 결정",
        "strategy": "급수의 일반항에서 1/n과 k/n을 분리해 낸 뒤 정적분 인테그럴 형태로 치환 변환합니다.",
        "tip": "구간 [0, 1]로 변환할 때는 k/n -> x, 1/n -> dx로 표준화하면 실수 없이 안전하게 풀립니다."
    },
    {
        "id": "0013", "page": 3, "unit": "03 적분법",
        "sub": "정적분과 급수의 관계",
        "ansIdx": 3, "ansText": "④",
        "conceptTitle": "다항함수와 급수의 정적분 결합",
        "conceptSub": "직사각형 넓이의 합의 극한",
        "strategy": "주어진 급수 식을 정적분으로 전환한 후 부정적분을 구하고 위끝·아래끝을 대입하여 값을 산출합니다.",
        "tip": "식 변형 시 공통인수 1/n을 급수 밖으로 빼내어 dx 자리로 배치하는 것이 핵심입니다."
    },
    {
        "id": "0014", "page": 3, "unit": "03 적분법",
        "sub": "좌표평면 위에서 움직인 거리",
        "ansIdx": 0, "ansText": "①",
        "conceptTitle": "평면 운동에서 점이 움직인 거리",
        "conceptSub": "s = int_a^b sqrt{(dx/dt)^2 + (dy/dt)^2} dt",
        "strategy": "속도 벡터 (dx/dt, dy/dt)를 구하고 속력 sqrt{(dx/dt)^2 + (dy/dt)^2}을 정리한 뒤 시간 t의 구간에서 정적분합니다.",
        "tip": "루트 안의 식 (dx/dt)^2 + (dy/dt)^2은 항상 완전제곱식 형태로 인수분해되어 루트가 깔끔하게 벗겨집니다."
    },
    {
        "id": "0015", "page": 3, "unit": "03 적분법",
        "sub": "좌표평면 위에서 움직인 거리",
        "ansIdx": 1, "ansText": "②",
        "conceptTitle": "곡선의 길이 및 이동 거리 킬러",
        "conceptSub": "속력 함수의 정적분과 적분 테크닉",
        "strategy": "t에 따른 좌표 x(t), y(t)의 도함수를 각각 구하고 피타고라스 정리에 따른 속력 함수를 세워 t=a부터 t=b까지 적분합니다.",
        "tip": "지수함수나 분수식이 포함된 경우 e^{2t} + 2 + e^{-2t} = (e^t + e^{-t})^2 처럼 가운데 상수항 부호 반전 패턴을 확인하세요."
    }
]

probs = {}
pages = {}

for m in meta_list:
    qid = m["id"]
    p_no = m["page"]
    q_img = f"mock_calc_img/q_{qid[-2:]}.png"
    sol_img = f"mock_calc_img/sol_{qid[-2:]}.png"
    
    q_html = f'<div style="margin-bottom:8px;font-weight:700;color:var(--yel);font-size:0.95rem;">[{m["sub"]}]</div>'
    q_html += f'<div style="text-align:center;margin:10px 0;"><img src="{q_img}" style="max-width:100%;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,0.4)" alt="문항 {qid}"></div>'
    
    sol_html = f'<div style="font-weight:800;color:var(--c3);font-size:1.05rem;margin-bottom:10px;">■ 정답: {m["ansText"]}</div>'
    sol_html += f'<div style="text-align:center;margin:10px 0;"><img src="{sol_img}" style="max-width:100%;border-radius:10px" alt="해설 {qid}"></div>'
    
    probs[qid] = {
        "id": qid,
        "page": p_no,
        "unit": m["unit"],
        "step": "수능·모의고사 실전 기출",
        "qText": q_html,
        "isChoice": True,
        "choices": CIRCLES,
        "ansIdx": m["ansIdx"],
        "ansText": m["ansText"],
        "solText": sol_html,
        "conceptTitle": m["conceptTitle"],
        "conceptSub": m["conceptSub"],
        "strategy": m["strategy"],
        "tip": m["tip"]
    }
    
    if p_no not in pages:
        pages[p_no] = {
            "page": p_no,
            "unit": m["unit"],
            "qids": []
        }
    pages[p_no]["qids"].append(qid)

out_data = {
    "pages": pages,
    "probs": probs
}

with open("parsed_mock_calc.json", "w", encoding="utf-8") as f:
    json.dump(out_data, f, ensure_ascii=False, indent=2)

print(f"Generated parsed_mock_calc.json: {len(pages)} pages, {len(probs)} problems.")
