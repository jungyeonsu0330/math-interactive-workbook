import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

roots = [
    r'C:\Users\Admin\Documents',
    r'C:\Users\Admin\Downloads',
    r'C:\Users\Admin\Desktop',
]

targets = ['유형내신', '고쟁이 대수', '고쟁이', 'rpm 기하', 'rpm']

found = []
for root_dir in roots:
    if not os.path.exists(root_dir):
        continue
    for r, d, files in os.walk(root_dir):
        for f in files:
            name = f.lower()
            if any(t in name for t in ['고쟁이 대수', '공통수학1', 'rpm 기하', '기하 학생용', '기하 정답']):
                found.append(os.path.join(r, f))

print(f"Found {len(found)} target files:")
for f in found:
    size = os.path.getsize(f) / (1024*1024)
    print(f"[{size:.2f} MB] {f}")
