"""Use the unified manga asset set after composing the page's older templates."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def apply_manga_style(document):
    manifest = json.loads((ROOT / 'manga-style-generation.json').read_text())
    assets = manifest['assets']
    replacements = {
        f"assets/{name}": asset
        for asset in assets
        for name in (asset['old'], asset['name'], *asset.get('previous_names', []))
    }
    for image in document.xpath('//img[@src]'):
        asset = replacements.get(image.get('src'))
        if asset is None:
            continue
        image.set('src', f"assets/{asset['name']}")
        image.set('width', str(asset['width']))
        image.set('height', str(asset['height']))
        image.set('decoding', 'async')
        if asset.get('alt'):
            image.set('alt', asset['alt'])
