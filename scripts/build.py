#!/usr/bin/env python3
"""Generate original, self-contained profile art. Standard library only."""
import argparse
import json
import math
import hashlib
import os
from pathlib import Path
import urllib.request
from html import escape
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
INK, PAPER, RED, MUTED, LINE = '#0c0c0e', '#ede9df', '#ff482b', '#99958d', '#303033'

def text(x, y, value, size=16, color=PAPER, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'

def svg(name, width, height, body, title, description):
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}} .mono{{font-family:'Courier New',monospace}} @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect width="{width}" height="{height}" fill="{INK}"/>{body}</svg>'''
    (ASSETS / name).write_text(content + '\n')


def hero():
    b = f'''<defs>
<radialGradient id="heat"><stop stop-color="{RED}" stop-opacity=".25"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{LINE}" stroke-width=".6"/></pattern>
<style>
.spin{{animation:spin 24s linear infinite;transform-origin:964px 304px}} .reverse{{animation:spin 40s linear infinite reverse;transform-origin:964px 304px}}
.pulse{{animation:pulse 4s ease-in-out infinite}} .scan{{animation:scan 7s linear infinite}} .flicker{{animation:flicker 8s steps(1) infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}} @keyframes pulse{{50%{{opacity:.35}}}} @keyframes scan{{to{{transform:translateY(520px)}}}} @keyframes flicker{{0%,94%,98%,100%{{opacity:1}}95%,97%{{opacity:.12}}}}
</style></defs>
<rect x="700" y="65" width="540" height="465" fill="url(#grid)"/>
<circle cx="964" cy="304" r="255" fill="url(#heat)"/>
<path d="M32 68H1248M32 550H1248" stroke="{LINE}"/>
{ text(32, 40, 'A / B     EXPERIMENTAL SYSTEMS DIVISION', 13, MUTED, extra='class="mono" letter-spacing="2"') }
<circle cx="1030" cy="35" r="4" fill="{RED}" class="pulse"/>
{ text(1044, 40, 'CORE ONLINE', 13, RED, extra='class="mono" letter-spacing="2"') }
{ text(32, 121, '001 / IDENTITY', 13, MUTED, extra='class="mono" letter-spacing="2"') }
{ text(25, 262, 'AFTER', 162, PAPER, 900, 'letter-spacing="-10"') }
{ text(25, 406, 'BURNERR', 137, PAPER, 900, 'letter-spacing="-8"') }
<rect x="35" y="440" width="268" height="35" fill="{RED}"/>
{ text(48, 463, 'RUN BEYOND THE DEFAULT.', 15, INK, 700, 'class="mono"') }
{ text(35, 513, 'AI TOOLING / AUTOMATION / GAME SYSTEMS', 15, MUTED, extra='class="mono"') }
<g fill="none" stroke="{RED}">
<circle cx="964" cy="304" r="187" stroke-opacity=".35"/>
<circle cx="964" cy="304" r="165" stroke-width="2" stroke-dasharray="2 14" class="reverse"/>
<circle cx="964" cy="304" r="144" stroke-width="14" stroke-dasharray="140 86 16 86" class="spin"/>
<circle cx="964" cy="304" r="119" stroke-opacity=".4"/>
<ellipse cx="964" cy="304" rx="83" ry="119" transform="rotate(35 964 304)"/>
<ellipse cx="964" cy="304" rx="83" ry="119" transform="rotate(-35 964 304)"/>
<ellipse cx="964" cy="304" rx="119" ry="39"/>
<path d="M964 99V146M964 462V509M759 304H806M1122 304H1169"/>
</g>
<circle cx="964" cy="304" r="57" fill="{RED}" class="pulse"/>
{ text(964, 317, 'A/B', 36, INK, 900, 'text-anchor="middle" letter-spacing="-3"') }
{ text(964, 87, 'AFTERBURNER REACTOR / R-01', 10, MUTED, extra='class="mono" text-anchor="middle" letter-spacing="2"') }
{ text(964, 535, 'EXPERIMENTAL · UNCONVENTIONAL', 10, MUTED, extra='class="mono" text-anchor="middle" letter-spacing="2"') }
<rect x="723" y="74" width="497" height="1" fill="{RED}" opacity=".18" class="scan"/>
{ text(32, 597, 'BUILD TOOLS.', 28, PAPER, 800) }
{ text(32, 633, 'BREAK ROUTINES.', 28, PAPER, 800) }
{ text(600, 598, 'Go · Python · TypeScript · Java', 18, PAPER, extra='class="mono"') }
{ text(600, 630, 'From local agents to multiplayer worlds.', 16, MUTED) }
{ text(1247, 663, 'AFTERBURNERR // FIELD NOTES', 10, MUTED, extra='class="mono" text-anchor="end" letter-spacing="2"') }
'''
    svg('core.svg', 1280, 680, b, 'AFTERBURNERR — Core Overdrive', 'Animated experimental reactor. AI tooling, automation and game systems. Go, Python, TypeScript and Java.')

PROJECTS = [
    ('aftsync', '01', 'SYNC WITHOUT FRICTION.', 'Encrypted config sync. One Go binary.', 'GO / AGE / SYSTEMD', 'sync'),
    ('warehouse-dashboards', '02', 'DATA, AT INDUSTRIAL SCALE.', 'Five dashboard designs for warehouse TVs.', 'HTML / DASHBOARDS / SCADA', 'grid'),
    ('FreeDeepSeekAPI', '03', 'A DIFFERENT WAY IN.', 'Local OpenAI-compatible DeepSeek proxy.', 'PYTHON / API / DOCKER', 'wave'),
    ('TownyRaids', '04', 'WORLDS WITH CONSEQUENCES.', 'Town-vs-town raid systems for Paper.', 'JAVA / PAPER / TOWNY', 'cross'),
]

def cards():
    for name, num, headline, desc, stack, kind in PROJECTS:
        b = f'<rect x=".5" y=".5" width="619" height="239" fill="none" stroke="{LINE}"/>'
        b += text(24, 31, f'{num} / SELECTED SYSTEM', 10, MUTED, extra='class="mono" letter-spacing="1.5"')
        b += text(24, 78, name, 29 if len(name) < 19 else 25, PAPER, 800, 'letter-spacing="-1"')
        b += text(24, 117, headline, 12, RED, 700, 'class="mono"')
        b += text(24, 147, desc, 14, MUTED)
        b += f'<path d="M24 175H596" stroke="{LINE}"/>'
        b += text(24, 211, stack, 11, MUTED, extra='class="mono"')
        b += text(576, 213, '↗', 25, RED)
        if kind == 'sync':
            b += f'<g fill="none" stroke="{RED}" stroke-width="2"><path d="M525 42a22 22 0 0 1 40 16l-8-8m8 8h-12M565 80a22 22 0 0 1-40-16l8 8m-8-8h12"/></g>'
        elif kind == 'grid':
            for i in range(3):
                for j in range(3):
                    b += f'<rect x="{523+i*20}" y="{37+j*20}" width="13" height="13" fill="{RED}" opacity="{.3 + ((i+j)%3)*.3}"/>'
        elif kind == 'wave':
            b += f'<path d="M514 69h10l6-22 12 43 10-61 12 57 8-17h17" fill="none" stroke="{RED}" stroke-width="2"/>'
        else:
            b += f'<path d="M518 39l49 49m0-49-49 49M518 39v15m0-15h15m34 0h-15m15 0v15M518 88V73m0 15h15m34 0h-15m15 0V73" fill="none" stroke="{RED}" stroke-width="2"/>'
        svg(f'{name}.svg', 620, 240, b, name, f'{headline} {desc} {stack}')


def api(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'afterburnerr-profile', 'X-GitHub-Api-Version': '2022-11-28'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com/' + path, headers=headers), timeout=30) as r:
        return json.load(r)


def telemetry():
    repos = []
    for page in range(1, 101):
        batch = api(f'users/afterburnerr/repos?type=owner&per_page=100&page={page}')
        repos.extend(r for r in batch if not r.get('private') and r['name'] != 'afterburnerr')
        if len(batch) < 100:
            break
    owned = [r for r in repos if not r['fork']]
    resonance(owned)
    languages = sorted({r['language'] for r in owned if r.get('language')})
    stars = sum(r['stargazers_count'] for r in owned)
    b = text(32, 34, '002 / PUBLIC TELEMETRY', 12, MUTED, extra='class="mono" letter-spacing="2"')
    b += text(1248, 34, datetime.now(timezone.utc).strftime('SNAPSHOT %Y-%m-%d / UTC'), 11, MUTED, extra='class="mono" text-anchor="end"')
    for x, value, label in [(32, f'{len(owned):02}', 'ORIGINAL PUBLIC REPOS'), (357, f'{stars:02}', 'STARS / ORIGINAL REPOS'), (682, f'{len(languages):02}', 'PRIMARY LANGUAGES')]:
        b += text(x, 111, value, 57, PAPER, 800, 'letter-spacing="-3"')
        b += text(x, 147, label, 11, MUTED, extra='class="mono" letter-spacing="1"')
    b += text(1007, 97, 'PUBLIC', 27, RED, 800)
    b += text(1007, 129, 'SIGNAL ONLY', 17, PAPER, 700)
    b += f'<path d="M320 65V150M645 65V150M970 65V150M32 175H1248" stroke="{LINE}"/>'
    b += text(32, 202, 'SOURCE: GITHUB API / ORIGINAL REPOS / PROFILE REPO EXCLUDED / NO PRIVATE DATA', 10, MUTED, extra='class="mono"')
    svg('telemetry.svg', 1280, 225, b, 'Public repository telemetry', f'{len(owned)} original public repositories, {stars} stars, {len(languages)} primary languages. Profile repository and forks excluded.')


def resonance(repos):
    # An artistic signature, not a contribution graph or an activity metric.
    identity = '|'.join(sorted(r['name'] for r in repos))
    seed = int(hashlib.sha256(identity.encode()).hexdigest()[:8], 16)
    b = text(32, 35, '003 / REPOSITORY RESONANCE', 12, MUTED, extra='class="mono" letter-spacing="2"')
    b += text(1248, 35, f'SIGNATURE {seed:08X}', 11, RED, extra='class="mono" text-anchor="end"')
    b += '<defs><linearGradient id="signal"><stop stop-color="#ff482b" stop-opacity=".12"/><stop offset=".5" stop-color="#ff482b"/><stop offset="1" stop-color="#ede9df" stop-opacity=".3"/></linearGradient></defs>'
    b += '<style>.signal{animation:flow 8s linear infinite}@keyframes flow{to{stroke-dashoffset:-400}}</style>'
    for i in range(38):
        points = []
        for x in range(32, 1250, 6):
            t = (x-32)/1216
            envelope = math.sin(t*math.pi)**1.6
            phase = (seed%97)/13
            y = 161 + (i-18.5)*3.5 + envelope*(math.sin(t*math.pi*4+phase+i*.09)*45 + math.sin(t*math.pi*9-i*.035)*15)
            points.append(f'{x},{y:.2f}')
        b += f'<polyline points="{" ".join(points)}" fill="none" stroke="url(#signal)" stroke-width=".85" opacity=".75"/>'
        if i in (5,18,31):
            b += f'<polyline points="{" ".join(points)}" fill="none" stroke="#ede9df" stroke-width="1.2" stroke-dasharray="5 395" class="signal" style="animation-delay:-{i/3}s"/>'
    b += '<path d="M32 268H1248" stroke="#303033"/>'
    b += text(32, 299, 'GENERATIVE ART / SEEDED BY ORIGINAL PUBLIC REPOSITORY NAMES', 11, MUTED, extra='class="mono"')
    b += text(1248, 299, 'YOUR CODE. YOUR FREQUENCY.', 11, RED, extra='class="mono" text-anchor="end"')
    svg('resonance.svg', 1280, 325, b, 'Repository resonance — generative signature', 'An original animated interference field seeded by public repository names. Artistic visualization, not an activity metric.')


def footer():
    b = f'<path d="M32 15H1248" stroke="{LINE}"/>'
    for i in range(72):
        x = 32 + i * 7
        b += f'<rect x="{x}" y="38" width="{2 if i%3 else 4}" height="{25 if i%5 else 36}" fill="{RED}" opacity="{.4 if i%4 else 1}"/>'
    b += text(1248, 48, 'END OF TRANSMISSION_', 18, PAPER, 800, 'text-anchor="end" letter-spacing="1"')
    b += text(1248, 72, 'AFTERBURNERR / ALWAYS UNDER CONSTRUCTION', 10, MUTED, extra='class="mono" text-anchor="end" letter-spacing="1"')
    svg('transmission.svg', 1280, 96, b, 'End of transmission', 'AFTERBURNERR. Always under construction.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--telemetry-only', action='store_true')
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    if not args.telemetry_only:
        hero()
        cards()
        footer()
    telemetry()
