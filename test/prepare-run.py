"""Makes the recorded Playwright run in the given directory look like this job's own run.

The run was recorded elsewhere: its paths start with a placeholder, and its times are when it was
recorded. A real run is written in the job's checkout, after the checkout, and isn't committed. So
this points the paths at the directory, in the report and inside each trace, moves the times so the
run starts now, and tells git to ignore the rewritten files.
"""

import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

PLACEHOLDER = "/__KWIKQA_RUN_ROOT__"


def parse_time(value):
    # Python before 3.11 doesn't read a trailing Z.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


root = Path(sys.argv[1]).resolve()
report_path = root / "report.json"
report = json.loads(report_path.read_text().replace(PLACEHOLDER, str(root)))

# Now, rather than when the run ends: GitHub creates a pull request's merge commit moments before
# the job, and a commit made after the run started reads as one the run never saw.
shift = datetime.now(timezone.utc) - parse_time(report["stats"]["startTime"])


def move_times(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "startTime" and isinstance(value, str):
                moved = parse_time(value) + shift
                node[key] = moved.isoformat(timespec="milliseconds").replace("+00:00", "Z")
            else:
                move_times(value)
    elif isinstance(node, list):
        for item in node:
            move_times(item)


move_times(report)
# Written as Playwright writes it, so only the paths and times change.
report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

# Only entries that hold the placeholder are rewritten, so binary entries stay as they are.
traces = sorted(root.glob("test-results/*/trace.zip"))
for trace in traces:
    with zipfile.ZipFile(trace) as archive:
        entries = [(info, archive.read(info)) for info in archive.infolist()]
    with zipfile.ZipFile(trace, "w") as archive:
        for info, data in entries:
            archive.writestr(info, data.replace(PLACEHOLDER.encode(), str(root).encode()))

subprocess.run(
    ["git", "update-index", "--skip-worktree", "--", str(report_path), *map(str, traces)],
    check=True,
)
print(f"Pointed the run at {root}; it starts at {datetime.now(timezone.utc):%H:%M:%S} UTC.")
