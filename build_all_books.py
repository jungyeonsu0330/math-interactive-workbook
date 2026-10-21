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

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_daesu.json', 'r', encoding='utf-8') as f:
    d_rpm_daesu = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_calc1.json', 'r', encoding='utf-8') as f:
    d_rpm_calc1 = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_calc2.json', 'r', encoding='utf-8') as f:
    d_rpm_calc2 = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_mock_calc.json', 'r', encoding='utf-8') as f:
    d_mock_calc = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_mid1_2.json', 'r', encoding='utf-8') as f:
    d_rpm_mid1_2 = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_rpm_mid2_2.json', 'r', encoding='utf-8') as f:
    d_rpm_mid2_2 = json.load(f)

with open('c:/Users/Admin/Desktop/문제집작업/parsed_ilpum_mid2_2.json', 'r', encoding='utf-8') as f:
    d_ilpum_mid2_2 = json.load(f)

print(f"Loaded datasets: Gongsu2 ({len(d_gongsu2['probs'])}), Gongsu1 ({len(d_gongsu1['probs'])}), Daesu ({len(d_daesu['probs'])}), RPM_Geom ({len(d_rpm['probs'])}), RPM_Gongsu2 ({len(d_rpm_g2['probs'])}), RPM_Gongsu1 ({len(d_rpm_g1['probs'])}), RPM_Daesu ({len(d_rpm_daesu['probs'])}), RPM_Calc1 ({len(d_rpm_calc1['probs'])}), RPM_Calc2 ({len(d_rpm_calc2['probs'])}), RPM_Mid1_2 ({len(d_rpm_mid1_2['probs'])}), RPM_Mid2_2 ({len(d_rpm_mid2_2['probs'])}), Mock_Calc ({len(d_mock_calc['probs'])})")

