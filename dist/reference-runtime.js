// Lightweight behavior for the static reference comparison.
// Vehicle movement, wheel rotation and speech timing use the original CSS.
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', event => {
    const id = anchor.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    history.replaceState(null, '', '#' + id);
  });
});

// Reveal the static copy's sections when they enter the viewport.
// Class removal matches the reference renderer's end state.
if ('IntersectionObserver' in window) {
  const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.remove('appear', 'appear-active');
      reveal.unobserve(entry.target);
    }
  }), { rootMargin: '100px 0px', threshold: 0 });
  document.querySelectorAll('.appear').forEach(element => reveal.observe(element));
}

const gallery = document.querySelector('#slider-wrapper-1');
if (gallery) {
  const photos = JSON.parse(gallery.dataset.referencePhotos || '[]');
  const slides = [...gallery.querySelectorAll('[data-reference-slide]')];
  const transformVariable = '--sd-a38d4a39_002ddf1b_002d453f_002d9748_002d360dd24c53e3-transform';
  let center = 3;
  let moving = false;
  const renderPhotos = () => slides.forEach((slide, index) => {
    const photo = photos[(center + index - 3 + photos.length) % photos.length];
    slide.querySelector('.image').style.backgroundImage = `url("${photo}")`;
  });
  const move = direction => {
    if (moving || !photos.length) return;
    moving = true;
    slides.forEach(slide => {
      slide.style.transitionDuration = '550ms';
      slide.style.setProperty(transformVariable, `translateX(${-direction * 100}%)`);
    });
    setTimeout(() => {
      center = (center + direction + photos.length) % photos.length;
      slides.forEach(slide => {
        slide.style.transitionDuration = '0ms';
        slide.style.setProperty(transformVariable, 'none');
      });
      renderPhotos();
      moving = false;
    }, 560);
  };
  gallery.querySelector('[aria-label="Prev Slide"]')?.addEventListener('click', () => move(-1));
  gallery.querySelector('[aria-label="Next Slide"]')?.addEventListener('click', () => move(1));
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) setInterval(() => move(1), 5500);
}
