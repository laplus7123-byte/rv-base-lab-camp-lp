"""Adapt the retained reference composition to RV BASE Lab content and colors."""
from pathlib import Path
from lxml import html, etree
import json, re, shutil, base64
from html import escape

ROOT = Path(__file__).resolve().parent
D = ROOT / 'dist'
A = D / 'assets'
A.mkdir(exist_ok=True)
doc = html.fromstring((D / 'index.html').read_text())
GREEN, BROWN, PAPER, INK = '#3e5d36', '#856248', '#f4f0e7', '#302d27'

def svg(name, w, h, body):
    (A / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><g font-family="Arial, Noto Sans JP, sans-serif">{body}</g></svg>')
    return 'assets/' + name

def text(x,y,value,size=40,fill=INK,weight=800,extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'

def node(key):
    return doc.xpath(f'//*[@data-s-{key}]')[0]

def settext(key,value):
    e = node(key)
    for c in list(e): e.remove(c)
    e.text = value
    return e

def img(key,src,alt=''):
    e=node(key); e.set('src',src); e.set('alt',alt)
    return e

def tree(x,y,s=1):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 L-28 45 H-17 L-39 78 H-10 V98 H10 V78 H39 L17 45 H28Z" fill="#ffffff" opacity=".12"/></g>'

hero = '<defs><clipPath id="r"><rect x="4" y="4" width="2368" height="1104" rx="42"/></clipPath></defs><g clip-path="url(#r)"><path fill="'+GREEN+'" d="M0 0H1200V1112H0Z"/><path fill="'+BROWN+'" d="M1200 0H2376V1112H1200Z"/>'
hero += text(78,210,'キャンピングカー修理',84,'#fff')
hero += text(1510,180,'CAMPER REPAIR',48,'#e1d4bd')+text(1510,244,'& MAINTENANCE',48,'#e1d4bd')
hero += text(70,670,'RV BASE',300,'#fff',900,'textLength="1040" lengthAdjust="spacingAndGlyphs"')
hero += text(1410,670,'Lab.',365,'#fff',900)
hero += '<path d="M86 720H2288" stroke="#fff" stroke-width="7"/>'
hero += text(1620,826,'直して、整えて。',58,'#fff')+text(1620,903,'また、旅に出よう。',58,'#fff')
hero += ''.join(tree(x,975,1.4) for x in [90,230,390,570,790,960,1320,1480,1680,1900,2120,2290])+'</g><rect x="4" y="4" width="2368" height="1104" rx="42" fill="none" stroke="'+INK+'" stroke-width="8"/>'
svg('rv-hero.svg',2376,1112,hero)
svg('rv-hero-mobile.svg',700,1040,f'<rect x="3" y="3" width="694" height="1034" rx="40" fill="{GREEN}" stroke="{INK}" stroke-width="6"/><path d="M355 6H655Q694 6 694 45V995Q694 1034 655 1034H355Z" fill="{BROWN}"/>'+''.join(tree(x,930,1) for x in range(40,700,110)))
svg('rv-mobile-copy.svg',700,1040,text(42,142,'キャンピングカーの',43,'#fff')+text(42,202,'修理・メンテナンス',43,'#fff'))
svg('rv-wordmark.svg',1617,280,text(0,245,'RV BASE Lab',266,'#fff',900,'textLength="1617" lengthAdjust="spacingAndGlyphs"'))
svg('rv-mobile-label.svg',82,436,text(38,20,'REPAIR & CAMP',26,'#fff',700,'writing-mode="vertical-rl"'))
logo = f'<circle cx="80" cy="80" r="77" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><path d="M12 56A73 73 0 0 1 148 56Z" fill="{GREEN}"/><path d="M12 105H148A73 73 0 0 1 12 105Z" fill="{BROWN}"/>'+text(80,81,'RV BASE',24,INK,900,'text-anchor="middle"')+text(80,101,'Lab',18,INK,800,'text-anchor="middle"')+text(80,39,'CAMPER REPAIR',9,'#fff',700,'text-anchor="middle"')
svg('rv-logo.svg',160,160,logo)
img('651bd7b3-b39e-4845-a3dc-c22b4cd0924c','assets/rv-hero.svg','RV BASE Lab キャンピングカーの修理工場')
img('19cec706-189d-4b0d-8f18-598604b9611c','assets/rv-hero-mobile.svg')
for key in ['da63b722-c333-4eaf-ad2e-81112d17663b','8e64fb03-d779-4ea3-b968-05b368559f3d']:
    img(key,'assets/rv-wordmark.svg','RV BASE Lab')
for id in ['fv-title-sp-jp','fv-label-sp-en','fv-houses-sp','fv-label-sp']:
    e=doc.get_element_by_id(id)
    e.set('style','background-image:url("assets/'+('rv-mobile-copy.svg' if id=='fv-title-sp-jp' else 'rv-mobile-label.svg' if id=='fv-label-sp' else 'rv-hero-mobile.svg')+'");')
    if id in ['fv-label-sp-en','fv-houses-sp']: e.set('class',e.get('class','')+' rv-mobile-hide')
for e in doc.xpath('//img[contains(@src,"329db2d4")]'):
    e.set('src','assets/rv-logo.svg');e.set('alt','RV BASE Lab')

# Use native typography in the original image slots so company/service names are editable.
for name,w,h,label in [('rv-about.svg',1038,282,'ABOUT RV BASE Lab'),('rv-service.svg',1110,273,'OUR SERVICE'),('rv-service-sp.svg',452,216,'SERVICE'),('rv-store.svg',1110,273,'VISIT OUR BASE'),('rv-store-sp.svg',496,212,'OUR BASE')]:
    svg(name,w,h,text(8,h*.78,label,h*.6,INK,900,f'textLength="{w-20}" lengthAdjust="spacingAndGlyphs"'))
for key,name,alt in [('07faab9f-d118-48f5-981a-dc303c5cf8b1','rv-about.svg','RV BASE Labについて'),('f78be495-32d3-4544-898a-d43c3ff35ba4','rv-service.svg','サービス'),('01007991-4422-4213-8990-1354a3a8b6e7','rv-service-sp.svg','サービス'),('51a83ba7-3c44-401b-918c-c83e0c0e9552','rv-store.svg','店舗・アクセス'),('405b930b-d998-401d-99e5-c64baed6db56','rv-store-sp.svg','店舗・アクセス')]: img(key,'assets/'+name,alt)

replacements = {
'fc8901d2-3592-4e6c-b2e4-4a7129cc5bae':'ABOUT RV BASE Lab',
'0df64aa6-cd53-4d71-b76c-c8d07b7af577':'キャンピングカービルダーで10年勤務したメカニックと、クルマの仕事に30年携わってきたパートナー。二人の経験を持ち寄り、旅する愛車の「気になる」に向き合います。修理も、設備の見直しも、まずはご相談ください。',
'01d12e48-c79a-4012-a98d-15fadbc041e8':'気になるところを、写真で送って',
'b254e645-f9a0-4cde-b27e-8bbc1bf4a5d1':'RV BASE Labが大切にすること',
'4dc34df2-1d55-494b-a7ae-dfac31523816':'RV BASE Labが大切にすること',
'2b8b376d-ef63-4cd1-ab00-9d83eaa6993e':'愛車のことも、旅のことも。',
'52cc5a27-84be-420d-820e-9434b13d2769':'症状や使い方を伺い、車両・設備の状態を確認します。',
'66188b83-df33-49b9-8627-e680d98f1d3c':'修理から電装、カスタムまで、ご希望に向き合います。',
'46c62e25-7cb4-4a07-b514-cba097bd1a41':'作業内容・費用・日程をご相談してから進めます。',
'85821e28-2d72-4894-81a2-ca071ef11d42':'旅する愛車の整備メニュー',
'dc30e06b-50e7-4350-9bc2-fa5e6a24af8f':'修理・メンテナンス',
'94deb672-73d1-4b5b-b7af-0dbb572fca6f':'充電や電装の不調、足回りの異音、消耗品、旅行前の点検など。車種・架装メーカー・年式と、気になる症状をお知らせください。愛車の状態や部品の供給状況を確認し、対応内容をご案内します。',
'1c810b38-94b9-4101-ac12-5522e7297460':'電装・快適装備の見直し',
'fed3223c-c31f-4d3c-8d6d-d8d54c05f950':'電装・快適装備の見直し',
'57e9f973-2826-47ec-9da2-9545bd143e77':'リチウムバッテリーへの換装、ソーラー・充電システム、FFヒーターなどをご相談いただけます。今の設備と旅先での使い方、ご希望を伺い、取付や見直しの内容を確認します。',
'ca261f8a-a677-49aa-b366-1eac6abfec6c':'リチウムバッテリー',
'9e90c49d-a440-427a-8b17-161a917999c2':'旅先での電気の使い方や、今のバッテリー・充電設備を確認し、換装をご相談いただけます。',
'a127ed13-3642-4ac5-9bda-1e300e125092':'ソーラー・充電システム',
'ed5c5611-5d72-4e47-b651-f725ee5fa72d':'ソーラーパネルの取付や充電システムの見直し。車両と既存設備の情報をお知らせください。',
'198f726c-e1ca-4ab6-a87a-29326d9557fe':'FFヒーター',
'9b90af12-7758-4542-ab54-1db86704f0af':'寒い季節の車内を快適に。FFヒーターの取付や、今お使いの設備についてご相談ください。',
'4c9c2f20-fa2f-40b1-b29f-c62ea11e39cc':'持込部品の取付',
'e64fab06-aad1-4a2f-ac81-c59bdc4ea1d2':'カスタム',
'f44eebd7-6797-45fe-be62-4ac403c9cdf0':'カスタム',
'7a194b74-6816-469e-8535-d8ad87d9367b':'レッカー・搬送',
'6e0025d0-4dfc-4eae-867b-4f6a79077ccf':'千葉・君津の修理工場へ。',
'096e7bc8-68f6-4ee2-a196-912e24c7c54e':'千葉・君津の修理工場へ。',
'191234f1-7f70-439e-b386-0374f462b361':'RV BASE Lab',
'9cb0c29c-ffe7-4089-b78d-239b1bf0ef39':'〒292-0455 千葉県君津市俵田729-3',
'1dc76c1d-1832-4de4-a26c-faee247cc51d':'〒292-0455 千葉県君津市俵田729-3',
'26a177c8-9fa2-4c6d-a3b6-0219ca86e909':'CAMPER LIFE',
'd6af66c2-22de-47b3-ab67-fae09d2f31a4':'旅する愛車と、これからも。',
'51e38800-e5d9-4707-9ea9-468aabfb2e12':'キャブコン、バンコン、軽キャンパー。車両のかたちも、楽しみ方もそれぞれ。愛車の車種や設備、気になることをお聞かせください。※車両イラストはイメージです。',
'cc6586db-9f2d-4142-946b-a3ad05ec1075':'店舗名',
'97fc5bf4-179c-46fb-919e-86e9cd3a4f6c':'RV BASE Lab',
'd5a35278-90bc-4070-8b62-671471bb0f63':'認証番号',
'f1a6a807-be80-4bc8-88a1-17cf398921a4':'関東運輸局長認証 第3-5923号',
'bf7cf840-44e8-4878-b3cf-46f0bda98f07':'〒292-0455 千葉県君津市俵田729-3',
'd55dbdb6-66c1-4203-abd7-6a831e9c39f6':'〒292-0455 千葉県君津市俵田729-3',
'cdc5c411-49e8-40f1-875b-f171d03c1426':'050-5585-9522',
'a1453fca-dcc4-4ecf-bc28-73381cb21403':'営業時間',
'4cf13a6c-b3d7-463c-b5c3-8c3202cf72bd':'24時間営業・定休日なし',
'c0763d0f-3baf-4783-8130-642379616964':'修理・整備／電装・快適装備／カスタム／持込部品取付',
'705b88bc-5d63-4f9d-9afa-196daddf705d':'050-5585-9522',
'5ecfc7d9-91bf-4fbe-8b6e-89d065764d4a':'ご来店前に',
'ef4c7adb-7751-4852-9c90-238a3d3f0daf':'まずはご相談ください',
'f73b9b20-130b-4744-ba8c-4a8ae7120314':'受付・対応状況はお問い合わせください',
'38a443ab-86e6-48d8-b1ed-e0af2b3fdd4c':'写真で相談する（LINE）',
'ff2173d9-856e-429e-a3ec-4eac7f8faf92':'LINEで整備の相談',
'0e2b054e-9d64-4f57-adc2-89335ff8b456':'© 2026 RV BASE Lab',
}
for key,value in replacements.items(): settext(key,value)
for e in doc.xpath('//p'):
    t=''.join(e.itertext())
    if 'まごころの車屋です' in t or '公式SNSにて' in t:
        for c in list(e):e.remove(c)
        e.text='旅する愛車の、かかりつけ。' if 'まごころ' in t else 'LINEで気軽にご相談！'
others=doc.xpath('//*[@data-s-64b00699]')
for e,value in zip(others,['購入したパーツの取付をご希望の方へ。部品のメーカー・型番・商品情報・付属品をお知らせください。取付可否を確認します。','車内の使い勝手や旅のスタイルに合わせたカスタム。こうしたい、というイメージからご相談いただけます。','動かせない場合や搬送が必要なときは、車両と現在の状況をお電話でお知らせください。対応可能な内容を確認します。']):
    for c in list(e):e.remove(c)
    e.text=value

# Remove reference-company destinations and make every contact/link useful.
for e in list(doc.xpath('//a[@href]')):
    href=e.get('href')
    if 'instagram.com' in href or 'youtube.com' in href:
        e.getparent().remove(e);continue
    if 'page.line.me' in href or href.startswith('mailto:'):e.set('href','https://lin.ee/bryjnk0')
    if href.startswith('tel:'):e.set('href','tel:05055859522')
    if 'maps.app.goo.gl' in href:e.set('href','https://www.google.com/maps/search/?api=1&query='+__import__('urllib.parse',fromlist=['quote']).quote('RV BASE Lab 千葉県君津市俵田729-3'))
    if e.get('href','').startswith('http'): e.set('target','_blank');e.set('rel','noopener noreferrer')
node('4cf13a6c-b3d7-463c-b5c3-8c3202cf72bd').set('href','https://rvbaselab.com/access')

# Replace service banner lettering; preserve their original slots and surrounding motion.
for name,w,h,label,n in [('rv-repair-wide.svg',2600,800,'REPAIR',1),('rv-repair-mobile.svg',780,540,'REPAIR',1),('rv-electrical-wide.svg',2600,800,'ELECTRICAL',2),('rv-electrical-mobile.svg',780,540,'ELECTRICAL',2)]:
    color=GREEN if n==1 else BROWN
    svg(name,w,h,f'<rect x="4" y="4" width="{w-8}" height="{h-8}" rx="30" fill="{color}" stroke="{INK}" stroke-width="7"/>'+text(40,h*.78,label,h*.7,'#fff',900,f'textLength="{w-80}" lengthAdjust="spacingAndGlyphs"'))
for key,name in [('c6a49506-dfb7-4cb0-9759-9c2b136dace9','rv-repair-wide.svg'),('2fe22140-b6a5-462a-9df5-49528e3023fd','rv-repair-mobile.svg'),('94e5273b-f78f-45b0-95e0-d7b370ce23a3','rv-electrical-wide.svg'),('bc15fc9a-5e0b-430a-98ff-18432aadaf80','rv-electrical-mobile.svg')]:img(key,'assets/'+name)

# Simple native service emblems match the reference's illustrated card structure.
icons=[
    '<rect x="132" y="180" width="250" height="165" rx="18"/><path d="M205 180V155H300V180M382 230H402V295H382"/><path d="M195 260H250M222 233V287M290 260H338"/>',
    '<path d="M180 190H340L370 340H150Z"/><path d="M170 240H350M160 290H360M232 190L220 340M288 190L300 340M260 340V380M210 380H310"/><circle cx="385" cy="137" r="35"/><path d="M385 75V58M385 216V200M446 137H464M306 137H322"/>',
    '<rect x="150" y="165" width="220" height="190" rx="28"/><path d="M185 215H335M185 255H335M185 295H335M205 375Q165 405 205 430M260 375Q220 405 260 430M315 375Q275 405 315 430"/>',
    '<path d="M185 120A75 75 0 0 0 250 230L365 345Q390 375 360 400Q335 420 310 392L200 280A75 75 0 0 1 120 180L165 225L208 180Z"/>',
    '<path d="M150 300V205H330L385 265V335H150Z"/><path d="M190 205V170H310V205M330 220V270H380"/><circle cx="205" cy="335" r="30"/><circle cx="330" cy="335" r="30"/><path d="M200 125H290M245 80V170"/>',
    '<path d="M120 300V230H235L275 285H370V330H120Z"/><circle cx="175" cy="330" r="30"/><circle cx="320" cy="330" r="30"/><path d="M280 285L320 135H385M385 135V225Q385 255 357 255"/>'
]
for i,graphic in enumerate(icons):
    svg(f'rv-service-{i}.svg',520,520,f'<circle cx="260" cy="260" r="247" fill="{PAPER}" stroke="{INK}" stroke-width="6"/><g fill="none" stroke="{GREEN if i%2==0 else BROWN}" stroke-width="13" stroke-linejoin="round" stroke-linecap="round">{graphic}</g>')
for i,key in enumerate(['818d2065-327a-4671-95c0-e329b3f25d78','45b42980-e7c0-4c41-8042-6e940f5cc2ef','6e2e814e-3b12-406c-b1ed-be903ed052fb','5359aed4-0bd4-4eca-8f0f-17bd013fd1f8','7830bbfd-2b41-424b-9fa9-460609b01499','713605ed-176d-4041-bf34-99c2c331631e']):img(key,f'assets/rv-service-{i}.svg')

for i,label in enumerate(['旅行前の点検も','電装の相談も','愛車とまた旅へ']):
    svg(f'rv-speech-{i}.svg',202,90,f'<path d="M12 4H190Q198 4 198 13V70Q198 78 190 78H107L100 87L94 78H12Q4 78 4 70V13Q4 4 12 4Z" fill="#fff" stroke="{INK}" stroke-width="4"/>'+text(101,48,label,20,INK,800,'text-anchor="middle"'))

variants=[('cabover','キャブコン'),('van','バンコン'),('mini','軽キャンパー')]
for index,car in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," camper-swapped ")]')):
    kind,label=variants[index%3]
    car.set('data-camper-type',kind)
    body=car.xpath('./img[contains(@class,"replacement-camper")]')[0]
    body.set('src',f'assets/camper-side-{kind}.png');body.set('alt',label+'の横向きイラスト')
    bubble=car.xpath('./img[starts-with(@id,"fv-car")]')
    if bubble:bubble[0].set('src',f'assets/rv-speech-{index%3}.svg');bubble[0].set('alt',['旅行前の点検も','電装の相談も','愛車とまた旅へ'][index%3])
