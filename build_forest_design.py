"""Original forest hero and campground navigation over the approved RV content."""
from pathlib import Path
from lxml import html, etree

ROOT = Path(__file__).resolve().parent
D = ROOT / 'dist'
doc = html.fromstring((D/'index.html').read_text())
page = doc.get_element_by_id('page-top')

def fragment(markup): return html.fromstring(markup)
def replace(old,new): old.getparent().replace(old,new)
def bykey(key): return doc.xpath(f'//*[@data-s-{key}]')[0]

brand_icon='''<svg viewBox="0 0 72 56" aria-hidden="true"><path d="M8 40V20h33l10 12h11v15H8Z"/><path d="M15 20V11h25v9M41 25v12h16M15 28h15v10H15Z"/><circle cx="21" cy="47" r="6"/><circle cx="51" cy="47" r="6"/><path d="M59 5 49 20h7l-6 9h18l-6-9h7Z"/></svg>'''
lantern='''<svg viewBox="0 0 60 72" aria-hidden="true"><path d="M20 16V11a10 10 0 0 1 20 0v5M15 20h30l5 40H10Z"/><path d="M22 21v38M38 21v38M10 60h40v7H10ZM20 16h20v5H20Z"/><path d="M30 34q-10 12 0 18 10-6 0-18Z"/></svg>'''
header=fragment(f'''<header class="camp-header">
 <a class="camp-brand" href="#page-top" aria-label="RV BASE Lab トップへ">{brand_icon}<span><strong>RV BASE <b>Lab</b></strong><small>CAMPER REPAIR &amp; CARE</small></span></a>
 <nav class="camp-desktop-nav" aria-label="メインナビゲーション"><a href="#about">私たちについて</a><a href="#service">整備メニュー</a><a href="#store-info">店舗・アクセス</a></nav>
 <a class="camp-header-contact" href="https://lin.ee/bryjnk0" target="_blank" rel="noopener noreferrer">{lantern}<span>LINEで相談 <b>↗</b></span></a>
 <button class="camp-menu-button" type="button" data-rv-menu="" aria-label="メニューを開く"><span></span><span></span><small>MENU</small></button>
</header>''')
cars=list(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," camper-swapped ")]'))
for e in list(page):
    if e.tag in ['h1','header'] or e.get('id') in ['header-contact','fv-wrapper']:page.remove(e)
for e in list(doc.xpath('//*[@id="sticky-logo"]')): e.getparent().remove(e)
page.insert(0,header)

hero=fragment('''<section class="forest-hero" aria-labelledby="forest-headline">
 <div class="forest-hero-layout">
  <div class="forest-copy">
   <p class="forest-eyebrow"><span></span> 千葉・君津のキャンピングカー修理工場</p>
   <p class="forest-wordmark">RV BASE <span>Lab</span></p>
   <h1 id="forest-headline">直して、整えて。<br/>また、<span>旅に出よう。</span></h1>
   <p class="forest-description">お気に入りの景色に、また会えるように。<br/>修理も、電装も、カスタムも。<br/>旅する愛車の「気になる」を、一緒に。</p>
   <a class="camp-primary-cta" href="https://lin.ee/bryjnk0" target="_blank" rel="noopener noreferrer">愛車のことを相談する <span>↗</span></a>
   <p class="forest-contact-note">写真があれば、LINEで気軽に。</p>
  </div>
  <div class="camp-window-area">
   <div class="camp-window-caption">好きな景色を、これからも。</div>
   <div class="camp-window"><img src="assets/forest-camper-life.png" width="1024" height="1024" alt="森のキャンプ場で、キャンピングカーの隣でコーヒーを楽しむ二人のイラスト" fetchpriority="high"/></div>
   <div class="camp-window-tag"><span class="camp-tag-star">✳</span><span>GOOD CAMPER,<br/><b>GOOD JOURNEY.</b></span></div>
  </div>
 </div>
 <div class="camp-route" aria-label="3種類のキャンピングカーが走るアニメーション"><div class="camp-route-ground"></div><div class="camp-route-line"></div></div>
 <a class="camp-scroll" href="#about">SCROLL <span>↓</span></a>
</section>''')
page.insert(1,hero)
route=hero.xpath('.//*[@class="camp-route"]')[0]
for e in cars:
    e.set('class','camp-route-car camper-swapped')
    for key in list(e.attrib):
        if key.startswith('data-s-'):del e.attrib[key]
    route.append(e)

