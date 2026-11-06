#!/usr/bin/env python3
"""Render confirmed resume JSON into self-contained HTML (Python standard library)."""
import argparse,base64,html,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def esc(x):
 if not isinstance(x,str):raise ValueError('Text fields must be strings')
 return html.escape(x,quote=True)
def contact(text):
 parts=re.split(r'(https?://[^\s<>｜]+)',text)
 return ''.join('<a href="'+esc(x)+'">'+esc(x)+'</a>' if re.match(r'^https?://',x) else esc(x) for x in parts)
def bullet(b):
 if isinstance(b,str):return esc(b)
 text=b['text'];marks=b.get('emphasis',[])
 if len(marks)>2 or any(not isinstance(m,str) or not m or m not in text for m in marks):
  raise ValueError('Each bullet allows at most two nonempty emphasis phrases from its text')
 if not marks:return esc(text)
 if any(a!=b and a in b for a in marks for b in marks):raise ValueError('Emphasis phrases must not overlap')
 if any(text.count(m)!=1 for m in marks):raise ValueError('Emphasis phrases must occur once')
 if any(len(m)>=len(text) for m in marks):raise ValueError('Emphasize a short phrase, not the whole bullet')
 pat='('+ '|'.join(re.escape(m) for m in sorted(marks,key=len,reverse=True))+')'
 return ''.join('<strong>'+esc(x)+'</strong>' if x in marks else esc(x) for x in re.split(pat,text))
def render(data,base,theme=None,photo=None,draft=False,no_photo=False):
 themes=json.loads((ROOT/'assets/resume/themes.json').read_text())
 key=theme or data.get('theme','teal')
 if key not in themes:raise ValueError('Unknown theme: '+str(key))
 colors=themes[key];css=(ROOT/'assets/resume/resume.css').read_text()
 lines=data.get('contact_lines',[])
 links=data.get('contact_links',[])
 if not isinstance(lines,list) or not isinstance(links,list) or len(lines)+bool(links)>3:raise ValueError('Contact information accepts up to three lines')
 if len(links)>3:raise ValueError('contact_links accepts up to three links')
 head='<div class="identity-text"><h1>'+esc(data['name'])+'</h1><div class="name-line"></div>'
 if data.get('target'):head+='<div class="target">'+esc(data['target'])+'</div>'
 head+=''.join('<p class="contact">'+contact(x)+'</p>' for x in lines)
 if links:
  anchors=[]
  for item in links:
   url=item['url'];label=item['label']
   if not isinstance(url,str) or not re.match(r'^https?://[^\s<>]+$',url):raise ValueError('Contact links require an HTTP(S) URL')
   anchors.append('<a href="'+esc(url)+'">'+esc(label)+'</a>')
  head+='<p class="contact contact-links">'+' ｜ '.join(anchors)+'</p>'
 head+='</div>'
 use_photo=not no_photo and data.get('show_photo',True)
 photo_path=photo or data.get('photo')
 if use_photo:
  if photo_path:
   p=Path(photo_path);p=p if p.is_absolute() else base/p
   raw=p.read_bytes()
   if raw.startswith(b'\x89PNG\r\n\x1a\n'):mime='image/png'
   elif raw.startswith(b'\xff\xd8\xff'):mime='image/jpeg'
   else:raise ValueError('Photo must be PNG or JPEG')
   src='data:'+mime+';base64,'+base64.b64encode(raw).decode()
   head+='<div class="photo"><img alt="证件照" src="'+src+'"></div>'
  elif draft:head+='<div class="photo"><div class="photo-placeholder">证件照待补</div></div>'
  else:raise ValueError('Provide a photo, choose --draft, or explicitly use --no-photo')
 body='<header class="identity">'+head+'</header>'
 for sec in data['sections']:
  body+='<section class="section"><h2>'+esc(sec['title'])+'</h2>'
  for ent in sec['entries']:
   name=ent.get('name','');date=ent.get('date','');lines=ent.get('lines',[])
   if not name and not lines:raise ValueError('Entry needs a name or labeled lines')
   if date and not name:raise ValueError('Dated entry needs a name')
   body+='<div class="entry'+(' allow-split' if ent.get('split_across_pages',False) else '')+'">'
   if name:
    body+='<div class="entry-heading'+(' has-date' if date else '')+'">'
    if date:body+='<span class="date">'+esc(date)+'</span>'
    body+='<span class="entry-name">'+esc(name)+'</span></div>'
   if ent.get('meta'):
    meta=ent['meta'];parts=re.split('[:：]',meta,maxsplit=1)
    formatted='<span class="meta-label">'+esc(parts[0])+'：</span>'+esc(parts[1].strip()) if len(parts)==2 else esc(meta)
    body+='<div class="meta">'+formatted+'</div>'
   for row in lines:
    body+='<p class="skill-line"><strong>'+esc(row['label'].rstrip('：:'))+'：</strong>'+esc(row['text'])+'</p>'
   if ent.get('bullets'):body+='<ul>'+''.join('<li>'+bullet(b)+'</li>' for b in ent['bullets'])+'</ul>'
   body+='</div>'
  body+='</section>'
 fit_js=(ROOT/'assets/resume/fit.js').read_text()
 style=':root{--light:'+colors['light']+';--accent:'+colors['accent']+';}'+css
 return '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(data['name'])+' · 简历</title><style>'+style+'</style></head><body><main class="resume" data-theme="'+key+'">'+body+'</main><aside class="layout-report" role="status">正在计算适合内容的字号…</aside><script>'+fit_js+'</script></body></html>'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('output',type=Path)
 p.add_argument('--theme',choices=['teal','green','pink','yellow','blue']);p.add_argument('--photo');p.add_argument('--draft',action='store_true');p.add_argument('--no-photo',action='store_true')
 a=p.parse_args()
 try:
  result=render(json.loads(a.input.read_text(encoding='utf-8')),a.input.parent,a.theme,a.photo,a.draft,a.no_photo)
  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(result,encoding='utf-8')
 except (ValueError,KeyError,TypeError,OSError) as e:p.error(str(e))
 print(a.output)
if __name__=='__main__':main()
