import re

TEMPLATE = "/root/.openclaw/workspace/orbital-shipyard/seg-station-walkthrough.html"
OUTDIR = "/root/.openclaw/workspace/orbital-shipyard/"

NAV = ('<a href="orbital-shipyard.html">OSY-7</a>'
       '<a href="seg-station.html">REALISTIC</a>'
       '<a href="seg-earth.html">SEG-EARTH</a>'
       '<a href="station-modular.html">MODULAR</a>'
       '<a href="station-rotating.html">ROTATING</a>'
       '<a href="station-detailed.html">DETAILED</a>')

stations = [
    dict(name='modular', file='station_modular_opt.glb',
         title='Realistic Sci-Fi Modular Space Station — In Orbit Above Mars',
         h1='MODULAR SPACE STATION', sub='REALISTIC SCI-FI MODULAR · IN ORBIT ABOVE MARS',
         hud='MODULAR STATION · MARS ORBIT', rot='// long axis is X — already horizontal'),
    dict(name='rotating', file='station_rotating_opt.glb',
         title='Hard Sci-Fi Rotating Space Station — In Orbit Above Mars',
         h1='ROTATING SPACE STATION', sub='HARD SCI-FI ROTATING · IN ORBIT ABOVE MARS',
         hud='ROTATING STATION · MARS ORBIT', rot='// long axis is X — already horizontal'),
    dict(name='detailed', file='station_detailed_opt.glb',
         title='Detailed Hard Sci-Fi Space Station — In Orbit Above Mars',
         h1='DETAILED SPACE STATION', sub='DETAILED HARD SCI-FI · IN ORBIT ABOVE MARS',
         hud='DETAILED STATION · MARS ORBIT', rot='station.rotation.y = Math.PI / 2;'),
]

tpl = open(TEMPLATE).read()

for s in stations:
    out = tpl
    out = out.replace('Realistic Hard Sci-Fi Space Station — In Orbit Above Mars', s['title'])
    out = out.replace('<h1>SEGMENTED MODULAR STATION</h1>', '<h1>' + s['h1'] + '</h1>')
    out = out.replace('<div class="sub">REALISTIC HARD SCI-FI · IN ORBIT ABOVE MARS</div>', '<div class="sub">' + s['sub'] + '</div>')
    out = out.replace('<div id="hud">HI3D SEGMENTED STATION · MARS ORBIT</div>', '<div id="hud">' + s['hud'] + '</div>')
    out = out.replace('<a href="orbital-shipyard.html">← VIEW OSY-7 ORBITAL SHIPYARD</a>', NAV)
    out = out.replace('./assets/characters/mars/station_opt.glb', './assets/characters/mars/' + s['file'])
    out = out.replace('station.rotation.y = Math.PI / 2;', s['rot'])
    path = OUTDIR + 'station-' + s['name'] + '.html'
    open(path, 'w').write(out)
    print('wrote', path)
