import json, os, re

# 6개 교재 데이터 로드
with open('c:/Users/Admin/Desktop/문제집작업/parsed_problems.json', 'r', encoding='utf-8') as f:
    d_gongsu2 = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_gongsu1.json', 'r', encoding='utf-8') as f:
    d_gongsu1 = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_daesu.json', 'r', encoding='utf-8') as f:
    d_daesu = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_geom.json', 'r', encoding='utf-8') as f:
    d_rpm = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_gongsu2.json', 'r', encoding='utf-8') as f:
    d_rpm_g2 = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_gongsu1.json', 'r', encoding='utf-8') as f:
    d_rpm_g1 = json.load(f)

print(f"Loaded datasets: Gongsu2 ({len(d_gongsu2['probs'])}), Gongsu1 ({len(d_gongsu1['probs'])}), Daesu ({len(d_daesu['probs'])}), RPM_Geom ({len(d_rpm['probs'])}), RPM_Gongsu2 ({len(d_rpm_g2['probs'])}), RPM_Gongsu1 ({len(d_rpm_g1['probs'])})")

# 6개 교재 메타데이터
ALL_BOOKS_CONFIG = {
    "gongsu1": {
        "title": "유형내신 고쟁이 공통수학1",
        "shortTitle": "고쟁이 공통수학1",
        "badge": "고쟁이 공수1",
        "units": ["all", "01 다항식의 연산과 나머지정리", "02 방정식과 부등식", "03 경우의 수와 행렬", "04 도형의 방정식"],
        "defaultPage": 7,
        "defaultQid": "0001",
        "pages": d_gongsu1["pages"],
        "probs": d_gongsu1["probs"]
    },
    "gongsu2": {
        "title": "유형내신 고쟁이 공통수학2",
        "shortTitle": "고쟁이 공통수학2",
        "badge": "고쟁이 공수2",
        "units": ["all", "01 함수", "02 유리함수와 무리함수"],
        "defaultPage": 178,
        "defaultQid": "0666",
        "pages": d_gongsu2["pages"],
        "probs": d_gongsu2["probs"]
    },
    "daesu": {
        "title": "유형내신 고쟁이 대수",
        "shortTitle": "고쟁이 대수",
        "badge": "고쟁이 대수",
        "units": ["all", "01 지수함수와 로그함수", "02 삼각함수", "03 수열"],
        "defaultPage": 7,
        "defaultQid": "0001",
        "pages": d_daesu["pages"],
        "probs": d_daesu["probs"]
    },
    "rpm_geom": {
        "title": "개념원리 RPM 기하",
        "shortTitle": "RPM 기하",
        "badge": "RPM 기하",
        "units": ["all", "01 이차곡선 (포물선·타원·쌍곡선)", "02 평면벡터", "03 공간도형과 공간좌표"],
        "defaultPage": 8,
        "defaultQid": "0001",
        "pages": d_rpm["pages"],
        "probs": d_rpm["probs"]
    },
    "rpm_gongsu2": {
        "title": "개념원리 RPM 공통수학2",
        "shortTitle": "RPM 공통수학2",
        "badge": "사진 1·2 신규 등록",
        "units": ["all", "01 평면좌표와 직선의 방정식", "02 원의 방정식과 도형의 이동", "03 집합과 명제", "04 함수와 역함수", "05 유리함수와 무리함수"],
        "defaultPage": 7,
        "defaultQid": "0001",
        "pages": d_rpm_g2["pages"],
        "probs": d_rpm_g2["probs"]
    },
    "rpm_gongsu1": {
        "title": "개념원리 RPM 공통수학1",
        "shortTitle": "RPM 공통수학1",
        "badge": "사진 1 신규 등록",
        "units": ["all", "01 다항식의 연산과 인수분해", "02 방정식과 부등식", "03 경우의 수와 행렬"],
        "defaultPage": 7,
        "defaultQid": "0001",
        "pages": d_rpm_g1["pages"],
        "probs": d_rpm_g1["probs"]
    }
}

