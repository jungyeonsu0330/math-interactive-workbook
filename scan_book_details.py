import sys, io, re, fitz
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

books = {
    "gongsu1": (r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형내신 고쟁이 공통수학1.pdf", r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형내신 고쟁이 공통수학1 정답 및 해설.PDF"),
    "daesu": (r"C:\Users\Admin\Documents\카카오톡 받은 파일\고쟁이 대수.pdf", r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형,내신 고쟁이 대수 정답과 해설-1.pdf"),
    "rpm_geom": (r"C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 기하 학생용_unlocked.pdf", r"C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 기하 정답_unlocked.pdf"),
}

for name, (f_main, f_ans) in books.items():
    doc_m = fitz.open(f_main)
    doc_a = fitz.open(f_ans)
    print(f"=== {name} ===")
    print(f"Main pages: {len(doc_m)}, Ans pages: {len(doc_a)}")
    
    # 빠른 정답 페이지 찾기 (본문 뒤쪽 10페이지 검사)
    quick_ans_found = []
    for p in range(len(doc_m)-15, len(doc_m)):
        t = doc_m[p].get_text("text")
        if "빠른 정답" in t or "정답" in t:
            m = re.findall(r'(\d{3,4})\s+([①②③④⑤]|\d+)', t)
            if len(m) > 10:
                quick_ans_found.append((p+1, len(m)))
    print(f"Quick answers in main: {quick_ans_found}")
    
    # 해설지 첫 몇 페이지에서 정답 양식 확인
    ans_samples = []
    for p in range(min(5, len(doc_a))):
        t = doc_a[p].get_text("text")
        m = re.findall(r'(?:^|\n)\s*(\d{3,4})\s*[\s\S]{0,80}?(?:답|)\s*([^\n]+)', t)
        if m:
            ans_samples.extend(m[:3])
    print(f"Ans samples from solution doc: {ans_samples[:5]}")
    print()
