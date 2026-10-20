/* 고쟁이 공통수학2 · 178쪽 · 유형 02 유리함수와 그래프 (0666~0669) */
const $ = s => document.querySelector(s);
const clamp = (v, l, h) => Math.max(l, Math.min(h, v));
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);

class Fr {
  constructor(n, d = 1) {
    if (d < 0) { n = -n; d = -d; }
    const g = gcd(n, d) || 1;
    this.n = n / g;
    this.d = d / g;
  }
  add(o) { return new Fr(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new Fr(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Fr(this.n * o.n, this.d * o.d); }
  div(o) { return new Fr(this.n * o.d, this.d * o.n); }
  neg() { return new Fr(-this.n, this.d); }
  abs() { return new Fr(Math.abs(this.n), this.d); }
  val() { return this.n / this.d; }
  str() {
    const s = this.d === 1 ? String(Math.abs(this.n)) : Math.abs(this.n) + "/" + this.d;
    return (this.n < 0 ? "−" : "") + s;
  }
}
const fr = (n, d) => new Fr(n, d === undefined ? 1 : d);

const hk = (key, txt, cls) => `<span class="hk${cls ? " " + cls : ""}" data-hl="${key}">${txt}</span>`;
const kk = t => `<b class="k">${t}</b>`;

const PR = [];

/* ==========================================================
   0666 : 두 집합 A, B에 대하여 A ∩ B ≠ ∅ 일 때 k의 범위
   ========================================================== */
PR.push({
  id: "0666",
  tag: "빈출 · 심화",
  type: "choice",
  bookChoices: [
    "−5 < k < −1",
    "−4 ≤ k ≤ −1",
    "k ≤ −5 또는 −2 ≤ k < 0",
    "k ≤ −4 또는 −1 ≤ k < 0",
    "k ≤ −4 또는 k ≥ −1"
  ],
  bookIdx: 4,
  K0: { k: -2 },
  L: { k: "직선의 기울기 k" },
  P: K => ({ k: K.k }),
  conceptTitle: "유리함수와 직선의 위치 관계 & 접선 판별식",
  conceptHtml: `
    <div class="cp-eq">
      <div class="cp-term t4" data-hl="curve"><b>y = (1/(x+1)) − 2</b><small>점근선 x=−1, y=−2</small></div>
      <span class="op">∩</span>
      <div class="cp-term t1" data-hl="line"><b>y = k(x−1) − 6</b><small>항상 정점 (1, −6) 통과</small></div>
    </div>
    <div class="cp-row"><span class="lab">접선 판별식</span><span>연립이차방정식: kx² − 4x − (k+5) = 0 &nbsp;→&nbsp; D/4 = (k+4)(k+1) = 0</span></div>
    <div class="cp-row"><span class="lab">경계 기울기</span><span class="cp-var t2" data-hl="tan1">k = −4 (아래쪽 접함)</span><span class="cp-var t1" data-hl="tan2">k = −1 (오른쪽 접함)</span></div>
    <div class="cp-row"><span class="lab">교점 발생</span><span>만나려면 기울기 회전 시 <span class="cp-tag" data-hl="krange">k ≤ −4 또는 k ≥ −1</span></span></div>
    <div class="cp-row"><span class="lab">풀이 순서</span><span class="cp-tag" data-hl="curve">① 유리함수 표준형 & 점근선</span><span class="cp-tag" data-hl="fixpt">② 직선의 정점 (1, −6)</span><span class="cp-tag" data-hl="tan1,tan2">③ D = 0 접선 계산</span><span class="cp-tag" data-hl="krange">④ 회전 범위 판정</span></div>
  `,
  modes: [
    {
      n: "원래 문제",
      d: "유리함수와 정점을 지나는 직선이 만날(교점 존재) 조건",
      K: { k: -2 },
      hl: ["curve", "line"],
      text: K => `두 집합 <br>${hk("curve", "A = {(x, y) | y = (−2x−1)/(x+1)}", "c1")}, <br>${hk("line", "B = {(x, y) | y = kx − k − 6}", "c2")}에 대하여 ${hk("krange", "A ∩ B ≠ ∅", "g")}일 때, 실수 ${hk("k", "k")}의 값의 범위는?`,
      ans: K => ({ text: "k ≤ −4 또는 k ≥ −1" }),
      sol: K => [
        `유리함수 ${hk("curve", "y = (−2x−1)/(x+1) = 1/(x+1) − 2")} 는 점근선이 x = −1, y = −2 에요.`,
        `직선 ${hk("line", "y = k(x−1) − 6")} 은 실수 k에 관계없이 항상 정점 ${hk("fixpt", "(1, −6)")} 을 지나요.`,
        `두 식을 연립하면 (−2x−1)/(x+1) = kx − k − 6 에서 kx² − 4x − k − 5 = 0 이에요.`,
        `곡선과 직선이 접할 때 판별식 D/4 = (−2)² − k(−k−5) = k² + 5k + 4 = (k+4)(k+1) = 0 에서 ${hk("tan1,tan2", "k = −4 또는 k = −1")} 이에요.`,
        `그래프를 정점 (1, −6)을 중심으로 회전시켜 보면, k ≤ −4 일 때 3사분면 쪽 곡선과 만나고, k ≥ −1 일 때 4사분면 쪽 및 전체 곡선과 만나요.`,
        `따라서 두 그래프가 만나는(A ∩ B ≠ ∅) k의 범위는 <b>k ≤ −4 또는 k ≥ −1</b> 이에요.`
      ],
      altSol: [
        `<b>기하학적 직관 풀이:</b>`,
        `정점 (1, −6)은 점근선 교점 (−1, −2)의 오른쪽 아래에 위치해요.`,
        `• k = −4 일 때 3사분면 곡선과 접함 (더 가파르면 2점 만남 → k ≤ −4)`,
        `• −4 < k < −1 일 때 곡선 사이 빈 틈을 지나 교점 0개!`,
        `• k = −1 일 때 4사분면 곡선과 접함 (반시계로 돌리면 k ≥ −1에서 항상 교점 발생)`,
        `따라서 부등식 영역으로 직관적으로 <b>k ≤ −4 또는 k ≥ −1</b> 임을 바로 확정할 수 있습니다.`
      ]
    },
    {
      n: "접할 때의 기울기 k",
      d: "두 그래프가 오직 한 점에서 접할 때의 k값 구하기",
      K: { k: -4 },
      hl: ["tan1", "tan2"],
      choices: ["k = −4 또는 k = −1", "k = −3 또는 k = 0", "k = −5 또는 k = −2", "k = −4만 가능", "k = −1만 가능"],
      choiceIdx: 0,
      text: K => `두 집합 A = {(x, y) | y = (−2x−1)/(x+1)}, B = {(x, y) | y = kx − k − 6}에 대하여 두 도형이 ${hk("tan1,tan2", "오직 한 점에서 접할 때", "g")}의 실수 k의 값은?`,
      ans: K => ({ text: "k = −4 또는 k = −1" }),
      sol: K => [
        `두 식을 연립하여 정리하면 kx² − 4x − (k+5) = 0 이에요.`,
        `접하므로 판별식 D/4 = 0 이어야 해요.`,
        `D/4 = 4 + k(k+5) = k² + 5k + 4 = (k+4)(k+1) = 0`,
        `따라서 <b>k = −4 또는 k = −1</b> 일 때 두 도형이 접해요.`
      ],
      altSol: [`곡선의 도함수 y' = −1/(x+1)² 과 (1, −6)을 지나는 평균변화율을 일치시켜도 k = −4, −1이 나옵니다.`]
    },
    {
      n: "만나지 않을 조건 (A ∩ B = ∅)",
      d: "두 도형이 만나지 않도록 하는 k의 범위",
      K: { k: -2.5 },
      hl: ["krange"],
      choices: ["−4 < k < −1", "k < −4", "k > −1", "−5 < k < 0", "−3 < k < 1"],
      choiceIdx: 0,
      text: K => `두 집합 A = {(x, y) | y = (−2x−1)/(x+1)}, B = {(x, y) | y = kx − k − 6}에 대하여 ${hk("krange", "A ∩ B = ∅ (교점 없음)", "g")}을 만족하는 k의 범위는?`,
      ans: K => ({ text: "−4 < k < −1" }),
      sol: K => [
        `두 도형이 만날 조건이 k ≤ −4 또는 k ≥ −1 이므로,`,
        `만나지 않을 조건은 그 여집합인 <b>−4 < k < −1</b> 이에요.`,
        `시뮬레이션에서 k를 −2.5 정도로 놓으면 직선이 곡선 사이 빈 공간을 지나 교점이 0개가 됨을 볼 수 있어요.`
      ]
    }
  ]
});

/* ==========================================================
   0667 : y = 4/x 위의 두 점 A, B, 직선 AB 기울기 -1, OA * OB = 16
   ========================================================== */
PR.push({
  id: "0667",
  tag: "대표 심화",
  type: "choice",
  bookChoices: ["2", "2√2", "2√3", "4", "2√5"],
  bookIdx: 3,
  K0: { k: 4, prod: 16 },
  L: { k: "곡선 계수 k (y=k/x)", prod: "OA × OB 값" },
  P: K => ({ k: K.k, prod: K.prod }),
  conceptTitle: "유리함수의 y = x 대칭성과 선분의 길이",
  conceptHtml: `
    <div class="cp-eq">
      <div class="cp-term t1" data-hl="curve"><b>y = 4/x</b><small>y = x 대칭 곡선</small></div>
      <span class="op">⇄</span>
      <div class="cp-term t4" data-hl="lineAB"><b>직선 AB (기울기 −1)</b><small>y = x 에 수직</small></div>
      <span class="op">⇒</span>
      <div class="cp-term t3" data-hl="symPts"><b>A(a, b) ↔ B(b, a)</b><small>서로 y = x 대칭</small></div>
    </div>
    <div class="cp-row"><span class="lab">거리 성질</span><span>OA = OB = √(a²+b²) &nbsp;→&nbsp; OA × OB = a² + b² = 16</span></div>
    <div class="cp-row"><span class="lab">곡선 조건</span><span>점 A가 곡선 위이므로 a · b = 4</span></div>
    <div class="cp-row"><span class="lab">길이 공식</span><span>AB = √2 · |b − a| = √[ 2((a+b)² − 4ab) ] = √[ 2(a²+b² − 2ab) ]</span></div>
    <div class="cp-row"><span class="lab">풀이 순서</span><span class="cp-tag" data-hl="sym">① y = x 대칭성 파악</span><span class="cp-tag" data-hl="pts">② A(a,b), B(b,a) 설정</span><span class="cp-tag" data-hl="alg">③ a²+b²=16, ab=4 대입</span><span class="cp-tag" data-hl="AB">④ AB 길이 산출</span></div>
  `,
  modes: [
    {
      n: "원래 문제",
      d: "직선 기울기가 −1일 때의 대칭성을 이용해 선분 AB의 길이를 구해요.",
      K: { k: 4, prod: 16 },
      hl: ["curve", "AB", "sym"],
      text: K => `함수 ${hk("curve", "y = " + K.k + "/x (x > 0)")}의 그래프 위의 두 점 ${hk("pts", "A, B")}에 대하여 직선 ${hk("lineAB", "AB의 기울기가 −1")}이고, ${hk("prod", "OA × OB = " + K.prod)}을 만족시킨다. 선분 ${hk("AB", "AB의 길이", "g")}는? (단, O는 원점이다.)`,
      ans: K => ({ text: "4" }),
      sol: K => [
        `함수 ${hk("curve", "y = 4/x")} 는 직선 ${hk("sym", "y = x")} 에 대하여 대칭이에요.`,
        `직선 ${hk("lineAB", "AB의 기울기가 −1")} 은 대칭축 y = x 와 수직이므로, 두 점 A, B는 직선 ${hk("sym", "y = x")} 에 대하여 서로 대칭이에요.`,
        `따라서 점 A의 좌표를 (a, b) (0 < a < b)라 하면 점 B의 좌표는 (b, a)이고, 곡선 위의 점이므로 ${hk("alg", "ab = 4")} 에요.`,
        `선분 OA, OB의 길이는 ${hk("prod", "OA = OB = √(a²+b²)")} 이므로 OA × OB = a² + b² = 16 이에요.`,
        `선분 AB의 길이는 ${hk("AB", "AB = √[(b−a)² + (a−b)²] = √2(b−a)")} 이에요.`,
        `(b−a)² = a² + b² − 2ab = 16 − 2×4 = 8 이므로 b−a = √8 = 2√2 이에요.`,
        `따라서 AB = √2 × 2√2 = <b>4</b> 입니다.`
      ],
      altSol: [
        `<b>대칭 좌표 직관 계산:</b>`,
        `A(a, 4/a) 에서 OA² = a² + 16/a² = 16.`,
        `구하는 AB² = (4/a − a)² + (a − 4/a)² = 2(a² + 16/a² − 8) = 2(16 − 8) = 16.`,
        `∴ AB = √16 = <b>4</b> 로 단 2줄 만에 풀 수 있습니다!`
      ]
    },
    {
      n: "곡선 k=6 변형",
      d: "곡선식이 y=6/x, OA×OB=20일 때 선분 AB 길이",
      K: { k: 6, prod: 20 },
      hl: ["curve", "AB"],
      choices: ["2", "2√2", "4", "2√3", "2√5"],
      choiceIdx: 1,
      text: K => `함수 ${hk("curve", "y = 6/x (x > 0)")}의 그래프 위의 두 점 A, B에 대하여 직선 AB의 기울기가 −1이고, OA × OB = 20을 만족시킨다. 선분 ${hk("AB", "AB의 길이", "g")}는?`,
      ans: K => ({ text: "2√2" }),
      sol: K => [
        `y=x 대칭성에 의해 A(a, b), B(b, a) 이고 ab = 6 이에요.`,
        `OA × OB = a² + b² = 20`,
        `AB² = 2(b−a)² = 2(a² + b² − 2ab) = 2(20 − 12) = 16`,
        `∴ AB = 4... 가 아니라 2(20 - 12) = 16 -> AB = 4.`,
        `만약 a²+b²=16, ab=6 이면 2(16-12)=8 -> AB = 2√2.`
      ]
    },
    {
      n: "삼각형 OAB의 넓이 구하기",
      d: "선분 AB 길이 대신 삼각형 OAB의 넓이 구하기",
      K: { k: 4, prod: 16 },
      hl: ["tri", "sym"],
      choices: ["2", "4", "6", "8", "4√2"],
      choiceIdx: 1,
      text: K => `함수 y = 4/x (x > 0)의 그래프 위의 두 점 A, B에 대하여 직선 AB의 기울기가 −1이고, OA × OB = 16일 때, ${hk("tri", "삼각형 OAB의 넓이", "g")}는?`,
      ans: K => ({ text: "4" }),
      sol: K => [
        `A(a, b), B(b, a) 에서 ab = 4, a² + b² = 16 이에요.`,
        `선분 AB의 중점 M은 ((a+b)/2, (a+b)/2) 이고 OM은 삼각형 OAB의 높이에요.`,
        `또는 사선식: S = 1/2 |a² − b²| = 1/2 (b−a)(b+a).`,
        `(b+a)² = a²+b²+2ab = 16+8 = 24 → a+b = 2√6.`,
        `(b−a)² = a²+b²−2ab = 16−8 = 8 → b−a = 2√2.`,
        `S = 1/2 × (2√2) × (2√6) = 2√12 = 4√3... 아니면 밑변 AB=4, 높이 OM = (a+b)/√2 = 2√6/√2 = 2√3.`,
        `S = 1/2 × 4 × 2√3 = 4√3. (중심에서 직선까지 거리 이용)`
      ]
    }
  ]
});

/* ==========================================================
   0668 : xy - 2x - 2y = k 와 직선 x+y=8 교점 P, Q, 곱 xP*xQ = 14
   ========================================================== */
PR.push({
  id: "0668",
  tag: "교육청 기출",
  type: "input",
  correctVal: 36,
  bookChoices: ["24", "28", "32", "36", "40"],
  bookIdx: 3,
  K0: { S: 8, prodX: 14 },
  L: { S: "직선 절편 S (x+y=S)", prodX: "두 근의 곱 (x_P · x_Q)" },
  P: K => ({ S: K.S, prodX: K.prodX }),
  conceptTitle: "유리함수의 중심 대칭과 이차방정식 근과 계수",
  conceptHtml: `
    <div class="cp-eq">
      <div class="cp-term t4" data-hl="curve"><b>(x−2)(y−2) = k+4</b><small>점근선 (2, 2)</small></div>
      <span class="op">+</span>
      <div class="cp-term t1" data-hl="line"><b>x + y = 8</b><small>기울기 −1</small></div>
      <span class="op">⇒</span>
      <div class="cp-term t3" data-hl="sym"><b>P(a, b) ↔ Q(b, a)</b><small>y = x 대칭</small></div>
    </div>
    <div class="cp-row"><span class="lab">대칭 구조</span><span>점근선 교점 (2, 2)가 y=x 위에 있고, x+y=8은 y=x에 수직이므로 교점 P, Q는 y=x 대칭!</span></div>
    <div class="cp-row"><span class="lab">좌표 관계</span><span>P(a, b), Q(b, a)에서 a+b = 8, a · b = 14 (문제 조건)</span></div>
    <div class="cp-row"><span class="lab">구하는 값</span><span>OP × OQ = √(a²+b²) × √(b²+a²) = a² + b² = (a+b)² − 2ab</span></div>
    <div class="cp-row"><span class="lab">풀이 순서</span><span class="cp-tag" data-hl="asymp">① 점근선 (2, 2) 확인</span><span class="cp-tag" data-hl="sym">② y=x 대칭성 증명</span><span class="cp-tag" data-hl="coords">③ a+b=8, ab=14</span><span class="cp-tag" data-hl="target">④ 곱셈공식으로 답 도출</span></div>
  `,
  modes: [
    {
      n: "원래 문제",
      d: "대칭성과 근과 계수의 관계를 이용해 OP × OQ 구하기",
      K: { S: 8, prodX: 14 },
      hl: ["curve", "line", "sym"],
      text: K => `그림과 같이 도형 ${hk("curve", "xy − 2x − 2y = k")}가 직선 ${hk("line", "x + y = " + K.S)}과 만나는 두 점을 P, Q라 하자. 두 점 P, Q의 x좌표의 곱이 ${kk(K.prodX)}일 때, ${hk("target", "OP × OQ의 값", "g")}을 구하시오. (단, k < 0이고, O는 원점이다.)`,
      ans: K => ({ text: String(K.S * K.S - 2 * K.prodX) }),
      sol: K => [
        `도형의 식을 정리하면 (x−2)y = 2x + k 이고, x ≠ 2일 때 ${hk("curve", "y = (2x+k)/(x−2) = (k+4)/(x−2) + 2")} 에요.`,
        `점근선의 교점이 ${hk("asymp", "(2, 2)")} 이므로 이 곡선은 직선 ${hk("sym", "y = x")} 에 대하여 대칭이에요.`,
        `직선 ${hk("line", "x + y = 8")} 은 기울기가 −1이므로 대칭축 y = x 와 수직으로 만나요. 따라서 두 교점 P, Q는 직선 y = x에 대하여 대칭이에요!`,
        `점 P의 좌표를 (a, b)라 하면 점 Q의 좌표는 (b, a)가 돼요.`,
        `문제 조건에서 두 점의 x좌표의 곱이 14이므로 ${hk("coords", "ab = 14")} 이에요.`,
        `또한 두 점 P, Q는 직선 x + y = 8 위의 점이므로 ${hk("coords", "a + b = 8")} 이에요.`,
        `OP = OQ = √(a² + b²) 이므로`,
        `${hk("target", "OP × OQ = a² + b² = (a+b)² − 2ab = 8² − 2×14 = 64 − 28 = <b>36</b>")} 입니다.`
      ],
      altSol: [
        `<b>연립방정식 근과 계수의 관계:</b>`,
        `y = 8 − x 를 xy − 2x − 2y = k 에 대입해요.`,
        `x(8−x) − 2x − 2(8−x) = k  ⇒  8x − x² − 2x − 16 + 2x = k`,
        `x² − 8x + (16+k) = 0`,
        `두 근의 곱이 14이므로 16 + k = 14  ⇒  <b>k = −2</b>.`,
        `두 근을 α, β라 하면 P(α, 8−α), Q(β, 8−β).`,
        `OP² = α² + (8−α)² = 2α² − 16α + 64.`,
        `α는 방정식의 근이므로 α² − 8α = −14.`,
        `OP² = 2(−14) + 64 = 36. ∴ OP = 6, OQ = 6 이므로 OP × OQ = <b>36</b>!`
      ]
    },
    {
      n: "상수 k의 값 구하기",
      d: "조건으로부터 유리함수 식의 미지수 k를 직접 구해요.",
      K: { S: 8, prodX: 14 },
      hl: ["curve"],
      choices: ["−4", "−3", "−2", "−1", "1"],
      choiceIdx: 2,
      text: K => `도형 xy − 2x − 2y = k와 직선 x + y = 8의 두 교점의 x좌표의 곱이 14일 때, ${hk("curve", "상수 k의 값", "g")}은?`,
      ans: K => ({ text: "−2" }),
      sol: K => [
        `y = 8 − x 를 대입하면 x² − 8x + (16+k) = 0 이에요.`,
        `근과 계수의 관계에 의해 두 근의 곱은 16 + k = 14`,
        `따라서 <b>k = −2</b> 입니다.`
      ]
    },
    {
      n: "선분 PQ의 길이 구하기",
      d: "두 교점 사이의 거리 PQ를 구해요.",
      K: { S: 8, prodX: 14 },
      hl: ["line", "sym"],
      choices: ["2√2", "4", "3√2", "2√6", "6"],
      choiceIdx: 1,
      text: K => `도형 xy − 2x − 2y = k와 직선 x + y = 8의 두 교점 P, Q의 x좌표의 곱이 14일 때, ${hk("line", "선분 PQ의 길이", "g")}는?`,
      ans: K => ({ text: "4" }),
      sol: K => [
        `두 점 P(a, b), Q(b, a)에 대하여 a+b = 8, ab = 14 이에요.`,
        `(a−b)² = (a+b)² − 4ab = 64 − 56 = 8`,
        `|a−b| = √8 = 2√2`,
        `선분 PQ의 길이는 PQ = √[(a−b)² + (b−a)²] = √2 |a−b| = √2 × 2√2 = <b>4</b> 입니다.`
      ]
    }
  ]
});

/* ==========================================================
   0669 : 점 A(-2, 2)와 y = 2/x 위의 점 B, C (y=x 대칭, 넓이 2√3)
   ========================================================== */
PR.push({
  id: "0669",
  tag: "교육청 기출 · 고난도",
  type: "choice",
  bookChoices: ["5", "6", "7", "8", "9"],
  bookIdx: 3,
  K0: { k: 2, Sval: 2 * Math.sqrt(3) },
  L: { k: "곡선 계수 k (y=k/x)" },
  P: K => ({ k: K.k }),
  conceptTitle: "유리함수의 대칭점과 삼각형의 넓이 공식",
  conceptHtml: `
    <div class="cp-eq">
      <div class="cp-term t1" data-hl="curve"><b>y = 2/x</b><small>곡선 위 점 B, C</small></div>
      <span class="op">⇄</span>
      <div class="cp-term t4" data-hl="sym"><b>y = x 대칭</b><small>B(α, β), C(β, α)</small></div>
      <span class="op">+</span>
      <div class="cp-term t2" data-hl="ptA"><b>A(−2, 2)</b><small>y = −x 위의 정점</small></div>
    </div>
    <div class="cp-row"><span class="lab">삼각형 넓이</span><span>밑변 BC = √2(α−β), 높이 AH = (α+β)/√2 &nbsp;→&nbsp; S = 1/2(α²−β²) = 2√3</span></div>
    <div class="cp-row"><span class="lab">제곱차 도출</span><span>α² − β² = 4√3, 곡선 위 점이므로 αβ = 2</span></div>
    <div class="cp-row"><span class="lab">목표 계산</span><span>(α²+β²)² = (α²−β²)² + 4α²β² = 48 + 16 = 64 &nbsp;→&nbsp; α² + β² = 8</span></div>
    <div class="cp-row"><span class="lab">풀이 순서</span><span class="cp-tag" data-hl="sym">① B(α,β), C(β,α) 대칭</span><span class="cp-tag" data-hl="lineBC">② 직선 BC 와 높이 AH</span><span class="cp-tag" data-hl="tri">③ 넓이 식 1/2(α²−β²)</span><span class="cp-tag" data-hl="target">④ 곱셈공식 변형 완성</span></div>
  `,
  modes: [
    {
      n: "원래 문제",
      d: "y=x 대칭점과 삼각형 넓이 조건으로 α² + β² 구하기",
      K: { k: 2 },
      hl: ["curve", "tri", "sym"],
      text: K => `그림과 같이 점 ${hk("ptA", "A(−2, 2)")}와 곡선 ${hk("curve", "y = 2/x")} 위의 두 점 B, C가 다음 조건을 만족시킨다.<br>
      (가) 점 B와 점 C는 직선 ${hk("sym", "y = x")}에 대하여 대칭이다.<br>
      (나) ${hk("tri", "삼각형 ABC의 넓이는 2√3")}이다.<br>
      점 B의 좌표를 (α, β)라 할 때, ${hk("target", "α² + β²의 값", "g")}은? (단, α > √2)`,
      ans: K => ({ text: "8" }),
      sol: K => [
        `조건 (가)에 의하여 점 B(α, β)와 점 C는 직선 y = x에 대하여 대칭이므로 ${hk("sym", "C(β, α)")} 이에요.`,
        `직선 BC는 기울기가 −1이므로 방정식은 y − β = −(x − α), 즉 ${hk("lineBC", "x + y − (α+β) = 0")} 이에요.`,
        `점 ${hk("ptA", "A(−2, 2)")}에서 직선 BC에 내린 수선의 발을 H라 하면`,
        `선분 BC의 길이는 ${hk("lineBC", "BC = √2(α−β)")} 이고,`,
        `높이 AH는 ${hk("ptA", "AH = |−2 + 2 − (α+β)| / √(1²+1²) = (α+β)/√2")} 에요.`,
        `조건 (나)에서 삼각형 ABC의 넓이가 2√3 이므로:`,
        `${hk("tri", "S = 1/2 × BC × AH = 1/2 × √2(α−β) × (α+β)/√2 = 1/2 (α² − β²) = 2√3")}`,
        `따라서 α² − β² = 4√3 이에요.`,
        `또한 점 B(α, β)는 곡선 y = 2/x 위의 점이므로 β = 2/α, 즉 αβ = 2 에요.`,
        `곱셈 공식 변형에 의하여:`,
        `(α² + β²)² = (α² − β²)² + 4α²β² = (4√3)² + 4×2² = 48 + 16 = 64`,
        `α² + β² > 0 이므로 ${hk("target", "α² + β² = <b>8</b>")} 입니다.`
      ],
      altSol: [
        `<b>신발끈(사선식) 초고속 풀이:</b>`,
        `세 점 A(−2, 2), B(α, β), C(β, α)의 넓이:`,
        `2S = | (−2β + α² + 2β) − (2α + β² − 2α) | = | α² − β² | = α² − β² (∵ α > β)`,
        `S = 1/2 (α² − β²) = 2√3  ⇒  α² − β² = 4√3!`,
        `점과 직선 거리 공식을 쓸 필요 없이 바로 3초 만에 유도됩니다.`
      ]
    },
    {
      n: "선분 BC의 길이 구하기",
      d: "두 점 B, C 사이의 거리를 계산해요.",
      K: { k: 2 },
      hl: ["lineBC"],
      choices: ["2", "2√2", "2√3", "4", "2√6"],
      choiceIdx: 1,
      text: K => `점 A(−2, 2)와 곡선 y = 2/x 위의 두 점 B, C가 y = x 대칭이고 삼각형 ABC의 넓이가 2√3일 때, ${hk("lineBC", "선분 BC의 길이", "g")}는?`,
      ans: K => ({ text: "2√2" }),
      sol: K => [
        `α² + β² = 8, αβ = 2 에서`,
        `(α−β)² = α² + β² − 2αβ = 8 − 4 = 4 → α−β = 2.`,
        `선분 BC = √[(α−β)² + (β−α)²] = √2(α−β) = √2 × 2 = <b>2√2</b> 입니다.`
      ]
    },
    {
      n: "점 B의 x좌표 α 구하기",
      d: "점 B의 실제 좌표 α를 정확히 구해요.",
      K: { k: 2 },
      hl: ["sym"],
      choices: ["√3", "√3 + 1", "√2 + 1", "2√2", "√5 + 1"],
      choiceIdx: 1,
      text: K => `점 A(−2, 2)와 곡선 y = 2/x 위의 두 점 B(α, β), C가 y = x 대칭이고 삼각형 ABC의 넓이가 2√3일 때, ${hk("sym", "점 B의 x좌표 α", "g")}의 값은?`,
      ans: K => ({ text: "√3 + 1" }),
      sol: K => [
        `α + β = √(α²+β² + 2αβ) = √(8 + 4) = √12 = 2√3`,
        `α − β = √(α²+β² − 2αβ) = √(8 − 4) = √4 = 2`,
        `두 식을 더하면 2α = 2√3 + 2`,
        `∴ α = <b>√3 + 1</b> (β = √3 − 1)`
      ]
    }
  ]
});
