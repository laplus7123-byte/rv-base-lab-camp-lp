(() => {
  const bubbles = [...document.querySelectorAll('.story-bubble')];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduced.matches || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('story-animate');
  document.querySelectorAll('.story-worry .story-bubble').forEach((bubble, i) => {
    bubble.style.setProperty('--bubble-delay', `${i * 110}ms`);
  });
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {threshold: 0.35, rootMargin: '0px 0px -35px 0px'});
  bubbles.forEach(bubble => observer.observe(bubble));
  reduced.addEventListener('change', event => {
    if (event.matches) {
      observer.disconnect();
      document.documentElement.classList.remove('story-animate');
    }
  });
})();
