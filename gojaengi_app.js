/* 고쟁이 135쪽~194쪽 통합 앱 로직 & 인터랙티브 캔버스 렌더링 엔진 */

// 핵심 유틸리티 함수
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);
const clamp = (v, l, h) => Math.max(l, Math.min(h, v));

let currentUnit = "all";
let currentPage = 178; // 기본 178쪽으로 시작
let currentQid = "0666";
let showSol = false;
let showAlt = false;
let solvedMap = {};
let dragTarget = null;
let animFrameId = null;

let cv, ctx;
let cw = 600, chh = 420;
let view = { x0: -6, x1: 6, y0: -8, y1: 4 };

// 좌표 변환 함수
const X = x => 40 + (x - view.x0) / (view.x1 - view.x0) * (cw - 60);
const Y = y => 20 + (view.y1 - y) / (view.y1 - view.y0) * (chh - 50);
const iX = px => view.x0 + (px - 40) / (cw - 60) * (view.x1 - view.x0);
const iY = py => view.y1 - (py - 20) / (chh - 50) * (view.y1 - view.y0);

function getCurProblem() {
  return GOJAENGI_DB[currentQid] || GOJAENGI_DB["0666"];
}

/* ---------- 1. 페이지 & 문제 네비게이션 렌더링 ---------- */

function renderPageBar() {
  const bar = $("#pageList");
  if (!bar) return;
  bar.innerHTML = "";

  const filteredPages = GOJAENGI_PAGES.filter(p => {
    if (currentUnit === "unit1") return p.page <= 164;
    if (currentUnit === "unit2") return p.page >= 165;
    return true;
  });

  filteredPages.forEach(p => {
    const btn = document.createElement("button");
    const isCur = p.page === currentPage;
    const isAllSolved = p.qids.every(qid => solvedMap[qid]);

    btn.className = `pg-btn ${isCur ? "active" : ""} ${isAllSolved ? "all-ok" : ""}`;
    btn.innerHTML = `${p.page}쪽 <small>${p.qids.length}문항</small>`;
    btn.onclick = () => selectPage(p.page);
    bar.appendChild(btn);

    // 현재 페이지가 활성화되면 스크롤 위치 맞추기
    if (isCur) {
      setTimeout(() => {
        btn.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      }, 50);
    }
  });
}

function renderQidBar() {
  const bar = $("#qidList");
  if (!bar) return;
  bar.innerHTML = "";

  const pageData = GOJAENGI_PAGES.find(p => p.page === currentPage);
  if (!pageData) return;

  pageData.qids.forEach(qid => {
    const btn = document.createElement("button");
    const isCur = qid === currentQid;
    const isSolved = solvedMap[qid];

    btn.className = `tb ${isCur ? "on" : ""} ${isSolved ? "ok" : ""}`;
    btn.textContent = (isSolved ? "✔ " : "") + qid;
    btn.onclick = () => selectProblem(qid);
    bar.appendChild(btn);
  });
}

function selectPage(pgNum) {
  currentPage = pgNum;
  const pageData = GOJAENGI_PAGES.find(p => p.page === pgNum);
  if (pageData && pageData.qids.length > 0) {
    currentQid = pageData.qids[0];
  }
  showSol = false;
  showAlt = false;
  renderPageBar();
  renderQidBar();
  renderProblemView();
}

function selectProblem(qid) {
  currentQid = qid;
  const prob = GOJAENGI_DB[qid];
  if (prob && prob.page !== currentPage) {
    currentPage = prob.page;
    renderPageBar();
  }
  showSol = false;
  showAlt = false;
  renderQidBar();
  renderProblemView();
}

/* ---------- 2. 문제 및 선택지/풀이 뷰 렌더링 ---------- */

