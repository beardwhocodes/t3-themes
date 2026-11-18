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
body{font:14px/1.5 -apple-system,system-ui,sans-serif;background:CANVAS;color:TEXT;display:flex;height:720px}
[data-slot=sidebar]{width:250px;flex:none;display:flex}
[data-slot=sidebar-inner]{flex:1;background:SIDEBAR;border-right:1px solid SBORDER;padding:14px 10px;box-sizing:border-box}
h2{margin:4px 8px 10px;font-size:11px;color:SMUTED;font-weight:600;text-transform:uppercase;letter-spacing:.06em}
[data-thread-item]{list-style:none;padding:1px 0}
[data-sidebar-row]{display:block;padding:7px 22px 7px 10px;border-radius:7px;color:STEXT;font-size:13px;text-decoration:none}
[data-sidebar-row][aria-current=page]{background:SACTIVE}
main{flex:1;display:flex;flex-direction:column;min-width:0}
[data-chat-header]{position:relative;height:44px;flex:none;display:flex;align-items:center;padding:0 18px;color:TOOLBAR;background:CANVAS}
[data-chat-header] h1{font-size:13px;font-weight:400;margin:0}
[data-workspace-area=conversation]{position:relative;flex:1;display:flex;flex-direction:column;background:CANVAS;min-height:0}
.messages-timeline-scroll{flex:1;overflow:auto;padding:28px max(14px,calc((100% - 640px)/2))}
.msg{background:MSG;color:MSGTEXT;border-radius:12px;padding:10px 14px;margin:0 0 18px auto;width:fit-content;max-width:70%}
.asst{margin:0 0 18px;max-width:64ch}.tool{font:12px ui-monospace,monospace;color:LABEL;margin:0 0 18px}
form{padding:0 max(14px,calc((100% - 640px)/2)) 18px}
[data-slot=composer-host]{background:SURFACE;border:1px solid BORDER;border-radius:14px;height:84px;padding:12px 14px;box-sizing:border-box}
textarea{display:block;background:none;border:0;color:inherit;font:inherit;width:100%;resize:none}
textarea::placeholder{color:PLACEHOLDER;opacity:1}
:focus-visible{outline:2px solid FOCUS;outline-offset:2px}
'''
P=theme.get('variants',{}).get('dark',theme['colors'])
roles = dict(
    SIDEBAR='sidebar', CANVAS='canvas', SBORDER='sidebarBorder',
    SMUTED='sidebarMutedForeground', SACTIVE='sidebarRowActive',
    STEXT='sidebarForeground', TOOLBAR='toolbarForeground', MSGTEXT='messageForeground',
    TEXT='text', MSG='messageSurface', SURFACE='surface', BORDER='border',
    LABEL='secondaryLabel', PLACEHOLDER='placeholder', FOCUS='focus',
)
base = re.sub(r'\b[A-Z]+\b', lambda match: P[roles[match[0]]], base)
cur='Working' if status=='working' else 'Completed'
ICON='<img alt="" src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 16 16\'%3E%3Cpath d=\'M8 1l6 4v6l-6 4-6-4V5z\' fill=\'%23000\'/%3E%3C/svg%3E" style="width:14px;height:14px;vertical-align:-2px;margin-right:6px">'
rows=[('Add a settings page',cur,True),('Fix flaky login test','Awaiting Input',False),('Write release notes','Completed',False),('Refactor auth module','Failed',False),('Plan the billing work','Plan Ready',False),('Update dependencies','Working',False)]
side=''.join(f'<li data-thread-item><a href="#conversation" data-sidebar-row aria-label="{t}, {s}, demo-app"{" aria-current=page" if c else ""}>{ICON}{t}</a></li>' for t,s,c in rows)
html=f'''<!doctype html><html lang="en" class="dark"><head><meta charset="utf-8"><title>Deep Field preview</title><style>{base}{css}</style></head><body>
<nav aria-label="Threads" data-slot="sidebar"><div data-slot="sidebar-inner"><h2>Threads</h2><ul style="margin:0;padding:0" role="list">{side}</ul></div></nav>
<main><header data-chat-header><h1>Add a settings page</h1></header><div id="conversation" data-workspace-area="conversation"><div class="messages-timeline-scroll">
<div data-timeline-row-kind="message" data-message-role="user"><div class="msg">Add a settings page with a dark mode toggle.</div></div>
<div class="chat-markdown asst" data-timeline-row-kind="message" data-message-role="assistant">I will add a <b>Settings</b> route, a toggle component and a stored preference. First I will read the current router setup.</div>
<div class="tool" data-timeline-row-kind="work">✓ Read src/router.tsx · ✓ Edited src/pages/Settings.tsx · ✓ Ran pnpm test</div>
<div class="chat-markdown asst" data-timeline-row-kind="message" data-message-role="assistant">The page is in place. The toggle saves the choice and applies it on the next load.</div>
</div></div><form data-chat-composer-form><div data-slot="composer-host"><textarea class="composer-tiptap" aria-label="Message" placeholder="Ask for follow-up changes"></textarea></div></form></main></body></html>'''
open(out,'w').write(html)
