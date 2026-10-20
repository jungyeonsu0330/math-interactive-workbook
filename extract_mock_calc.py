import fitz, os, sys, io, json, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"C:\Users\Admin\Downloads\261020_수능&모의 미적분_문제지.pdf"
doc = fitz.open(pdf_path)

print("Pages:", len(doc))
# Let's inspect page 4 (quick answers) and page 5..11 (solutions)
for p_idx in range(len(doc)):
    page = doc[p_idx]
    text = page.get_text()
    imgs = page.get_images()
    print(f"Page {p_idx+1}: {len(text.strip())} chars, {len(imgs)} images")
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    print("  Lines:", lines[:10])
