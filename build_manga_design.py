"""Current entrypoint: preserve poster FV, build illustrated service landing page."""
from pathlib import Path
import runpy
from lxml import html, etree
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'build_poster_design.py'))
p=ROOT/'dist/index.html'; doc=html.fromstring(p.read_text())
def replace(selector,markup):
 old=doc.xpath(selector)[0]; old.getparent().replace(old,html.fromstring(markup))
line='https://lin.ee/bryjnk0'
replace('//section[contains(@class,"purpose")]', '''<section class="manga-intro" aria-labelledby="worry-title"><div class="container"><div class="chapter"><span>01</span><p>BEFORE YOUR NEXT TRIP</p><b>旅の前の、気がかり。</b></div><div class="intro-title"><h2 id="worry-title">楽しみな旅に、<br><em>「ちょっと心配」</em>を<br class="mobile-only">持っていかない。</h2><p>走ること。車内で過ごすこと。<br>どちらも大切な、キャンピングカーだから。</p></div><div class="worry-strip"><a class="worry-frame" href="#repair"><span class="worry-quote">この音、<br>いつもと違うかも。</span><img src="assets/manga-repair.png" width="1536" height="1024" loading="lazy" alt="キャンピングカーの足回りを点検する整備士"><span class="worry-caption">走り・設備の不調 <b>01 →</b></span></a><a class="worry-frame" href="#electrical"><span class="worry-quote">旅先で電気、<br>足りるかな？</span><img src="assets/manga-electrical.png" width="1536" height="1024" loading="lazy" alt="車内のバッテリーを確認する整備士"><span class="worry-caption">バッテリー・充電 <b>02 →</b></span></a><a class="worry-frame" href="#install"><span class="worry-quote">ここがもっと<br>使いやすければ！</span><img src="assets/manga-install.png" width="1536" height="1024" loading="lazy" alt="車内の収納を相談するオーナーと整備士"><span class="worry-caption">使い勝手・カスタム <b>05 →</b></span></a></div><div class="intro-answer"><span class="answer-arrow" aria-hidden="true">↓</span><p>その気がかり、<br><strong>RV BASE Labに<br class="mobile-only">聞かせてください。</strong></p><span class="answer-note">症状がうまく説明できなくても大丈夫。<br>愛車の状態と、あなたの使い方から考えます。</span></div></div></section>''')
services=doc.xpath('//section[@id="service"]')[0]
services.set('class','manga-services')
cards=services.xpath('.//article[contains(@class,"service-card")]')
notes=[('repair','REPAIR & MAINTENANCE','まずは、状態を見てみましょう。','不調を見つけて、次の旅へ。'),('electrical','BATTERY & ELECTRICAL','どんな家電を使っていますか？','旅の電気を、使い方から考える。'),('solar','SOLAR & CHARGING','屋根も、充電設備も確認します。','充電の選択肢を、もっと。'),('heater','FF HEATER','寒い季節の過ごし方も、一緒に。','車内の時間を、あたたかく。'),('install','PARTS & CUSTOM','その「こうしたい」、聞かせてください。','あなたの旅に、使いやすさを。'),('transport','RECOVERY & TRANSPORT','まずは現在の状況をお電話で。','動かせないときも、相談から。')]
for card,(ident,eng,bubble,benefit) in zip(cards,notes):
 title=card.xpath('./h3')[0].text_content(); num=card.xpath('.//span[@class="number"]')[0].text_content()
 desc=card.xpath('./p[@class="service-description"]')[0].text_content(); tags=card.xpath('./p[@class="service-tags"]')[0].text_content()
 details=card.xpath('./details')[0]
 alt={'repair':'工場でキャンピングカーの前輪を点検する整備士','electrical':'サブバッテリーと電装設備を点検する整備士','solar':'キャンピングカーの屋根のソーラーパネルを確認する整備士','heater':'車内のFFヒーターについて説明する整備士','install':'オーナーと相談しながら収納を取り付ける整備士','transport':'搬送車に載せたキャンピングカーの状況を電話で伝える整備士'}[ident]
 new=html.fromstring(f'''<article class="comic-service" id="{ident}"><div class="comic-service-title"><span class="comic-number">{num}</span><div><p>{eng}</p><h3>{title}</h3></div></div><figure class="comic-scene"><img src="assets/manga-{ident}.png" width="1536" height="1024" loading="lazy" alt="{alt}"><figcaption>{bubble}</figcaption></figure><div class="comic-service-copy"><h4>{benefit}</h4><p>{desc}</p><div class="comic-tags">{''.join('<span>'+x.strip()+'</span>' for x in tags.split('/'))}</div></div></article>''')
 new.xpath('./div[@class="comic-service-copy"]')[0].append(details)
 card.getparent().replace(card,new)