function renderProblemView() {
  const prob = getCurProblem();
  const pageData = GOJAENGI_PAGES.find(p => p.page === currentPage);

  // 헤더 정보
  const pBadge = $("#pageBadge");
  if (pBadge) pBadge.textContent = `${currentPage}쪽 · ${pageData ? pageData.step : ""}`;
  
  const qTitle = $("#qidTitle");
  if (qTitle) {
    qTitle.innerHTML = `${prob.id} · <span style="color:#facc15">${pageData ? pageData.unit : ""}</span>` +
      (prob.tag ? ` <span class="tag">${prob.tag}</span>` : "");
  }

  // 문제 텍스트
  const qText = $("#qText");
  if (qText) qText.innerHTML = prob.q;

  // 선택지
  const choiceBox = $("#choicesBox");
  const inputBox = $("#inputAnsBox");
  const fbMsg = $("#feedbackMsg");
  if (fbMsg) fbMsg.innerHTML = "";

  if (prob.isInput || !prob.choices) {
    if (choiceBox) choiceBox.style.display = "none";
    if (inputBox) {
      inputBox.style.display = "flex";
      $("#txtUserAns").value = "";
      $("#btnCheckInput").onclick = () => {
        const uAns = $("#txtUserAns").value.trim();
        const expected = String(prob.correctVal || prob.ansStr || "").trim();
        if (uAns === expected || (expected.includes("/") && uAns.replace(/\s+/g, '') === expected)) {
          fbMsg.innerHTML = `<span style="color:#4ade80;font-weight:800">🎉 정답입니다! 정답: ${expected}</span>`;
          solvedMap[currentQid] = true;
          renderPageBar();
          renderQidBar();
        } else {
          fbMsg.innerHTML = `<span style="color:#fb7185;font-weight:800">다시 계산해 보세요. (힌트: [풀이 보기]를 확인하세요)</span>`;
        }
      };
    }
  } else {
    if (inputBox) inputBox.style.display = "none";
    if (choiceBox) {
      choiceBox.style.display = "grid";
      choiceBox.innerHTML = "";

      prob.choices.forEach((cText, idx) => {
        const btn = document.createElement("button");
        btn.className = "ch";
        btn.innerHTML = `${"①②③④⑤"[idx]} ${cText}`;
        btn.onclick = () => {
          if (idx === prob.ansIdx) {
            btn.classList.add("good");
            solvedMap[currentQid] = true;
            renderPageBar();
            renderQidBar();
            fbMsg.innerHTML = `<span style="color:#4ade80;font-weight:800">🎉 정답입니다! [풀이 보기]로 과정을 확인해 보세요.</span>`;
          } else {
            btn.classList.add("bad");
            fbMsg.innerHTML = `<span style="color:#fb7185">다시 풀어보세요! 핵심 개념과 대칭성을 점검하세요.</span>`;
          }
        };
        choiceBox.appendChild(btn);
      });
    }
  }

  // 풀이 카드
  const solCard = $("#solCard");
  const btnSol = $("#btnToggleSol");
  if (solCard) solCard.style.display = showSol ? "block" : "none";
  if (btnSol) btnSol.textContent = showSol ? "풀이 접기" : "풀이 보기";
  if (showSol && $("#solBody")) {
    $("#solBody").innerHTML = prob.sol.map((line, i) => `<div style="margin:6px 0">${"①②③④⑤⑥"[i] || "•"} ${line}</div>`).join("") +
      `<div class="big ok" style="margin-top:12px">정답: ${prob.ansStr}</div>`;
  }

  // 다른 풀이 카드
  const altCard = $("#altCard");
  const btnAlt = $("#btnToggleAlt");
  if (altCard) altCard.style.display = showAlt ? "block" : "none";
  if (btnAlt) btnAlt.textContent = showAlt ? "다른 풀이 접기" : "다른 풀이";
  if (showAlt && $("#altBody")) {
    $("#altBody").innerHTML = `<div class="altt">💡 실전 시험 직관 TIP</div>` +
      `<div style="line-height:1.75">${prob.tip || "대칭성과 점근선 특성을 활용하면 빠르고 정확하게 풀 수 있습니다."}</div>`;
  }

  // 핵심 개념 카드
  const concCard = $("#conceptCard");
  if (concCard) {
    concCard.innerHTML = `
      <div style="font-weight:800;color:#facc15;margin-bottom:6px">${prob.conceptTitle || "유형 핵심 도구"}</div>
      <div style="font-size:13.5px;color:#cbd5e1;line-height:1.65">
        • <b>대칭성 활용</b>: y = x 대칭 또는 점근선의 교점 대칭 관계를 먼저 확인합니다.<br>
        • <b>판별식과 위치 관계</b>: D > 0(2점), D = 0(접함), D < 0(안 만남).<br>
        • <b>곡선 위의 점</b>: 대칭점을 (a, b)와 (b, a)로 세팅하여 미지수를 줄입니다.
      </div>
    `;
  }

  // 힌트 텍스트
  const cHint = $("#canvasHint");
  if (cHint) {
    if (currentQid === "0666") {
      cHint.innerHTML = `노란 점을 위아래로 끌어 <b>직선의 기울기 k</b>를 조절해 보세요. 접선(k=−4, −1)과 교점 개수를 실시간 관찰할 수 있습니다.`;
    } else if (currentQid === "0667") {
      cHint.innerHTML = `곡선 위의 <b>노란 점 A</b>를 드래그해 보세요. y = x 대칭점 B와 선분 AB의 길이가 실시간으로 계산됩니다.`;
    } else if (currentQid === "0668") {
      cHint.innerHTML = `<b>직선 x + y = 8</b>과 유리함수의 대칭 교점 P, Q의 좌표를 인터랙티브하게 확인해 보세요.`;
    } else if (currentQid === "0669") {
      cHint.innerHTML = `<b>노란 점 B</b>를 드래그하면 삼각형 ABC 영역과 넓이 2√3, α² + β² = 8이 실시간 계산됩니다.`;
    } else {
      cHint.innerHTML = `고쟁이 ${currentPage}쪽 [${prob.id}번] 기하 시각화 시뮬레이션입니다.`;
    }
  }

  updateCanvasSize();
}

