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
const camper = document.querySelector('.hero-camper');
const speech = document.querySelector('.camper-speech');
const phrases = ['今度の休みは、どこ行こう？', '出発前に、ちょっと点検。', 'まだまだ、一緒に走ろう。', '次のキャンプが、楽しみだ。'];
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
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const headingObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        headingObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.about h2, .section-heading h2, .promise-copy h2, .contact h2').forEach(heading => {
    heading.classList.add('reveal-heading');
    headingObserver.observe(heading);
  });
}
