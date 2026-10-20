import sys, io, re, fitz
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f_rpm_m = r"C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 기하 학생용_unlocked.pdf"
f_rpm_a = r"C:\Users\Admin\Documents\카카오톡 받은 파일\RPM 기하 정답_unlocked.pdf"

doc_m = fitz.open(f_rpm_m)
doc_a = fitz.open(f_rpm_a)

print("RPM Main pages:", len(doc_m))
print("RPM Ans pages:", len(doc_a))

# RPM Main 차례 확인
for p in range(min(10, len(doc_m))):
    t = doc_m[p].get_text("text").strip()
    if "차례" in t or "목차" in t or "이차곡선" in t:
        print(f"Main Page {p+1}:")
        print(t[:400])
        print("="*40)

# RPM Ans 앞부분 확인
for p in range(min(5, len(doc_a))):
    t = doc_a[p].get_text("text").strip()
    print(f"Ans Page {p+1} sample:")
    print(t[:300])
    print("="*40)
