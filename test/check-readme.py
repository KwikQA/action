"""Checks that the README's Inputs table lists exactly the inputs action.yml declares.

action.yml is the source of truth for the Action's inputs; the README repeats them. Run by the Test
workflow on every pull request: python3 test/check-readme.py
"""

import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
action = (root / "action.yml").read_text()
readme = (root / "README.md").read_text()

inputs_block = action.split("\ninputs:\n", 1)[1].split("\nruns:\n", 1)[0]
declared = re.findall(r"^  ([a-z][a-z0-9-]*):$", inputs_block, re.M)
table = readme.split("\n## Inputs\n", 1)[1].split("\n## ", 1)[0]
documented = re.findall(r"^\| `([a-z][a-z0-9-]*)` \|", table, re.M)

problems = []
for name in declared:
    if name not in documented:
        problems.append(f"action.yml declares `{name}`, but the README's Inputs table doesn't list it")
for name in documented:
    if name not in declared:
        problems.append(f"the README lists `{name}`, which action.yml doesn't declare")
if set(documented) == set(declared) and documented != declared:
    problems.append("the README lists the inputs in a different order from action.yml")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"The README documents all {len(declared)} inputs of action.yml.")