/* ---------- 3. 인터랙티브 캔버스 렌더러 ---------- */

function updateCanvasSize() {
  if (!cv) return;
  const dpr = window.devicePixelRatio || 1;
  cw = Math.max(320, cv.clientWidth || 600);
  chh = Math.round(cw * 0.7);
  cv.width = cw * dpr;
  cv.height = chh * dpr;
  cv.style.height = chh + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function drawAxes() {
  ctx.save();
  ctx.strokeStyle = "rgba(148, 163, 184, 0.15)";
  ctx.lineWidth = 1;
  ctx.fillStyle = "#64748b";
  ctx.font = "11px sans-serif";

  // 격자
  const xStep = (view.x1 - view.x0) > 12 ? 2 : 1;
  for (let x = Math.ceil(view.x0 / xStep) * xStep; x <= view.x1; x += xStep) {
    ctx.beginPath();
    ctx.moveTo(X(x), 20);
    ctx.lineTo(X(x), chh - 30);
    ctx.stroke();
    if (x !== 0) ctx.fillText(String(x), X(x) - 4, Y(0) + 14);
  }

  const yStep = (view.y1 - view.y0) > 12 ? 2 : 1;
  for (let y = Math.ceil(view.y0 / yStep) * yStep; y <= view.y1; y += yStep) {
    ctx.beginPath();
    ctx.moveTo(40, Y(y));
    ctx.lineTo(cw - 20, Y(y));
    ctx.stroke();
    if (y !== 0) ctx.fillText(String(y), 18, Y(y) + 4);
  }

  // 축
  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 1.8;
  if (view.y0 <= 0 && view.y1 >= 0) {
    ctx.beginPath();
    ctx.moveTo(40, Y(0));
    ctx.lineTo(cw - 20, Y(0));
    ctx.stroke();
    ctx.fillText("x", cw - 30, Y(0) - 6);
  }
  if (view.x0 <= 0 && view.x1 >= 0) {
    ctx.beginPath();
    ctx.moveTo(X(0), 20);
    ctx.lineTo(X(0), chh - 30);
    ctx.stroke();
    ctx.fillText("y", X(0) + 6, 32);
  }
  ctx.fillText("O", X(0) - 12, Y(0) + 14);
  ctx.restore();
}

function drawHandle(x, y, radius = 7, label = "") {
  ctx.save();
  const pul = 0.5 + 0.5 * Math.sin(performance.now() / 200);
  ctx.fillStyle = "#facc15";
  ctx.shadowColor = "#facc15";
  ctx.shadowBlur = 10 + 8 * pul;
  ctx.beginPath();
  ctx.arc(X(x), Y(y), radius, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.restore();

  if (label) {
    ctx.fillStyle = "#facc15";
    ctx.font = "bold 13px sans-serif";
    ctx.fillText(label, X(x) + 10, Y(y) - 8);
  }
}

function drawPill(text, x, y, col) {
  ctx.save();
  ctx.font = "800 12.5px sans-serif";
  const w = ctx.measureText(text).width + 14;
  const h = 22;
  const px = clamp(x - w / 2, 4, cw - w - 4);
  const py = clamp(y - h / 2, 4, chh - h - 4);

  ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
  ctx.strokeStyle = col;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.roundRect(px, py, w, h, 6);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = col;
  ctx.fillText(text, px + 7, py + 15);
  ctx.restore();
}

function drawLoop() {
  const prob = getCurProblem();

  // 뷰포트 설정
  if (currentQid === "0666") view = { x0: -6, x1: 6, y0: -8, y1: 4 };
  else if (currentQid === "0667") view = { x0: -1, x1: 7, y0: -1, y1: 7 };
  else if (currentQid === "0668") view = { x0: -1, x1: 10, y0: -1, y1: 10 };
  else if (currentQid === "0669") view = { x0: -4, x1: 5, y0: -2, y1: 5 };
  else view = { x0: -5, x1: 5, y0: -5, y1: 5 };

  ctx.clearRect(0, 0, cw, chh);
  ctx.fillStyle = "#0b1226";
  ctx.fillRect(0, 0, cw, chh);

  drawAxes();

  // 178쪽 전용 렌더링
  if (currentQid === "0666") {
    const k = prob.params.kLine !== undefined ? prob.params.kLine : -2;
    // 점근선
    ctx.save();
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
    ctx.beginPath(); ctx.moveTo(X(-1), 20); ctx.lineTo(X(-1), chh - 30); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(40, Y(-2)); ctx.lineTo(cw - 20, Y(-2)); ctx.stroke();
    ctx.restore();

    // 곡선 y = 1/(x+1) - 2
    ctx.save();
    ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = 40; px <= X(-1.08); px += 2) {
      const x = iX(px);
      const y = 1 / (x + 1) - 2;
      px === 40 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    ctx.beginPath();
    let first = true;
    for (let px = X(-0.92); px <= cw - 20; px += 2) {
      const x = iX(px);
      const y = 1 / (x + 1) - 2;
      first ? (ctx.moveTo(px, Y(y)), first = false) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    ctx.restore();

    // 동적 직선
    ctx.save();
    ctx.strokeStyle = "#f43f5e"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(X(view.x0), Y(k * (view.x0 - 1) - 6));
    ctx.lineTo(X(view.x1), Y(k * (view.x1 - 1) - 6));
    ctx.stroke();
    ctx.restore();

    // 정점 (1, -6)
    ctx.fillStyle = "#fb923c";
    ctx.beginPath(); ctx.arc(X(1), Y(-6), 6, 0, Math.PI * 2); ctx.fill();

    // 기울기 핸들
    const hx = 2.5, hy = k * (hx - 1) - 6;
    drawHandle(hx, hy, 7, `k = ${k.toFixed(1)}`);

    drawPill("곡선 y = (−2x−1)/(x+1)", X(2), Y(-1.2), "#38bdf8");
    drawPill(`직선 y = ${k.toFixed(1)}(x−1)−6`, X(hx - 0.5), Y(hy + 1.2), "#f43f5e");
  } else if (currentQid === "0667") {
    // 대칭축 y = x
    ctx.save();
    ctx.setLineDash([6, 5]);
    ctx.strokeStyle = "rgba(250, 204, 21, 0.5)";
    ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(6), Y(6)); ctx.stroke();
    ctx.restore();

    // 곡선 y = 4/x
    ctx.save();
    ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = X(0.4); px <= cw - 20; px += 2) {
      const x = iX(px);
      const y = 4 / x;
      px === X(0.4) ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    ctx.restore();

    const a = prob.params.a !== undefined ? prob.params.a : 1.035;
    const b = 4 / a;

    // 직선 AB
    ctx.save();
    ctx.strokeStyle = "#f43f5e"; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(X(a - 0.6), Y(b + 0.6)); ctx.lineTo(X(b + 0.6), Y(a - 0.6)); ctx.stroke();
    ctx.restore();

    drawHandle(a, b, 7, "A");
    ctx.fillStyle = "#38bdf8";
    ctx.beginPath(); ctx.arc(X(b), Y(a), 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillText("B", X(b) + 8, Y(a) - 6);

    const AB = Math.hypot(b - a, a - b);
    drawPill("y = 4/x", X(4.5), Y(1.5), "#38bdf8");
    drawPill("대칭축 y = x", X(5), Y(5), "#facc15");
    drawPill(`선분 AB = ${AB.toFixed(1)}`, X((a + b) / 2), Y((a + b) / 2 + 0.8), "#f43f5e");
  } else if (currentQid === "0668") {
    // 점근선 (2, 2)
    ctx.save();
    ctx.setLineDash([5, 5]); ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
    ctx.beginPath(); ctx.moveTo(X(2), 20); ctx.lineTo(X(2), chh - 30); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(40, Y(2)); ctx.lineTo(cw - 20, Y(2)); ctx.stroke();
    ctx.restore();

    // y = x 대칭축
    ctx.save();
    ctx.setLineDash([6, 5]); ctx.strokeStyle = "rgba(250, 204, 21, 0.4)";
    ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(9), Y(9)); ctx.stroke();
    ctx.restore();

    // 직선 x + y = 8
    ctx.save();
    ctx.strokeStyle = "#f43f5e"; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(X(0), Y(8)); ctx.lineTo(X(8), Y(0)); ctx.stroke();
    ctx.restore();

    // 곡선 (x-2)(y-2) = 2
    ctx.save();
    ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = X(2.2); px <= cw - 20; px += 2) {
      const x = iX(px);
      const y = 2 + 2 / (x - 2);
      px === X(2.2) ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    ctx.restore();

    const xP = 4 - Math.sqrt(2), yP = 4 + Math.sqrt(2);
    const xQ = 4 + Math.sqrt(2), yQ = 4 - Math.sqrt(2);
    drawHandle(xP, yP, 7, "P");
    ctx.fillStyle = "#38bdf8";
    ctx.beginPath(); ctx.arc(X(xQ), Y(yQ), 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillText("Q", X(xQ) + 8, Y(yQ) - 6);

    drawPill("x + y = 8", X(7), Y(1.5), "#f43f5e");
    drawPill("xy − 2x − 2y = −2", X(7), Y(3), "#38bdf8");
    drawPill("대칭축 y = x", X(7), Y(7), "#facc15");
  } else if (currentQid === "0669") {
    // y = x
    ctx.save();
    ctx.setLineDash([6, 5]); ctx.strokeStyle = "rgba(250, 204, 21, 0.4)";
    ctx.beginPath(); ctx.moveTo(X(-3), Y(-3)); ctx.lineTo(X(4), Y(4)); ctx.stroke();
    ctx.restore();

    // 곡선 y = 2/x
    ctx.save();
    ctx.strokeStyle = "#38bdf8"; ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = X(0.3); px <= cw - 20; px += 2) {
      const x = iX(px);
      const y = 2 / x;
      px === X(0.3) ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
    }
    ctx.stroke();
    ctx.restore();

    const al = prob.params.alpha !== undefined ? prob.params.alpha : 2.732;
    const be = 2 / al;

    // 삼각형 ABC
    ctx.save();
    ctx.fillStyle = "rgba(167, 139, 250, 0.25)";
    ctx.strokeStyle = "#a78bfa";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(X(-2), Y(2)); ctx.lineTo(X(al), Y(be)); ctx.lineTo(X(be), Y(al)); ctx.closePath();
    ctx.fill(); ctx.stroke();
    ctx.restore();

    // 점 A(-2, 2)
    ctx.fillStyle = "#f43f5e";
    ctx.beginPath(); ctx.arc(X(-2), Y(2), 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillText("A(−2, 2)", X(-2) - 48, Y(2) - 8);

    drawHandle(al, be, 7, "B(α, β)");
    ctx.fillStyle = "#38bdf8";
    ctx.beginPath(); ctx.arc(X(be), Y(al), 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillText("C(β, α)", X(be) - 42, Y(al) - 6);

    const triArea = 0.5 * (al * al - be * be);
    drawPill("y = 2/x", X(4), Y(0.8), "#38bdf8");
    drawPill("y = x 대칭", X(3.8), Y(3.8), "#facc15");
    drawPill(`△ABC 넓이 = ${triArea.toFixed(2)}`, X(0.5), Y(1.8), "#a78bfa");
  } else {
    // 일반 문항 그래프 기본 시각화
    ctx.save();
    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 15px Pretendard, sans-serif";
    ctx.fillText(`고쟁이 ${currentPage}쪽 [${prob.id}번] 함수 시뮬레이션`, 50, 60);

    // 단원에 따른 대표 곡선
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    if (currentPage >= 165) {
      // 유리/무리함수 계열
      for (let px = X(0.2); px <= cw - 20; px += 2) {
        const x = iX(px);
        const y = 2 / x;
        px === X(0.2) ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
      }
    } else {
      // 01 함수 계열 (이차/다항함수)
      for (let px = 40; px <= cw - 20; px += 2) {
        const x = iX(px);
        const y = 0.25 * x * x - 2;
        px === 40 ? ctx.moveTo(px, Y(y)) : ctx.lineTo(px, Y(y));
      }
    }
    ctx.stroke();

    // 인터랙티브 노란 핸들 제공
    drawHandle(2, 1, 7, "점 P");
    drawPill("기본 함수 모델", X(2.5), Y(2.5), "#38bdf8");
    ctx.restore();
  }

  animFrameId = requestAnimationFrame(drawLoop);
}

/* ---------- 4. 드래그 이벤트 ---------- */
function getCanvasPos(e) {
  const rect = cv.getBoundingClientRect();
  const cx = e.touches ? e.touches[0].clientX : e.clientX;
  const cy = e.touches ? e.touches[0].clientY : e.clientY;
  return { x: cx - rect.left, y: cy - rect.top };
}

function attachEvents() {
  cv.addEventListener("mousedown", onDown);
  cv.addEventListener("touchstart", onDown, { passive: false });
  window.addEventListener("mousemove", onMove);
  window.addEventListener("touchmove", onMove, { passive: false });
  window.addEventListener("mouseup", () => dragTarget = null);
  window.addEventListener("touchend", () => dragTarget = null);

  $("#btnToggleSol").onclick = () => {
    showSol = !showSol;
    renderProblemView();
  };

  $("#btnToggleAlt").onclick = () => {
    showAlt = !showAlt;
    renderProblemView();
  };

  $("#btnResetState").onclick = () => {
    const prob = getCurProblem();
    if (currentQid === "0666") prob.params.kLine = -2;
    if (currentQid === "0667") prob.params.a = 1.035;
    if (currentQid === "0669") prob.params.alpha = 2.732;
    renderProblemView();
  };

  // 단원 필터 탭
  $$(".unit-tab").forEach(tab => {
    tab.onclick = () => {
      $$(".unit-tab").forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      currentUnit = tab.dataset.unit;
      if (currentUnit === "unit1") selectPage(135);
      else if (currentUnit === "unit2") selectPage(167);
      else selectPage(178);
    };
  });
}

function onDown(e) {
  const p = getCanvasPos(e);
  const prob = getCurProblem();

  if (currentQid === "0666") {
    dragTarget = "0666_k";
    if (e.cancelable) e.preventDefault();
  } else if (currentQid === "0667") {
    dragTarget = "0667_a";
    if (e.cancelable) e.preventDefault();
  } else if (currentQid === "0669") {
    dragTarget = "0669_alpha";
    if (e.cancelable) e.preventDefault();
  }
}

function onMove(e) {
  if (!dragTarget) return;
  if (e.cancelable) e.preventDefault();
  const p = getCanvasPos(e);
  const mx = iX(p.x), my = iY(p.y);
  const prob = getCurProblem();

  if (dragTarget === "0666_k") {
    const dx = mx - 1, dy = my - (-6);
    if (Math.abs(dx) > 0.1) {
      prob.params.kLine = clamp(dy / dx, -8, 5);
    }
  } else if (dragTarget === "0667_a") {
    prob.params.a = clamp(mx, 0.5, 2.0);
  } else if (dragTarget === "0669_alpha") {
    prob.params.alpha = clamp(mx, 1.45, 3.8);
  }
}

/* ---------- 5. 초기 구동 ---------- */
window.addEventListener("DOMContentLoaded", () => {
  cv = $("#cv");
  ctx = cv.getContext("2d");
  attachEvents();
  selectPage(178);
  drawLoop();
});

// 스크립트가 DOM 완료 후 실행될 때를 대비
if (document.readyState === "complete" || document.readyState === "interactive") {
  cv = $("#cv");
  if (cv) {
    ctx = cv.getContext("2d");
    attachEvents();
    selectPage(178);
    drawLoop();
  }
}
