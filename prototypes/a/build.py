from pathlib import Path
from html import escape
import random
random.seed(42)
P=Path(__file__).parent
ink='#262522'; paper='#eee9dd'; orange='#ec5435'
# Loose engraving lines; no external illustration or font dependency.
hatch=[]
for i in range(92):
    y=274+i*1.25
    x=606+random.randint(-8,12)
    hatch.append(f'<path d="M{x} {y:.1f}l{random.randint(17,36)} -{random.randint(3,9)}"/>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="660" viewBox="0 0 1040 660" role="img" aria-labelledby="title desc">
<title id="title">afterburnerr — здесь кто-то живёт</title>
<desc id="desc">An ink creature inhabits a paper README. Every twelve seconds it takes a repository from a pile, eats it, and spits out a tiny bug. A surreal animated profile prototype.</desc>
<defs>
<pattern id="paper" width="61" height="59" patternUnits="userSpaceOnUse"><path d="M3 11h1m13 24h1m24-18h1M8 48h1m43 4h1" stroke="#8d8576" stroke-opacity=".13"/></pattern>
<pattern id="shade" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(28)"><path d="M0 0V7" stroke="{ink}" stroke-width=".8"/></pattern>
<style>
text{{font-family:Georgia,serif;fill:{ink}}}.small{{font-family:'Courier New',monospace;font-size:12px}}.line{{fill:none;stroke:{ink};stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}}
#eye{{animation:eye 12s infinite}}#lid{{animation:blink 6s infinite;transform-origin:591px 208px}}#jaw{{animation:jaw 12s infinite;transform-origin:586px 315px}}
#food{{animation:food 12s infinite;transform-origin:300px 384px}}#arm{{animation:arm 12s infinite;transform-origin:611px 378px}}#bug{{animation:bug 12s infinite}}#breath{{animation:breathe 4s ease-in-out infinite;transform-origin:630px 415px}}
#sign{{animation:swing 8s ease-in-out infinite;transform-origin:904px 363px}}
@keyframes food{{0%,12%{{transform:translate(0,0) rotate(-8deg);opacity:1}}25%{{transform:translate(65px,-90px) rotate(12deg);opacity:1}}42%{{transform:translate(228px,-99px) rotate(-14deg);opacity:1}}49%{{transform:translate(245px,-68px) scale(.75);opacity:1}}54%,95%{{transform:translate(275px,-65px) scale(.2);opacity:0}}100%{{opacity:0}}}}
@keyframes arm{{0%,10%,95%,100%{{transform:rotate(0deg)}}25%{{transform:rotate(20deg)}}42%,55%{{transform:scale(.35,.9) rotate(20deg)}}68%{{transform:rotate(-8deg)}}}}
@keyframes jaw{{0%,30%,65%,100%{{transform:rotate(0deg)}}40%,52%{{transform:rotate(24deg)}}58%{{transform:rotate(-4deg)}}}}
@keyframes eye{{0%,15%,78%,100%{{transform:translate(0,0)}}25%,48%{{transform:translate(-10px,9px)}}62%{{transform:translate(5px,0)}}}}
@keyframes blink{{0%,43%,48%,100%{{transform:scaleY(1)}}45%{{transform:scaleY(.06)}}}}
@keyframes bug{{0%,65%{{opacity:0;transform:translate(0,0)}}66%{{opacity:1;transform:translate(0,0)}}74%{{opacity:1;transform:translate(132px,34px) rotate(75deg)}}85%,100%{{opacity:1;transform:translate(206px,89px) rotate(180deg)}}}}
@keyframes breathe{{50%{{transform:scale(1.014,1.024)}}}}
@keyframes swing{{50%{{transform:rotate(4deg)}}}}
@keyframes startle{{20%{{transform:translate(-7px,-17px) rotate(-2deg)}}40%{{transform:translate(8px,-12px) rotate(2deg)}}60%{{transform:translate(-4px,-9px)}}}}
.startled{{animation:startle .65s!important}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style></defs>
<rect width="1040" height="660" fill="{paper}"/><rect width="1040" height="660" fill="url(#paper)"/>
<path d="M29 35Q502 27 1011 39L1007 624Q510 637 31 621Z" fill="none" stroke="#c5beaf"/>
<text x="59" y="86" font-size="47" font-style="italic" letter-spacing="-2">afterburnerr</text>
<path d="M62 98q120 5 257-3" fill="none" stroke="{ink}" stroke-width="1.5"/>
<text x="64" y="120" class="small" fill="#746d60">здесь кто-то живёт.</text>
<text x="785" y="80" class="small">не кормить после релиза</text>
<path d="M956 98q-23 25-34 54m-5-16 5 17 16-10" class="line" stroke-width="1"/>
<!-- The inhabited README: a dented body, one stalk-eye, two improbable feet. -->
<g id="creature">
<g id="breath">
<path d="M586 267C563 213 610 165 652 178C676 185 671 236 690 255C706 273 712 319 705 355C731 375 718 446 691 460L579 460C537 442 533 410 548 372C522 351 538 310 566 303Z" fill="{paper}" stroke="{ink}" stroke-width="3"/>
<path d="M650 179C677 188 670 235 690 255C706 273 712 319 705 355C731 375 718 446 691 460L652 460C674 407 660 365 660 321C661 278 640 228 650 179Z" fill="url(#shade)"/>
<g stroke="{ink}" fill="none" stroke-width=".7" opacity=".65">{''.join(hatch)}</g>
<path d="M573 432q-13 34-7 57l-40 17q-13 12 37 9l30-7 7-66M667 439q19 25 11 57l24 8q20 18-13 12l-38-4-12-53" fill="{paper}" stroke="{ink}" stroke-width="3"/>
<path d="M587 257Q552 228 571 200Q583 184 610 193" fill="none" stroke="{ink}" stroke-width="20"/>
<path d="M587 257Q552 228 571 200Q583 184 610 193" fill="none" stroke="{paper}" stroke-width="14"/>
<g id="lid"><ellipse cx="591" cy="208" rx="31" ry="29" fill="{paper}" stroke="{ink}" stroke-width="3"/>
<ellipse cx="584" cy="206" rx="22" ry="23" fill="white" stroke="{ink}" stroke-width="1.5"/>
<g id="eye"><ellipse cx="578" cy="207" rx="8" ry="13" fill="{ink}"/><circle cx="576" cy="202" r="2.5" fill="white"/></g></g>
<path d="M565 279Q532 289 529 306L609 334 624 307Z" fill="{ink}"/>
<path d="M537 295l8 17 9-12 8 16 9-12 9 18 8-13 9 16 8-12" fill="{paper}"/>
<g id="jaw"><path d="M530 312Q542 353 587 355L624 331 605 319Z" fill="{paper}" stroke="{ink}" stroke-width="3"/><path d="M542 322l9-9 8 16 11-11 7 16 11-11 7 16" fill="{ink}"/>
<path d="M546 339q20 16 49 1" class="line" stroke-width="1"/></g>
<g id="arm"><path d="M611 378C546 380 470 390 340 397" fill="none" stroke="{ink}" stroke-width="12"/><path d="M611 378C546 380 470 390 340 397" fill="none" stroke="{paper}" stroke-width="7"/>
<path d="M341 395l-17-12-12 6m29 6-23 0-11 11m34-11-20 12 1 10" class="line"/></g>
</g>
</g>
<!-- Repository food, stacked like discarded paper packages. -->
<g transform="translate(127 405) rotate(-6)"><path d="M0 0h178l-4 58H-3Z" fill="#d4cbb9" stroke="{ink}" stroke-width="2"/><path d="M8 9h151m-7 9H13" stroke="#aaa08b"/><text x="16" y="39" font-size="22">TownyRaids</text></g>
<g transform="translate(152 461) rotate(4)"><path d="M0 0h208l-4 36H-3Z" fill="{paper}" stroke="{ink}" stroke-width="2"/><text x="10" y="26" font-size="17">FreeDeepSeekAPI</text></g>
<g transform="translate(131 498) rotate(-2)"><path d="M0 0h233l-4 31H-3Z" fill="#ded6c7" stroke="{ink}" stroke-width="2"/><text x="10" y="22" font-size="15">warehouse-dashboards</text></g>
<g id="food"><path d="M251 365l99-3 4 37-97 3Z" fill="{orange}" stroke="{ink}" stroke-width="2"/><path d="M261 373h82m-79 21 76-2" stroke="{ink}" stroke-width=".7"/><text x="271" y="390" font-size="20">aftsync</text></g>
<!-- Spat out bug follows an arc, then becomes part of the floor. -->
<g id="bug" transform-origin="531px 322px"><ellipse cx="531" cy="322" rx="8" ry="5" fill="{ink}"/><path d="M526 318l-4-6m9 5v-8m5 10 6-6m-16 13-5 5m10-5v9m6-10 6 5" stroke="{ink}" stroke-width="1.5"/></g>
<path d="M78 533q135-9 272 0m155 1q130-7 223-1m41 0q122 3 199-6" fill="none" stroke="{ink}" stroke-width="1.5"/>
<g id="sign"><path d="M903 358l-8 169" stroke="{ink}" stroke-width="4"/><path d="M802 360l199 11-3 65-200-12Z" fill="{paper}" stroke="{ink}" stroke-width="2"/>
<text x="819" y="390" font-size="17" transform="rotate(3 819 390)">оно иногда работает.</text><text x="814" y="413" class="small" transform="rotate(3 814 413)">причина неизвестна</text></g>
<!-- Little details reward a second look. -->
<g transform="translate(406 512) rotate(-13)"><path d="M0 0h25v21H0Z" fill="{paper}" stroke="{ink}"/><text x="4" y="15" class="small">404</text></g>
<path d="M775 168q8-13 17-3l-2 15-11 1Zm8-1v-18q3-14 12-8" class="line" stroke-width="1"/>
<text x="76" y="586" font-size="16" font-style="italic">Go, Python, TypeScript, Java. Всё идёт в одну пасть.</text>
<text x="954" y="590" class="small" text-anchor="end">рис. 01 / местная фауна</text>
</svg>'''
(P/'creature.svg').write_text(svg)
(P/'index.html').write_text('''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>afterburnerr — местная фауна</title><style>body{margin:0;background:#eee9dd;color:#262522}main{max-width:1040px;margin:12px auto}svg{width:100%;height:auto;display:block}nav{display:flex;justify-content:center;gap:12px;padding:12px;flex-wrap:wrap}button,a{border:1px solid #262522;background:transparent;color:inherit;padding:10px 16px;font:16px Georgia;cursor:pointer}button:hover{background:#262522;color:#eee9dd}p{text-align:center;font:14px Georgia;padding:0 16px}.hint{font-size:12px;color:#766e60}</style><main>'''+svg+'''<nav><button id="feed">дать ещё репозиторий</button><button id="knock">постучать по стеклу</button><button id="pause">пусть поспит</button></nav><p id="notice" aria-live="polite">Пишу штуки. Кто-то их ест.</p><p class="hint">Прототип: кнопки работают здесь. Для GitHub действия можно перенести в Issues → Actions.</p></main><script>
const svg=document.querySelector('svg');let sleeping=false;
document.querySelector('#feed').onclick=()=>{sleeping=false;svg.querySelectorAll('*').forEach(e=>e.style.animationPlayState='running');document.querySelector('#pause').textContent='пусть поспит';const food=document.querySelector('#food');food.style.animation='none';void food.getBoundingClientRect();food.style.animation='food 3s linear 1';document.querySelector('#jaw').style.animation='jaw 3s linear 1';document.querySelector('#arm').style.animation='arm 3s linear 1';document.querySelector('#bug').style.animation='bug 3s linear 1';document.querySelector('#notice').textContent='Репозиторий принят. За баги не отвечает.';setTimeout(()=>['food','jaw','arm','bug'].forEach(id=>document.getElementById(id).style.animation=''),3100)};
document.querySelector('#knock').onclick=()=>{const c=document.querySelector('#creature');c.classList.remove('startled');void c.getBoundingClientRect();c.classList.add('startled');document.querySelector('#notice').textContent='Оно тебя заметило.';setTimeout(()=>c.classList.remove('startled'),700)};
document.querySelector('#pause').onclick=e=>{sleeping=!sleeping;svg.querySelectorAll('*').forEach(n=>n.style.animationPlayState=sleeping?'paused':'running');e.target.textContent=sleeping?'разбудить':'пусть поспит';document.querySelector('#notice').textContent=sleeping?'Тихо. Пусть переварит.':'Снова голодное.'};
</script></html>''')
(P/'README.md').write_text('''# Местная фауна — вариант A\n\n![Здесь кто-то живёт](creature.svg)\n\nПишу штуки. Кто-то их ест.\n\n[Код](https://github.com/afterburnerr?tab=repositories)\n\n---\n\nЭто прототип, не новая версия опубликованного профиля. `index.html` содержит три работающие кнопки: кормить, стучать, усыплять. SVG самостоятельно проигрывает 12-секундную сцену и работает как изображение в GitHub README. Браузерные кнопки не выполняются внутри GitHub; возможная следующая версия использует Issue-команды и Actions для общего состояния существа.\n\nРисунок и анимация написаны с нуля: SVG, без внешних картинок, шрифтов и сервисов. Пересборка: `python3 build.py`.\n''')
