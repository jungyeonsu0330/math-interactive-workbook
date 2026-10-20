import sys, io, fitz
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

books = {
    "gongsu1_main": r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형내신 고쟁이 공통수학1.pdf",
    "gongsu1_ans": r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형내신 고쟁이 공통수학1 정답 및 해설.PDF",
    "daesu_main": r"C:\Users\Admin\Documents\카카오톡 받은 파일\고쟁이 대수.pdf",
    "daesu_ans": r"C:\Users\Admin\Documents\카카오톡 받은 파일\유형,내신 고쟁이 대수 정답과 해설-1.pdf",
    "rpm_geom_main": r"C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 기하 학생용_unlocked.pdf",
    "rpm_geom_ans": r"C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 기하 정답_unlocked.pdf",
}

for name, path in books.items():
    doc = fitz.open(path)
    print(f"[{name}] pages: {len(doc)}")
    # 목차 또는 처음 몇 페이지 텍스트 샘플
    toc_sample = ""
    for p in range(min(6, len(doc))):
        t = doc[p].get_text("text").strip()
        if any(k in t for k in ["차례", "목차", "다항식", "지수", "이차곡선", "벡터"]):
            toc_sample = f"Page {p+1}:\n" + t[:300]
            break
    print(f"  TOC info: {toc_sample[:150]}...")
    print("-" * 50)
