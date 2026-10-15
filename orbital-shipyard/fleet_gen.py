import os

TEMPLATE = "/root/.openclaw/workspace/orbital-shipyard/seg-station-walkthrough.html"
OUTDIR = "/root/.openclaw/workspace/orbital-shipyard/"
GLBDIR = "./assets/fleet/"

fleet = [
    dict(name='capital_military', page='capital-ship.html',
         title='Hard Sci-Fi Military Capital Starship', h1='MILITARY CAPITAL STARSHIP',
         sub='CAPITAL SHIP · MARS SYSTEM', hud='CAPITAL STARSHIP · FLEET', rot='station.rotation.y = Math.PI / 2;'),
    dict(name='military_starship', page='military-starship.html',
         title='Realistic Hard Sci-Fi Military Starship', h1='MILITARY STARSHIP',
         sub='MILITARY SHIP · MARS SYSTEM', hud='MILITARY STARSHIP · FLEET', rot='station.rotation.y = Math.PI / 2;'),
    dict(name='colony_starship', page='colony-ship.html',
         title='Realistic Hard Sci-Fi Colony Starship', h1='COLONY STARSHIP',
         sub='COLONY SHIP · MARS SYSTEM', hud='COLONY STARSHIP · FLEET', rot='station.rotation.y = Math.PI / 2;'),
    dict(name='seed_one_modular', page='seed-one-modular.html',
         title='Seed One Modular Starship', h1='SEED ONE MODULAR',
         sub='COLONY SHIP · MARS SYSTEM', hud='SEED ONE MODULAR · FLEET', rot='// long axis is X — already horizontal'),
    dict(name='seed_one_intergalactic', page='seed-one-intergalactic.html',
         title='Seed One Class Intergalactic Starship', h1='SEED ONE INTERGALACTIC',
         sub='INTERGALACTIC · MARS SYSTEM', hud='SEED ONE INTERGALACTIC · FLEET', rot='station.rotation.y = Math.PI / 2;'),
    dict(name='station_truss_arms', page='station-truss.html',
         title='Hard Surface Space Station Truss', h1='TRUSS STATION',
         sub='STATION TRUSS · MARS SYSTEM', hud='TRUSS STATION · FLEET', rot='station.rotation.y = Math.PI / 2;'),
    dict(name='station_photoreal_modular', page='station-photoreal.html',
         title='Photorealistic Modular Space Station', h1='PHOTOREAL MODULAR',
         sub='MODULAR STATION · MARS SYSTEM', hud='PHOTOREAL MODULAR · FLEET', rot='station.rotation.y = Math.PI / 2;'),
    dict(name='x302_fighter', page='x302-fighter.html',
         title='X-302 Stealth Fighter Jet', h1='X-302 FIGHTER',
         sub='STEALTH FIGHTER · MARS SYSTEM', hud='X-302 FIGHTER · FLEET', rot='// long axis is X — already horizontal'),
]

tpl = open(TEMPLATE).read()

for s in fleet:
    out = tpl
    out = out.replace('Realistic Hard Sci-Fi Space Station — In Orbit Above Mars', s['title'])
    out = out.replace('<h1>SEGMENTED MODULAR STATION</h1>', '<h1>' + s['h1'] + '</h1>')
    out = out.replace('<div class="sub">REALISTIC HARD SCI-FI · IN ORBIT ABOVE MARS</div>', '<div class="sub">' + s['sub'] + '</div>')
    out = out.replace('<div id="hud">HI3D SEGMENTED STATION · MARS ORBIT</div>', '<div id="hud">' + s['hud'] + '</div>')
    out = out.replace('<a href="orbital-shipyard.html">← VIEW OSY-7 ORBITAL SHIPYARD</a>', '<a href="stations.html">← FLEET</a>')
    out = out.replace("./assets/characters/mars/station_opt.glb?v=3", GLBDIR + s['name'] + '_opt.glb')
    out = out.replace('station.rotation.y = Math.PI / 2;', s['rot'])
    path = OUTDIR + s['page']
    open(path, 'w').write(out)
    print('wrote', path)