doc.get_element_by_id('service1-cars-img').set('src','assets/camper-side-cabover.png')
doc.get_element_by_id('overview-car-img').set('src','assets/camper-side-van.png')

# A camper illustration carousel replaces photographs of the unrelated reference shop.
covers=[]
for kind,label in variants:
    encoded=base64.b64encode((A/f'camper-side-{kind}.png').read_bytes()).decode()
    covers.append(svg(f'rv-gallery-{kind}.svg',1080,720,f'<rect width="1080" height="720" fill="{PAPER}"/>'+text(55,100,label,54,GREEN)+text(57,143,'CAMPER LIFE / RV BASE Lab',22,BROWN,600)+f'<image href="data:image/png;base64,{encoded}" x="60" y="190" width="960" height="460" preserveAspectRatio="xMidYMid meet"/>'))
gallery=doc.get_element_by_id('slider-wrapper-1');gallery.set('data-reference-photos',json.dumps(covers))
for i,photo in enumerate(gallery.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," image ")]')):
    photo.set('style',f'background-image:url("{covers[i%3]}");')
mapframe=node('e7ed8e53-f8ab-443b-b6ba-d9b6ab0bebb2')
mapframe.set('class',mapframe.get('class','')+' rv-map-card')
etree.SubElement(mapframe,'p',{'class':'rv-map-kicker'}).text='CHIBA / KIMITSU'
etree.SubElement(mapframe,'h3').text='RV BASE Lab'
etree.SubElement(mapframe,'p').text='千葉県君津市俵田729-3'
etree.SubElement(mapframe,'p').text='ご来店前に、車両とご相談内容をお知らせください。'
etree.SubElement(mapframe,'a',{'href':node('c940a4b8-4cd9-42e4-8e84-dea43e2be4b2').get('href'),'target':'_blank','rel':'noopener noreferrer'}).text='Google マップで道順を見る ↗'

