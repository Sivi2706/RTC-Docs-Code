import re, json, hashlib, collections, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES={'WOS':str(ROOT/'Combined 1609.bib'),'IEEE':str(ROOT/'Combined IEEE 788.bib')}
startre=re.compile(r'@([a-zA-Z]+)\s*\{')
fieldre=re.compile(r'([A-Za-z][A-Za-z0-9_-]*)\s*=\s*')
def clean(s):
 s=s.strip();s=re.sub(r'[{}]','',s);s=re.sub(r'\\([&%_#])',r'\1',s);s=re.sub(r'\s+',' ',s)
 return s

def parsefile(file):
 text=Path(file).read_text(errors='replace')
 matches=list(startre.finditer(text));out=[]
 for ix,m in enumerate(matches):
  seg=text[m.end():matches[ix+1].start() if ix+1<len(matches) else len(text)]
  comma=seg.find(','); key=seg[:comma].strip(); seg=seg[comma+1:]
  fields={};p=0
  while True:
   mm=fieldre.search(seg,p)
   if not mm:break
   name=mm.group(1).lower(); p=mm.end()
   if p>=len(seg):break
   if seg[p]=='{':
    j=p+1;depth=1; in_escape=False
    while j<len(seg) and depth>0:
     c=seg[j]
     if c=='{' and not in_escape:depth+=1
     elif c=='}' and not in_escape:depth-=1
     if c=='\\':in_escape=not in_escape
     else: in_escape=False
     j+=1
    val=seg[p+1:j-1];p=j
   elif seg[p]=='"':
    j=p+1
    while j<len(seg):
     if seg[j]=='"' and seg[j-1]!='\\':break
     j+=1
    val=seg[p+1:j];p=j+1
   else:
    e=seg.find(',',p);val=seg[p:e if e>=0 else len(seg)];p=e+1 if e>=0 else len(seg)
   fields[name]=clean(val)
  fields.update({'_key':key,'_entrytype':m.group(1),'_source':file});out.append(fields)
 return out

records=[]
for tag,fn in FILES.items():
 arr=parsefile(fn)
 print('parsed',tag,len(arr),'with title',sum('title' in a for a in arr),'with abstract',sum('abstract' in a for a in arr))
 for x in arr:x['_source']=tag
 records+=arr
print('Total',len(records))

def normalized(x):
 doi=x.get('doi','').lower().strip().replace('https://doi.org/','')
 if doi:return 'doi:'+doi
 title=re.sub('[^a-z0-9]','',x.get('title','').lower())
 return 'title:'+title
bykey={}
duplicates=[]
for r in records:
 key=normalized(r)
 if key in bykey:duplicates.append((r,bykey[key]));continue
 bykey[key]=r
print('unique',len(bykey),'deduplicated',len(duplicates))

# high recall search: student/competition or actual rocket avionics, must prioritize titles
competition_pat=re.compile(r'(?i)student|competit|college|university|czech rocket|euroc|european rocketry|irec|spaceport america|teknofest|can.?sat|high.?power|model rocket|experimental rocket|solid rocket|sounding rocket|3.?km|3000 m|3000m|3,000',re.I)
avionics_pat=re.compile(r'(?i)avionic|flight computer|electronic|telemetr|data log|parachute|recovery|apogee|flight control|sensor|attitude|control system|navigation|payload|onboard|on-board|embedded|altimet|gps|tracking',re.I)
rock_pat=re.compile(r'(?i)rocket|sounding|launch vehicle|irec|euroc|teknofest|spaceport',re.I)
shortlist=[]
for r in bykey.values():
 title=r.get('title',''); abs=r.get('abstract','');txt=title+' '+abs
 if rock_pat.search(txt) and avionics_pat.search(txt):
  score=(3 if competition_pat.search(title) else 0)+(2 if avionics_pat.search(title) else 0)+(2 if competition_pat.search(abs) else 0)+(2 if re.search('(?i)3.?km|3000.?m|2[,.]?[0-9]{3} ?m|apogee|altitude',txt) else 0)
  shortlist.append((score,r))
print('rocket and avionics',len(shortlist),'competition terms in either',sum(bool(competition_pat.search(r.get('title','')+' '+r.get('abstract',''))) for _,r in shortlist))
shortlist.sort(key=lambda x:(-x[0],x[1].get('title','').lower()))
with open(ROOT/'candidate_screening.csv','w') as f:
 writer=csv.writer(f);writer.writerow(['score','source','entrykey','title','year','doi','abstract','author','url'])
 for score,r in shortlist:writer.writerow([score,r['_source'],r.get('_key'),r.get('title'),r.get('year'),r.get('doi'),r.get('abstract'),r.get('author'),r.get('url')])
with open(ROOT/'candidates.txt','w') as f:
 for score,r in shortlist:
  if score>=5:f.write(f"{score:2} {r['_source']:4} {r.get('year',''):4} {r.get('doi','')[:42]:44} {r.get('title','')}\n")
Path(ROOT/'stats.json').write_text(json.dumps({'records':len(records),'wos':1609,'ieee':788,'unique':len(bykey),'duplicates':len(duplicates),'rocket_avionics':len(shortlist),'competition_terms':sum(bool(competition_pat.search(r.get('title','')+' '+r.get('abstract',''))) for _,r in shortlist)},indent=2))
Path(ROOT/'records.json').write_text(json.dumps(list(bykey.values()),ensure_ascii=False))

# Optional figure tables (candidate terms are lexical flags, not flight evidence)
with open(ROOT/'figure_annual_counts.csv','w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['year','wos','ieee','total'])
 for year in range(2014,2027):
  subset=[r for score,r in shortlist if r.get('year','')==str(year)]
  n_w=sum(r['_source']=='WOS' for r in subset);n_i=sum(r['_source']=='IEEE' for r in subset)
  writer.writerow([year,n_w,n_i,n_w+n_i])
themes={
 'Altitude_or_navigation':r'\bimu\b|inertial|baromet|\bgps\b|\bgnss\b|altimet|navigation|attitude',
 'Telemetry_or_ground_link':r'telemetr|downlink|ground station',
 'Flight_computer_or_avionics':r'\bflight computer\b|\bavionics\b|\bonboard computer\b',
 'Recovery_or_deployment':r'parachute|recovery system|drogue|apogee|deploy',
 'Redundancy_or_faults':r'redundan|fault.toleran|fail.safe|watchdog|fault.detect',
 'Data_logging_or_storage':r'data log|data record|sd card|\bflash memory\b|black box|data acquisition',
 'Power_or_energy':r'power suppl|battery|power distribut|energy storag|supercapacitor'
}
with open(ROOT/'figure_topic_signals.csv','w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['category','match_count','denominator','regex_rule'])
 for key,pattern in themes.items():
  count=sum(bool(re.search(pattern,(r.get('title','')+' '+r.get('abstract','')),re.I)) for score,r in shortlist)
  writer.writerow([key,count,len(shortlist),pattern])