grid=services.xpath('.//div[@class="service-grid"]')[0];grid.set('class','comic-service-grid')
heading=services.xpath('.//div[@class="section-heading"]')[0]
heading.getparent().replace(heading,html.fromstring('''<div class="chapter"><span>02</span><p>OUR SERVICES</p><b>整備で、旅をもっと自由に。</b></div><div class="comic-section-title"><span class="comic-label">愛車のこと、まるごと相談。</span><h2>「直したい」も、<br>「もっと快適に」も。</h2><p>キャンピングカーの修理から、車内設備のアップデートまで。<br>6つのサービスで、あなたの旅を支えます。</p></div>'''))
help=services.xpath('.//div[@class="service-help"]')[0]
help.getparent().replace(help,html.fromstring(f'''<div class="comic-consult"><div class="consult-face"><img src="assets/rv-mechanic-ink-v2.png" alt="" width="1024" height="1280" loading="lazy"></div><div><span>「これも相談していい？」と思ったら。</span><h3>気になるところを、<br>写真で見せてください。</h3><p>車種・症状・ご希望からお伺いします。</p></div><a class="manga-button" href="{line}" target="_blank" rel="noopener noreferrer">LINEで愛車の相談をする <b>↗</b></a></div><p class="illustration-note">※漫画はサービスのイメージです。対応内容は車両・設備の状態を確認してご案内します。</p>'''))
about=doc.xpath('//section[@id="about"]')[0];about.set('class','about section manga-about')
art=about.xpath('.//div[@class="about-art"]')[0]
art.getparent().replace(art,html.fromstring('''<div class="workshop-comic"><div class="workshop-caption">旅するクルマの、かかりつけ。</div><img src="assets/manga-repair.png" width="1536" height="1024" loading="lazy" alt="愛車の状態に向き合う整備士のイメージ"><div class="workshop-speech">クルマのことも、<br>旅のことも。</div><div class="workshop-cert"><b>関東運輸局長認証工場</b><span>自動車特定整備事業 第3-5923号</span></div></div>'''))
about.xpath('.//p[@class="eyebrow"]')[0].text='03 / WHY RV BASE LAB?'
flow=doc.xpath('//section[@id="flow"]')[0];flow.set('class','flow section manga-flow')
flow.xpath('.//p[@class="eyebrow"]')[0].text='04 / HOW IT WORKS'
flowtitles=['まずは、写真を。','愛車と希望を確認。','内容・費用に納得。','整えて、お渡し。']
flowicons=['chat','check','wrench','van']
native_icons={
'chat':'<path d="M9 10h44v34H28L14 55V44H9Z M18 22h25 M18 31h18"/>',
'check':'<path d="M32 5 54 14v18c0 14-22 25-22 25S10 46 10 32V14Z m-11 26 8 8 15-16"/>',
'wrench':'<path d="M40 7a15 15 0 0 0-18 19L8 40a8 8 0 0 0 12 12l14-14a15 15 0 0 0 19-18L42 31 31 20Z"/>',
'van':'<path d="M5 43V20h32l13 13h7v15H5ZM37 25v12h16M12 20v-9h21v9M12 28h13v10H12Z"/><circle cx="16" cy="48" r="6"/><circle cx="46" cy="48" r="6"/>'}
for i,li in enumerate(flow.xpath('.//ol/li')):
 li.insert(1,html.fromstring('<div class="flow-comic-icon">'+'<svg viewBox="0 0 64 64" aria-hidden="true">'+native_icons[flowicons[i]]+'</svg>'+'</div>'))
 li.xpath('./h3')[0].text=flowtitles[i]
faq=doc.xpath('//section[@id="faq"]')[0];faq.set('class','faq section manga-faq')
contact=doc.xpath('//section[@id="contact"]')[0];contact.set('class','contact section manga-contact')
lane=doc.xpath('//div[@class="camper-lane"]')[0]
lane.set('class','camper-lane angle-lane')
for kind,label in [('cabover','キャブコン'),('van','バンコン'),('mini','軽キャンパー')]:
 car=lane.xpath('.//figure[contains(@class,"type-'+kind+'") ]')[0]
 im=car.xpath('.//img')[0];im.set('src','assets/camper-front-'+kind+'.png');im.set('alt',label+'の斜め前向きイラスト');im.set('width','1280');im.set('height','1280')
 for rim in car.xpath('.//*[contains(@class,"rim")]'):rim.getparent().remove(rim)
head=doc.find('head');etree.SubElement(head,'link',{'rel':'stylesheet','href':'manga-design.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'camper-angle.css'})
p.write_text('<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html'))
print('Built illustrated manga LP, preserving poster FV.')
