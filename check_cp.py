import fitz

doc1 = fitz.open(r'C:\Users\Admin\.gemini\antigravity-ide\brain\b0f952ba-0320-493c-8d4e-9b48723e3c2d\.user_uploaded\media_1792448127372.pdf')
txt = doc1[186].get_text('text')
idx = txt.find('"#')
sub = txt[idx:idx+15]
print("repr:", repr(sub))
for ch in sub:
    print(ch, hex(ord(ch)))
