"""Build only the separate lithium LP. Never modify the existing repair page."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'lithium-lp'
DESTINATION = ROOT / 'dist' / 'lithium'
DESTINATION.mkdir(exist_ok=True)
(DESTINATION / 'assets').mkdir(exist_ok=True)

for name in ('index.html', 'styles.css', 'app.js'):
    shutil.copy2(SOURCE / name, DESTINATION / name)

shared_assets = {
    'rv-base-lab-official-logo.png': 'rv-base-lab-official-logo.png',
    'line-brand-icon.png': 'line-brand-icon.png',
    'manga-line-worry-appliances-v2.png': 'family-appliances.png',
    'manga-line-worry-comfort-v1.png': 'family-comfort.png',
    'manga-line-service-electrical-v1.png': 'electrical-inspection.png',
    'manga-line-flow-guide-listen-v1.png': 'mechanic-guide.png',
}
for source, destination in shared_assets.items():
    shutil.copy2(ROOT / 'dist' / 'assets' / source, DESTINATION / 'assets' / destination)

for name in ('camp-lights-on.png', 'camp-lights-off.png'):
    if not (DESTINATION / 'assets' / name).is_file():
        raise FileNotFoundError(f'Missing generated opening image: {name}')

print('Built dist/lithium/. Existing dist/index.html and repair assets are unchanged.')
