"""Apply the branded camper/family hero and remove the separate site header."""
from pathlib import Path
from lxml import html, etree
ROOT = Path(__file__).resolve().parent

def apply_hero_scene(document):
    old = document.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," poster-hero ")]')[0]
    old.getparent().replace(old, html.fromstring((ROOT / 'hero-scene.html').read_text()))
    head = document.find('head')
    for header in document.xpath('//header[contains(concat(" ",normalize-space(@class)," ")," site-header ")]'):
        header.getparent().remove(header)
    # This script only controls the removed header menu and assumes it exists.
    for script in head.xpath('./script[@src="service-design.js"]'):
        head.remove(script)
    if not head.xpath('./link[@href="hero-scene.css"]'):
        etree.SubElement(head, 'link', {'rel': 'stylesheet', 'href': 'hero-scene.css'})

if __name__ == '__main__':
    path = ROOT / 'dist/index.html'
    document = html.fromstring(path.read_text())
    apply_hero_scene(document)
    from apply_manga_style import apply_manga_style
    apply_manga_style(document)
    path.write_text('<!doctype html>\n' + html.tostring(document, encoding='unicode', method='html'))
