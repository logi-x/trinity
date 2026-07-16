from pathlib import Path
import re

p = Path("/home/developer/resources/agent-visualization/export_data.py")
text = p.read_text()

pattern = re.compile(
    r"def note_age_days\(nid, git_recency\):.*?return max\(0, \(TODAY - max\(dates\)\)\.days\)",
    re.S,
)
replacement = '''def note_age_days(nid, git_recency):
    """Most-recent touch in days. Frontmatter `updated`/`created` vs git, whichever is newer."""
    dates = []
    g = git_recency.get(nid)
    if g and _date(g):
        dates.append(_date(g))
    path = os.path.join(VAULT, nid)
    if os.path.exists(path):
        head = read_text(path, limit=600)
        for field in ("updated", "created", "date"):
            # Accept YAML-quoted or bare ISO dates: updated: "2026-07-15" or updated: 2026-07-15
            m = re.search(
                rf"^{field}:\\s*[\\"\\']?([0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}})[\\"\\']?",
                head,
                re.M,
            )
            if m and _date(m.group(1)):
                dates.append(_date(m.group(1)))
        if not dates:
            # Fall back to filesystem mtime so brand-new uncommitted notes stay "recent"
            try:
                from datetime import datetime as _dt
                dates.append(_dt.fromtimestamp(os.path.getmtime(path)).date())
            except Exception:
                pass
    if not dates:
        return 999
    return max(0, (TODAY - max(dates)).days)'''

new_text, n = pattern.subn(replacement, text, count=1)
if n != 1:
    raise SystemExit(f"replace count={n}")
p.write_text(new_text)
print("patched ok")

# normalize frontmatter quotes on the meeting note
note = Path("/home/developer/Brain/Projects/HoWA/meetings/howa-staff-29-16-07-2026-prep.md")
t = note.read_text()
t = t.replace('updated: "2026-07-15"', "updated: 2026-07-15", 1)
t = t.replace('date: "2026-07-16"', "date: 2026-07-16", 1)
note.write_text(t)
print("frontmatter normalized")
