import zipfile, re, sys
src,dst=sys.argv[1],sys.argv[2]
z=zipfile.ZipFile(src)
names=z.namelist()
rels=z.read('word/_rels/document.xml.rels').decode()
xml=''.join(z.read(n).decode('utf8','ignore') for n in names if n.startswith('word/') and n.endswith('.xml') and '_rels' not in n)
used=set(re.findall(r'r:(?:embed|id|link)="([^"]+)"',xml))
drop_ids=[]; drop_files=set()
for m in re.finditer(r'<Relationship [^>]*?Id="([^"]+)"[^>]*?/>',rels):
    tag=m.group(0); rid=m.group(1)
    if 'relationships/image' in tag and rid not in used:
        drop_ids.append(tag); drop_files.add('word/'+re.search(r'Target="([^"]+)"',tag).group(1))
for t in drop_ids: rels=rels.replace(t,'')
# keep files referenced by other rels (headers etc.)
other=''.join(z.read(n).decode() for n in names if n.endswith('.rels') and n!='word/_rels/document.xml.rels')
drop_files={f for f in drop_files if f.split('/')[-1] not in other}
out=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
for n in names:
    if n in drop_files: continue
    data=rels.encode() if n=='word/_rels/document.xml.rels' else z.read(n)
    out.writestr(z.getinfo(n),data)
out.close(); print('dropped',len(drop_files))
