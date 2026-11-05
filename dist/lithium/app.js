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

  const tabs = [...document.querySelectorAll('[role="tab"][data-scene]')];
  const selectScene = (selected, focus = false) => {
    tabs.forEach(tab => {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
    });
    if (focus) selected.focus();
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectScene(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      selectScene(tabs[next], true);
    });
  });

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
