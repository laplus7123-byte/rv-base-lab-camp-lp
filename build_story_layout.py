"""Current entrypoint: original poster FV with reference-inspired storytelling below."""
from pathlib import Path
import runpy
from lxml import html, etree
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'build_manga_design.py'))
p=ROOT/'dist/index.html';d=html.fromstring(p.read_text())
intro=d.xpath('//section[@class="manga-intro"]')[0]
new=html.fromstring('''<section class="story-worries" aria-labelledby="worry-title"><div class="container"><p class="story-eyebrow">BEFORE YOUR NEXT JOURNEY</p><h2 id="worry-title">次の旅の前に、<br><em>愛車のこと</em>で<br class="mobile-only">気になっていませんか？</h2><div class="story-worry-grid"><article class="story-worry"><a href="#repair" class="story-circle"><img src="assets/manga-repair.png" width="1536" height="1024" loading="lazy" alt="キャンピングカーを点検する整備士"><span class="story-bubble">この音、<br>いつもと違うかも。</span></a><h3>小さな不調、<br>そのままにしていませんか。</h3><p>気になる異音や設備の不調。<br>旅に出る前に、<br>一度きちんと見ておきたい。</p></article><article class="story-worry"><a href="#electrical" class="story-circle"><img src="assets/manga-electrical.png" width="1536" height="1024" loading="lazy" alt="バッテリーを点検する整備士"><span class="story-bubble">旅先で電気、<br>足りるかな？</span></a><h3>旅先でも、<br>心地よく過ごしたい。</h3><p>バッテリーや充電、冬の暖房。<br>車内で過ごす時間も、<br>安心して楽しみたい。</p></article><article class="story-worry"><a href="#install" class="story-circle"><img src="assets/manga-install.png" width="1536" height="1024" loading="lazy" alt="車内の使い勝手を相談するオーナーと整備士"><span class="story-bubble">ここがもっと<br>使いやすければ！</span></a><h3>「こうしたい」を、<br>どこに相談しよう。</h3><p>部品の取付や収納の見直し。<br>自分たちの旅に合う一台に、<br>少しずつ整えていきたい。</p></article></div><div class="story-down" aria-hidden="true"><span></span><span></span></div></div></section>''')
intro.getparent().replace(intro,new)
worry_copy=[
 ('小さな不調も、<br>ご相談ください。','いつもと違う音や、設備の不調。気になることは、旅に出る前に一度確認しておきませんか。修理も点検も、愛車の状態からお伺いします。','修理・メンテナンスを見る'),
 ('旅先でも、<br>心地よい車内に。','バッテリーや充電、寒い季節の暖房。旅先での使い方に合わせて、車内の設備を見直しませんか。今お使いの装備からご相談いただけます。','電装・バッテリーを見る'),
 ('愛車を、もっと<br>使いやすく。','部品の取付や収納の見直し。「ここがこうなったら」というご希望をお聞かせください。自分たちの旅に合う一台を、一緒に考えます。','部品取付・カスタムを見る')]
for card,(title,description,link_text) in zip(new.xpath('.//article'),worry_copy):
 picture=card.xpath('./a')[0];picture.set('class','worry-picture')
 for bubble in picture.xpath('./span'):picture.remove(bubble)
 for item in card.xpath('./h3|./p'):card.remove(item)
 copy=html.fromstring(f'<div class="worry-copy"><h3>{title}</h3><p>{description}</p><a class="worry-more" href="{picture.get("href")}">{link_text}<span aria-hidden="true">↗</span></a></div>')
 card.append(copy)
services=d.xpath('//section[@id="service"]')[0];services.set('class','story-services')
for old in services.xpath('.//div[@class="chapter"]|.//div[@class="comic-section-title"]'):old.getparent().remove(old)
grid=services.xpath('.//div[@class="comic-service-grid"]')[0];grid.set('class','story-solutions')
center=html.fromstring('''<div class="story-solution-center"><div class="story-center-sticky"><p class="story-eyebrow">RV BASE Lab</p><h2><span>愛車の悩みに、</span><strong>整備でこたえる。</strong></h2><div class="story-guide"><span class="story-bubble">直して、整えて。<br>また、旅に出よう。</span><img src="assets/rv-mechanic-ink-v2.png" width="1024" height="1280" alt="工具を持ったRV BASE Labのオリジナル整備士" loading="lazy"></div></div></div>''')
grid.insert(0,center)
for i,card in enumerate(grid.xpath('./article')):
 card.set('class','story-service');card.set('style',f'--story-row:{i//2+1};--story-column:{1 if i%2==0 else 3}')
 card.xpath('./div[@class="comic-service-title"]')[0].set('class','story-service-title')
 card.xpath('./div[@class="comic-service-copy"]')[0].set('class','story-service-copy')
 cap=card.xpath('.//figcaption')[0];cap.set('class','story-bubble')
help=services.xpath('.//div[@class="comic-consult"]')[0];help.set('class','comic-consult story-consult')
old_about=d.xpath('//section[@id="about"]')[0]
about=html.fromstring((ROOT/'camp-about.html').read_text())
old_about.getparent().replace(old_about,about)
old_flow=d.xpath('//section[@id="flow"]')[0]
flow=html.fromstring((ROOT/'flow-accordion.html').read_text())
old_flow.getparent().replace(old_flow,flow)
faq=d.xpath('//section[@id="faq"]')[0];faq.set('class','camp-faq');faq.set('aria-labelledby','camp-faq-title')
faq_grid=faq.xpath('./div')[0];faq_grid.set('class','camp-faq-inner')
faq_heading=html.fromstring('''<header class="camp-faq-intro"><div class="camp-faq-copy"><h2 id="camp-faq-title"><span>よくある</span><strong>質問</strong></h2><p>キャンピングカーのこと、<br>整備のこと。<br>よくあるご質問をまとめました。</p></div><figure class="camp-faq-guide"><figcaption class="story-bubble">わかりやすく<br class="faq-bubble-break">お答えします！</figcaption><img src="assets/rv-mechanic-ink-v2.png" width="1122" height="1402" loading="lazy" alt="工具を持って案内する整備士のイラスト"></figure></header>''')
faq_grid.replace(faq_grid[0],faq_heading)
access=d.xpath('//section[@id="store-info"]')[0];access.set('class',access.get('class')+' story-access')
contact=d.xpath('//section[@id="contact"]')[0];contact.set('class',contact.get('class')+' story-contact')
for old in flow.xpath('.//p[@class="eyebrow"]'):old.text='HOW IT WORKS'
for old in about.xpath('.//p[@class="eyebrow"]'):old.text='YOUR CAMPER’S HOME BASE'
head=d.find('head');etree.SubElement(head,'link',{'rel':'stylesheet','href':'story-layout.css'});etree.SubElement(head,'script',{'src':'story-layout.js','defer':'defer'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'flow-accordion.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'story-refinement.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'camp-about.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'camp-faq.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'camp-proof.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'worry-editorial.css'})
p.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode',method='html'))
print('Built reference-inspired storytelling. Poster FV, official logo and fixed camper preserved.')
