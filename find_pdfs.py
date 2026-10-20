import os, glob

search_dirs = [
    r'C:\Users\Admin\Documents',
    r'C:\Users\Admin\Downloads',
    r'C:\Users\Admin\Desktop',
]

print("Searching for PDF files in common folders...")
for base in search_dirs:
    if not os.path.exists(base):
        continue
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.lower().endswith('.pdf'):
                fpath = os.path.join(root, f)
                size_mb = os.path.getsize(fpath) / (1024*1024)
                print(f"{size_mb:.1f} MB | {fpath}")
