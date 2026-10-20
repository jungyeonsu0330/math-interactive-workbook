/* 고쟁이 178쪽 엔진: 캔버스 렌더링 · 대칭성 시각화 · 드래그 인터랙션 · 형광 연동 */
const cv = $("#cv"), ctx = cv.getContext("2d");
let cur = 0, mi = 0, K = {}, P = {}, showSol = false, showAlt = false, dragged = false;
let solved = {}, lockHL = null, hoverHL = null, drag = null;
let cw = 600, chh = 420, V = null;
window.HLK = [];
window.PILLS = [];

const def = () => PR[cur], mode = () => def().modes[mi];

const COL = {
  curve: "#38bdf8",     // 밝은 하늘색
  line: "#f43f5e",      // 밝은 로즈 레드
  lineAB: "#f43f5e",
  lineBC: "#f43f5e",
  sym: "#facc15",       // 노란색 (대칭축)
  pts: "#4ade80",       // 녹색
  symPts: "#4ade80",
  tri: "#a78bfa",       // 보라색
  fixpt: "#fb923c",     // 주황색
  tan1: "#ec4899",
  tan2: "#a855f7",
  asymp: "rgba(148, 163, 184, 0.4)",
  axis: "#94a3b8"
};

function recomputeHL() {
  window.HLK = hoverHL || lockHL || [];
  document.querySelectorAll("[data-hl]").forEach(e => {
    const ks = e.dataset.hl.split(",");
    e.classList.toggle("hkon", window.HLK.length > 0 && ks.some(k => window.HLK.includes(k)));
  });
}

document.addEventListener("mouseover", e => {
  const t = e.target.closest && e.target.closest("[data-hl]");
  if (t) { hoverHL = t.dataset.hl.split(","); recomputeHL(); }
});
document.addEventListener("mouseout", e => {
  const t = e.target.closest && e.target.closest("[data-hl]");
  if (t) { hoverHL = null; recomputeHL(); }
});
document.addEventListener("click", e => {
  const t = e.target.closest && e.target.closest("[data-hl]");
  if (t && !t.classList.contains("tb") && !t.classList.contains("vc")) {
    const ks = t.dataset.hl.split(",");
    lockHL = (lockHL && lockHL.join() === ks.join()) ? null : ks;
    recomputeHL();
  }
});

/* ---------- 수식 포맷팅 ---------- */
function fmt(t) {
  if (!t) return "";
  t = String(t);
  t = t.replace(/²[ ]*([+\-×÷=])/g, "² $1");
  return t;
}

/* ---------- 상태 설정 ---------- */
function setMode(i, Kn) {
  mi = i;
  const m = mode();
  K = Object.assign({}, Kn || m.K);
  P = def().P(K);
  dragged = false;
  showSol = false;
  showAlt = false;
  lockHL = null;
  hoverHL = null;
  render();
}

function renderChoices() {
  const box = $("#choices");
  const inputBox = $("#ansInputBox");
  box.innerHTML = "";

  const d = def(), m = mode();
  if (d.type === "input" && mi === 0) {
    box.style.display = "none";
    inputBox.style.display = "flex";
    $("#userAns").value = "";
    $("#bSubmitAns").onclick = () => {
      const v = Number($("#userAns").value.trim());
      if (v === d.correctVal) {
        $("#vmsg").innerHTML = `<span style="color:#4ade80;font-weight:800">정답입니다! 36 (풀이 보기로 과정을 확인하세요.)</span>`;
        solved[cur] = 1;
        renderNav();
      } else {
        $("#vmsg").innerHTML = `<span style="color:#fb7185;font-weight:800">다시 계산해 보세요. 대칭점의 성질 a+b=8, ab=14를 이용해요.</span>`;
      }
    };
    return;
  }

  box.style.display = "grid";
  inputBox.style.display = "none";

  const choicesList = m.choices || d.bookChoices;
  const correctIndex = m.choiceIdx !== undefined ? m.choiceIdx : d.bookIdx;

  choicesList.forEach((c, idx) => {
    const b = document.createElement("button");
    b.className = "ch";
    b.innerHTML = "①②③④⑤"[idx] + " " + fmt(c);
    b.onclick = () => {
      if (idx === correctIndex) {
        b.classList.add("good");
        solved[cur] = 1;
        renderNav();
        $("#vmsg").innerHTML = `<span style="color:#4ade80;font-weight:800">정답이에요! [풀이 보기]로 상세한 풀이 과정을 확인해 보세요.</span>`;
      } else {
        b.classList.add("bad");
        $("#vmsg").innerHTML = `<span style="color:#fb7185">다시 풀어보세요! 유리함수의 그래프 대칭성과 점근선을 먼저 파악하세요.</span>`;
      }
    };
    box.appendChild(b);
  });
}

