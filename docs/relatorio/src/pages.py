import json, re, subprocess, sys
pdf=sys.argv[1]
n=int(re.search(r"Pages:\s+(\d+)",subprocess.run(["pdfinfo",pdf],capture_output=True,text=True).stdout).group(1))
texts=[]
for i in range(1,n+1):
    t=subprocess.run(["pdftotext","-f",str(i),"-l",str(i),"-layout",pdf,"-"],capture_output=True,text=True).stdout
    texts.append(re.sub(r"\s+"," ",t))
S=json.load(open("build/structure.json"))
norm=lambda x: re.sub(r"\s+"," ",x).strip()
# start: first page without dot leaders that contains INTRODUÇÃO
start=next(i for i,t in enumerate(texts) if "INTRODUÇÃO" in t and "...." not in t)
out={}; cur=start
for i,(lvl,h) in enumerate(S["headings"]):
    key=norm(h)
    for j in range(cur,n):
        if key in texts[j]:
            out[f"H{i}"]=j  # physical index 0-based → displayed = j (since physical = j+1, displayed = physical-1)
            cur=j; break
    else:
        print("NOT FOUND heading",h)
for kind,items in S["captions"].items():
    cur=start
    for num,cap in items:
        pat=f"{kind} {num} — "
        for j in range(cur,n):
            if pat in texts[j]:
                out[f"{kind}{num}"]=j; cur=j; break
        else:
            print("NOT FOUND",pat)
json.dump(out,open("build/pages.json","w"))
print(len(out), "intro page", out.get("H0"))