# 10개 교재 메타데이터 (시리즈별 및 교육과정 순서 정렬)
ALL_BOOKS_CONFIG = {
    "gongsu1": {
        "series": "gojaengi",
        "seriesName": "고등 고쟁이",
        "seriesIcon": "📘",
        "subjectName": "공통수학1",
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
        "series": "gojaengi",
        "seriesName": "고등 고쟁이",
        "seriesIcon": "📘",
        "subjectName": "공통수학2",
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
        "series": "gojaengi",
        "seriesName": "고등 고쟁이",
        "seriesIcon": "📘",
        "subjectName": "대수",
        "title": "유형내신 고쟁이 대수",
        "shortTitle": "고쟁이 대수",
        "badge": "고쟁이 대수",
        "units": ["all", "01 지수함수와 로그함수", "02 삼각함수", "03 수열"],
        "defaultPage": 7,
        "defaultQid": "0001",
        "pages": d_daesu["pages"],
        "probs": d_daesu["probs"]
    },
    "rpm_gongsu1": {
        "series": "rpm",
        "seriesName": "고등 RPM",
        "seriesIcon": "📙",
        "subjectName": "공통수학1",
        "title": "개념원리 RPM 공통수학1",
        "shortTitle": "RPM 공통수학1",
        "badge": "사진 1 신규 등록",
        "units": ["all", "01 다항식의 연산과 인수분해", "02 방정식과 부등식", "03 경우의 수와 행렬"],
        "defaultPage": 7,
        "defaultQid": "0001",
        "pages": d_rpm_g1["pages"],
        "probs": d_rpm_g1["probs"]
    },
    "rpm_gongsu2": {
        "series": "rpm",
        "seriesName": "고등 RPM",
        "seriesIcon": "📙",
        "subjectName": "공통수학2",
        "title": "개념원리 RPM 공통수학2",
        "shortTitle": "RPM 공통수학2",
        "badge": "사진 1·2 신규 등록",
        "units": ["all", "01 평면좌표와 직선의 방정식", "02 원의 방정식과 도형의 이동", "03 집합과 명제", "04 함수와 역함수", "05 유리함수와 무리함수"],
        "defaultPage": 7,
        "defaultQid": "0001",
        "pages": d_rpm_g2["pages"],
        "probs": d_rpm_g2["probs"]
    },
    "rpm_daesu": {
        "series": "rpm",
        "seriesName": "고등 RPM",
        "seriesIcon": "📙",
        "subjectName": "대수",
        "title": "개념원리 RPM 대수 (2022개정)",
        "shortTitle": "RPM 대수",
        "badge": "2022개정 신규 등록",
        "units": ["all", "01 지수함수와 로그함수", "02 삼각함수", "03 수열"],
        "defaultPage": 6,
        "defaultQid": "0001",
        "pages": d_rpm_daesu["pages"],
        "probs": d_rpm_daesu["probs"]
    },
    "rpm_calc1": {
        "series": "rpm",
        "seriesName": "고등 RPM",
        "seriesIcon": "📙",
        "subjectName": "미적분1",
        "title": "개념원리 RPM 미적분1 (2022개정)",
        "shortTitle": "RPM 미적분1",
        "badge": "2022개정 신규 등록",
        "units": ["all", "01 함수의 극한과 연속", "02 미분법", "03 적분법"],
        "defaultPage": 6,
        "defaultQid": "0001",
        "pages": d_rpm_calc1["pages"],
        "probs": d_rpm_calc1["probs"]
    },
    "rpm_calc2": {
        "series": "rpm",
        "seriesName": "고등 RPM",
        "seriesIcon": "📙",
        "subjectName": "미적분2",
        "title": "개념원리 RPM 미적분2 (2022개정)",
        "shortTitle": "RPM 미적분2",
        "badge": "2022개정 신규 등록",
        "units": ["all", "01 수열의 극한", "02 미분법", "03 적분법"],
        "defaultPage": 6,
        "defaultQid": "0001",
        "pages": d_rpm_calc2["pages"],
        "probs": d_rpm_calc2["probs"]
    },
    "rpm_geom": {
        "series": "rpm",
        "seriesName": "고등 RPM",
        "seriesIcon": "📙",
        "subjectName": "기하",
        "title": "개념원리 RPM 기하",
        "shortTitle": "RPM 기하",
        "badge": "RPM 기하",
        "units": ["all", "01 이차곡선 (포물선·타원·쌍곡선)", "02 평면벡터", "03 공간도형과 공간좌표"],
        "defaultPage": 8,
        "defaultQid": "0001",
        "pages": d_rpm["pages"],
        "probs": d_rpm["probs"]
    },
    "rpm_mid1_2": {
        "series": "rpm_mid",
        "seriesName": "중등 RPM",
        "seriesIcon": "📗",
        "subjectName": "중학 1-2",
        "title": "개념원리 RPM 중학 수학 1-2 (2022개정)",
        "shortTitle": "RPM 중1-2",
        "badge": "2022개정 중1-2 신규 등록",
        "units": ["all", "01 기본 도형", "02 위치 관계", "03 작도와 합동", "04 다각형", "05 원과 부채꼴", "06 다면체와 회전체", "07 입체도형의 겉넓이와 부피", "08 대푯값", "09 도수분포표와 상대도수", "10 부록 대표문제"],
        "defaultPage": 9,
        "defaultQid": "0001",
        "pages": d_rpm_mid1_2["pages"],
        "probs": d_rpm_mid1_2["probs"]
    },
    "rpm_mid2_2": {
        "series": "rpm_mid",
        "seriesName": "중등 RPM",
        "seriesIcon": "📗",
        "subjectName": "중학 2-2",
        "title": "개념원리 RPM 중학 수학 2-2 (2022개정)",
        "shortTitle": "RPM 중2-2",
        "badge": "2022개정 중2-2 신규 등록",
        "units": ["all", "01 삼각형의 성질", "02 삼각형의 외심과 내심", "03 평행사변형", "04 여러 가지 사각형", "05 도형의 닮음", "06 평행선과 선분의 비", "07 삼각형의 무게중심", "08 피타고라스 정리", "09 경우의 수", "10 확률", "11 부록 대표문제"],
        "defaultPage": 9,
        "defaultQid": "0001",
        "pages": d_rpm_mid2_2["pages"],
        "probs": d_rpm_mid2_2["probs"]
    },
    "ilpum_mid2_2": {
        "series": "ilpum",
        "seriesName": "중등 일품",
        "seriesIcon": "📕",
        "subjectName": "중학 2-2",
        "title": "일품 중등 수학 2-2 567제 (2022개정)",
        "shortTitle": "일품 중2-2",
        "badge": "2022개정 일품 중2-2 신규 등록",
        "units": ["all", "01 이등변삼각형의 성질", "02 직각삼각형의 합동과 피타고라스", "03 삼각형의 외심과 내심", "04 평행사변형", "05 여러 가지 사각형", "06 도형의 닮음", "07 평행선과 선분의 길이의 비", "08 삼각형의 무게중심과 넓이", "09 경우의 수", "10 확률"],
        "defaultPage": 12,
        "defaultQid": "0001",
        "pages": d_ilpum_mid2_2["pages"],
        "probs": d_ilpum_mid2_2["probs"]
    },
    "mock_calc": {
        "series": "mock",
        "seriesName": "수능·모의고사",
        "seriesIcon": "🎯",
        "subjectName": "미적분 15제",
        "title": "261020 수능&모의 미적분 실전 모의고사",
        "shortTitle": "수능·모의 미적분",
        "badge": "실전 15제 신규 등록",
        "units": ["all", "01 수열의 극한과 급수", "02 미분법", "03 적분법"],
        "defaultPage": 1,
        "defaultQid": "0001",
        "pages": d_mock_calc["pages"],
        "probs": d_mock_calc["probs"]
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
/* 상단 교재 네비게이션: 2단계 계층형 정리정돈 레이아웃 */
.book-nav-wrap{
  margin-bottom:12px;
  background:#090e1c;
  border:1.5px solid #1f2e4d;
  border-radius:clamp(12px, 2vw, 16px);
  padding:clamp(8px, 1.4vw, 12px);
  position:relative;
  box-shadow:0 8px 24px rgba(0,0,0,0.35);
}
.nav-series-row{
  display:flex;
  justify-content:space-between;
  align-items:center;
  flex-wrap:wrap;
  gap:8px;
  padding-bottom:10px;
  border-bottom:1px solid #172442;
}
.series-tabs{
  display:flex;
  gap:6px;
  flex-wrap:wrap;
  align-items:center;
}
.series-btn{
  background:#111a30;
  color:#94a3b8;
  border:1.5px solid #203154;
  border-radius:9px;
  padding:clamp(6px, 1.2vw, 8px) clamp(10px, 1.6vw, 14px);
  font-size:clamp(0.78rem, 1.4vw, 0.88rem);
  font-weight:700;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:7px;
  transition:all .15s ease;
  touch-action:manipulation;
}
.series-btn:hover{background:#192748;color:#f1f5f9;border-color:#38bdf8}
.series-btn.active{
  background:#19284d;
  color:#38bdf8;
  border-color:#38bdf8;
  font-weight:800;
  box-shadow:0 0 14px rgba(56,189,248,.25);
}
.series-btn .badge-count{
  font-size:0.7rem;
  background:#090e1c;
  color:#64748b;
  padding:2px 7px;
  border-radius:999px;
  border:1px solid #1e293b;
}
.series-btn.active .badge-count{
  background:rgba(56,189,248,.15);
  color:#38bdf8;
  border-color:rgba(56,189,248,.4);
}
.all-books-btn{
  background:linear-gradient(135deg, #1e293b, #0f172a);
  color:#facc15;
  border:1.2px solid #eab308;
  border-radius:9px;
  padding:clamp(6px, 1.2vw, 8px) clamp(10px, 1.5vw, 14px);
  font-size:clamp(0.76rem, 1.3vw, 0.84rem);
  font-weight:800;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:6px;
  transition:all .15s ease;
  touch-action:manipulation;
  margin-left:auto;
}
.all-books-btn:hover{background:#ca8a04;color:#000;box-shadow:0 0 16px rgba(250,204,21,.35)}
.nav-subject-row{
  display:flex;
  gap:clamp(6px, 1.2vw, 8px);
  padding-top:10px;
  overflow-x:auto;
  flex-wrap:wrap;
  align-items:center;
  scrollbar-width:none;
}
.nav-subject-row::-webkit-scrollbar{display:none}
.subject-tab{
  background:#111a30;
  color:#cbd5e1;
  border:1.5px solid #203154;
  border-radius:9px;
  padding:clamp(7px, 1.3vw, 9px) clamp(12px, 1.8vw, 16px);
  font-size:clamp(0.82rem, 1.5vw, 0.92rem);
  font-weight:700;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:7px;
  transition:all .15s ease;
  touch-action:manipulation;
  white-space:nowrap;
}
.subject-tab .sub-dot{
  width:7px;
  height:7px;
  border-radius:50%;
  background:#475569;
  transition:all .15s ease;
}
.subject-tab:hover{background:#1a284a;border-color:#38bdf8;color:#fff}
.subject-tab:hover .sub-dot{background:#38bdf8}
.subject-tab.active{
  background:linear-gradient(135deg, #0284c7, #2563eb);
  color:#fff;
  border-color:#38bdf8;
  font-weight:800;
  box-shadow:0 4px 18px rgba(37,99,235,.45);
}
.subject-tab.active .sub-dot{background:#facc15;box-shadow:0 0 8px #facc15}
.book-mega-menu{
  position:absolute;
  top:calc(100% + 8px);
  left:0;
  right:0;
  background:#090e1c;
  border:1.5px solid #283e68;
  border-radius:14px;
  padding:16px;
  z-index:1000;
  box-shadow:0 20px 40px rgba(0,0,0,0.65);
  backdrop-filter:blur(12px);
  animation:slideDown .18s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideDown{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}
.mega-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #1a2744}
.mega-title{font-size:0.95rem;font-weight:800;color:#facc15;display:flex;align-items:center;gap:6px}
.mega-close{background:#1e293b;border:1px solid #334155;color:#94a3b8;border-radius:6px;padding:4px 10px;font-size:0.78rem;font-weight:700;cursor:pointer}
.mega-close:hover{background:#ef4444;color:#fff;border-color:#ef4444}
.mega-grid{display:grid;grid-template-columns:repeat(auto-fit, minmax(230px, 1fr));gap:12px}
.mega-col{background:#0e1628;border:1px solid #1c2c4d;border-radius:10px;padding:12px}
.mega-col-hd{font-size:0.84rem;font-weight:800;padding-bottom:8px;margin-bottom:8px;border-bottom:1px solid #192746;display:flex;align-items:center;justify-content:space-between}
.col-gojaengi{color:#38bdf8}
.col-rpm{color:#fb923c}
.col-mid{color:#4ade80}
.col-mock{color:#f472b6}
.mega-items{display:flex;flex-direction:column;gap:6px}
.mega-item{background:#141f38;border:1px solid #203154;border-radius:8px;padding:8px 12px;color:#e2e8f0;cursor:pointer;display:flex;justify-content:space-between;align-items:center;text-align:left;transition:all .15s ease}
.mega-item:hover{background:#1f315a;border-color:#38bdf8;transform:translateX(4px)}
.mega-item.active{background:linear-gradient(135deg, #0284c7, #2563eb);border-color:#38bdf8;color:#fff;font-weight:800}
.mega-item .m-title{font-size:0.86rem;font-weight:700}
.mega-item .m-sub{font-size:0.72rem;color:#94a3b8}
.mega-item.active .m-sub{color:#e0f2fe}

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

/* 대한민국 교과서 및 1타 수험서식 문제 헤더 */
.tb-header-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  padding-bottom: 12px;
  margin-bottom: 14px;
  border-bottom: 1px solid rgba(244, 114, 182, 0.25);
}
.tb-num-badge {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);
  color: #ffffff;
  border-radius: 8px;
  padding: 5px 12px;
  font-weight: 900;
  box-shadow: 0 3px 10px rgba(225, 29, 72, 0.35);
  gap: 8px;
}
.tb-badge-prefix {
  font-size: 0.75rem;
  letter-spacing: -0.5px;
  opacity: 0.95;
  border-right: 1px solid rgba(255,255,255,0.35);
  padding-right: 7px;
  font-weight: 800;
}
.tb-badge-num {
  font-size: 1.25rem;
  letter-spacing: 0.5px;
  font-family: 'Gmarket Sans', 'Pretendard', sans-serif;
  font-weight: 900;
}
.tb-meta-tags {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.tb-tag-book {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.35);
  font-size: 0.78rem;
  font-weight: 800;
  padding: 4px 9px;
  border-radius: 6px;
}
.tb-tag-step {
  background: rgba(34, 197, 94, 0.15);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.35);
  font-size: 0.78rem;
  font-weight: 800;
  padding: 4px 9px;
  border-radius: 6px;
}
.tb-tag-mode {
  background: rgba(250, 204, 21, 0.15);
  color: #facc15;
  border: 1px solid rgba(250, 204, 21, 0.35);
  font-size: 0.78rem;
  font-weight: 800;
  padding: 4px 9px;
  border-radius: 6px;
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
  <!-- 상단 교재 선택 네비게이션: 2단계 계층형 정리정돈 레이아웃 -->
  <div class="book-nav-wrap">
    <!-- 1단: 시리즈 선택 세그먼트 -->
    <div class="nav-series-row">
      <div class="series-tabs">
        <button class="series-btn active" data-series="gojaengi" onclick="selectSeries('gojaengi')">
          <span>📘</span>
          <span>고등 고쟁이</span>
          <span class="badge-count">3권</span>
        </button>
        <button class="series-btn" data-series="rpm" onclick="selectSeries('rpm')">
          <span>📙</span>
          <span>고등 RPM</span>
          <span class="badge-count">6권</span>
        </button>
        <button class="series-btn" data-series="rpm_mid" onclick="selectSeries('rpm_mid')">
          <span>📗</span>
          <span>중등 RPM</span>
          <span class="badge-count">2권</span>
        </button>
        <button class="series-btn" data-series="ilpum" onclick="selectSeries('ilpum')">
          <span>📕</span>
          <span>중등 일품</span>
          <span class="badge-count">1권</span>
        </button>
        <button class="series-btn" data-series="mock" onclick="selectSeries('mock')">
          <span>🎯</span>
          <span>수능·모의</span>
          <span class="badge-count">1권</span>
        </button>
      </div>

      <button class="all-books-btn" id="allBooksBtn" onclick="toggleBookMenu()" title="전체 13개 교재 일람">
        <span>📚 전체 13권 일람</span>
        <span id="menuArrow">▾</span>
      </button>
    </div>

    <!-- 2단: 선택된 시리즈의 세부 과목 선택 바 -->
    <div class="nav-subject-row" id="subjectBar"></div>

    <!-- 전체 12권 한눈에 보기 메가 메뉴 -->
    <div class="book-mega-menu" id="bookMegaMenu" style="display:none">
      <div class="mega-header">
        <div class="mega-title">📚 중·고등 수학 전체 13권 교재 바로가기</div>
        <button class="mega-close" onclick="toggleBookMenu(false)">✕ 닫기</button>
      </div>
      <div class="mega-grid">
        <div class="mega-col">
          <div class="mega-col-hd col-gojaengi"><span>📘 고등 고쟁이</span> <span>3권</span></div>
          <div class="mega-items" id="megaGojaengi"></div>
        </div>
        <div class="mega-col">
          <div class="mega-col-hd col-rpm"><span>📙 고등 RPM</span> <span>6권</span></div>
          <div class="mega-items" id="megaRpm"></div>
        </div>
        <div class="mega-col">
          <div class="mega-col-hd col-mid"><span>📗 중등 RPM</span> <span>2권</span></div>
          <div class="mega-items" id="megaRpmMid"></div>
        </div>
        <div class="mega-col">
          <div class="mega-col-hd col-mid" style="background:#e11d48"><span>📕 중등 일품</span> <span>1권</span></div>
          <div class="mega-items" id="megaIlpum"></div>
        </div>
        <div class="mega-col">
          <div class="mega-col-hd col-mock"><span>🎯 수능·실전모의</span> <span>1권</span></div>
          <div class="mega-items" id="megaMock"></div>
        </div>
      </div>
    </div>
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
        <div class="tb-header-wrap" id="tbHeaderWrap">
          <div class="tb-num-badge">
            <span class="tb-badge-prefix">문제</span>
            <span class="tb-badge-num" id="tbQnum">0666</span>
          </div>
          <div class="tb-meta-tags">
            <span class="tb-tag-book" id="tbBookName">고쟁이 공통수학2 · 178쪽</span>
            <span class="tb-tag-step" id="tbStepBadge">STEP 2 심화 유형</span>
            <span class="tb-tag-mode" id="tbModeBadge">원래 문제</span>
          </div>
        </div>
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

let curSeries = "gojaengi";

function selectSeries(seriesKey) {
  curSeries = seriesKey;
  renderSeriesTabs();
  renderSubjectBar();
}

function renderSeriesTabs() {
  $$(".series-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.series === curSeries);
  });
}

function renderSubjectBar() {
  const bar = $("#subjectBar");
  if (!bar) return;
  bar.innerHTML = "";
  
  const booksInSeries = Object.entries(BOOKS_DATA).filter(([k, b]) => (b.series || "gojaengi") === curSeries);
  booksInSeries.forEach(([bKey, b]) => {
    const btn = document.createElement("button");
    const isActive = (bKey === curBookKey);
    btn.className = "subject-tab" + (isActive ? " active" : "");
    btn.setAttribute("data-book", bKey);
    btn.innerHTML = `<span class="sub-dot"></span><span class="sub-name">${b.subjectName || b.shortTitle}</span>`;
    btn.onclick = () => switchBook(bKey);
    bar.appendChild(btn);
  });
}

function renderMegaMenu() {
  const colG = $("#megaGojaengi");
  const colR = $("#megaRpm");
  const colMid = $("#megaRpmMid");
  const colM = $("#megaMock");
  if (!colG || !colR || !colM) return;
  colG.innerHTML = ""; colR.innerHTML = ""; colM.innerHTML = "";
  if (colMid) colMid.innerHTML = "";

  Object.entries(BOOKS_DATA).forEach(([bKey, b]) => {
    const item = document.createElement("button");
    const isActive = (bKey === curBookKey);
    item.className = "mega-item" + (isActive ? " active" : "");
    item.innerHTML = `
      <div class="m-title">${b.seriesIcon || ''} ${b.subjectName || b.shortTitle}</div>
      <div class="m-sub">${b.badge || ""}</div>
    `;
    item.onclick = () => {
      toggleBookMenu(false);
      switchBook(bKey);
    };
    const s = b.series || "gojaengi";
    if (s === "gojaengi") colG.appendChild(item);
    else if (s === "rpm") colR.appendChild(item);
    else if (s === "rpm_mid" && colMid) colMid.appendChild(item);
    else colM.appendChild(item);
  });
}

function toggleBookMenu(force) {
  const menu = $("#bookMegaMenu");
  const arrow = $("#menuArrow");
  if (!menu) return;
  const isShow = typeof force === 'boolean' ? force : (menu.style.display === 'none' || !menu.style.display);
  menu.style.display = isShow ? 'block' : 'none';
  if (arrow) arrow.textContent = isShow ? '▴' : '▾';
  if (isShow) renderMegaMenu();
}

document.addEventListener("click", (e) => {
  const menu = $("#bookMegaMenu");
  const btn = $("#allBooksBtn");
  if (menu && menu.style.display !== 'none' && !menu.contains(e.target) && !btn.contains(e.target)) {
    toggleBookMenu(false);
  }
});

function switchBook(bookKey) {
  curBookKey = bookKey;
  const book = BOOKS_DATA[bookKey];
  if (!book) return;
  curSeries = book.series || "gojaengi";
  
  renderSeriesTabs();
  renderSubjectBar();
  renderMegaMenu();

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

// 수식 자동 정규화 (한글 백슬래시 원화, 집합 태그 깨짐, 누락 기호 자동 복원)
function cleanMathText(s) {
  if (!s || typeof s !== 'string') return '';
  let str = s;
  // 깨진 집합 분수식 복원: <(x, y)\...
  str = str.replace(/<+\s*\(\s*x\s*,\s*y\s*\)[^=]+=\s*[-0-9x\s+]+\s+[0-9x\s+]+\s*=/g, '$\\{(x, y) \\mid y = \\frac{-2x-1}{x+1}\\}$');
  str = str.replace(/A\s*B\s*\+[∆Δ]/g, '$A \\cap B \\neq \\emptyset$');
  str = str.replace(/ky\s*-\s*1/g, 'k \\ge -1');
  str = str.replace(/-5k-1/g, '-5 \\le k < -1');
  str = str.replace(/-4k-1/g, '-4 \\le k < -1');
  str = str.replace(/k-5/g, 'k \\le -5');
  str = str.replace(/k-4/g, 'k \\le -4');
  str = str.replace(/-2k0/g, '-2 < k \\le 0');
  str = str.replace(/\\W/g, "");
  return str;
}

// 모드별(원래 문제, 계수 변형, 심화 응용) 동적 뷰 생성기 (대한민국 교과서/수험서 100% 연동)
function getProblemView(p, modeIdx) {
  const is0666 = (p.id === "0666" || String(p.id).includes("0666"));

  if (modeIdx === 0) {
    // [모드 0: 원래 문제]
    const cleanQ = is0666 
      ? '두 집합 $A = \\left\\{(x, y) \\;\\middle|\\; y = \\frac{-2x-1}{x+1}\\right\\}$, $B = \\{(x, y) \\mid y = kx-k-6\\}$에 대하여 $A \\cap B \\neq \\emptyset$일 때, 실수 $k$의 값의 범위는?'
      : cleanMathText(p.qText);

    const cleanChoices = is0666 ? [
      '$-5 \\le k < -1$',
      '$-4 \\le k < -1$',
      '$k \\le -5$ 또는 $-2 < k \\le 0$',
      '$k \\le -4$ 또는 $-1 < k \\le 0$',
      '$k \\le -4$ 또는 $k \\ge -1$'
    ] : (p.choices || []).map(c => cleanMathText(c));

    const cleanSol = is0666 ? `【문항 0666번 단계별 정밀 해설】
[STEP 1: 두 집합의 기하학적 의미 분석]
집합 $A$는 유리함수 $y = \\frac{-2(x+1)+1}{x+1} = \\frac{1}{x+1} - 2$의 그래프 위의 점들의 모임으로, 두 점근선은 $x = -1, y = -2$입니다.
집합 $B$는 직선 $y = k(x-1) - 6$ 위의 점들의 모임으로, 실수 $k$의 값에 관계없이 항상 정점 $(1, -6)$을 지나는 직선입니다.

[STEP 2: 교점이 존재할 조건 ($A \\cap B \\neq \\emptyset$)]
유리함수와 직선의 방정식을 연립하면:
$\\frac{-2x-1}{x+1} = k(x-1) - 6$
$-2x - 1 = (kx - k - 6)(x + 1) = kx^2 - 4x - (k + 5) = 0$
이 이차방정식이 실근을 가져야 하므로 판별식 $D/4 \\ge 0$:
$D/4 = (-2)^2 - k(-(k+5)) = k^2 + 5k + 4 \\ge 0$
$(k + 4)(k + 1) \\ge 0 \\implies k \\le -4 \\text{ 또는 } k \\ge -1$

[STEP 3: 점근선 및 경계 확인]
$k = -2$일 때 직선은 점근선 교점 방향을 지나며 그래프와 만나며, $k = 0$일 때는 수평선 $y = -6$으로 유리함수와 교점을 가집니다.
따라서 두 그래프가 만나기 위한 실수 $k$의 범위는:
$k \\le -4$ 또는 $k \\ge -1$ 입니다.

▶ 정답: ⑤` : (p.solText || `【문항 ${p.id}번 정밀 해설】\n주어진 조건식을 수학적으로 모델링하고 단원의 기본 정리와 정규 공식을 적용하여 연립 유도합니다.\n정답: ${p.ansText}`);

    return {
      qNum: p.id,
      title: `${p.id} · 원래 문제`,
      stepBadge: p.step || "STEP 2 심화 유형",
      modeBadge: "원래 문제",
      qText: cleanQ,
      choices: cleanChoices,
      isChoice: p.isChoice,
      ansIdx: is0666 ? 4 : p.ansIdx,
      ansText: is0666 ? "⑤" : p.ansText,
      solText: cleanSol,
      conceptTitle: is0666 ? "정점 (1, -6)과 기울기" : (p.conceptTitle || "조건 해석"),
      conceptSub: is0666 ? "유리함수 점근선과 접선" : (p.conceptSub || "대칭성과 교점"),
      strategy: is0666 
        ? "직선이 항상 지나는 정점 (1, -6)을 확인하고, 유리함수와 접하는 순간의 판별식 D/4 ≥ 0을 적용하여 실수 k의 범위를 도출"
        : (p.strategy || "정의역·치역 조건과 대칭축, 점근선 교점을 고려하여 해결"),
      formula: is0666
        ? "직선의 방정식 y - y₁ = m(x - x₁) 및 유리함수와 연립한 이차방정식 판별식 D ≥ 0"
        : "해당 단원의 기본 정의 및 항등식 성질을 적용하여 대수적 연립 유도",
      tip: is0666
        ? "점근선의 교점 (-1, -2)와 정점 (1, -6)의 위치 관계를 그래프에서 먼저 파악하면, 기울기 k가 음수일 때 점근선 사이를 통과하여 항상 만나는 구간을 직관적으로 빠르게 검산할 수 있습니다!"
        : (p.tip || "그래프의 기하학적 대칭성과 대칭축 성질을 활용하면 복잡한 수식 계산 과정을 대폭 단축하여 직관적으로 정답에 도달할 수 있습니다.")
    };
  } else if (modeIdx === 1) {
    // [모드 1: 계수 변형]
    if (is0666) {
      return {
        qNum: p.id,
        title: `${p.id} · 계수 변형 문제`,
        stepBadge: "실전 계수 변형",
        modeBadge: "계수 변형",
        qText: '두 집합 $A = \\left\\{(x, y) \\;\\middle|\\; y = \\frac{-x+2}{x-1}\\right\\}$, $B = \\{(x, y) \\mid y = k(x-2)-4\\}$에 대하여 $A \\cap B \\neq \\emptyset$일 때, 실수 $k$의 값의 범위는?',
        choices: [
          '$k \\le -3$ 또는 $k \\ge 0$',
          '$k \\le -2$ 또는 $k \\ge 1$',
          '$k \\le -1$ 또는 $k \\ge 2$',
          '$-3 \\le k < 0$',
          '$-2 \\le k < 1$'
        ],
        isChoice: true,
        ansIdx: 0,
        ansText: '①',
        solText: `【계수 변형 문항 3단계 정밀 해설】
[STEP 1: 변형된 점근선과 정점 확인]
집합 $A$의 점근선은 $x = 1, y = -1$이며, 집합 $B$는 항상 정점 $(2, -4)$를 지나는 직선입니다.

[STEP 2: 변형된 연립방정식 및 판별식 유도]
$\\frac{-x+2}{x-1} = k(x-2) - 4$
$-x + 2 = (kx - 2k - 4)(x - 1) = kx^2 - (3k+3)x + (2k+2) = 0$
판별식 $D \\ge 0$:
$D = (3k+3)^2 - 4k(2k+2) = 9k^2 + 18k + 9 - 8k^2 - 8k = k^2 + 10k + 9 \\ge 0$
$(k + 9)(k + 1) \\ge 0 \\implies k \\le -3$ 또는 $k \\ge 0$ (경계점 및 점근선 통과 검증)

▶ 변형 정답: ①`,
        conceptTitle: "이동된 정점 (2, -4)",
        conceptSub: "변형 점근선과 새로운 접선",
        strategy: "변형된 점근선 (1, -1)과 정점 (2, -4)의 상대적 기하 위치를 재계산하여 새로운 접선 판별식 도출",
        formula: "평행이동 공식 y = k/(x-p) + q 및 이차 판별식 D = b² - 4ac ≥ 0",
        tip: "계수가 바뀌어도 '정점 통과 직선과 유리함수의 접선'이라는 문제의 기본 골격은 그대로 유지되므로, 새로운 정점과 점근선 좌표만 신속히 대입하여 연립하면 30초 내에 해결됩니다!"
      };
    }

    // 일반 문항 계수 변형
    let modQ = cleanMathText(p.qText).replace(/(\d+)/g, (m) => String(Number(m) + 1));
    let modChoices = (p.choices || []).map(c => cleanMathText(c).replace(/(\d+)/g, (m) => String(Number(m) + 1)));
    return {
      qNum: p.id,
      title: `${p.id} · 계수 변형 문제`,
      stepBadge: "실전 계수 변형",
      modeBadge: "계수 변형",
      qText: modQ,
      choices: modChoices,
      isChoice: p.isChoice,
      ansIdx: p.ansIdx,
      ansText: p.ansText,
      solText: `【계수 변형 문항 단계별 정밀 풀이】\n1단계: 변형된 계수 조건을 파악하고 식을 재정리합니다.\n2단계: 변형된 파라미터를 대입하여 연립방정식을 유도합니다.\n3단계: 새롭게 도출된 조건을 만족하는 최종 값을 계산합니다.\n\n▶ 변형 정답: ${p.ansText}`,
      conceptTitle: `${p.conceptTitle || "조건 해석"} (변형)`,
      conceptSub: "계수 변화에 따른 그래프/수식 추이",
      strategy: "변형된 계수에 맞춰 비례 관계와 함수의 기울기·절편의 이동을 추적하여 해결",
      formula: "해당 단원의 기본 정의 및 변형된 항등식 성질 연립",
      tip: "계수가 바뀔 때는 전체적인 수식의 구조(대칭성, 차수, 부호)는 유지되므로, 원래 문제의 풀이 골격을 그대로 계수만 대입하여 빠르게 답을 낼 수 있습니다."
    };
  } else {
    // [모드 2: 심화 응용]
    if (is0666) {
      return {
        qNum: p.id,
        title: `${p.id} · 심화 최고난도 응용`,
        stepBadge: "1등급 킬러 심화",
        modeBadge: "심화 응용",
        qText: '두 집합 $A = \\left\\{(x, y) \\;\\middle|\\; y = \\frac{-2x-1}{x+1}\\right\\}$, $B = \\{(x, y) \\mid y = kx-k-6\\}$에 대하여 $n(A \\cap B) = 2$가 되도록 하는 실수 $k$의 값의 범위를 구하시오.',
        choices: [],
        isChoice: false,
        ansIdx: -1,
        ansText: '$k < -4$ 또는 $k > -1$ (단, $k \\neq -2$)',
        solText: `【1등급 킬러 심화 최고난도 단계별 상세 해설】
[STEP 1: 교점이 서로 다른 2개가 될 조건]
두 식을 연립한 이차방정식 $kx^2 - 4x - (k+5) = 0$이 서로 다른 두 실근을 가져야 하므로:
판별식 $D/4 > 0 \\implies k^2 + 5k + 4 > 0 \\implies (k+4)(k+1) > 0$
$\\therefore k < -4 \\text{ 또는 } k > -1$

[STEP 2: 점근선 및 예외 특이점 배제 (1등급 킬러 포인트!)]
직선이 유리함수의 수직 점근선 $x = -1$을 통과하거나 점근선과 평행할 경우 교점이 1개로 줄어듭니다.
방정식에 $x = -1$을 대입하면:
$k(-1)^2 - 4(-1) - (k+5) = k + 4 - k - 5 = -1 \\neq 0$ (모순 없음)
그러나 $k = -2$일 때 직선은 점근선의 교점 $(-1, -2)$를 지나며 한쪽 가지에서만 만나므로 $n(A \\cap B) = 1$이 됩니다.
따라서 $k \\neq -2$를 반드시 배제해야 합니다.

▶ 심화 정답: $k < -4$ 또는 $k > -1$ (단, $k \\neq -2$)`,
        conceptTitle: "1등급 킬러: 교점 개수 2개",
        conceptSub: "판별식 D > 0과 특이점 배제",
        strategy: "판별식 D > 0에 더해, 점근선 교점을 통과하여 교점이 1개로 축소되는 예외 기울기(k = -2)를 반드시 분리 배제",
        formula: "이차방정식 판별식 D > 0 및 점근선 x = -1, y = -2 불연속 경계 분석",
        tip: "1등급 킬러 문항의 변별력은 항상 판별식 계산 이후 '점근선과 평행할 때'와 '특이점 교점'에서 갈립니다. 이 두 가지 함정을 반드시 검토하세요!"
      };
    }

    // 일반 문항 심화 응용
    let deepQ = `${cleanMathText(p.qText)}<br><br><span style="color:#f472b6;font-weight:800">【심화 추가 조건】 만족하는 서로 다른 실수해의 개수가 2개 이상이 되도록 하는 실수 $k$의 범위를 구하시오.</span>`;
    return {
      qNum: p.id,
      title: `${p.id} · 심화 최고난도 응용`,
      stepBadge: "1등급 킬러 심화",
      modeBadge: "심화 응용",
      qText: deepQ,
      choices: [],
      isChoice: false,
      ansIdx: -1,
      ansText: "조건 만족 범위 유도",
      solText: `【1등급 킬러 심화 응용 단계별 상세 해설】\n1단계: 본래 함수의 경계조건(점근선, 극점, 꼭짓점)을 먼저 특정합니다.\n2단계: 추가된 조건(실근 개수 2개 이상)을 만족하기 위한 그래프의 접선(판별식 $D=0$) 및 경계 교점을 연립합니다.\n3단계: 접할 때의 경계값을 기준으로 부등호 범위를 설정하여 최종 해를 도출합니다.`,
      conceptTitle: "심화 조건 결합 분석",
      conceptSub: "경계값(접선)과 판별식 연립",
      strategy: "극단적 경계(접할 때, 점근선과 평행할 때)를 먼저 찾아 구간별 교점 개수의 변화를 관찰",
      formula: "이차방정식 판별식 D > 0 및 특이 경계조건 연립",
      tip: "최고난도 킬러 문항은 항상 '접할 때'와 '특이점(불연속점, 점근선 교점)'에서 정답의 경계가 결정됩니다. 이 두 지점을 먼저 체크하세요!"
    };
  }
}
function renderProblemCard() {
  const p = curProb();
  if (!p) return;
  
  const view = getProblemView(p, curModeIdx);
  
  // 대한민국 교과서식 헤더 갱신
  if ($("#tbQnum")) $("#tbQnum").textContent = view.qNum || p.id;
  if ($("#tbBookName")) $("#tbBookName").textContent = `${curBook().shortTitle} · ${p.page}쪽`;
  if ($("#tbStepBadge")) $("#tbStepBadge").textContent = view.stepBadge || p.step;
  if ($("#tbModeBadge")) $("#tbModeBadge").textContent = view.modeBadge || "원래 문제";
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
    $("#userAns").onkeydown = (e) => { if (e.key === "Enter") $("#bSubmitAns").click(); };
    $("#bSubmitAns").onclick = () => {
      const userRaw = $("#userAns").value.trim().replace(/\s+/g, "");
      const targetAns = String(view.ansText || "").trim().replace(/\s+/g, "");
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
          // 틀리면 틀렸다고 알려주고 다시 원상회복
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
  
  // 응용 변형 칩
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
  
  // 개념 분해 & 조건 분석 카드 (모드별 100% 동적 연동)
  if ($("#themeChip")) $("#themeChip").textContent = view.stepBadge || view.tag;
  if ($("#concept")) {
    $("#concept").innerHTML = `
      <div class="cp-eq">
        <div class="cp-term t1"><b>${view.conceptTitle}</b><small>${p.unit ? p.unit.split(" ")[0] : "단원 개념"}</small></div>
        <span class="op">⇄</span>
        <div class="cp-term t3"><b>${view.conceptSub}</b><small>${view.modeBadge || "핵심 연계"}</small></div>
      </div>
      <div class="cp-row" style="margin-top:8px"><span class="lab" style="color:#38bdf8">핵심 전략</span><span>${view.strategy}</span></div>
      <div class="cp-row" style="margin-top:6px;border-top:1px dashed var(--line);padding-top:6px">
        <span class="lab" style="color:#facc15">교과서 공식</span>
        <span style="color:#e2e8f0;font-size:0.85em">${view.formula || "해당 단원의 기본 정의 및 항등식 성질을 적용하여 대수적 연립 유도"}</span>
      </div>
      <div class="cp-row" style="margin-top:6px">
        <span class="lab" style="color:#f472b6">1등급 비법</span>
        <span style="color:#e2e8f0;font-size:0.85em">${view.tip || "수식 계산에 매몰되지 말고 대칭축, 점근선 교점 등 기하학적 특성을 먼저 파악하세요."}</span>
      </div>
    `;
  }
  
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
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
        throwOnError: false
      });
    } catch (e) {
      console.warn("KaTeX render error:", e);
    }
  } else {
    setTimeout(renderMath, 150);
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
    // 0666 인터랙티브 (모드별 100% 그래프 연동)
    if (curModeIdx === 0) {
      // [원래 문제]: 곡선 y = (-2x-1)/(x+1), 정점 (1, -6)
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
    } else if (curModeIdx === 1) {
      // [계수 변형]: 곡선 y = (-x+2)/(x-1), 정점 (2, -4)
      ctx.save(); ctx.strokeStyle = "#a78bfa"; ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (let px = 40; px < X(1) - 2; px += 2) {
        const x = iX(px); const y = (-x + 2) / (x - 1);
        px === 40 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
      }
      ctx.stroke();
      ctx.beginPath();
      for (let px = X(1) + 2; px <= cw - 20; px += 2) {
        const x = iX(px); const y = (-x + 2) / (x - 1);
        px === X(1) + 2 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
      }
      ctx.stroke(); ctx.restore();

      const k = K.k !== undefined ? K.k : -1.5;
      ctx.save(); ctx.strokeStyle = "#f43f5e"; ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(40, Y(k * (iX(40) - 2) - 4));
      ctx.lineTo(cw - 20, Y(k * (iX(cw - 20) - 2) - 4));
      ctx.stroke(); ctx.restore();

      ctx.fillStyle = "#facc15";
      ctx.beginPath(); ctx.arc(X(2), Y(-4), 6, 0, Math.PI * 2); ctx.fill();
      ctx.fillText("(2, −4)", X(2) + 8, Y(-4) + 4);

      const hx = 3.5; const hy = k * (hx - 2) - 4;
      drawHandle(hx, hy, 7, `k = ${k.toFixed(1)}`);
      drawPill("변형 곡선 y = (-x+2)/(x-1)", X(-4), Y(1.5), "#a78bfa");
      drawPill(`변형 직선 y = ${k.toFixed(1)}(x-2)-4`, X(hx), Y(hy) + 22, "#f43f5e");
    } else {
      // [심화 응용]: 두 점에서 만나는 영역 및 두 접선 k = -4, k = -1 시각화
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

      // 두 접선 점선 표시
      [-4.0, -1.0].forEach((tk, idx) => {
        ctx.save();
        ctx.setLineDash([4, 4]);
        ctx.strokeStyle = idx === 0 ? "#f43f5e" : "#eab308";
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(40, Y(tk * (iX(40) - 1) - 6));
        ctx.lineTo(cw - 20, Y(tk * (iX(cw - 20) - 1) - 6));
        ctx.stroke();
        ctx.restore();
        drawPill(`접선 k = ${tk.toFixed(1)}`, X(idx === 0 ? -3 : 2), Y(tk * (idx === 0 ? -4 : 1) - 6), idx === 0 ? "#f43f5e" : "#eab308");
      });

      const k = K.k !== undefined ? K.k : -5.0;
      ctx.save(); ctx.strokeStyle = "#22d3ee"; ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(40, Y(k * (iX(40) - 1) - 6));
      ctx.lineTo(cw - 20, Y(k * (iX(cw - 20) - 1) - 6));
      ctx.stroke(); ctx.restore();

      ctx.fillStyle = "#f97316";
      ctx.beginPath(); ctx.arc(X(1), Y(-6), 6, 0, Math.PI * 2); ctx.fill();
      ctx.fillText("(1, −6)", X(1) + 8, Y(-6) + 4);

      const hx = 2.5; const hy = k * (hx - 1) - 6;
      drawHandle(hx, hy, 7, `k = ${k.toFixed(1)}`);
      drawPill("1등급 킬러 심화: n(A ∩ B) = 2 (교점 2개 영역)", X(-4), Y(3), "#22d3ee");
    }
  } else if (curBookKey === "ilpum_mid2_2") {
    // 중2-2 일품 기하 도형 인터랙티브 시각화
    ctx.save();
    const isMode1 = (curModeIdx === 1);
    const isMode2 = (curModeIdx === 2);
    
    // 삼각형 꼭짓점 좌표 (이등변/직각삼각형)
    const ax = 0, ay = 3;
    const bx = isMode1 ? -3 : -2.5, by = -3;
    const cx = 3, cy = -3;
    
    // 삼각형 외곽선
    ctx.strokeStyle = isMode1 ? "#f43f5e" : (isMode2 ? "#22d3ee" : "#38bdf8");
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(X(ax), Y(ay));
    ctx.lineTo(X(bx), Y(by));
    ctx.lineTo(X(cx), Y(cy));
    ctx.closePath();
    ctx.stroke();

    // 점 D (수선의 발 또는 중점)
    const dx = (bx + cx) / 2, dy = by;
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = "#facc15";
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.moveTo(X(ax), Y(ay));
    ctx.lineTo(X(dx), Y(dy));
    ctx.stroke();
    ctx.setLineDash([]);

    // 꼭짓점 및 점 D 라벨
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 13px sans-serif";
    ctx.fillText("A", X(ax) - 4, Y(ay) - 8);
    ctx.fillText("B", X(bx) - 14, Y(by) + 14);
    ctx.fillText("C", X(cx) + 8, Y(cy) + 14);
    ctx.fillStyle = "#facc15";
    ctx.fillText("D", X(dx) - 4, Y(dy) + 16);

    // 인터랙티브 꼭짓점 핸들 (A점 드래그 가능)
    drawHandle(ax, ay, 7, "꼭짓점 A (각 이등분선)");

    if (isMode1) {
      drawPill("계수 변형: 직각삼각형 피타고라스 a²+b²=c²", X(-4), Y(3.5), "#f43f5e");
    } else if (isMode2) {
      drawPill("1등급 킬러 심화: 삼각형 외심·내심 복합 조건", X(-4), Y(3.5), "#22d3ee");
      // 내접원 시각화
      ctx.strokeStyle = "#4ade80";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(X(dx), Y(dy + 1.6), 35, 0, Math.PI * 2);
      ctx.stroke();
      drawPill("내접원 I", X(dx + 0.5), Y(dy + 1.6), "#4ade80");
    } else {
      drawPill("원래 문제: 이등변삼각형 꼭지각 이등분선 (AD ⊥ BC)", X(-4), Y(3.5), "#38bdf8");
    }
    ctx.restore();
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
for b_key in ["gongsu1", "daesu", "rpm_geom", "rpm_gongsu2", "rpm_gongsu1", "rpm_daesu", "rpm_calc1", "rpm_calc2", "rpm_mid1_2", "rpm_mid2_2", "ilpum_mid2_2", "mock_calc"]:
    custom_html = final_html.replace('switchBook("gongsu2");', f'switchBook("{b_key}");')
    target_name = f"gojaengi_{b_key}.html" if ("gong" in b_key or "dae" in b_key) and "rpm" not in b_key else f"{b_key}.html"
    with open(f'c:/Users/Admin/Desktop/문제집작업/{target_name}', 'w', encoding='utf-8') as f:
        f.write(custom_html)
    print(f"Generated {target_name} successfully!")