function renderNav() {
  $("#nav").innerHTML = "";
  PR.forEach((p, i) => {
    const b = document.createElement("button");
    b.className = "tb" + (i === cur ? " on" : "") + (solved[i] ? " ok" : "");
    b.textContent = (solved[i] ? "✔ " : "") + p.id + (p.tag ? " · " + p.tag.split("·")[0].trim() : "");
    b.onclick = () => { cur = i; setMode(0); };
    $("#nav").appendChild(b);
  });
}

function renderVar() {
  const d = def(), box = $("#vchips");
  box.innerHTML = "";
  d.modes.forEach((m, i) => {
    const b = document.createElement("button");
    b.className = "vc" + (i === mi ? " on" : "");
    b.innerHTML = fmt(m.n);
    b.title = m.d || "";
    b.onclick = () => setMode(i);
    b.onmouseenter = () => { hoverHL = m.hl; recomputeHL(); };
    b.onmouseleave = () => { hoverHL = null; recomputeHL(); };
    box.appendChild(b);
  });

  const kb = $("#vknobs");
  kb.innerHTML = "";
  if (mode().K) {
    Object.keys(mode().K).forEach(k => {
      const l = document.createElement("label");
      l.className = "cv";
      l.innerHTML = `${d.L && d.L[k] ? d.L[k] : k} <input type="number" step="0.5" data-k="${k}" value="${K[k]}">`;
      kb.appendChild(l);
    });
  }
  $("#vmsg").textContent = mode().d || "조건을 바꾼 응용 문제예요.";
}

function readKnobs() {
  const o = {};
  document.querySelectorAll("#vknobs input").forEach(i => o[i.dataset.k] = Number(i.value));
  return o;
}

function makeVariant() {
  const m = mode();
  const mk = Object.assign({}, m.K, readKnobs());
  setMode(mi, mk);
  $("#vmsg").textContent = "지정한 수치로 변형 문제를 구성했어요.";
}

function render() {
  const d = def(), m = mode();
  $("#qid").innerHTML = `${d.id} · ${m.n}` + (d.tag ? ` <span class="tag">${d.tag}</span>` : "");
  $("#q").innerHTML = m.text(K);
  $("#solcard").style.display = "none";
  $("#alt").style.display = "none";
  $("#bAlt").textContent = "다른 풀이";
  $("#bSol").textContent = "풀이 보기";

  $("#themeChip").textContent = d.conceptTitle;
  $("#concept").innerHTML = d.conceptHtml;

  renderChoices();
  renderNav();
  renderVar();
  recomputeHL();
  sizeCv();
  updateHint();
}

function updateHint() {
  if (cur === 0) {
    $("#chint").innerHTML = `노란 점을 위아래로 끌어 <b>직선의 기울기 k</b>를 바꿔보세요. 교점 개수(접함/2점/0점)가 실시간으로 변합니다.`;
  } else if (cur === 1) {
    $("#chint").innerHTML = `노란 점 A를 곡선 위에서 드래그해보세요. y=x 대칭점 B와 선분 AB의 길이가 자동으로 계산됩니다.`;
  } else if (cur === 2) {
    $("#chint").innerHTML = `노란 점을 좌우로 끌어 직선 <b>x + y = S</b>의 위치를 조절하고 대칭 교점 P, Q의 좌표를 관찰해 보세요.`;
  } else if (cur === 3) {
    $("#chint").innerHTML = `노란 점 B를 곡선 위에서 드래그해보세요. 삼각형 ABC의 넓이와 α² + β²의 관계를 확인할 수 있습니다.`;
  }
}

function solText() {
  const m = mode();
  return m.sol(K).map((l, i) => `<div style="margin:6px 0">${"①②③④⑤⑥"[i] || "•"} ${l}</div>`).join("") +
    `<div class="big ok" style="margin-top:10px">정답: ${m.ans(K).text}</div>`;
}

function altText() {
  const m = mode();
  if (m.altSol) {
    return m.altSol.map(l => `<div style="margin:4px 0">${l}</div>`).join("");
  }
  return `<div>대칭성 또는 공식을 이용하면 복잡한 계산을 대폭 줄일 수 있습니다.</div>`;
}

$("#bSol").onclick = () => {
  showSol = !showSol;
  $("#solcard").style.display = showSol ? "block" : "none";
  $("#bSol").textContent = showSol ? "풀이 접기" : "풀이 보기";
  if (showSol) $("#sol").innerHTML = solText();
};

$("#bAlt").onclick = () => {
  showAlt = !showAlt;
  $("#alt").style.display = showAlt ? "block" : "none";
  $("#bAlt").textContent = showAlt ? "다른 풀이 접기" : "다른 풀이";
  if (showAlt) $("#altContent").innerHTML = altText();
};