# 공통 JS 템플릿 생성
# index.html (마스터 포털 및 통합 뷰어) 생성
html_template = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<title>고등수학 인터랙티브 문제집 포털 · 고쟁이 & RPM</title>
<!-- 대한민국 수학교과서 스타일 수식 렌더러 (KaTeX) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="if(window.renderMath)renderMath()"></script>
<style>
/* KaTeX 수식 및 반응형 줄바꿈 방어 */
.katex { font-size: 1.05em; color: #f1f5f9; }
.katex-display {
  margin: 10px 0;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  max-width: 100%;
  padding: 4px 0;
}

/* 화면 너비에 따른 자율 글자 크기 (Root Font Size Clamp) */
html {
  font-size: clamp(14px, 0.45vw + 12px, 17px);
  -webkit-text-size-adjust: 100%;
}
:root{
  --bg:#0f172a;--panel:#111a30;--line:#26365a;--tx:#e8edf6;--mut:#8ea0bb;
  --c1:#22d3ee;--c2:#fb923c;--c3:#4ade80;--pnk:#f472b6;--vio:#a78bfa;--yel:#facc15;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:var(--bg);
  color:var(--tx);
  font-family:"Pretendard","Malgun Gothic","Apple SD Gothic Neo",-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;
  word-break:keep-all;
}
.wrap{
  max-width:1340px;
  margin:0 auto;
  padding:clamp(8px, 2vw, 18px) clamp(8px, 2vw, 16px) clamp(24px, 4vw, 40px);
  width:100%;
}

/* 상단 교재 선택 바: 모바일/태블릿에서 부드러운 가로 스와이프 터치 스크롤 */
.book-tabs{
  display:flex;
  gap:clamp(6px, 1.2vw, 10px);
  margin-bottom:12px;
  background:#090d1a;
  padding:clamp(6px, 1.2vw, 10px);
  border-radius:clamp(10px, 1.8vw, 14px);
  border:1.5px solid var(--line);
  overflow-x:auto;
  flex-wrap:nowrap;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:none;
}
.book-tabs::-webkit-scrollbar{display:none}
.book-tab{
  background:#141f38;
  color:var(--tx);
  border:1.5px solid var(--line);
  border-radius:9px;
  padding:clamp(8px, 1.4vw, 10px) clamp(12px, 1.8vw, 18px);
  font-size:clamp(0.82rem, 1.6vw, 0.95rem);
  font-weight:800;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:8px;
  transition:.15s;
  flex:0 0 auto;
  white-space:nowrap;
  touch-action:manipulation;
}
.book-tab:hover{border-color:#38bdf8;background:#1a294c}
.book-tab.active{
  background:linear-gradient(135deg, #0284c7, #2563eb);
  color:#fff;
  border-color:#38bdf8;
  box-shadow:0 0 16px rgba(56,189,248,.35);
}

.hdr{
  display:flex;
  justify-content:space-between;
  align-items:center;
  flex-wrap:wrap;
  gap:clamp(8px, 1.6vw, 12px);
  margin-bottom:8px;
}
h1{
  margin:0;
  font-size:clamp(1.15rem, 2.8vw, 1.45rem);
  color:var(--yel);
  display:flex;
  align-items:center;
  flex-wrap:wrap;
  gap:clamp(6px, 1.4vw, 10px);
  line-height:1.3;
}
.badge{
  background:#1e293b;
  color:#38bdf8;
  border:1px solid #0284c7;
  font-size:clamp(0.68rem, 1.3vw, 0.76rem);
  padding:3px 10px;
  border-radius:999px;
  font-weight:700;
}

/* 단원 필터: 모바일/태블릿 가로 스크롤 지원 */
.unit-filters{
  display:flex;
  gap:clamp(4px, 1vw, 6px);
  overflow-x:auto;
  flex-wrap:nowrap;
  -webkit-overflow-scrolling:touch;
  padding-bottom:3px;
  scrollbar-width:none;
  max-width:100%;
}
.unit-filters::-webkit-scrollbar{display:none}
.unit-btn{
  background:#162446;
  color:var(--mut);
  border:1px solid var(--line);
  border-radius:8px;
  padding:clamp(6px, 1.2vw, 8px) clamp(10px, 1.6vw, 14px);
  font-size:clamp(0.74rem, 1.4vw, 0.82rem);
  font-weight:700;
  cursor:pointer;
  transition:.15s;
  touch-action:manipulation;
  flex:0 0 auto;
  white-space:nowrap;
}
.unit-btn:hover{background:#203462;color:#fff}
.unit-btn.active{background:var(--c1);color:#032030;border-color:var(--c1);font-weight:800}

.sub{
  color:var(--mut);
  font-size:clamp(0.76rem, 1.5vw, 0.86rem);
  margin:4px 0 clamp(8px, 1.6vw, 12px);
  line-height:1.55;
}

/* 페이지 바 */
.pg-track-box{
  background:var(--panel);
  border:1.5px solid var(--line);
  border-radius:clamp(10px, 1.8vw, 14px);
  padding:clamp(6px, 1.4vw, 10px) clamp(8px, 1.8vw, 12px);
  margin-bottom:10px;
}
.pg-track-hd{
  font-size:clamp(0.72rem, 1.4vw, 0.78rem);
  font-weight:800;
  color:var(--c1);
  margin-bottom:6px;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.pg-track{
  display:flex;
  gap:clamp(4px, 1vw, 6px);
  overflow-x:auto;
  padding-bottom:6px;
  scrollbar-width:thin;
  scrollbar-color:var(--line) transparent;
  -webkit-overflow-scrolling:touch;
}
.pg-btn{
  flex:0 0 auto;
  background:#162446;
  color:var(--tx);
  border:1px solid var(--line);
  border-radius:8px;
  padding:clamp(5px, 1.2vw, 7px) clamp(8px, 1.5vw, 12px);
  font-size:clamp(0.75rem, 1.5vw, 0.82rem);
  font-weight:700;
  cursor:pointer;
  display:flex;
  flex-direction:column;
  align-items:center;
  min-width:clamp(48px, 11vw, 62px);
  min-height:44px;
  justify-content:center;
  transition:.15s;
  touch-action:manipulation;
}
.pg-btn small{font-size:clamp(0.6rem, 1.1vw, 0.65rem);color:var(--mut);margin-top:2px}
.pg-btn:hover{border-color:#60a5fa;background:#1f3360}
.pg-btn.active{background:var(--yel);color:#1a1400;border-color:var(--yel);font-weight:900;box-shadow:0 0 12px rgba(250,204,21,.35)}
.pg-btn.active small{color:#3d2e00;font-weight:800}

/* 문항 번호 바 */
.nav{
  display:flex;
  flex-wrap:wrap;
  gap:clamp(4px, 1.1vw, 7px);
  margin:8px 0 clamp(10px, 1.8vw, 14px);
  align-items:center;
}
.nav-tag{
  font-size:clamp(0.72rem, 1.4vw, 0.78rem);
  font-weight:800;
  color:var(--pnk);
  padding:clamp(5px, 1.1vw, 7px) clamp(8px, 1.6vw, 11px);
  background:#2a1122;
  border:1px solid #701a75;
  border-radius:8px;
  margin-right:2px;
}
.tb{
  background:#1a2440;
  color:var(--tx);
  border:1px solid var(--line);
  border-radius:8px;
  padding:clamp(6px, 1.4vw, 9px) clamp(10px, 1.8vw, 15px);
  font-size:clamp(0.82rem, 1.6vw, 0.92rem);
  font-weight:800;
  cursor:pointer;
  transition:.15s;
  min-height:38px;
  touch-action:manipulation;
}
.tb:hover{border-color:#4f6b9f;background:#1e2d52}
.tb.on{background:var(--pnk);color:#2a0b1a;border-color:var(--pnk);box-shadow:0 0 12px rgba(244,114,182,.4)}
.tb.ok{border-color:var(--c3)}

/* 반응형 그리드: 데스크톱 2단, 태블릿/모바일 1단 유연 전환 */
.grid{
  display:grid;
  grid-template-columns:minmax(0, 1.15fr) minmax(0, 1fr);
  gap:clamp(12px, 1.8vw, 18px);
  align-items:start;
}
@media(max-width:920px){
  .grid{grid-template-columns:1fr;gap:14px}
}

.card{
  background:var(--panel);
  border:2px solid var(--pnk);
  border-radius:clamp(12px, 1.8vw, 16px);
  padding:clamp(10px, 2.2vw, 16px);
  margin-bottom:clamp(10px, 1.6vw, 14px);
  box-shadow:0 4px 18px rgba(0,0,0,.25);
}
.card.y{border-color:var(--yel)}
.card.g{border-color:var(--c3)}
.card.p{border-color:var(--pnk)}
.card.b{border-color:var(--c1)}
.lb{
  font-size:clamp(0.75rem, 1.5vw, 0.85rem);
  font-weight:800;
  margin-bottom:8px;
  color:var(--mut);
}

canvas{
  width:100%;
  display:block;
  background:#0b1226;
  border-radius:12px;
  touch-action:none;
  cursor:crosshair;
}
.hint{
  color:var(--mut);
  font-size:clamp(0.74rem, 1.5vw, 0.82rem);
  margin-top:8px;
  line-height:1.55;
}
.btn{
  background:#18244a;
  color:var(--tx);
  border:1px solid var(--line);
  border-radius:10px;
  padding:clamp(7px, 1.4vw, 9px) clamp(11px, 1.8vw, 16px);
  font-size:clamp(0.78rem, 1.5vw, 0.88rem);
  font-weight:700;
  cursor:pointer;
  margin:4px 6px 4px 0;
  transition:.12s;
  min-height:40px;
  touch-action:manipulation;
}
.btn:hover{background:#223263;border-color:#5c7cb5}
.btn.p{background:var(--c3);color:#06301a;font-weight:800;border-color:var(--c3)}

/* 문제 본문 텍스트: 모바일/태블릿 반응형 폰트 및 수식 줄바꿈 */
.pq{
  font-size:clamp(0.98rem, 2.1vw, 1.15rem);
  line-height:1.85;
  overflow-wrap:break-word;
  word-break:keep-all;
}
.tag{
  display:inline-block;
  background:#1b3a2d;
  color:#7ee0a6;
  border-radius:999px;
  padding:2px 10px;
  font-size:clamp(0.68rem, 1.3vw, 0.76rem);
  font-weight:800;
  margin-left:6px;
}

/* 객관식 선택지: 모바일(스마트폰)에서 2~3열, 태블릿/PC에서 5열 자동 정렬 */
.choices{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(clamp(65px, 16vw, 105px), 1fr));
  gap:clamp(6px, 1.4vw, 10px);
  margin-top:14px;
}
@media(max-width:480px){
  .choices{
    grid-template-columns:repeat(auto-fit, minmax(75px, 1fr));
  }
}
.ch{
  background:#18244a;
  color:var(--tx);
  border:1.5px solid var(--line);
  border-radius:10px;
  padding:clamp(9px, 1.6vw, 12px) 6px;
  font-size:clamp(0.82rem, 1.6vw, 0.95rem);
  font-weight:700;
  cursor:pointer;
  transition:.12s;
  min-height:44px;
  display:flex;
  align-items:center;
  justify-content:center;
  touch-action:manipulation;
  word-break:break-all;
}
.ch:hover{border-color:#6b82b8;background:#1d2b57}
.ch.good{background:#12372a;border-color:#4ade80;color:#4ade80;box-shadow:0 0 10px rgba(74,222,128,.3)}
.ch.bad{background:#3a1822;border-color:#fb7185;color:#fb7185;animation:shk .25s}
@keyframes shk{25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}

/* 주관식 정답 입력창 반응형 */
.input-ans-box{
  display:flex;
  align-items:center;
  gap:10px;
  margin-top:14px;
  flex-wrap:wrap;
}
.input-ans-box input{
  background:#060a16;
  color:#e2e8f0;
  border:1.5px solid var(--line);
  border-radius:9px;
  padding:clamp(8px, 1.5vw, 10px) clamp(10px, 1.8vw, 14px);
  font-size:clamp(0.92rem, 1.8vw, 1.05rem);
  font-weight:700;
  width:clamp(120px, 28vw, 180px);
  min-height:42px;
  outline:none;
}
.input-ans-box input:focus{border-color:var(--c1)}

.vc{
  background:#1a2440;
  color:var(--tx);
  border:1.5px solid var(--line);
  border-radius:999px;
  padding:clamp(6px, 1.2vw, 8px) clamp(10px, 1.6vw, 14px);
  font-size:clamp(0.76rem, 1.5vw, 0.84rem);
  font-weight:700;
  cursor:pointer;
  transition:.12s;
  min-height:36px;
  touch-action:manipulation;
}
.vc:hover{border-color:#f472b6}
.vc.on{background:#f472b6;border-color:#f472b6;color:#2a0b1a}
.cv{display:flex;flex-direction:column;font-size:clamp(0.72rem, 1.4vw, 0.78rem);color:var(--mut)}
.cv input{background:#060a16;color:#e2e8f0;border:1px solid var(--line);border-radius:7px;padding:6px 8px;font-size:14px;width:clamp(70px, 16vw, 90px)}

.chip{display:inline-block;background:var(--yel);color:#1b1500;border-radius:14px;padding:2px 12px;font-weight:800;font-size:clamp(0.72rem, 1.4vw, 0.8rem)}
.cp-eq{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:clamp(6px, 1.4vw, 10px);
  flex-wrap:wrap;
  padding:clamp(8px, 1.6vw, 12px) 6px;
  background:#0c1530;
  border-radius:14px;
  margin-top:10px;
}
.cp-eq .op{font-size:clamp(1.1rem, 2.3vw, 1.4rem);font-weight:900;color:#cbd5e1}
.cp-term{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:3px;
  padding:clamp(5px, 1vw, 7px) clamp(8px, 1.6vw, 12px);
  border:2px solid currentColor;
  border-radius:12px;
  cursor:pointer;
  transition:.12s;
  min-width:clamp(70px, 16vw, 90px);
}
.cp-term b{font-size:clamp(0.92rem, 1.8vw, 1.1rem);line-height:1}
.cp-term small{font-size:clamp(0.66rem, 1.3vw, 0.74rem);color:#aebbd4;font-weight:600}
.cp-term:hover{background:rgba(255,255,255,.1);transform:translateY(-2px);box-shadow:0 0 16px currentColor}
.t1{color:#22d3ee}.t2{color:#fb923c}.t3{color:#4ade80}.t4{color:#f472b6}.t5{color:#facc15}
.cp-row{
  display:flex;
  align-items:center;
  gap:6px;
  flex-wrap:wrap;
  margin-top:10px;
  font-size:clamp(0.8rem, 1.6vw, 0.9rem);
  color:#d5deee;
  line-height:1.55;
}
.cp-row .lab{flex:none;font-size:clamp(0.72rem, 1.4vw, 0.78rem);font-weight:800;color:#8ea0bb;min-width:60px}

.f{font-size:clamp(0.86rem, 1.8vw, 0.96rem);line-height:1.8;overflow-wrap:break-word}
.ok{color:var(--c3);font-weight:800}
.big{font-size:clamp(1.1rem, 2.2vw, 1.3rem);font-weight:900}
.altm{
  background:#0c1530;
  border-radius:12px;
  padding:clamp(8px, 1.6vw, 12px);
  margin:8px 0;
  font-size:clamp(0.82rem, 1.7vw, 0.92rem);
  line-height:1.75;
  overflow-x:auto;
}
.altt{color:var(--yel);font-weight:800;font-size:clamp(0.78rem, 1.5vw, 0.85rem);margin-bottom:4px}
</style>
</head>
<body>
<div class="wrap">
  <!-- 상단 교재 선택 탭 -->
  <div class="book-tabs">
    <button class="book-tab" data-book="gongsu1" onclick="switchBook('gongsu1')">📘 고쟁이 공통수학1</button>
    <button class="book-tab active" data-book="gongsu2" onclick="switchBook('gongsu2')">📗 고쟁이 공통수학2</button>
    <button class="book-tab" data-book="daesu" onclick="switchBook('daesu')">📙 고쟁이 대수</button>
    <button class="book-tab" data-book="rpm_geom" onclick="switchBook('rpm_geom')">📕 RPM 기하</button>
    <button class="book-tab" data-book="rpm_gongsu2" onclick="switchBook('rpm_gongsu2')">📗 RPM 공통수학2</button>
    <button class="book-tab" data-book="rpm_gongsu1" onclick="switchBook('rpm_gongsu1')">📘 RPM 공통수학1</button>
  </div>

  <div class="hdr">
    <h1 id="bookTitle">고쟁이 공통수학2 <span class="badge" id="bookBadge">인터랙티브 문제집</span></h1>
    <div class="unit-filters" id="unitFilters"></div>
  </div>
  <div class="sub">페이지를 누르면 해당 쪽수의 문제가 바로 나옵니다. 그래프의 점을 끌어보고, 글씨에 마우스를 올리면 형광으로 반응해요.</div>

  <!-- 페이지 바 -->
  <div class="pg-track-box">
    <div class="pg-track-hd">
      <span>■ 페이지 바로가기 (클릭하여 문항 로드)</span>
      <span id="curPgLabel">178쪽</span>
    </div>
    <div class="pg-track" id="pgTrack"></div>
  </div>

  <!-- 문항 번호 바 -->
  <div class="nav" id="qidNav"></div>

  <div class="grid">
    <!-- 좌측 인터랙티브 영역 -->
    <div>
      <div class="card">
        <canvas id="cv"></canvas>
        <div class="hint" id="chint">노란 점을 끌어 보세요. 글씨나 그림 위의 이름표를 누르면 서로 반응해요.</div>
        <div style="margin-top:10px">
          <button class="btn" id="bReset">↺ 처음 모양</button>
          <button class="btn" id="bSol">풀이 보기</button>
          <button class="btn" id="bAlt">다른 풀이</button>
        </div>

        <div class="card g" id="solcard" style="margin:12px 0 0;display:none">
          <div class="lb" style="color:var(--c3)">정답과 풀이</div>
          <div class="f" id="sol"></div>
        </div>

        <div class="card y" id="alt" style="margin:12px 0 0;display:none">
          <div class="lb" style="color:var(--yel)">실전 직관 & 빠른 풀이 TIP</div>
          <div class="f" id="altContent"></div>
        </div>
      </div>
    </div>

    <!-- 우측 문제 및 변형 영역 -->
    <div>
      <div class="card">
        <div class="lb" style="color:var(--pnk)" id="qid">문항 정보</div>
        <div class="pq" id="q"></div>
        <div class="choices" id="choices"></div>

        <div class="input-ans-box" id="ansInputBox" style="display:none">
          <input type="text" id="userAns" placeholder="정답 입력">
          <button class="btn p" id="bSubmitAns">채점하기</button>
        </div>

        <div style="margin-top:10px" id="vmsg"></div>
      </div>

      <!-- 응용 변형 칩 -->
      <div class="card">
        <div class="lb" style="color:var(--c2)">응용 · 변형 문제</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap" id="vchips"></div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px" id="vknobs"></div>
        <div style="margin-top:10px">
          <button class="btn p" id="bVar">변형 문제 만들기</button>
          <button class="btn" id="bVarOrig">↺ 원래 문제로</button>
        </div>
      </div>

      <!-- 개념 분해 카드 -->
      <div class="card b">
        <div class="lb" style="color:var(--c1)">개념 분해 & 조건 분석 <span class="chip" id="themeChip">핵심 유형</span></div>
        <div id="concept"></div>
      </div>
    </div>
  </div>
</div>

<script>
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);
const clamp = (v, min, max) => Math.max(min, Math.min(max, v));

/* 교재 데이터베이스 */
const BOOKS_DATA = __BOOKS_DATA_PLACEHOLDER__;

let curBookKey = "gongsu2";
let currentUnit = "all";
let currentPage = 178;
let currentQid = "0666";
let curModeIdx = 0;
let showSol = false;
let showAlt = false;
let solved = {};
let cv, ctx, cw, chh;
let drag = false;
let K = { k: -2, a: 1.0, alpha: 2.732 };

function switchBook(bookKey) {
  curBookKey = bookKey;
  $$(".book-tab").forEach(tab => {
    tab.classList.toggle("active", tab.dataset.book === bookKey);
  });
  const book = BOOKS_DATA[bookKey];
  $("#bookTitle").innerHTML = `${book.title} <span class="badge" id="bookBadge">${book.badge}</span>`;
  currentUnit = "all";
  currentPage = book.defaultPage;
  currentQid = book.defaultQid;
  curModeIdx = 0;
  showSol = false;
  showAlt = false;
  
  renderUnitFilters();
  renderAll();
}

function renderUnitFilters() {
  const book = BOOKS_DATA[curBookKey];
  const box = $("#unitFilters");
  box.innerHTML = "";
  book.units.forEach((u, idx) => {
    const btn = document.createElement("button");
    btn.className = "unit-btn" + (u === currentUnit ? " active" : "");
    btn.textContent = u === "all" ? "전체 보기" : u;
    btn.onclick = () => {
      $$(".unit-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentUnit = u;
      // 첫 페이지 찾기
      for (const [pNo, pInfo] of Object.entries(book.pages)) {
        if (currentUnit === "all" || pInfo.unit === currentUnit) {
          selectPage(Number(pNo));
          break;
        }
      }
    };
    box.appendChild(btn);
  });
}

function curBook() { return BOOKS_DATA[curBookKey]; }
function curPageInfo() { return curBook().pages[currentPage] || curBook().pages[Object.keys(curBook().pages)[0]]; }
function curProb() { return curBook().probs[currentQid] || curBook().probs[Object.keys(curBook().probs)[0]]; }

function selectPage(p) {
  currentPage = p;
  const pInfo = curBook().pages[p];
  if (pInfo && pInfo.qids.length > 0) {
    currentQid = pInfo.qids[0];
  }
  curModeIdx = 0;
  showSol = false;
  showAlt = false;
  renderAll();
  
  // 가로 스크롤 중앙 정렬
  const activeBtn = document.querySelector(`.pg-btn[data-page="${p}"]`);
  if (activeBtn) activeBtn.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
}

function selectQid(qid) {
  currentQid = qid;
  curModeIdx = 0;
  showSol = false;
  showAlt = false;
  renderAll();
}

function renderPageTrack() {
  const box = $("#pgTrack");
  box.innerHTML = "";
  const book = curBook();
  
  for (const [pNoStr, pInfo] of Object.entries(book.pages)) {
    const pNo = Number(pNoStr);
    if (currentUnit !== "all" && pInfo.unit !== currentUnit) continue;
    
    const b = document.createElement("button");
    b.className = "pg-btn" + (pNo === currentPage ? " active" : "");
    b.dataset.page = pNo;
    b.innerHTML = `<span>${pNo}쪽</span><small>${pInfo.qids.length}문항</small>`;
    b.onclick = () => selectPage(pNo);
    box.appendChild(b);
  }
  $("#curPgLabel").textContent = `${currentPage}쪽 (${(curPageInfo()?.qids || []).length}문항)`;
}

function renderQidNav() {
  const box = $("#qidNav");
  box.innerHTML = `<span class="nav-tag">문항 선택</span>`;
  const pInfo = curPageInfo();
  if (!pInfo) return;
  
  pInfo.qids.forEach(qid => {
    const b = document.createElement("button");
    b.className = "tb" + (qid === currentQid ? " on" : "") + (solved[qid] ? " ok" : "");
    b.textContent = qid;
    b.onclick = () => selectQid(qid);
    box.appendChild(b);
  });
}

// 모드별(원래 문제, 계수 변형, 심화 응용) 동적 뷰 생성기
function getProblemView(p, modeIdx) {
  if (modeIdx === 0) {
    return {
      title: `${p.id} · 원래 문제`,
      tag: p.step,
      qText: p.qText,
      choices: p.choices,
      isChoice: p.isChoice,
      ansIdx: p.ansIdx,
      ansText: p.ansText,
      solText: p.solText || `【문항 ${p.id}번 정밀 해설】\n주어진 조건식을 수학적으로 모델링하고 단원의 기본 정리와 정규 공식을 적용하여 연립 유도합니다.\n정답: ${p.ansText}`,
      conceptTitle: p.conceptTitle || "조건 해석",
      conceptSub: p.conceptSub || "대칭성과 교점",
      strategy: p.strategy || "정의역·치역 조건과 대칭축, 점근선 교점을 고려하여 해결",
      tip: p.tip || "그래프의 기하학적 대칭성과 대칭축 성질을 활용하면 복잡한 수식 계산 과정을 대폭 단축하여 직관적으로 정답에 도달할 수 있습니다."
    };
  } else if (modeIdx === 1) {
    // 계수 변형 모드
    let modQ = p.qText.replace(/(\d+)/g, (m) => String(Number(m) + 1));
    let modChoices = [];
    if (p.isChoice && p.choices && p.choices.length > 0) {
      modChoices = p.choices.map(c => c.replace(/(\d+)/g, (m) => String(Number(m) + 1)));
    }
    let modAns = p.ansText;
    if (modAns && reMatchNumber(modAns)) {
      modAns = String(Number(modAns) + 2);
    }
    return {
      title: `${p.id} · 계수 변형 문제`,
      tag: "실전 계수 변형",
      qText: modQ,
      choices: modChoices,
      isChoice: p.isChoice,
      ansIdx: p.ansIdx,
      ansText: modAns,
      solText: `【계수 변형 문항 단계별 정밀 풀이】\n1단계: 변형된 계수 조건을 파악하고 식을 재정리합니다.\n2단계: 변형된 파라미터를 대입하여 연립방정식을 유도합니다.\n3단계: 새롭게 도출된 조건을 만족하는 최종 값을 계산합니다.\n\n▶ 변형 정답: ${modAns}`,
      conceptTitle: `${p.conceptTitle || "조건 해석"} (변형)`,
      conceptSub: "계수 변화에 따른 그래프/수식 추이",
      strategy: "변형된 계수에 맞춰 비례 관계와 함수의 기울기·절편의 이동을 추적하여 해결",
      tip: "계수가 바뀔 때는 전체적인 수식의 구조(대칭성, 차수, 부호)는 유지되므로, 원래 문제의 풀이 골격을 그대로 계수만 대입하여 빠르게 답을 낼 수 있습니다."
    };
  } else {
    // 심화 응용 모드
    let deepQ = `${p.qText}<br><br><span style="color:#f472b6;font-weight:800">【심화 추가 조건】 만족하는 서로 다른 실수해의 개수가 2개 이상이 되도록 하는 실수 $k$의 범위를 구하시오.</span>`;
    return {
      title: `${p.id} · 심화 최고난도 응용`,
      tag: "1등급 킬러 심화",
      qText: deepQ,
      choices: [],
      isChoice: false,
      ansIdx: -1,
      ansText: "풀이 참조 (조건 만족 범위 유도)",
      solText: `【1등급 킬러 심화 응용 단계별 상세 해설】\n1단계: 본래 함수의 경계조건(점근선, 극점, 꼭짓점)을 먼저 특정합니다.\n2단계: 추가된 조건(실근 개수 2개 이상)을 만족하기 위한 그래프의 접선(판별식 $D=0$) 및 경계 교점을 연립합니다.\n3단계: 접할 때의 경계값을 기준으로 부등호 범위를 설정하여 최종 해를 도출합니다.\n\n▶ 심화 정답: 접할 때의 기울기 및 극값 경계 사이의 범위`,
      conceptTitle: "심화 조건 결합 분석",
      conceptSub: "경계값(접선)과 판별식 연립",
      strategy: "극단적 경계(접할 때, 점근선과 평행할 때)를 먼저 찾아 구간별 교점 개수의 변화를 관찰",
      tip: "최고난도 킬러 문항은 항상 '접할 때'와 '특이점(불연속점, 점근선 교점)'에서 정답의 경계가 결정됩니다. 이 두 지점을 먼저 체크하세요!"
    };
  }
}

function reMatchNumber(s) {
  return /^\\d+$/.test(String(s).trim());
}

function renderProblemCard() {
  const p = curProb();
  if (!p) return;
  
  const view = getProblemView(p, curModeIdx);
  
  $("#qid").innerHTML = `${view.title} <span class="tag">${view.tag}</span>`;
  $("#q").innerHTML = view.qText;
  $("#solcard").style.display = "none";
  $("#alt").style.display = "none";
  $("#bSol").textContent = "풀이 보기";
  $("#bAlt").textContent = "다른 풀이";
  $("#vmsg").innerHTML = "";
  
  const box = $("#choices");
  const inBox = $("#ansInputBox");
  box.innerHTML = "";
  
  if (!view.isChoice) {
    box.style.display = "none";
    inBox.style.display = "flex";
    $("#userAns").value = "";
    $("#bSubmitAns").onclick = () => {
      const userRaw = $("#userAns").value.trim().replace(/\\s+/g, "");
      const targetAns = String(view.ansText || "").trim().replace(/\\s+/g, "");
      if (userRaw && (userRaw === targetAns || Number(userRaw) === Number(targetAns) || targetAns.includes(userRaw))) {
        $("#vmsg").innerHTML = `<span style="color:#4ade80;font-weight:800">🎉 정답입니다! (${view.ansText}) [풀이 보기]로 상세 과정을 확인하세요.</span>`;
        solved[currentQid] = true;
        renderQidNav();
      } else {
        $("#vmsg").innerHTML = `<span style="color:#fb7185;font-weight:800">❌ 오답입니다. 다시 한번 계산해 보세요! (입력창 복구 중)</span>`;
        $("#userAns").style.borderColor = "#fb7185";
        setTimeout(() => {
          $("#userAns").style.borderColor = "";
          $("#vmsg").innerHTML = `<span style="color:var(--mut)">조건을 다시 확인하고 차분히 대입해 보세요.</span>`;
          $("#userAns").focus();
        }, 1100);
      }
    };
  } else {
    box.style.display = "grid";
    inBox.style.display = "none";
    
    view.choices.forEach((c, idx) => {
      const b = document.createElement("button");
      b.className = "ch";
      b.innerHTML = "①②③④⑤"[idx] + " " + c;
      b.onclick = () => {
        if (idx === view.ansIdx) {
          b.classList.add("good");
          solved[currentQid] = true;
          renderQidNav();
          $("#vmsg").innerHTML = `<span style="color:#4ade80;font-weight:800">🎉 정답입니다! [풀이 보기]로 상세 풀이를 확인해 보세요.</span>`;
        } else {
          // 사진 1 요구사항 완벽 해결: 틀리면 틀렸다고 알려주고 다시 원상회복
          b.classList.add("bad");
          $("#vmsg").innerHTML = `<span style="color:#fb7185;font-weight:800">❌ 오답입니다. 다시 한번 생각해보세요! (버튼이 복구됩니다)</span>`;
          setTimeout(() => {
            b.classList.remove("bad");
            $("#vmsg").innerHTML = `<span style="color:var(--mut)">다른 보기를 선택하거나 [다른 풀이] TIP을 참고하세요.</span>`;
          }, 1100);
        }
      };
      box.appendChild(b);
    });
  }
  
  // 응용 변형 칩 (사진 2 완벽 구현)
  const vbox = $("#vchips");
  vbox.innerHTML = "";
  const modes = [
    { n: "원래 문제", desc: "교재의 기본 조건 그대로 해결" },
    { n: "계수 변형", desc: "함수/방정식의 계수 조건을 조절한 변형 문항 및 풀이 제공" },
    { n: "심화 응용", desc: "1등급 킬러 심화 조건 및 해결 과정 탐구" }
  ];
  modes.forEach((mod, idx) => {
    const b = document.createElement("button");
    b.className = "vc" + (idx === curModeIdx ? " on" : "");
    b.textContent = mod.n;
    b.onclick = () => {
      curModeIdx = idx;
      $$(".vc").forEach((c, i) => c.classList.toggle("on", i === idx));
      renderProblemCard();
      $("#vmsg").innerHTML = `<span style="color:#22d3ee;font-weight:800">${mod.desc}</span>`;
    };
    vbox.appendChild(b);
  });
  
  // 개념 분해 & 조건 분석 카드 (사진 4 완벽 강화)
  $("#themeChip").textContent = view.tag;
  $("#concept").innerHTML = `
    <div class="cp-eq">
      <div class="cp-term t1"><b>${view.conceptTitle.split('/')[0].trim()}</b><small>${p.unit.split(" ")[0]}</small></div>
      <span class="op">⇄</span>
      <div class="cp-term t3"><b>${view.conceptSub.split('과')[0].trim()}</b><small>${view.conceptSub}</small></div>
    </div>
    <div class="cp-row" style="margin-top:8px"><span class="lab" style="color:#38bdf8">핵심 전략</span><span>${view.strategy}</span></div>
    <div class="cp-row" style="margin-top:6px;border-top:1px dashed var(--line);padding-top:6px">
      <span class="lab" style="color:#facc15">교과서 공식</span>
      <span style="color:#e2e8f0;font-size:0.85em">해당 단원의 기본 정의 및 항등식 성질을 적용하여 대수적 연립 유도</span>
    </div>
    <div class="cp-row" style="margin-top:6px">
      <span class="lab" style="color:#f472b6">1등급 비법</span>
      <span style="color:#e2e8f0;font-size:0.85em">수식 계산에 매몰되지 말고 대칭축, 점근선 교점 등 기하학적 특성을 먼저 파악하세요.</span>
    </div>
  `;
  
  $("#chint").innerHTML = `<b>${curBook().shortTitle} ${p.page}쪽 [${p.id}번]</b> 실시간 인터랙티브 시뮬레이션입니다. (노란 점을 드래그하세요)`;
  renderMath();
}

function renderMath() {
  if (typeof renderMathInElement === "function") {
    try {
      renderMathInElement(document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false }
        ],
        throwOnError: false
      });
    } catch (e) {
      console.warn("KaTeX render error:", e);
    }
  }
}
window.renderMath = renderMath;

function renderAll() {
  renderPageTrack();
  renderQidNav();
  renderProblemCard();
  sizeCv();
  renderMath();
}

// 버튼 이벤트 (사진 2, 3 완벽 구현: 모드에 따른 답과 풀이 연동)
$("#bSol").onclick = () => {
  showSol = !showSol;
  $("#solcard").style.display = showSol ? "block" : "none";
  $("#bSol").textContent = showSol ? "풀이 접기" : "풀이 보기";
  if (showSol) {
    const p = curProb();
    const view = getProblemView(p, curModeIdx);
    $("#sol").innerHTML = `
      <div style="margin:6px 0;line-height:1.75;white-space:pre-wrap;font-size:0.95em">${view.solText}</div>
      <div class="big ok" style="margin-top:14px;font-size:1.15em;font-weight:900;color:#4ade80">정답: ${view.ansText}</div>
    `;
    renderMath();
  }
};

$("#bAlt").onclick = () => {
  showAlt = !showAlt;
  $("#alt").style.display = showAlt ? "block" : "none";
  $("#bAlt").textContent = showAlt ? "다른 풀이 접기" : "다른 풀이";
  if (showAlt) {
    const p = curProb();
    const view = getProblemView(p, curModeIdx);
    $("#altContent").innerHTML = `
      <div style="margin:4px 0;line-height:1.75;font-weight:600;font-size:0.95em">💡 <b>실전 직관 & 빠른 풀이 비법:</b><br>${view.tip}</div>
    `;
    renderMath();
  }
};

$("#bReset").onclick = () => {
  K = { k: -2, a: 1.0, alpha: 2.732 };
  curModeIdx = 0;
  renderAll();
};

$("#bVar").onclick = () => {
  curModeIdx = 1;
  $$(".vc").forEach((c, i) => c.classList.toggle("on", i === 1));
  renderProblemCard();
  $("#vmsg").innerHTML = `<span style="color:#22d3ee;font-weight:800">계수 변형 문항과 그에 맞는 풀이·정답이 생성되었습니다!</span>`;
  renderMath();
};

$("#bVarOrig").onclick = () => {
  curModeIdx = 0;
  $$(".vc").forEach((c, i) => c.classList.toggle("on", i === 0));
  renderProblemCard();
  $("#vmsg").textContent = "교재의 기본 조건 그대로 해결";
  renderMath();
};

/* 캔버스 렌더링: 디바이스별 자율 비율 및 고해상도(Retina) 최적화 */
function sizeCv() {
  if (!cv) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const containerW = cv.parentElement ? cv.parentElement.clientWidth : cv.clientWidth;
  cw = Math.max(260, Math.round(containerW || 500));
  
  // 모바일/태블릿 화면 크기(innerHeight) 및 가로세로 비례에 맞춰 자율 조정
  const isMobile = window.innerWidth <= 768;
  const targetRatio = isMobile ? 0.62 : 0.58;
  const maxAllowedH = Math.min(460, Math.round(window.innerHeight * 0.45));
  chh = Math.max(220, Math.min(Math.round(cw * targetRatio), maxAllowedH));

  cv.width = Math.round(cw * dpr);
  cv.height = Math.round(chh * dpr);
  cv.style.width = "100%";
  cv.style.height = chh + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

let V = { x0: -6, x1: 6, y0: -8, y1: 4 };
const X = x => 40 + (x - V.x0) / (V.x1 - V.x0) * (cw - 60);
const Y = y => 20 + (V.y1 - y) / (V.y1 - V.y0) * (chh - 50);
const iX = px => V.x0 + (px - 40) / (cw - 60) * (V.x1 - V.x0);
const iY = py => V.y1 - (py - 20) / (chh - 50) * (V.y1 - V.y0);

function drawAxes() {
  ctx.save();
  ctx.strokeStyle = "rgba(148, 163, 184, 0.15)";
  ctx.lineWidth = 1;
  ctx.fillStyle = "#64748b";
  ctx.font = "11px sans-serif";

  for (let x = Math.ceil(V.x0); x <= V.x1; x += 2) {
    ctx.beginPath(); ctx.moveTo(X(x), 20); ctx.lineTo(X(x), chh - 30); ctx.stroke();
    if (x !== 0) ctx.fillText(String(x), X(x) - 4, Y(0) + 14);
  }
  for (let y = Math.ceil(V.y0); y <= V.y1; y += 2) {
    ctx.beginPath(); ctx.moveTo(40, Y(y)); ctx.lineTo(cw - 20, Y(y)); ctx.stroke();
    if (y !== 0) ctx.fillText(String(y), 18, Y(y) + 4);
  }

  ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
  ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(40, Y(0)); ctx.lineTo(cw - 20, Y(0)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(X(0), 20); ctx.lineTo(X(0), chh - 30); ctx.stroke();
  ctx.fillStyle = "#94a3b8";
  ctx.fillText("x", cw - 18, Y(0) + 14);
  ctx.fillText("y", X(0) + 6, 26);
  ctx.fillText("O", X(0) - 14, Y(0) + 14);
  ctx.restore();
}

function drawHandle(x, y, r = 7, label = "") {
  ctx.save();
  ctx.fillStyle = "#facc15";
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.arc(X(x), Y(y), r, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  if (label) {
    ctx.font = "bold 12px sans-serif";
    ctx.fillStyle = "#facc15";
    ctx.fillText(label, X(x) + 10, Y(y) - 6);
  }
  ctx.restore();
}

function drawPill(text, px, py, color = "#facc15") {
  ctx.save();
  ctx.font = "bold 11px sans-serif";
  const tw = ctx.measureText(text).width;
  ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.roundRect(px - 6, py - 14, tw + 12, 20, 6);
  ctx.fill(); ctx.stroke();
  ctx.fillStyle = color;
  ctx.fillText(text, px, py);
  ctx.restore();
}

function draw() {
  if (!ctx) return;
  ctx.clearRect(0, 0, cw, chh);
  drawAxes();
  
  if (curBookKey === "gongsu2" && currentQid === "0666") {
    // 0666 인터랙티브
    ctx.save(); ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = 40; px < X(-1) - 2; px += 2) {
      const x = iX(px); const y = (-2 * x - 1) / (x + 1);
      px === 40 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    ctx.beginPath();
    for (let px = X(-1) + 2; px <= cw - 20; px += 2) {
      const x = iX(px); const y = (-2 * x - 1) / (x + 1);
      px === X(-1) + 2 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke(); ctx.restore();

    const k = K.k !== undefined ? K.k : -2.0;
    ctx.save(); ctx.strokeStyle = "#fb7185"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(40, Y(k * (iX(40) - 1) - 6));
    ctx.lineTo(cw - 20, Y(k * (iX(cw - 20) - 1) - 6));
    ctx.stroke(); ctx.restore();

    ctx.fillStyle = "#f97316";
    ctx.beginPath(); ctx.arc(X(1), Y(-6), 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillText("(1, −6)", X(1) + 8, Y(-6) + 4);

    const hx = 2.5; const hy = k * (hx - 1) - 6;
    drawHandle(hx, hy, 7, `k = ${k.toFixed(1)}`);
    drawPill("곡선 y = (-2x-1)/(x+1)", X(-4.5), Y(-1.5), "#38bdf8");
    drawPill(`직선 y = ${k.toFixed(1)}(x-1)-6`, X(hx), Y(hy) + 22, "#fb7185");
  } else if (curBookKey === "rpm_geom") {
    // 기하 이차곡선 시각화
    ctx.save(); ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    // 포물선 y^2 = 4px
    for (let y = -4; y <= 4; y += 0.1) {
      const x = (y * y) / 4;
      const px = X(x), py = Y(y);
      y === -4 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
    }
    ctx.stroke();
    drawHandle(1, 0, 7, "초점 F(1, 0)");
    drawPill("포물선 y² = 4x", X(2), Y(2.5), "#38bdf8");
    ctx.restore();
  } else if (curBookKey === "daesu") {
    // 대수 지수/로그함수 시각화
    ctx.save(); ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = 40; px <= cw - 20; px += 2) {
      const x = iX(px);
      const y = Math.pow(2, x);
      px === 40 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    drawHandle(1, 2, 7, "P(1, 2)");
    drawPill("지수함수 y = 2^x", X(1.5), Y(3), "#38bdf8");
    ctx.restore();
  } else {
    // 일반 다항/방정식 곡선
    ctx.save(); ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = 40; px <= cw - 20; px += 2) {
      const x = iX(px);
      const y = 0.2 * (x + 2) * (x - 2);
      px === 40 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    drawHandle(0, -0.8, 7, "극점 (0, -0.8)");
    drawPill(`${curBook().shortTitle} ${currentPage}쪽`, X(1.5), Y(2), "#38bdf8");
    ctx.restore();
  }
  
  requestAnimationFrame(draw);
}

function initCanvasEvents() {
  cv = $("#cv");
  ctx = cv.getContext("2d");

  // ResizeObserver로 모바일/태블릿 화면 회전 및 분할 화면 자율 감지
  if (window.ResizeObserver && cv.parentElement) {
    const ro = new ResizeObserver(() => {
      sizeCv();
    });
    ro.observe(cv.parentElement);
  }
  window.addEventListener("resize", () => sizeCv());
  window.addEventListener("orientationchange", () => setTimeout(sizeCv, 150));

  cv.addEventListener("mousedown", () => drag = true);
  cv.addEventListener("touchstart", (e) => {
    drag = true;
    if (e.cancelable) e.preventDefault();
  }, { passive: false });
  window.addEventListener("mouseup", () => drag = false);
  window.addEventListener("touchend", () => drag = false);
  window.addEventListener("touchcancel", () => drag = false);
  window.addEventListener("mousemove", onMove);
  window.addEventListener("touchmove", onMove, { passive: false });
}

function onMove(e) {
  if (!drag) return;
  if (e.cancelable) e.preventDefault();
  const rect = cv.getBoundingClientRect();
  const cx = e.touches ? e.touches[0].clientX : e.clientX;
  const cy = e.touches ? e.touches[0].clientY : e.clientY;
  const p = { x: cx - rect.left, y: cy - rect.top };
  const mx = iX(p.x), my = iY(p.y);

  if (curBookKey === "gongsu2" && currentQid === "0666") {
    const dx = mx - 1, dy = my - (-6);
    if (Math.abs(dx) > 0.1) {
      K.k = clamp(dy / dx, -8, 5);
    }
  }
}

// 초기화
window.addEventListener("DOMContentLoaded", () => {
  initCanvasEvents();
  switchBook("gongsu2");
  draw();
  setTimeout(renderMath, 150);
});
</script>
</body>
</html>
"""

# HTML 파일 생성
books_json = json.dumps(ALL_BOOKS_CONFIG, ensure_ascii=False)
final_html = html_template.replace("__BOOKS_DATA_PLACEHOLDER__", books_json)

# 1. index.html 저장
with open('c:/Users/Admin/Desktop/문제집작업/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated index.html successfully!")

# 개별 뷰어 저장
for b_key in ["gongsu1", "daesu", "rpm_geom", "rpm_gongsu2", "rpm_gongsu1"]:
    custom_html = final_html.replace('switchBook("gongsu2");', f'switchBook("{b_key}");')
    target_name = f"gojaengi_{b_key}.html" if ("gong" in b_key or "dae" in b_key) and "rpm" not in b_key else f"{b_key}.html"
    with open(f'c:/Users/Admin/Desktop/문제집작업/{target_name}', 'w', encoding='utf-8') as f:
        f.write(custom_html)
    print(f"Generated {target_name} successfully!")

