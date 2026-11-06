"""Run from project root: python3 tests/test_layout.py"""
import importlib.util,json,tempfile,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=root/'skills/resume-evolution'
spec=importlib.util.spec_from_file_location('layout',s/'scripts/render_resume.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
d=json.loads((root/'examples/layout-input.json').read_text())
d.pop('photo',None)
for key,c in json.loads((s/'assets/resume/themes.json').read_text()).items():
 out=m.render(d,root,theme=key,draft=True)
 assert c['light'] in out and c['accent'] in out
 assert '<strong>领导罗德岛医疗项目</strong>' in out
 assert '证件照待补' in out
assert 'data-theme="teal"' in m.render(d,root,draft=True)
try:m.render(d,root)
except ValueError:pass
else:raise AssertionError('Missing photo must not become a final photo version')
assert 'class="photo"' not in m.render(d,root,no_photo=True)
evil=dict(d,name='<script>alert(1)</script>',contact_lines=['https://example.com/portfolio','<img src=x onerror=alert(1)>'])
out=m.render(evil,root,no_photo=True)
assert '<script>alert(1)</script>' not in out and '<img src=x' not in out
assert 'href="https://example.com/portfolio"' in out
try:m.bullet({'text':'abc def ghi','emphasis':['abc','def','ghi']})
except ValueError:pass
else:raise AssertionError('Three emphasis phrases accepted')
try:m.bullet({'text':'abc','emphasis':['abc']})
except ValueError:pass
else:raise AssertionError('Whole bullet emphasized')
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'photo.png';p.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aRZkAAAAASUVORK5CYII='))
 out=m.render(d,root,photo=str(p));assert 'data:image/png;base64,' in out and '证件照待补' not in out
css=(s/'assets/resume/resume.css').read_text()
for x in ['size:A4','margin:12mm 14mm','font-size:10.5pt','width:27mm','height:36mm','break-inside:avoid']:
 assert x in css,x
print('PASS: five themes, default, photo handling, escaping, links, emphasis and geometry tokens')

structured=dict(d,sections=[{'title':'技能','entries':[{'lines':[{'label':'编程与环境','text':'Python、Linux'}]}]},{'title':'教育经历','entries':[{'name':'示例大学','date':'2023.09—2027.06','meta':'专业：机械工程','bullets':['一条说明'],'split_across_pages':True}]}])
out=m.render(structured,root,no_photo=True)
assert '<strong>编程与环境：</strong>' in out
assert 'entry allow-split' in out and 'entry-heading has-date' in out
assert out.index('2023.09—2027.06')<out.index('示例大学')
assert '<span class="meta-label">专业：</span>' in out
assert '（预计毕业）' not in out
print('PASS: labeled skill lines, date-first reading order, meta labels and long entry pagination')

linked=dict(d,contact_lines=['电话与邮箱'],contact_links=[{'label':'GitHub · demo','url':'https://github.com/demo?tab=repositories'}])
out=m.render(linked,root,no_photo=True)
assert '<a href="https://github.com/demo?tab=repositories">GitHub · demo</a>' in out
try:m.render(dict(linked,contact_links=[{'label':'bad','url':'javascript:alert(1)'}]),root,no_photo=True)
except ValueError:pass
else:raise AssertionError('Unsafe link scheme accepted')
print('PASS: short contact link labels preserve complete destinations')
