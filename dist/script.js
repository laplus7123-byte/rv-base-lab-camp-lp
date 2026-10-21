const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  mobileNav.hidden = expanded;
  if (!expanded) mobileNav.style.top = `${document.querySelector('.header').getBoundingClientRect().bottom}px`;
});
window.addEventListener('scroll', () => {
  if (!mobileNav.hidden) mobileNav.style.top = `${document.querySelector('.header').getBoundingClientRect().bottom}px`;
}, { passive: true });
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  menuButton.setAttribute('aria-expanded', 'false');
  mobileNav.hidden = true;
}));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !mobileNav.hidden) {
    menuButton.setAttribute('aria-expanded', 'false');
    mobileNav.hidden = true;
    menuButton.focus();
  }
});
const camper = document.querySelector('.camper-button');
const speech = document.querySelector('.camper-speech');
const phrases = ['次は、どこへ行こう？', 'その不調、まずは相談しよう！', '相棒を整えて、出発！', '次のキャンプが、楽しみだ！'];
let phrase = 0;
camper.addEventListener('click', () => {
  phrase = (phrase + 1) % phrases.length;
  speech.textContent = phrases[phrase];
  camper.classList.remove('excited');
  void camper.offsetWidth;
  camper.classList.add('excited');
});
document.querySelectorAll('[data-service]').forEach(button => button.addEventListener('click', () => {
  const selection = document.querySelector('#selected-service');
  selection.textContent = `「${button.dataset.service}」のご相談ですね。下記からお気軽にご連絡ください。`;
  selection.hidden = false;
  document.querySelector('#contact').scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
}));
