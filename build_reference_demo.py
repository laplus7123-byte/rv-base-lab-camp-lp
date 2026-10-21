from pathlib import Path
from urllib.parse import urljoin, urlparse
import json
from lxml import html, etree

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
SOURCE = ROOT / 'reference-source/rendered.html'
PAGE = ROOT / 'reference-source/page.json'
CSS = ROOT / 'reference-source/layout.css'
ORIGIN = 'https://maruyoshi-car.com/'
manifest_path = DIST / 'reference-assets/manifest.json'
assets = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

nodes = {}
def collect(value):
    if isinstance(value, dict):
        if value.get('uuid'):
            nodes[value['uuid']] = value
        for child in value.values():
            collect(child)
    elif isinstance(value, list):
        for child in value:
            collect(child)
collect(json.loads(PAGE.read_text()))

doc = html.fromstring(SOURCE.read_text())
head = doc.find('head')
for tag in list(doc.xpath('//script|//style')):
    tag.getparent().remove(tag)
for link in list(doc.xpath('//link')):
    rel = link.get('rel', '')
    if rel in ('modulepreload', 'prefetch', 'preload', 'canonical'):
        link.getparent().remove(link)
        continue
    if link.get('href'):
        original = urljoin(ORIGIN, link.get('href'))
        link.set('href', assets.get(original, original))

images_resolved = 0
for img in doc.xpath('//img'):
    key = next((key[7:] for key in img.attrib if key.startswith('data-s-')), None)
    item = nodes.get(key, {}).get('content', {})
    src = item.get('src')
    if isinstance(src, str) and src.startswith('https://'):
        img.set('src', assets.get(src, src))
        images_resolved += 1
    elif img.get('src', '').startswith('http'):
        img.set('src', assets.get(img.get('src'), img.get('src')))
    img.attrib.pop('srcset', None)
    img.attrib.pop('loading', None)

for image in doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " image ")]'):
    key = next((key[7:] for key in image.attrib if key.startswith('data-s-')), None)
    src = nodes.get(key, {}).get('content', {}).get('src')
    if isinstance(src, str) and src.startswith('https://'):
        local = assets.get(src, src)
        image.set('style', image.get('style', '') + f';background-image:url("{local}");')

gallery = doc.get_element_by_id('slider-wrapper-1')
covers = [assets.get(item['cover'], item['cover']) for item in nodes['31f603ca-c584-4b3b-aea4-a96034451258']['state']['list']]
gallery.set('data-reference-photos', json.dumps(covers))
slides = [child for child in gallery if child.get('id') == 'slide-1']
for index, slide in enumerate(slides):
    slide.set('data-reference-slide', str(index))
    photo = next(e for e in slide.iter() if 'image' in e.get('class', '').split())
    photo.set('style', photo.get('style', '') + f';background-image:url("{covers[index % len(covers)]}");')

for anchor in doc.xpath('//a[@href]'):
    parsed = urlparse(urljoin(ORIGIN, anchor.get('href')))
    if parsed.netloc == 'maruyoshi-car.com' and parsed.path in ('', '/'):
        anchor.set('href', '#' + (parsed.fragment or 'page-top'))

vehicle_bodies = ('47a2475d', '38ba8bf2', '08769ac4')
changed = 0
for car in doc.xpath('//*[starts-with(@id,"car") and not(contains(@id,"tire"))]'):
    body = next((e for e in car if e.tag == 'img' and any(key in e.get('src', '') for key in vehicle_bodies)), None)
    if body is None:
        continue
    body.set('src', 'assets/camper.png')
    body.set('alt', 'キャンピングカー')
    body.set('class', body.get('class', '') + ' replacement-camper')
    car.set('class', car.get('class', '') + ' camper-swapped')
    for position in ('front', 'back'):
        original_wheel = next((e for e in car if e.get('id', '').endswith('-tire-' + position)), None)
        if original_wheel is None:
            continue
        rim = etree.Element('span', {'class': 'camper-rim camper-rim-' + position, 'aria-hidden': 'true'})
        spin = etree.SubElement(rim, 'span', {'id': original_wheel.get('id'), 'class': 'camper-rim-spin'})
        car.replace(original_wheel, rim)
    changed += 1

for rel in ('reference-layout.css', 'camper-swap.css'):
    etree.SubElement(head, 'link', {'rel': 'stylesheet', 'href': rel})
etree.SubElement(head, 'meta', {'name': 'robots', 'content': 'noindex, nofollow'})
etree.SubElement(head, 'script', {'src': 'reference-runtime.js', 'defer': 'defer'})
DIST.joinpath('reference-layout.css').write_text(CSS.read_text())
DIST.joinpath('index.html').write_text('<!DOCTYPE html>\n' + html.tostring(doc, encoding='unicode', method='html'))
assert changed == 6, f'Expected six animated vehicle instances, got {changed}'
print(json.dumps({'camper_instances': changed, 'resolved_images': images_resolved, 'local_asset_mappings': len(assets)}))
