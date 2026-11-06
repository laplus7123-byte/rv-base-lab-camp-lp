(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const opening = document.querySelector('.opening');
  const lightSwitch = document.querySelector('.light-switch');
  let introTimer;
  let userChangedLights = false;
  const setLights = on => {
    opening.classList.toggle('is-lit', on);
    document.body.classList.toggle('camp-is-lit', on);
    lightSwitch.setAttribute('aria-pressed', String(on));
    lightSwitch.setAttribute('aria-label', on ? 'イラストの灯りを消す' : 'イラストの灯りをつける');
    lightSwitch.querySelector('span').textContent = on ? '灯りを消す' : '灯りをつける';
  };
  if (opening && lightSwitch) {
    opening.classList.add('lights-ready');
    lightSwitch.hidden = false;
    lightSwitch.addEventListener('click', () => {
      userChangedLights = true;
      clearTimeout(introTimer);
      setLights(!opening.classList.contains('is-lit'));
    });
    const frames = [...opening.querySelectorAll('.hero-frame')];
    Promise.all(frames.map(img => img.decode ? img.decode().catch(() => {}) : Promise.resolve())).then(() => {
      if (userChangedLights) return;
      introTimer = setTimeout(() => setLights(true), reduced.matches ? 0 : 750);
    });
  }

  if (opening) {
    let heroInView = true;
    const updateHeroMotion = () => {
      opening.classList.toggle('hero-motion-active', heroInView && !document.hidden && !reduced.matches);
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        heroInView = entries[0].isIntersecting;
        updateHeroMotion();
      }).observe(opening.querySelector('.hero-copy'));
    }
    document.addEventListener('visibilitychange', updateHeroMotion);
    reduced.addEventListener?.('change', updateHeroMotion);
    updateHeroMotion();
  }

  const carousel = document.querySelector('.scene-carousel');
  if (carousel) {
    const viewport = carousel.querySelector('.scene-viewport');
    const track = carousel.querySelector('.scene-track');
    const originals = [...track.children];
    const dots = [...carousel.querySelectorAll('[data-slide-to]')];
    const rotation = carousel.querySelector('.scene-autoplay');
    const status = carousel.querySelector('.scene-status');
    const clone = slide => {
      const copy = slide.cloneNode(true);
      copy.classList.add('is-clone');
      copy.setAttribute('aria-hidden', 'true');
      return copy;
    };
    // End copies make the final-to-first transition travel in the same direction.
    track.prepend(clone(originals[originals.length - 1]));
    track.append(clone(originals[0]));
    const slides = [...track.children];
    let position = 1;
    let logicalIndex = 0;
    let moving = false;
    let autoTimer;
    let settleTimer;
    let inView = false;
    let focused = false;
    let explicitPlay = false;
    let wantsRotation = !reduced.matches;
    let pointerStart;
    let suppressClick = false;

    const updateRotationButton = () => {
      rotation.classList.toggle('is-paused', !wantsRotation);
      const label = wantsRotation ? '自動切り替えを一時停止' : '自動切り替えを再生';
      rotation.setAttribute('aria-label', label);
      rotation.title = label;
    };
    const scheduleRotation = () => {
      clearTimeout(autoTimer);
      if (!wantsRotation || !inView || pointerStart || (focused && !explicitPlay) || document.hidden || moving) return;
      autoTimer = setTimeout(() => moveTo(position + 1), 4800);
    };
    const stopRotation = () => {
      wantsRotation = false;
      explicitPlay = false;
      clearTimeout(autoTimer);
      updateRotationButton();
    };
    const render = animate => {
      track.classList.toggle('is-moving', animate && !reduced.matches);
      const cardWidth = slides[0].offsetWidth;
      const gap = parseFloat(getComputedStyle(track).gap) || 0;
      const x = (viewport.clientWidth - cardWidth) / 2 - position * (cardWidth + gap);
      track.style.transform = `translate3d(${x}px,0,0)`;
      slides.forEach((slide, index) => slide.classList.toggle('is-active', index === position));
      originals.forEach((slide, index) => slide.setAttribute('aria-hidden', String(index !== logicalIndex)));
      dots.forEach((dot, index) => {
        if (index === logicalIndex) dot.setAttribute('aria-current', 'true');
        else dot.removeAttribute('aria-current');
      });
    };
    const settle = () => {
      clearTimeout(settleTimer);
      if (position === 0) position = originals.length;
      else if (position === slides.length - 1) position = 1;
      render(false);
      moving = false;
      scheduleRotation();
    };
    const moveTo = (next, manual = false) => {
      if (moving) return;
      clearTimeout(autoTimer);
      position = Math.max(0, Math.min(slides.length - 1, next));
      logicalIndex = (position - 1 + originals.length) % originals.length;
      moving = !reduced.matches;
      render(true);
      if (manual) status.textContent = originals[logicalIndex].getAttribute('aria-label');
      if (moving) settleTimer = setTimeout(settle, 650);
      else settle();
    };
    track.addEventListener('transitionend', event => {
      if (event.target === track && event.propertyName === 'transform' && moving) settle();
    });
    carousel.classList.add('carousel-ready');
    carousel.querySelector('.scene-controls').hidden = false;
    carousel.querySelector('.scene-hint').hidden = false;
    render(false);
    updateRotationButton();
    carousel.querySelector('.scene-prev').addEventListener('click', () => moveTo(position - 1, true));
    carousel.querySelector('.scene-next').addEventListener('click', () => moveTo(position + 1, true));
    dots.forEach((dot, index) => dot.addEventListener('click', () => moveTo(index + 1, true)));
    carousel.addEventListener('keydown', event => {
      const next = {ArrowLeft: position - 1, ArrowRight: position + 1, Home: 1, End: originals.length}[event.key];
      if (next === undefined) return;
      event.preventDefault();
      moveTo(next, true);
    });
    rotation.addEventListener('click', () => {
      wantsRotation = !wantsRotation;
      explicitPlay = wantsRotation;
      updateRotationButton();
      scheduleRotation();
    });
    track.addEventListener('click', event => {
      if (suppressClick) { suppressClick = false; return; }
      const card = event.target.closest('.scene-card');
      if (card && !card.classList.contains('is-active')) moveTo(slides.indexOf(card), true);
    });
    viewport.addEventListener('pointerdown', event => {
      if (!event.isPrimary || event.button !== 0) return;
      pointerStart = {x: event.clientX, y: event.clientY, id: event.pointerId};
      suppressClick = false;
      clearTimeout(autoTimer);
    });
    window.addEventListener('pointerup', event => {
      if (!pointerStart || event.pointerId !== pointerStart.id) return;
      const dx = event.clientX - pointerStart.x;
      const dy = event.clientY - pointerStart.y;
      pointerStart = null;
      if (Math.abs(dx) < 35 || Math.abs(dx) < Math.abs(dy) * 1.25) { scheduleRotation(); return; }
      suppressClick = true;
      moveTo(position + (dx < 0 ? 1 : -1), true);
    });
    window.addEventListener('pointercancel', () => { pointerStart = null; scheduleRotation(); });
    // Pointer controls reset the interval; keyboard focus pauses for reading.
    carousel.addEventListener('pointerdown', () => { focused = false; }, {capture: true});
    carousel.addEventListener('focusin', event => {
      focused = event.target.matches(':focus-visible');
      explicitPlay = false;
      scheduleRotation();
    });
    carousel.addEventListener('keydown', () => { focused = true; explicitPlay = false; clearTimeout(autoTimer); });
    carousel.addEventListener('focusout', event => {
      if (carousel.contains(event.relatedTarget)) return;
      focused = false;
      scheduleRotation();
    });
    document.addEventListener('visibilitychange', scheduleRotation);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        inView = entries[0].isIntersecting && entries[0].intersectionRatio >= .35;
        scheduleRotation();
      }, {threshold: .35}).observe(carousel);
    } else {
      const checkVisibility = () => {
        const box = carousel.getBoundingClientRect();
        inView = box.top < innerHeight * .7 && box.bottom > innerHeight * .3;
        scheduleRotation();
      };
      window.addEventListener('scroll', checkVisibility, {passive: true});
      checkVisibility();
    }
    if ('ResizeObserver' in window) new ResizeObserver(settle).observe(viewport);
    else window.addEventListener('resize', settle);
    reduced.addEventListener?.('change', () => { stopRotation(); settle(); });
  }

  const powerMap = document.querySelector('.power-map');
  if (powerMap && 'IntersectionObserver' in window) {
    const chargeToggle = powerMap.querySelector('.charge-toggle');
    let chargeInView = false;
    let chargePaused = false;
    const updateCharge = () => {
      powerMap.classList.toggle('charge-running', !reduced.matches);
      powerMap.classList.toggle('charge-paused', chargePaused || !chargeInView || document.hidden);
      chargeToggle.hidden = reduced.matches;
      chargeToggle.classList.toggle('is-paused', chargePaused);
      chargeToggle.setAttribute('aria-label', chargePaused ? '充電アニメーションを再生' : '充電アニメーションを一時停止');
      chargeToggle.querySelector('span').textContent = chargePaused ? '再生' : '一時停止';
    };
    new IntersectionObserver(entries => {
      chargeInView = entries[0].isIntersecting && entries[0].intersectionRatio >= .35;
      updateCharge();
    }, {threshold: .35}).observe(powerMap);
    chargeToggle.addEventListener('click', () => { chargePaused = !chargePaused; updateCharge(); });
    document.addEventListener('visibilitychange', updateCharge);
    reduced.addEventListener?.('change', updateCharge);
    updateCharge();
  }

  let revealObserver;
  try {
    if (!reduced.matches && 'IntersectionObserver' in window) {
      revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        });
      }, {threshold: 0.12, rootMargin: '0px 0px -24px 0px'});
      document.querySelectorAll('.reveal, .travel-ribbon').forEach(el => revealObserver.observe(el));
      document.documentElement.classList.add('motion-ready');
    }
  } catch {
    revealObserver?.disconnect();
    document.documentElement.classList.remove('motion-ready');
  }
  reduced.addEventListener?.('change', event => {
    if (!event.matches) return;
    clearTimeout(introTimer);
    if (!userChangedLights && opening && lightSwitch) setLights(true);
    revealObserver?.disconnect();
    document.documentElement.classList.remove('motion-ready');
  });

  const chapters = [...document.querySelectorAll('[data-chapter]')];
  const navLinks = [...document.querySelectorAll('.chapter-nav a[href^="#"]')];
  const sticky = document.querySelector('.sticky-contact');
  const contact = document.getElementById('contact');
  let framePending = false;
  let activeId;
  const updateScrollState = () => {
    framePending = false;
    const readingLine = Math.min(window.innerHeight * 0.35, 240);
    let nextId = chapters[0]?.id;
    chapters.forEach(section => {
      if (section.getBoundingClientRect().top <= readingLine) nextId = section.id;
    });
    if (nextId !== activeId) {
      activeId = nextId;
      navLinks.forEach(link => {
        const current = link.getAttribute('href') === '#' + activeId;
        link.classList.toggle('is-current', current);
        if (current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
    if (sticky && opening && contact) {
      const visible = opening.getBoundingClientRect().bottom < 80 && contact.getBoundingClientRect().top > window.innerHeight * 0.55;
      sticky.classList.toggle('is-visible', visible);
    }
  };
  const scheduleScrollState = () => {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(updateScrollState);
  };
  window.addEventListener('scroll', scheduleScrollState, {passive:true});
  window.addEventListener('resize', scheduleScrollState, {passive:true});
  window.addEventListener('load', scheduleScrollState, {once:true});
  updateScrollState();
})();
