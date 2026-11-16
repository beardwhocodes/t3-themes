"""Build a mock T3 Code page that uses a theme, for screenshots.

Usage: python3 mock_page.py <theme.json> <idle|working> <speed> <out.html>
speed > 1 divides every animation duration, so a GIF shows motion.
"""
import json,re,sys
theme=json.load(open(sys.argv[1])); status=sys.argv[2]; speed=float(sys.argv[3]); out=sys.argv[4]
css=theme['css']
if speed!=1:
    def sc(m):
        return re.sub(r'(?<![\w.-])(\d+(?:\.\d+)?)s\b', lambda n: f"{float(n.group(1))/speed:g}s", m.group(0))
    css=re.sub(r'animation(-duration)?\s*:[^;}]*', sc, css)
base='''html,body{margin:0;height:100%}
body{font:14px/1.5 -apple-system,system-ui,sans-serif;background:#0a0a0a;color:#f5f5f5;display:flex;height:720px}
aside{width:250px;background:#050505;border-right:1px solid #161616;padding:14px 10px;box-sizing:border-box}
aside h6{margin:4px 8px 10px;font-size:11px;color:#777;font-weight:600;text-transform:uppercase;letter-spacing:.06em}
[data-sidebar-row]{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:7px;color:#bbb;font-size:13px}
[data-sidebar-row][aria-current=page]{background:#161616;color:#fff}
.dot{width:7px;height:7px;border-radius:50%;background:#444}.w .dot{background:#5b9cff;box-shadow:0 0 6px #5b9cff}
main{flex:1;display:flex;flex-direction:column;min-width:0}
header{height:44px;border-bottom:1px solid #161616;display:flex;align-items:center;padding:0 18px;font-size:13px;color:#ccc}
[data-workspace-area="conversation"]{position:relative;flex:1;display:flex;flex-direction:column;background:#0a0a0a;min-height:0}
.timeline{padding:28px 16%}.msg{background:#161616;border-radius:12px;padding:10px 14px;margin:0 0 18px auto;width:fit-content;max-width:70%}
.asst{margin:0 0 18px;color:#e5e5e5;max-width:64ch}
.tool{font:12px ui-monospace,monospace;color:#8a8a8a;margin:0 0 18px}
.composer{margin:0 16% 18px;background:#111;border:1px solid #1d1d1d;border-radius:14px;height:84px;padding:12px 14px;box-sizing:border-box;color:#666}
'''
cur='Working' if status=='working' else 'Completed'
html=f'''<!doctype html><html class="dark"><head><meta charset="utf-8"><style>{base}
{css}</style></head><body><aside><h6>Threads</h6>
<div data-thread-item><div data-sidebar-row aria-current="page" aria-label="Add a settings page, {cur}, demo-app" class="{'w' if status=='working' else ''}"><span class="dot"></span>Add a settings page</div></div>
<div data-thread-item><div data-sidebar-row aria-label="Fix flaky login test, Completed, demo-app"><span class="dot"></span>Fix flaky login test</div></div>
<div data-thread-item><div data-sidebar-row aria-label="Write release notes, Completed, demo-app"><span class="dot"></span>Write release notes</div></div>
</aside><main><header>Add a settings page</header><div data-workspace-area="conversation"><div class="timeline">
<div class="msg">Add a settings page with a dark mode toggle.</div>
<div class="asst">I will add a <b>Settings</b> route, a toggle component and a stored preference. First I will read the current router setup.</div>
<div class="tool">✓ Read src/router.tsx · ✓ Edited src/pages/Settings.tsx · ✓ Ran pnpm test</div>
<div class="asst">The page is in place. The toggle saves the choice and applies it on the next load.</div>
</div></div><div class="composer">Ask for follow-up changes</div></main></body></html>'''
open(out,'w').write(html)