# Replace marquees and baked reference wordmarks without changing their timing.
for name,w,h,label in [('rv-marquee.svg',2705,88,'CAMPER REPAIR — RV BASE Lab — CAMPER REPAIR — RV BASE Lab —'),('rv-contact-marquee.svg',2849,88,'LET’S TALK ABOUT YOUR CAMPER — RV BASE Lab —'),('rv-footer-label.svg',230,93,'RV BASE Lab')]:
    svg(name,w,h,text(4,h*.78,label,h*.75,INK,900,f'textLength="{w-8}" lengthAdjust="spacingAndGlyphs"'))
for e in doc.xpath('//img'):
    src=e.get('src','')
    if 'bdeee24e' in src:e.set('src','assets/rv-marquee.svg')
    if 'a8905137' in src:e.set('src','assets/rv-contact-marquee.svg')
    if '773995d1' in src:e.set('src','assets/rv-footer-label.svg')
    if src.startswith('reference-assets/') and any(x in src for x in ['1621a0cf','dc4dbbee','8dca9d5a','cf955d45','bd2a8b2d','70367200','e9eca1f6','d218713e','0cffce71','ea19e62a','e755cab9']):e.set('class',e.get('class','')+' rv-earth-art')
    e.set('alt',e.get('alt','').replace('MARUYOSHI','RV BASE Lab').replace('マルヨシ自動車','RV BASE Lab'))

