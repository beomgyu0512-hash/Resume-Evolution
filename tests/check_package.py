from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
s=root/'skills/resume-evidence'
assert (s/'SKILL.md').is_file()
for p in s.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' not in link:
   assert (p.parent/link).exists(), (p,link)
t=(s/'references/scoring.md').read_text()
weights=[int(x) for x in re.findall(r'\|\s*(\d+)\s*\|',t)]
assert weights==[30,25,25,15,5],weights
assert sum(weights)==100
assert 'name: resume-evidence' in (s/'SKILL.md').read_text()
print('PASS: structure, local references, scoring weights')
