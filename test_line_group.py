import fitz, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

doc = fitz.open(r'C:\Users\Admin\Documents\카카오톡 받은 파일\고쟁이 대수.pdf')
p = doc[33]

blocks = p.get_text('blocks')
content_blocks = [b for b in blocks if 50 <= b[1] <= 805 and '저작권법' not in b[4] and '대수' not in b[4]]

# 119번 블록들: y0 < 425
p119_blocks = [b for b in content_blocks if b[0] < 310 and b[1] < 425]

# Line grouping
lines = []
for b in sorted(p119_blocks, key=lambda x: (x[1], x[0])):
    text = b[4].strip()
    if not text: continue
    placed = False
    for l in lines:
        if abs(l[0]['y0'] - b[1]) <= 8:
            l.append({'x0': b[0], 'y0': b[1], 'text': text})
            placed = True
            break
    if not placed:
        lines.append([{'x0': b[0], 'y0': b[1], 'text': text}])

print("=== Reconstructed Lines for Problem 119 ===")
full_text = []
for l in sorted(lines, key=lambda l: l[0]['y0']):
    l_sorted = sorted(l, key=lambda x: x['x0'])
    line_str = " ".join([x['text'] for x in l_sorted])
    full_text.append(line_str)
    print(line_str)

full_combined = "\n".join(full_text)
print("\n=== Split by ▶ ===")
parts = full_combined.split('▶')
print("Q_TEXT:")
print(parts[0])
if len(parts) > 1:
    print("SOL_TEXT:")
    print(parts[1])
