from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
s=root/'skills/resume-evolution'
assert (s/'SKILL.md').is_file()
for p in s.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' not in link:
   assert (p.parent/link).exists(), (p,link)
t=(s/'references/scoring.md').read_text()
weights=[int(x) for x in re.findall(r'\|\s*(\d+)\s*\|',t)]
assert weights==[30,25,25,15,5],weights
assert sum(weights)==100
assert 'name: resume-evolution' in (s/'SKILL.md').read_text()
assert 'awaiting_confirmation' in (s/'SKILL.md').read_text()
assert '对下列几点，分别用自然语言描述掌握你的掌握/了解程度' in (s/'references/confirmation.md').read_text()
assert '独立重新计算' in (s/'references/scoring.md').read_text()
print('PASS: structure, references, weights, confirmation and scoring contracts')

