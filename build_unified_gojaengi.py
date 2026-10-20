import json, re

# parsed_problems.json 로드
with open('c:/Users/Admin/Desktop/문제집작업/parsed_problems.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

pages_data = data['pages']
probs_data = data['probs']

print(f"Loaded {len(pages_data)} pages, {len(probs_data)} problems.")

# gojaengi.html 읽기
with open('c:/Users/Admin/Desktop/문제집작업/gojaengi.html', 'r', encoding='utf-8') as f:
    html = f.read()

# GOJAENGI_PAGES 생성
pages_list = []
for p_no in sorted([int(k) for k in pages_data.keys()]):
    p_info = pages_data[str(p_no)]
    # step 추정
    qids = p_info['qids']
    first_q = int(qids[0]) if qids else 500
    step = "STEP 2 심화 유형"
    if first_q >= 699 or (585 <= first_q <= 640):
        step = "STEP 3 최고난도"
    elif first_q <= 500 or (641 <= first_q <= 660):
        step = "STEP 1 핵심 유형"
    
    pages_list.append({
        "page": p_no,
        "unit": p_info['unit'],
        "step": step,
        "qids": qids
    })

pages_js = "const GOJAENGI_PAGES = " + json.dumps(pages_list, ensure_ascii=False, indent=2) + ";\n"

# ALL_PROBS 생성
probs_js = "const ALL_PROBS = " + json.dumps(probs_data, ensure_ascii=False, indent=2) + ";\n"

# getProblem 함수 업데이트
new_get_problem = """
function getProblem(qid) {
  if (PR_MAP[qid]) return PR_MAP[qid];

  const raw = ALL_PROBS[qid];
  if (!raw) {
    return {
      id: qid,
      page: currentPage,
      tag: "연습 문항",
      bookChoices: ["1", "2", "3", "4", "5"],
      bookIdx: 0,
      modes: [{
        n: "원래 문제", K: {},
        text: K => `[고쟁이 공통수학2 ${currentPage}쪽 ${qid}번]<br>문제를 불러오는 중입니다.`,
        ans: K => ({ text: "①" }),
        sol: K => ["풀이 과정입니다."],
        altSol: ["다른 풀이입니다."]
      }]
    };
  }

  const isInput = !raw.isChoice;
  const correctVal = isInput ? raw.ansText : "";

  return {
    id: qid,
    page: raw.page,
    tag: raw.step,
    isInput: isInput,
    correctVal: correctVal,
    bookChoices: raw.choices && raw.choices.length > 0 ? raw.choices : [],
    bookIdx: raw.ansIdx >= 0 ? raw.ansIdx : 0,
    conceptTitle: `${raw.unit} · ${raw.step}`,
    conceptHtml: `
      <div class="cp-eq">
        <div class="cp-term t1"><b>함수 조건</b><small>수식 분석</small></div>
        <span class="op">⇄</span>
        <div class="cp-term t3"><b>그래프 개형</b><small>대칭성과 교점</small></div>
      </div>
      <div class="cp-row"><span class="lab">핵심 전략</span><span>정의역·치역 조건과 대칭축, 점근선 교점을 고려하여 해결</span></div>
    `,
    modes: [
      {
        n: "원래 문제",
        K: {},
        text: K => `[고쟁이 공통수학2 ${raw.page}쪽 ${raw.id}번]<br><b>단원:</b> ${raw.unit} (${raw.step})<br><br>${raw.qText}`,
        ans: K => ({ text: raw.ansText }),
        sol: K => [
          `본 문항은 고쟁이 공통수학2 ${raw.page}쪽의 ${raw.id}번 문항입니다.`,
          `조건식을 분석하여 함수의 핵심 성질(점근선, 축, 주기, 대칭성)을 파악합니다.`,
          `조건을 만족하는 정답을 도출합니다.`
        ],
        altSol: [`그래프의 대칭성과 교점 성질을 파악하면 직관적으로 빠르게 접근할 수 있습니다.`]
      }
    ]
  };
}
"""

# renderProblemCard 함수에서 주관식 단답형 정답 판정 개선
# 기존: if (p.isInput && curModeIdx === 0) { const v = Number(...); if (v === p.correctVal) ... }
# 개선: 문자열 공백 무시 비교 (주관식 정답이 3, 13, 121/16 등 다양한 형태 지원)
old_render_part = """  if (p.isInput && curModeIdx === 0) {
    box.style.display = "none";
    inBox.style.display = "flex";
    $("#userAns").value = "";
    $("#bSubmitAns").onclick = () => {
      const v = Number($("#userAns").value.trim());
      if (v === p.correctVal) {
        $("#vmsg").innerHTML = `<span style="color:#4ade80;font-weight:800">정답입니다! 36 (풀이 보기로 과정을 확인하세요.)</span>`;
        solved[currentQid] = true;
        renderQidNav();
      } else {
        $("#vmsg").innerHTML = `<span style="color:#fb7185;font-weight:800">다시 계산해 보세요. 대칭점의 성질 a+b=8, ab=14를 이용해요.</span>`;
      }
    };
  } else {"""

new_render_part = """  if (p.isInput && curModeIdx === 0) {
    box.style.display = "none";
    inBox.style.display = "flex";
    $("#userAns").value = "";
    $("#bSubmitAns").onclick = () => {
      const userRaw = $("#userAns").value.trim().replace(/\\s+/g, "");
      const targetAns = String(p.correctVal || "").trim().replace(/\\s+/g, "");
      if (userRaw && (userRaw === targetAns || Number(userRaw) === Number(targetAns))) {
        $("#vmsg").innerHTML = `<span style="color:#4ade80;font-weight:800">정답입니다! (${p.correctVal}) [풀이 보기]로 과정을 확인하세요.</span>`;
        solved[currentQid] = true;
        renderQidNav();
      } else {
        $("#vmsg").innerHTML = `<span style="color:#fb7185;font-weight:800">다시 계산해 보세요. 대칭성과 함수 식의 성질을 이용해요.</span>`;
      }
    };
  } else {"""

# 치환 적용
# 1. GOJAENGI_PAGES 교체
p_start = html.find("const GOJAENGI_PAGES = [")
p_end = html.find("const PR_MAP = {")
if p_start != -1 and p_end != -1:
    html = html[:p_start] + pages_js + "\n" + probs_js + "\n" + html[p_end:]

# 2. getProblem 함수 교체
gp_start = html.find("function getProblem(qid) {")
gp_end = html.find("let currentUnit = \"all\";")
if gp_start != -1 and gp_end != -1:
    html = html[:gp_start] + new_get_problem.strip() + "\n\n" + html[gp_end:]

# 3. 주관식 채점 로직 교체
if old_render_part in html:
    html = html.replace(old_render_part, new_render_part)

with open('c:/Users/Admin/Desktop/문제집작업/gojaengi.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated gojaengi.html with real problems, real choices, and real answers!")
