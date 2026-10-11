h=open('head3.html').read().replace('</style>', """.links{border:1.5px solid var(--accent-2);border-radius:10px;padding:10px 16px;background:var(--surface)}
.links>summary{cursor:pointer;font-family:var(--display);font-weight:800;color:var(--accent);letter-spacing:.06em;text-transform:uppercase;font-size:.95rem}
.links>summary small{font-family:var(--body);font-weight:500;text-transform:none;letter-spacing:0;color:var(--muted);font-size:.8rem;margin-left:6px}
.links[open]>summary{margin-bottom:12px}
.links .note{margin-top:10px}
.lkc{background:var(--bg)}
.links .lk{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:12px}
.lkc{border:1px solid var(--line);border-radius:10px;padding:12px 14px;display:grid;gap:6px;align-content:start}
.lkc h3{margin:0 0 2px}
.lkc a{color:var(--accent-2);font-weight:600;font-size:.88rem;text-decoration:none;overflow-wrap:anywhere}
.lkc a:hover{text-decoration:underline}
</style>""",1)
b=open('body3.html').read().replace('__LOGO__',open('../logo.datauri').read().strip())

a=open('app3.js').read().replace('__ROSTER__',open('roster.json').read())
open('leaderboard-cl2026.html','w').write(h+b+'<script>\n'+a+'\n</script>\n'); print('comite ok')
