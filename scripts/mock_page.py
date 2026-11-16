"""Build a mock T3 Code page that uses a theme, for screenshots.

Usage: python3 mock_page.py <theme.json> <idle|working> <speed> <out.html>
The page uses the stable theme hooks from AGENTS.md and the dark palette from the theme.
speed > 1 divides every animation duration, so a GIF shows motion.
"""
import json,re,sys
theme=json.load(open(sys.argv[1])); css=theme["css"]; status=sys.argv[2]; speed=float(sys.argv[3]); out=sys.argv[4]
if speed!=1:
    css=re.sub(r'animation(-duration)?:[^;}]*',lambda m:re.sub(r'(?<![\w.-])(\d*\.?\d+)s\b',lambda n:f"{float(n.group(1))/speed:g}s",m.group(0)),css)
base=''':root{--sidebar:SIDEBAR}html,body{margin:0;height:100%}
body{font:14px/1.5 -apple-system,system-ui,sans-serif;background:CANVAS;color:#f5f5f5;display:flex;height:720px}
[data-slot=sidebar]{width:250px;flex:none;display:flex}
[data-slot=sidebar-inner]{flex:1;background:SIDEBAR;border-right:1px solid SBORDER;padding:14px 10px;box-sizing:border-box}
h6{margin:4px 8px 10px;font-size:11px;color:SMUTED;font-weight:600;text-transform:uppercase;letter-spacing:.06em}
[data-thread-item]{list-style:none;padding:1px 0}
[data-sidebar-row]{padding:7px 22px 7px 10px;border-radius:7px;color:#c6ced8;font-size:13px}
[data-sidebar-row][aria-current=page]{background:SACTIVE;color:#fff}
main{flex:1;display:flex;flex-direction:column;min-width:0}
[data-chat-header]{position:relative;height:44px;flex:none;display:flex;align-items:center;padding:0 18px;font-size:13px;color:#ccc;background:CANVAS}
[data-workspace-area=conversation]{position:relative;flex:1;display:flex;flex-direction:column;background:CANVAS;min-height:0}
.messages-timeline-scroll{flex:1;overflow:auto;padding:28px 16%}
.msg{background:MSG;border-radius:12px;padding:10px 14px;margin:0 0 18px auto;width:fit-content;max-width:70%}
.asst{margin:0 0 18px;color:#e5e5e5;max-width:64ch}.tool{font:12px ui-monospace,monospace;color:#8a8a8a;margin:0 0 18px}
form{padding:0 16% 18px}[data-slot=composer-host]{background:SURFACE;border:1px solid BORDER;border-radius:14px;height:84px;padding:12px 14px;box-sizing:border-box;color:#667}
'''
P=theme.get('variants',{}).get('dark',theme['colors'])
for k,v in dict(SIDEBAR='sidebar',CANVAS='canvas',SBORDER='sidebarBorder',SMUTED='sidebarMutedForeground',SACTIVE='sidebarRowActive',MSG='messageSurface',SURFACE='surface',BORDER='border').items(): base=base.replace(k,P[v])
cur='Working' if status=='working' else 'Completed'
ICON='<img src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 16 16\'%3E%3Cpath d=\'M8 1l6 4v6l-6 4-6-4V5z\' fill=\'%23000\'/%3E%3C/svg%3E" style="width:14px;height:14px;vertical-align:-2px;margin-right:6px">'
rows=[('Add a settings page',cur,True),('Fix flaky login test','Awaiting Input',False),('Write release notes','Completed',False),('Refactor auth module','Failed',False),('Plan the billing work','Plan Ready',False),('Update dependencies','Working',False)]
side=''.join(f'<li data-thread-item><div data-sidebar-row aria-label="{t}, {s}, demo-app"{" aria-current=page" if c else ""}>{ICON}{t}</div></li>' for t,s,c in rows)
html=f'''<!doctype html><html class="dark"><head><meta charset="utf-8"><style>{base}{css}</style></head><body>
<div data-slot="sidebar"><div data-slot="sidebar-inner"><h6>Threads</h6><ul style="margin:0;padding:0">{side}</ul></div></div>
<main><header data-chat-header>Add a settings page</header><div data-workspace-area="conversation"><div class="messages-timeline-scroll">
<div class="msg">Add a settings page with a dark mode toggle.</div>
<div class="asst">I will add a <b>Settings</b> route, a toggle component and a stored preference. First I will read the current router setup.</div>
<div class="tool">✓ Read src/router.tsx · ✓ Edited src/pages/Settings.tsx · ✓ Ran pnpm test</div>
<div class="asst">The page is in place. The toggle saves the choice and applies it on the next load.</div>
</div></div><form data-chat-composer-form><div data-slot="composer-host">Ask for follow-up changes</div></form></main></body></html>'''
open(out,'w').write(html)
