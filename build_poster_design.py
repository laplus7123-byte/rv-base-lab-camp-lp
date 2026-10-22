"""Current design entrypoint: an original high-impact camper repair poster."""
from pathlib import Path
import runpy
from lxml import html,etree
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'build_garage_design.py'))
p=ROOT/'dist/index.html';doc=html.fromstring(p.read_text())
hero=doc.xpath('//section[contains(@class,"garage-hero")]')[0]
lane=hero.xpath('./div[@class="camper-lane"]')[0]
hero.remove(lane)
new=html.fromstring('''<section class="garage-hero poster-hero" aria-labelledby="poster-title"><div class="poster-panel"><div class="poster-color" aria-hidden="true"></div><div class="poster-scenery" aria-hidden="true"><svg viewBox="0 0 1440 120" preserveAspectRatio="none"><path d="M0 120V97L70 75L135 90L215 43L301 83L365 65L430 106L520 75L620 100L710 83L800 105L890 75L980 90L1080 48L1150 78L1220 55L1330 95L1440 75V120Z"/><path d="M43 112V76H25L47 42H36L60 5L84 42H73L95 76H77V112ZM170 120V90H157L175 62H166L186 30L206 62H197L215 90H201V120ZM1198 120V80H1180L1204 43H1192L1218 3L1244 43H1232L1256 80H1238V120ZM1365 120V94H1350L1370 63H1360L1382 29L1404 63H1394L1414 94H1400V120Z"/></svg></div><div class="poster-heading"><p>旅する愛車の、かかりつけ。</p><h1 id="poster-title">キャンピングカー修理</h1></div><p class="poster-english">CAMPER REPAIR<br>& MAINTENANCE</p><div class="poster-wordmark" aria-hidden="true"><span>RV BASE</span><span>Lab.</span></div><div class="poster-rule" aria-hidden="true"></div><p class="poster-tagline">直して、整えて。<br>また、旅に出よう。</p><img class="poster-mechanic" src="assets/rv-mechanic-ink-v2.png" width="1024" height="1280" alt="黒い作業着で工具を持つ、RV BASE Labオリジナルの整備士キャラクター" fetchpriority="high"><span class="poster-location">CHIBA / KIMITSU</span></div><div class="poster-follow"><a class="poster-consult" href="https://lin.ee/bryjnk0" target="_blank" rel="noopener noreferrer"><span>愛車のこと、相談する</span><b>↗</b></a><a class="poster-menu" href="#service">整備メニューを見る ↓</a></div></section>''')
new.append(lane)
hero.getparent().replace(hero,new)
headerbrand=doc.xpath('//header//a[contains(@class,"brand")]')[0]
brand=html.fromstring('''<a class="poster-brand" href="#top" aria-label="RV BASE Lab トップ"><span class="badge-top">CAMPER REPAIR</span><strong>RV BASE<span>Lab</span></strong><svg viewBox="0 0 64 40" aria-hidden="true"><path d="M5 26V11h31l12 9h10v13H5ZM36 13v11h18M10 11V5h24v6M12 17h13v8H12Z"/><circle cx="16" cy="33" r="5"/><circle cx="47" cy="33" r="5"/></svg></a>''')
headerbrand.getparent().replace(headerbrand,brand)
head=doc.find('head');etree.SubElement(head,'link',{'rel':'stylesheet','href':'poster-design.css'})
p.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html'))
print('Built poster composition with centered original mechanic.')
