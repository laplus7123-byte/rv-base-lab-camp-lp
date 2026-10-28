"""Current entrypoint: original poster FV with reference-inspired storytelling below."""
from pathlib import Path
import runpy
from lxml import html, etree
ROOT=Path(__file__).resolve().parent
runpy.run_path(str(ROOT/'build_manga_design.py'))
p=ROOT/'dist/index.html';d=html.fromstring(p.read_text())
intro=d.xpath('//section[@class="manga-intro"]')[0]
new=html.fromstring((ROOT/'worry-section.html').read_text())
intro.getparent().replace(intro,new)
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
map_link=access.xpath('.//a[contains(@href,"google.com/maps")]')[0]
map_link.set('href','https://maps.app.goo.gl/UdEobBBbQLo8JsiH7')
map_link.text='Google マップで場所・経路を確認 '
map_frame=html.fromstring('''<div class="access-map"><iframe title="RV BASE Labの所在地：千葉県君津市俵田729-3" src="https://www.google.com/maps?q=%E5%8D%83%E8%91%89%E7%9C%8C%E5%90%9B%E6%B4%A5%E5%B8%82%E4%BF%B5%E7%94%B0729-3&amp;ll=35.3170053,140.0579389&amp;z=16&amp;hl=ja&amp;output=embed" width="600" height="360" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>''')
map_link.addprevious(map_frame)
contact=d.xpath('//section[@id="contact"]')[0];contact.set('class',contact.get('class')+' story-contact')
for form_link in contact.xpath('.//a[@class="contact-form"]'):form_link.drop_tree()
for old in flow.xpath('.//p[@class="eyebrow"]'):old.text='HOW IT WORKS'
for old in about.xpath('.//p[@class="eyebrow"]'):old.text='YOUR CAMPER’S HOME BASE'
head=d.find('head');etree.SubElement(head,'link',{'rel':'stylesheet','href':'story-layout.css'});etree.SubElement(head,'script',{'src':'story-layout.js','defer':'defer'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'flow-accordion.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'story-refinement.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'camp-about.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'camp-faq.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'camp-proof.css'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'worry-editorial.css'})
# Purpose-made illustrations: keep the original hero and photo consultation flow.
for img in d.xpath('//section[@class="story-worries"]//img | //section[@id="service"]//article//img'):
 old_src=img.get('src','')
 for service in ('repair','electrical','solar','heater','install','transport'):
  if old_src == f'assets/manga-{service}.png':
   img.set('src',f'assets/service-{service}-v3.webp')
   img.set('width','1536');img.set('height','1024');img.set('decoding','async')
faq_image=faq.xpath('.//figure[@class="camp-faq-guide"]/img')[0]
faq_image.set('src','assets/faq-guide-v3.webp')
faq_image.set('width','1086');faq_image.set('height','1448')
faq_image.set('alt','質問の見出しに視線を向けて案内する整備士')
faq_image.set('decoding','async')
etree.SubElement(head,'link',{'rel':'stylesheet','href':'illustration-refresh.css'})
# Consultation copy before the right-hand character; logo on every LINE entry.
consult=services.xpath('.//div[contains(@class,"story-consult")]')[0]
consult.xpath('./div[not(@class)]')[0].set('class','consult-message')
for link in d.xpath('//a[contains(@href,"lin.ee/")]'):
 if 'header-cta' in link.get('class',''):link.set('aria-label','LINEで相談する（新しいタブで開きます）')
 for generic_icon in link.xpath('./svg'):generic_icon.drop_tree()
 if not link.xpath('./img[@class="line-brand-icon"]'):
  label=etree.Element('span',{'class':'line-cta-label'})
  label.text=link.text or ''
  link.text=None
  for child in list(link):label.append(child)
  link.append(label)
  logo=etree.Element('img',{'class':'line-brand-icon','src':'assets/line-brand-icon.png','width':'40','height':'40','alt':'','aria-hidden':'true','decoding':'async'})
  if 'header-cta' not in link.get('class',''):link.insert(0,logo)
  link.set('class',(link.get('class','')+' line-branded-cta').strip())
for mobile_line in d.xpath('//div[@class="mobile-contact"]/a[contains(@href,"lin.ee/")]'):
 mobile_line.set('aria-label','今すぐLINEでチャット相談（新しいタブで開きます）')
 label=mobile_line.xpath('./span[@class="line-cta-label"]')[0]
 label.clear();label.set('class','line-cta-label')
 copy=etree.SubElement(label,'span',{'class':'mobile-line-copy'})
 copy.text='今すぐLINEで';etree.SubElement(copy,'br').tail='チャット相談'
 arrow=etree.SubElement(label,'span',{'aria-hidden':'true'});arrow.text='↗'
for mobile_phone in d.xpath('//div[@class="mobile-contact"]/a[starts-with(@href,"tel:")]'):
 mobile_phone.set('class','mobile-phone-cta')
 mobile_phone.text=None
 icon=html.fromstring('<svg class="phone-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.69 2.79a2 2 0 0 1-.45 2.11L8.09 9.89a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.89.33 1.83.56 2.79.69A2 2 0 0 1 22 16.92z"/></svg>')
 mobile_phone.append(icon)
 etree.SubElement(mobile_phone,'span').text='電話で相談'
etree.SubElement(head,'link',{'rel':'stylesheet','href':'layout-polish.css'})
for arrow in d.xpath('//a[contains(@class,"line-branded-cta")]//span[normalize-space(text())="↗"] | //a[contains(@class,"line-branded-cta")]//b[normalize-space(text())="↗"]'):
 arrow.set('class',(arrow.get('class','')+' cta-arrow').strip())
 arrow.set('aria-hidden','true')
etree.SubElement(head,'link',{'rel':'stylesheet','href':'text-motion.css'})
etree.SubElement(head,'script',{'src':'text-motion.js','defer':'defer'})
# Remove decorative English captions; retain brand and service names.
for caption in d.xpath('//p[contains(@class,"eyebrow")] | //p[@class="poster-english"] | //div[@class="story-service-title"]/div/p'):
 caption.getparent().remove(caption)
for location in d.xpath('//span[@class="poster-location"]'):location.text='千葉県君津市'
for top_link in d.xpath('//a[@class="back-top"]'):top_link.text='ページの先頭へ ↑'
# Preserve the 430px preview layout; mobile browsers choose the fit-to-screen scale.
d.xpath('//meta[@name="viewport"]')[0].set('content','width=430, viewport-fit=cover')
etree.SubElement(head,'link',{'rel':'stylesheet','href':'fixed-width.css?v=preview430-20261026'})
from apply_hero_scene import apply_hero_scene
apply_hero_scene(d)
from apply_manga_style import apply_manga_style
apply_manga_style(d)
d.find('body').set('class',(d.find('body').get('class','')+' mobile-lp').strip())
etree.SubElement(head,'link',{'rel':'stylesheet','href':'mobile-lp.css?v=subtle-logo-20261028'})
p.write_text('<!doctype html>\n'+html.tostring(d,encoding='unicode',method='html'))
print('Built reference-inspired storytelling. Poster FV, official logo and fixed camper preserved.')