def section_title(kicker,title,detail=''):
    return fragment(f'''<div class="camp-section-heading"><div class="camp-wood-sign">{lantern}<div><span>{kicker}</span><h2>{title}</h2></div><i aria-hidden="true"></i></div>{f'<p>{detail}</p>' if detail else ''}</div>''')
about=doc.get_element_by_id('about')
replace(about[0][0],section_title('ABOUT OUR BASE','RV BASE Labについて'))
service=doc.get_element_by_id('service')
replace(service[0][0],section_title('SERVICE MENU','キャンピングカーの整備メニュー','「困った」も、「こうしたい」も。まずはご相談ください。'))
store=doc.get_element_by_id('store-info')
replace(store[0][0],section_title('VISIT OUR BASE','房総の、キャンパーの基地へ。','千葉・君津で、お待ちしています。'))

# The old social CTA used a traffic-signal housing. Replace its entire structure.
replace(bykey('a9feb764-15dd-4543-8e0e-6d14cedfea6f'),fragment(f'''<div class="camp-consult"><span class="camp-consult-icon">{lantern}</span><div><p>気になるところを、写真で送って</p><h3>LINEで気軽にご相談。</h3><a href="https://lin.ee/bryjnk0" target="_blank" rel="noopener noreferrer">愛車の写真と一緒に相談する ↗</a></div></div>'''))
for e in list(doc.xpath('//*[@id="overview_bar"]')):e.getparent().remove(e)

# Give the footer the same original woodland vocabulary and direct contact options.
oldfooter=doc.xpath('//footer')[0]
newfooter=fragment(f'''<footer class="camp-footer">
 <div class="camp-footer-content"><span class="camp-footer-lantern">{lantern}</span><p class="camp-footer-eyebrow">BEFORE YOUR NEXT JOURNEY</p><h2>次の旅の前に、<br/>愛車の気になることを。</h2><p>車種・症状・ご希望を、分かる範囲でお知らせください。</p><div class="camp-footer-actions"><a class="camp-primary-cta" href="https://lin.ee/bryjnk0" target="_blank" rel="noopener noreferrer">LINEで写真相談 <span>↗</span></a><a class="camp-phone" href="tel:05055859522"><small>お電話でのご相談</small><strong>050-5585-9522</strong></a></div><p class="camp-footer-note">ご来店前にご相談ください。受付・対応状況はお問い合わせください。</p></div>
 <div class="camp-footer-bottom"><a class="camp-brand" href="#page-top">{brand_icon}<span><strong>RV BASE <b>Lab</b></strong><small>CAMPER REPAIR &amp; CARE</small></span></a><p>〒292-0455 千葉県君津市俵田729-3</p><span>© 2026 RV BASE Lab</span><a href="#page-top" class="camp-top-link">PAGE TOP ↑</a></div>
</footer>''')
replace(oldfooter,newfooter)
etree.SubElement(doc.find('head'),'link',{'rel':'stylesheet','href':'forest-design.css'})
etree.SubElement(doc.find('head'),'link',{'rel':'preload','href':'assets/forest-camper-life.png','as':'image'})
doc.find('head').find('title').text='RV BASE Lab｜旅する愛車の、かかりつけ。｜キャンピングカー修理'
(D/'index.html').write_text('<!DOCTYPE html>\n'+html.tostring(doc,encoding='unicode',method='html'))
assert len(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," camper-swapped ")]'))==6
assert not doc.xpath('//*[@id="header-contact" or @id="header-nav" or @id="fv-man" or @id="service-title" or @id="store-info-bar"]')
print('Original woodland hero, framed camper life, camping signs and contact navigation built.')