# This slot originally contained the reference company's storefront; use a native label.
svg('rv-base-sign.svg',2340,1200,f'<rect x="8" y="8" width="2324" height="1184" rx="65" fill="{GREEN}" stroke="{INK}" stroke-width="12"/>'+text(1170,280,'CAMPER REPAIR WORKSHOP',75,'#e8eddf',700,'text-anchor="middle"')+text(1170,600,'RV BASE Lab',240,'#fff',900,'text-anchor="middle"')+text(1170,810,'千葉県君津市 / 房総のキャンピングカー修理工場',64,'#fff',700,'text-anchor="middle"')+text(1170,990,'直して、整えて。また、旅に出よう。',60,'#e8eddf',700,'text-anchor="middle"'))
img('2a4a899d-7d01-4870-81b2-f1febb6a1991','assets/rv-base-sign.svg','RV BASE Lab 千葉県君津市')
svg('rv-overview-ring.svg',720,720,f'<circle cx="360" cy="360" r="351" fill="{GREEN}" stroke="{INK}" stroke-width="8"/><circle cx="360" cy="360" r="256" fill="{PAPER}" stroke="{PAPER}" stroke-width="5"/><defs><path id="ring" d="M360 62 A298 298 0 1 1 359.9 62"/></defs><text fill="{PAPER}" font-size="42" font-weight="800" letter-spacing="4"><textPath href="#ring" startOffset="0%">RV BASE Lab · CAMPER REPAIR · RV BASE Lab · CAMPER REPAIR · </textPath></text>')
for key in ['f297743d-f5d9-4b68-90ca-bfdb3339f50f','2e3b7721-5587-4c67-89af-bd8f673c1e4c']:img(key,'assets/rv-overview-ring.svg')
for e in doc.xpath('//p[normalize-space(text())="MENU"]'):
    e.set('role','button');e.set('tabindex','0');e.set('data-rv-menu','');e.set('aria-label','メニューを開く')

