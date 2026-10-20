import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 카카오톡 받은 파일 경로 후보
candidates = [
    r'C:\Users\Admin\Documents\카카오톡 받은 파일',
    r'C:\Users\Admin\Documents\KakaoTalk Downloads',
    r'C:\Users\Admin\Desktop',
    r'C:\Users\Admin\Downloads',
]

print("Scanning for exact Kakao files...")
keywords = ['고쟁이', 'rpm', '기하', '대수', '공통수학1', 'unlocked']

for base in candidates:
    if not os.path.exists(base):
        continue
    for root, dirs, files in os.walk(base):
        for f in files:
            f_lower = f.lower()
            if any(k in f_lower for k in keywords):
                full_path = os.path.join(root, f)
                size_mb = os.path.getsize(full_path) / (1024*1024)
                print(f"MATCH: [{size_mb:.2f} MB] {full_path}")