$("#bReset").onclick = () => {
  setMode(mi, mode().K);
  dragged = false;
  lockHL = null;
  recomputeHL();
};
$("#bVar").onclick = makeVariant;
$("#bVarOrig").onclick = () => setMode(0);

/* ---------- Canvas 그래픽스 엔진 ---------- */
function sizeCv() {
  const dpr = window.devicePixelRatio || 1;
  cw = Math.max(300, cv.clientWidth || 600);
  chh = Math.round(cw * 0.7);
  cv.width = cw * dpr;
  cv.height = chh * dpr;
  cv.style.height = chh + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
window.addEventListener("resize", () => sizeCv());

const ML = 40, MR = 20, MT = 20, MB = 30;

function getViewBounds() {
  if (cur === 0) return { x0: -6, x1: 6, y0: -8, y1: 4 };
  if (cur === 1) return { x0: -1, x1: 7, y0: -1, y1: 7 };
  if (cur === 2) return { x0: -1, x1: 10, y0: -1, y1: 10 };
  if (cur === 3) return { x0: -4, x1: 5, y0: -2, y1: 5 };
  return { x0: -5, x1: 5, y0: -5, y1: 5 };
}

const X = x => ML + (x - V.x0) / (V.x1 - V.x0) * (cw - ML - MR);
const Y = y => MT + (V.y1 - y) / (V.y1 - V.y0) * (chh - MT - MB);
const iX = px => V.x0 + (px - ML) / (cw - ML - MR) * (V.x1 - V.x0);
const iY = py => V.y1 - (py - MT) / (chh - MT - MB) * (V.y1 - V.y0);

function drawAxes() {
  ctx.save();
  ctx.strokeStyle = "rgba(148, 163, 184, 0.15)";
  ctx.lineWidth = 1;
  ctx.fillStyle = "#64748b";
  ctx.font = "11px sans-serif";

  // x-grid & labels
  const xStep = (V.x1 - V.x0) > 12 ? 2 : 1;
  for (let x = Math.ceil(V.x0 / xStep) * xStep; x <= V.x1; x += xStep) {
    ctx.beginPath();
    ctx.moveTo(X(x), MT);
    ctx.lineTo(X(x), chh - MB);
    ctx.stroke();
    if (x !== 0) ctx.fillText(String(x), X(x) - 4, Y(0) + 14);
  }

  // y-grid & labels
  const yStep = (V.y1 - V.y0) > 12 ? 2 : 1;
  for (let y = Math.ceil(V.y0 / yStep) * yStep; y <= V.y1; y += yStep) {
    ctx.beginPath();
    ctx.moveTo(ML, Y(y));
    ctx.lineTo(cw - MR, Y(y));
    ctx.stroke();
    if (y !== 0) ctx.fillText(String(y), ML - 24, Y(y) + 4);
  }

  // Axes lines
  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 1.8;
  // x-axis
  if (V.y0 <= 0 && V.y1 >= 0) {
    ctx.beginPath();
    ctx.moveTo(ML, Y(0));
    ctx.lineTo(cw - MR, Y(0));
    ctx.stroke();
    ctx.fillText("x", cw - MR - 10, Y(0) - 6);
  }
  // y-axis
  if (V.x0 <= 0 && V.x1 >= 0) {
    ctx.beginPath();
    ctx.moveTo(X(0), MT);
    ctx.lineTo(X(0), chh - MB);
    ctx.stroke();
    ctx.fillText("y", X(0) + 6, MT + 12);
  }
  ctx.fillText("O", X(0) - 12, Y(0) + 14);
  ctx.restore();
}

function drawPill(text, x, y, col, isHL = false) {
  const pul = 0.5 + 0.5 * Math.sin(performance.now() / 150);
  ctx.save();
  ctx.font = "800 13px Pretendard, sans-serif";
  const w = ctx.measureText(text).width + 14;
  const h = 22;
  const px = clamp(x - w / 2, 4, cw - w - 4);
  const py = clamp(y - h / 2, 4, chh - h - 4);

  ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
  ctx.strokeStyle = col;
  ctx.lineWidth = isHL ? 3 : 1.5;
  if (isHL) {
    ctx.shadowColor = col;
    ctx.shadowBlur = 12 + 10 * pul;
  }
  ctx.beginPath();
  ctx.roundRect(px, py, w, h, 6);
  ctx.fill();
  ctx.stroke();

  ctx.shadowBlur = 0;
  ctx.fillStyle = col;
  ctx.fillText(text, px + 7, py + 15);
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

/* ---------- 개별 문제별 특화 렌더링 ---------- */

function drawQ0666() {
  const k = K.k !== undefined ? K.k : -2;
  const isHL_curve = window.HLK.includes("curve");
  const isHL_line = window.HLK.includes("line");
  const isHL_tan = window.HLK.includes("tan1") || window.HLK.includes("tan2");
  const isHL_fix = window.HLK.includes("fixpt");

  // 1. 점근선
  ctx.save();
  ctx.setLineDash([5, 5]);
  ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
  ctx.lineWidth = 1.5;
  // x = -1
  ctx.beginPath(); ctx.moveTo(X(-1), MT); ctx.lineTo(X(-1), chh - MB); ctx.stroke();
  // y = -2
  ctx.beginPath(); ctx.moveTo(ML, Y(-2)); ctx.lineTo(cw - MR, Y(-2)); ctx.stroke();
  ctx.fillStyle = "rgba(148, 163, 184, 0.8)";
  ctx.fillText("x = −1", X(-1) + 4, MT + 20);
  ctx.fillText("y = −2", cw - MR - 45, Y(-2) - 6);
  ctx.restore();

  // 2. 유리함수 y = 1/(x+1) - 2
  ctx.save();
  ctx.strokeStyle = isHL_curve ? "#38bdf8" : "#0284c7";
  ctx.lineWidth = isHL_curve ? 3.5 : 2.5;
  if (isHL_curve) { ctx.shadowColor = "#38bdf8"; ctx.shadowBlur = 12; }

  // branch 1: x < -1
  ctx.beginPath();
  let first = true;
  for (let px = ML; px <= X(-1.05); px += 2) {
    const x = iX(px);
    const y = 1 / (x + 1) - 2;
    if (y >= V.y0 - 2 && y <= V.y1 + 2) {
      if (first) { ctx.moveTo(px, Y(y)); first = false; }
      else ctx.lineTo(px, Y(y));
    }
  }
  ctx.stroke();

  // branch 2: x > -1
  ctx.beginPath();
  first = true;
  for (let px = X(-0.95); px <= cw - MR; px += 2) {
    const x = iX(px);
    const y = 1 / (x + 1) - 2;
    if (y >= V.y0 - 2 && y <= V.y1 + 2) {
      if (first) { ctx.moveTo(px, Y(y)); first = false; }
      else ctx.lineTo(px, Y(y));
    }
  }
  ctx.stroke();
  ctx.restore();

  // 3. 접선 경계 가이드선 (k = -4, k = -1)
  ctx.save();
  ctx.setLineDash([4, 4]);
  ctx.lineWidth = isHL_tan ? 2 : 1;
  ctx.strokeStyle = "rgba(244, 114, 182, 0.4)";
  // k = -4: y = -4(x-1) - 6 = -4x - 2
  ctx.beginPath(); ctx.moveTo(X(-2), Y(6)); ctx.lineTo(X(2), Y(-10)); ctx.stroke();
  // k = -1: y = -(x-1) - 6 = -x - 5
  ctx.beginPath(); ctx.moveTo(X(-5), Y(0)); ctx.lineTo(X(4), Y(-9)); ctx.stroke();
  ctx.restore();

  // 4. 동적 직선 y = k(x-1) - 6
  ctx.save();
  ctx.strokeStyle = isHL_line ? "#fb7185" : "#f43f5e";
  ctx.lineWidth = isHL_line ? 3.5 : 2.5;
  if (isHL_line) { ctx.shadowColor = "#fb7185"; ctx.shadowBlur = 12; }
  ctx.beginPath();
  const yL = k * (V.x0 - 1) - 6;
  const yR = k * (V.x1 - 1) - 6;
  ctx.moveTo(X(V.x0), Y(yL));
  ctx.lineTo(X(V.x1), Y(yR));
  ctx.stroke();
  ctx.restore();

  // 5. 정점 (1, -6)
  ctx.save();
  ctx.fillStyle = isHL_fix ? "#fb923c" : "#f97316";
  ctx.beginPath(); ctx.arc(X(1), Y(-6), 6, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "#fdba74";
  ctx.font = "bold 12px sans-serif";
  ctx.fillText("정점 (1, −6)", X(1) + 8, Y(-6) + 14);
  ctx.restore();

  // 6. 교점 판정 및 시각화
  // kx^2 - 4x - (k+5) = 0
  const disc = 16 + 4 * k * (k + 5); // = 4(k+4)(k+1)
  let meets = 0;
  if (k === 0) {
    // -4x - 5 = 0 -> x = -5/4
    const xi = -1.25, yi = -6;
    ctx.fillStyle = "#4ade80";
    ctx.beginPath(); ctx.arc(X(xi), Y(yi), 5, 0, Math.PI * 2); ctx.fill();
    meets = 1;
  } else if (disc >= 0) {
    const x1 = (4 + Math.sqrt(disc)) / (2 * k);
    const x2 = (4 - Math.sqrt(disc)) / (2 * k);
    [x1, x2].forEach(xi => {
      const yi = k * (xi - 1) - 6;
      ctx.fillStyle = "#4ade80";
      ctx.beginPath(); ctx.arc(X(xi), Y(yi), 5, 0, Math.PI * 2); ctx.fill();
    });
    meets = disc === 0 ? 1 : 2;
  }

  // 상태 텍스트 뱃지
  const stateBadge = $("#graphState");
  if (meets > 0) {
    stateBadge.textContent = `현재 k = ${k.toFixed(2)} (교점 ${meets}개 · A ∩ B ≠ ∅ 만남)`;
    stateBadge.style.color = "#4ade80";
    stateBadge.style.borderColor = "#4ade80";
  } else {
    stateBadge.textContent = `현재 k = ${k.toFixed(2)} (교점 0개 · 만나지 않음)`;
    stateBadge.style.color = "#fb7185";
    stateBadge.style.borderColor = "#fb7185";
  }

  // 기울기 조절 핸들 (정점에서 x=3 지점의 점)
  const hx = 2.5, hy = k * (hx - 1) - 6;
  drawHandle(hx, hy, 7, `k = ${k.toFixed(2)}`);

  drawPill("곡선 y = (−2x−1)/(x+1)", X(2), Y(-1.2), "#38bdf8", isHL_curve);
  drawPill(`직선 y = ${k.toFixed(1)}(x−1)−6`, X(hx - 0.5), Y(hy + 1.2), "#f43f5e", isHL_line);
}

function drawQ0667() {
  const k = K.k || 4;
  const isHL_curve = window.HLK.includes("curve");
  const isHL_sym = window.HLK.includes("sym");
  const isHL_AB = window.HLK.includes("AB");
  const isHL_prod = window.HLK.includes("prod");

  // 1. 대칭축 y = x
  ctx.save();
  ctx.strokeStyle = isHL_sym ? "#facc15" : "rgba(250, 204, 21, 0.4)";
  ctx.lineWidth = isHL_sym ? 2.5 : 1.5;
  ctx.setLineDash([6, 5]);
  if (isHL_sym) { ctx.shadowColor = "#facc15"; ctx.shadowBlur = 10; }
  ctx.beginPath();
  ctx.moveTo(X(V.x0), Y(V.x0));
  ctx.lineTo(X(V.x1), Y(V.x1));
  ctx.stroke();
  ctx.restore();

  // 2. 유리함수 y = 4/x (x > 0)
  ctx.save();
  ctx.strokeStyle = isHL_curve ? "#38bdf8" : "#0284c7";
  ctx.lineWidth = isHL_curve ? 3.5 : 2.5;
  if (isHL_curve) { ctx.shadowColor = "#38bdf8"; ctx.shadowBlur = 12; }
  ctx.beginPath();
  let first = true;
  for (let px = X(0.2); px <= cw - MR; px += 2) {
    const x = iX(px);
    const y = k / x;
    if (y >= V.y0 && y <= V.y1) {
      if (first) { ctx.moveTo(px, Y(y)); first = false; }
      else ctx.lineTo(px, Y(y));
    }
  }
  ctx.stroke();
  ctx.restore();

  // 3. 점 A, B 계산
  // OA * OB = a^2 + b^2 = 16, ab = 4.
  // (b-a)^2 = 16 - 8 = 8 -> b - a = 2√2.
  // (b+a)^2 = 16 + 8 = 24 -> b + a = 2√6.
  // a = √6 - √2 ≈ 1.035, b = √6 + √2 ≈ 3.864
  let a = P.a || (Math.sqrt(6) - Math.sqrt(2));
  a = clamp(a, 0.5, 1.8);
  const b = k / a;

  // 점 A(a, b), B(b, a)
  const Ax = a, Ay = b;
  const Bx = b, By = a;

  // 4. 선분 OA, OB
  ctx.save();
  ctx.strokeStyle = isHL_prod ? "#4ade80" : "rgba(74, 222, 128, 0.4)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(Ax), Y(Ay));
  ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(Bx), Y(By));
  ctx.stroke();
  ctx.restore();

  // 5. 직선 AB (기울기 -1)
  ctx.save();
  ctx.strokeStyle = isHL_AB ? "#fb7185" : "#f43f5e";
  ctx.lineWidth = isHL_AB ? 3.5 : 2.5;
  if (isHL_AB) { ctx.shadowColor = "#fb7185"; ctx.shadowBlur = 12; }
  ctx.beginPath();
  ctx.moveTo(X(Ax - 0.8), Y(Ay + 0.8));
  ctx.lineTo(X(Bx + 0.8), Y(By - 0.8));
  ctx.stroke();
  ctx.restore();

  // 6. 점 A, B 그리기
  drawHandle(Ax, Ay, 7, "A");
  ctx.fillStyle = "#38bdf8";
  ctx.beginPath(); ctx.arc(X(Bx), Y(By), 6, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "#e2e8f0";
  ctx.font = "bold 13px sans-serif";
  ctx.fillText("B", X(Bx) + 9, Y(By) - 8);

  // 길이 & 곱 계산치
  const OA = Math.hypot(Ax, Ay);
  const OB = Math.hypot(Bx, By);
  const AB = Math.hypot(Bx - Ax, By - Ay);

  const stateBadge = $("#graphState");
  stateBadge.textContent = `A(${Ax.toFixed(2)}, ${Ay.toFixed(2)}), B(${Bx.toFixed(2)}, ${By.toFixed(2)}) | AB = ${AB.toFixed(2)}`;
  stateBadge.style.color = "#38bdf8";

  drawPill("y = 4/x", X(4.5), Y(1.5), "#38bdf8", isHL_curve);
  drawPill("대칭축 y = x", X(5), Y(5), "#facc15", isHL_sym);
  drawPill(`선분 AB = ${AB.toFixed(1)}`, X((Ax + Bx) / 2), Y((Ay + By) / 2 + 0.8), "#f43f5e", isHL_AB);
}

function drawQ0668() {
  const S = K.S || 8;
  const prodX = K.prodX || 14;
  const isHL_curve = window.HLK.includes("curve");
  const isHL_line = window.HLK.includes("line");
  const isHL_sym = window.HLK.includes("sym");
  const isHL_asymp = window.HLK.includes("asymp");
  const isHL_target = window.HLK.includes("target");

  // 1. 점근선 x = 2, y = 2
  ctx.save();
  ctx.setLineDash([5, 5]);
  ctx.strokeStyle = isHL_asymp ? "#facc15" : "rgba(148, 163, 184, 0.4)";
  ctx.lineWidth = isHL_asymp ? 2 : 1.2;
  ctx.beginPath(); ctx.moveTo(X(2), MT); ctx.lineTo(X(2), chh - MB); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ML, Y(2)); ctx.lineTo(cw - MR, Y(2)); ctx.stroke();
  ctx.fillStyle = "rgba(148, 163, 184, 0.8)";
  ctx.fillText("x = 2", X(2) + 4, MT + 20);
  ctx.fillText("y = 2", cw - MR - 40, Y(2) - 6);
  ctx.restore();

  // 2. 대칭축 y = x
  ctx.save();
  ctx.setLineDash([6, 5]);
  ctx.strokeStyle = isHL_sym ? "#facc15" : "rgba(250, 204, 21, 0.35)";
  ctx.lineWidth = isHL_sym ? 2.5 : 1.5;
  ctx.beginPath(); ctx.moveTo(X(V.x0), Y(V.x0)); ctx.lineTo(X(V.x1), Y(V.x1)); ctx.stroke();
  ctx.restore();

  // k = -2 일 때 (x-2)(y-2) = 2
  const cVal = S === 8 && prodX === 14 ? 2 : (prodX - 2 * S + 4);
  const kConst = cVal > 0 ? cVal : 2;

  // 3. 곡선 (x-2)(y-2) = k+4
  ctx.save();
  ctx.strokeStyle = isHL_curve ? "#38bdf8" : "#0284c7";
  ctx.lineWidth = isHL_curve ? 3.5 : 2.5;
  // branch x > 2
  ctx.beginPath();
  let first = true;
  for (let px = X(2.1); px <= cw - MR; px += 2) {
    const x = iX(px);
    const y = 2 + kConst / (x - 2);
    if (y >= V.y0 && y <= V.y1) {
      if (first) { ctx.moveTo(px, Y(y)); first = false; }
      else ctx.lineTo(px, Y(y));
    }
  }
  ctx.stroke();

  // branch x < 2
  ctx.beginPath();
  first = true;
  for (let px = ML; px <= X(1.9); px += 2) {
    const x = iX(px);
    const y = 2 + kConst / (x - 2);
    if (y >= V.y0 && y <= V.y1) {
      if (first) { ctx.moveTo(px, Y(y)); first = false; }
      else ctx.lineTo(px, Y(y));
    }
  }
  ctx.stroke();
  ctx.restore();

  // 4. 직선 x + y = S
  ctx.save();
  ctx.strokeStyle = isHL_line ? "#fb7185" : "#f43f5e";
  ctx.lineWidth = isHL_line ? 3.5 : 2.5;
  ctx.beginPath();
  ctx.moveTo(X(V.x0), Y(S - V.x0));
  ctx.lineTo(X(V.x1), Y(S - V.x1));
  ctx.stroke();
  ctx.restore();

  // 5. 교점 P, Q 계산 (x^2 - Sx + prodX = 0)
  const dval = S * S - 4 * prodX;
  if (dval >= 0) {
    const xP = (S - Math.sqrt(dval)) / 2;
    const yP = S - xP;
    const xQ = (S + Math.sqrt(dval)) / 2;
    const yQ = S - xQ;

    // 원점 연결선 OP, OQ
    ctx.save();
    ctx.strokeStyle = isHL_target ? "#4ade80" : "rgba(74, 222, 128, 0.45)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(xP), Y(yP));
    ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(xQ), Y(yQ));
    ctx.stroke();
    ctx.restore();

    drawHandle(xP, yP, 7, "P");
    ctx.fillStyle = "#38bdf8";
    ctx.beginPath(); ctx.arc(X(xQ), Y(yQ), 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#e2e8f0";
    ctx.font = "bold 13px sans-serif";
    ctx.fillText("Q", X(xQ) + 8, Y(yQ) - 6);

    const targetVal = (xP * xP + yP * yP);
    $("#graphState").textContent = `P(${xP.toFixed(2)}, ${yP.toFixed(2)}), Q(${xQ.toFixed(2)}, ${yQ.toFixed(2)}) | OP × OQ = ${targetVal.toFixed(0)}`;
  }

  drawPill(`x + y = ${S}`, X(S - 1), Y(1.5), "#f43f5e", isHL_line);
  drawPill("xy − 2x − 2y = −2", X(7), Y(3), "#38bdf8", isHL_curve);
  drawPill("대칭축 y = x", X(7), Y(7), "#facc15", isHL_sym);
}

function drawQ0669() {
  const isHL_curve = window.HLK.includes("curve");
  const isHL_tri = window.HLK.includes("tri");
  const isHL_sym = window.HLK.includes("sym");
  const isHL_A = window.HLK.includes("ptA");
  const isHL_BC = window.HLK.includes("lineBC");

  // 1. 대칭축 y = x
  ctx.save();
  ctx.setLineDash([6, 5]);
  ctx.strokeStyle = isHL_sym ? "#facc15" : "rgba(250, 204, 21, 0.4)";
  ctx.lineWidth = isHL_sym ? 2.5 : 1.5;
  ctx.beginPath(); ctx.moveTo(X(V.x0), Y(V.x0)); ctx.lineTo(X(V.x1), Y(V.x1)); ctx.stroke();
  ctx.restore();

  // 2. 곡선 y = 2/x (1사분면 위주)
  ctx.save();
  ctx.strokeStyle = isHL_curve ? "#38bdf8" : "#0284c7";
  ctx.lineWidth = isHL_curve ? 3.5 : 2.5;
  ctx.beginPath();
  let first = true;
  for (let px = X(0.2); px <= cw - MR; px += 2) {
    const x = iX(px);
    const y = 2 / x;
    if (y >= V.y0 && y <= V.y1) {
      if (first) { ctx.moveTo(px, Y(y)); first = false; }
      else ctx.lineTo(px, Y(y));
    }
  }
  ctx.stroke();
  ctx.restore();

  // 3. 점 A(-2, 2)
  const Ax = -2, Ay = 2;
  ctx.save();
  ctx.fillStyle = isHL_A ? "#f43f5e" : "#e11d48";
  ctx.beginPath(); ctx.arc(X(Ax), Y(Ay), 6, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "#fda4af";
  ctx.font = "bold 13px sans-serif";
  ctx.fillText("A(−2, 2)", X(Ax) - 52, Y(Ay) - 8);
  ctx.restore();

  // 4. 점 B(α, β), C(β, α) 계산
  // α = √3 + 1 ≈ 2.732, β = √3 - 1 ≈ 0.732
  let alpha = P.alpha || (Math.sqrt(3) + 1);
  alpha = clamp(alpha, 1.45, 4.0);
  const beta = 2 / alpha;

  const Bx = alpha, By = beta;
  const Cx = beta, Cy = alpha;

  // 5. 삼각형 ABC 영역 채우기
  ctx.save();
  ctx.fillStyle = isHL_tri ? "rgba(167, 139, 250, 0.4)" : "rgba(167, 139, 250, 0.2)";
  ctx.strokeStyle = isHL_tri ? "#a78bfa" : "rgba(167, 139, 250, 0.6)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(X(Ax), Y(Ay));
  ctx.lineTo(X(Bx), Y(By));
  ctx.lineTo(X(Cx), Y(Cy));
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.restore();

  // 6. 선분 BC
  ctx.save();
  ctx.strokeStyle = isHL_BC ? "#fb7185" : "#f43f5e";
  ctx.lineWidth = isHL_BC ? 3 : 2;
  ctx.beginPath(); ctx.moveTo(X(Bx), Y(By)); ctx.lineTo(X(Cx), Y(Cy)); ctx.stroke();
  ctx.restore();

  // 7. 점 B, C 그리기 & 드래그 핸들
  drawHandle(Bx, By, 7, "B(α, β)");
  ctx.fillStyle = "#38bdf8";
  ctx.beginPath(); ctx.arc(X(Cx), Y(Cy), 6, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "#e2e8f0";
  ctx.font = "bold 13px sans-serif";
  ctx.fillText("C(β, α)", X(Cx) - 45, Y(Cy) - 6);

  const triArea = 0.5 * (alpha * alpha - beta * beta);
  const sqSum = alpha * alpha + beta * beta;

  $("#graphState").textContent = `α = ${alpha.toFixed(2)}, β = ${beta.toFixed(2)} | 넓이 S = ${triArea.toFixed(2)} (목표 2√3 ≈ 3.46) | α² + β² = ${sqSum.toFixed(2)}`;

  drawPill("y = 2/x", X(4), Y(0.8), "#38bdf8", isHL_curve);
  drawPill("y = x 대칭", X(3.8), Y(3.8), "#facc15", isHL_sym);
  drawPill(`△ABC 넓이 = ${triArea.toFixed(2)}`, X(0.5), Y(1.8), "#a78bfa", isHL_tri);
}

function draw() {
  V = getViewBounds();
  ctx.clearRect(0, 0, cw, chh);
  ctx.fillStyle = "#0b1226";
  ctx.fillRect(0, 0, cw, chh);

  drawAxes();

  if (cur === 0) drawQ0666();
  else if (cur === 1) drawQ0667();
  else if (cur === 2) drawQ0668();
  else if (cur === 3) drawQ0669();

  requestAnimationFrame(draw);
}

/* ---------- 드래그 & 터치 인터랙션 ---------- */
function getCanvasPos(e) {
  const rect = cv.getBoundingClientRect();
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const clientY = e.touches ? e.touches[0].clientY : e.clientY;
  return {
    x: clientX - rect.left,
    y: clientY - rect.top
  };
}

cv.addEventListener("mousedown", onDown);
cv.addEventListener("touchstart", onDown, { passive: false });
window.addEventListener("mousemove", onMove);
window.addEventListener("touchmove", onMove, { passive: false });
window.addEventListener("mouseup", onUp);
window.addEventListener("touchend", onUp);

function onDown(e) {
  const p = getCanvasPos(e);
  const mx = iX(p.x), my = iY(p.y);

  if (cur === 0) {
    // 0666: 기울기 조절
    const k = K.k !== undefined ? K.k : -2;
    const hx = 2.5, hy = k * (hx - 1) - 6;
    if (Math.hypot(p.x - X(hx), p.y - Y(hy)) < 24) {
      drag = "k";
      if (e.cancelable) e.preventDefault();
    }
  } else if (cur === 1) {
    // 0667: 점 A 조절
    let a = P.a || (Math.sqrt(6) - Math.sqrt(2));
    const b = (K.k || 4) / a;
    if (Math.hypot(p.x - X(a), p.y - Y(b)) < 24) {
      drag = "a";
      if (e.cancelable) e.preventDefault();
    }
  } else if (cur === 2) {
    // 0668: 직선 S 조절
    drag = "S";
    if (e.cancelable) e.preventDefault();
  } else if (cur === 3) {
    // 0669: 점 B의 α 조절
    let alpha = P.alpha || (Math.sqrt(3) + 1);
    const beta = 2 / alpha;
    if (Math.hypot(p.x - X(alpha), p.y - Y(beta)) < 24) {
      drag = "alpha";
      if (e.cancelable) e.preventDefault();
    }
  }
}

function onMove(e) {
  if (!drag) return;
  if (e.cancelable) e.preventDefault();
  const p = getCanvasPos(e);
  const mx = iX(p.x), my = iY(p.y);

  if (drag === "k") {
    // 정점 (1, -6) 기준 기울기
    const dx = mx - 1;
    const dy = my - (-6);
    if (Math.abs(dx) > 0.1) {
      K.k = clamp(dy / dx, -8, 5);
      P.k = K.k;
      renderVar();
    }
  } else if (drag === "a") {
    P.a = clamp(mx, 0.4, 2.0);
  } else if (drag === "S") {
    K.S = clamp(Math.round(mx + my), 5, 12);
    P.S = K.S;
    renderVar();
  } else if (drag === "alpha") {
    P.alpha = clamp(mx, 1.45, 4.0);
  }
}

function onUp() {
  drag = null;
}

/* 초기화 실행 */
setMode(0);
draw();