head=doc.find('head')
for e in list(head.xpath('./meta[@property]|./link[@rel="icon"]|./link[@rel="apple-touch-icon"]')):head.remove(e)
head.find('title').text='RV BASE Lab｜キャンピングカー修理・メンテナンス｜千葉県君津市'
for e in head.xpath('./meta[@name="description"]'):e.set('content','千葉県君津市のRV BASE Lab。キャンピングカーの修理、電装・快適装備、持込部品取付、カスタムのご相談。')
etree.SubElement(head,'link',{'rel':'icon','href':'assets/rv-logo.svg','type':'image/svg+xml'})
etree.SubElement(head,'link',{'rel':'stylesheet','href':'rv-theme.css'})
for e in list(doc.xpath('//*[@id="codex-browser-sidebar-comments-root"]')):e.getparent().remove(e)
for e in doc.xpath('//*[not(*)]'):
    if e.text and 'マルヨシ自動車株式会社｜' in e.text:e.text='RV BASE Lab 読み込まれました'
    for key in ['aria-label','title']:
        if e.get(key):e.set(key,e.get(key).replace('マルヨシ自動車','RV BASE Lab'))

# Resolve design tokens and raw colors in the retained compiled sheet.
css=(D/'reference-layout.css').read_text()
for old,new in {'#00a0e9ff':GREEN,'#e60012ff':BROWN,'#d9f3ffff':'#e8eddf','#ffe2e4ff':'#eee3d4','#eaeff1ff':PAPER,'#171523ff':INK,'#42515bff':'#51483f','#00d11cff':GREEN,'#99a9b0ff':'#a29c89','#cdd1d4ff':'#ded6c5'}.items():css=css.replace(old,new)
(D/'reference-layout.css').write_text(css)
(D/'index.html').write_text('<!DOCTYPE html>\n'+html.tostring(doc,encoding='unicode',method='html'))
assert 'tel:0287' not in (D/'index.html').read_text()
print('Adapted RV BASE Lab content, contact links, palette, and three camper variants.')
