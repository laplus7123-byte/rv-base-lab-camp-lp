const camper = document.querySelector('.fixed-camper');
const toggle = camper.querySelector('.fixed-motion-control');
toggle.addEventListener('click', () => {
  const paused = camper.classList.toggle('is-paused');
  toggle.setAttribute('aria-pressed', String(paused));
  toggle.textContent = paused ? '動かす ▶' : '動きを止める Ⅱ';
});
