"""Current entry point: original illustrated garage identity over RV service content."""
from pathlib import Path
import runpy
from lxml import html, etree
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'build_service_design.py'))
p=ROOT/'dist/index.html'
doc=html.fromstring(p.read_text())
hero=doc.xpath('//section[@class="hero"]')[0]
vehicles=''
for kind,name,bubble in [('cabover','キャブコン','旅の前に、点検を。'),('van','バンコン','電装の相談も。'),('mini','軽キャンパー','また、旅に出よう。')]:
 vehicles+=f'''<figure class="track-car type-{kind}"><figcaption>{bubble}</figcaption><div class="car-drawing"><img src="assets/camper-side-{kind}.png" alt="{name}の横向きイラスト" width="1700" height="1000"><i class="rim front" aria-hidden="true"></i><i class="rim rear" aria-hidden="true"></i></div></figure>'''
new=html.fromstring(f'''<section class="garage-hero" aria-labelledby="garage-title">
<div class="garage-board"><div class="garage-topline"><span>CAMPER REPAIR & MAINTENANCE</span><span>CHIBA / KIMITSU</span></div>
<div class="garage-stage"><div class="garage-copy"><p class="garage-eyebrow">キャンピングカーの修理・整備</p><h1 id="garage-title">RV BASE<span>Lab<span class="brand-dot">.</span></span></h1><div class="garage-message"><p>直して、整えて。<br>また、旅に出よう。</p><span>修理・点検 / 電装・バッテリー / 部品取付</span></div><div class="garage-actions"><a href="https://lin.ee/bryjnk0" class="garage-cta" target="_blank" rel="noopener noreferrer">愛車のこと、相談する <b>↗</b></a><a class="garage-service-link" href="#service">整備メニューを見る ↓</a></div></div>
<div class="garage-character"><div class="garage-door" aria-hidden="true"><span>REPAIR BASE</span><div class="door-lines"></div></div><img class="mechanic-original" src="assets/rv-original-mechanic.png" alt="工具を手に迎える、RV BASE Labのオリジナル整備士キャラクター" width="1024" height="1536" fetchpriority="high"><div class="garage-stamp" aria-hidden="true"><svg viewBox="0 0 60 60"><path d="M38 7a15 15 0 0 0-18 20L6 41a7 7 0 0 0 11 11l14-14a15 15 0 0 0 20-18L40 31 29 20Z"/></svg><b>REPAIR<br>& CAMP</b></div></div></div>
<div class="garage-bottomline"><span>旅する愛車の、かかりつけ。</span><small>関東運輸局長認証工場 第3-5923号</small></div></div>
<div class="camper-lane"><div class="lane-dashes" aria-hidden="true"></div>{vehicles}<button class="motion-control" type="button" aria-pressed="false">動きを止める Ⅱ</button></div>
</section>''')
hero.getparent().replace(hero,new)
for e in doc.xpath('//*[@class="utility"]'):e.getparent().remove(e)
# Keep workshop character as a fictional illustration, not a staff photograph.
head=doc.find('head')
etree.SubElement(head,'link',{'rel':'stylesheet','href':'garage-design.css'})
etree.SubElement(head,'script',{'src':'garage-design.js','defer':''})
chapters={'service':'01','about':'02','flow':'03','faq':'04','store-info':'05'}
for ident,num in chapters.items():doc.get_element_by_id(ident).set('data-chapter',num)
for e in doc.xpath('//*[@id="purpose-title"]'):e.text='その「気になる」、お聞かせください。'
for e in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," purpose-heading ")]/p'):e.text='WHAT CAN WE FIX FOR YOU?'
# Use one restrained brand wordmark instead of the reference company's badge.
for a in doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," brand ")]'):
 for svg in a.xpath('./svg'): a.remove(svg)
 a.insert(0,html.fromstring('<span class="brand-monogram" aria-hidden="true">RV</span>'))
p.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html'))
print('Built original garage design with new mechanic and animated campers.')
