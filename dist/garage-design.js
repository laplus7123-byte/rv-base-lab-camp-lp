const motionButton = document.querySelector('.motion-control');
const garageHero = document.querySelector('.garage-hero');
motionButton.addEventListener('click', () => {
  const paused = !garageHero.classList.contains('is-paused');
  garageHero.classList.toggle('is-paused', paused);
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.textContent = paused ? '動かす ▶' : '動きを止める Ⅱ';
});
