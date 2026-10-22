(() => {
  const camper = document.querySelector('.fixed-camper');
  const bubble = document.querySelector('.fixed-camper-bubble');
  if (!camper || !bubble) return;

  const messages = [
    ['.poster-hero', '旅の前に、点検を。'],
    ['.story-worries', '愛車の「気になる」、聞かせて。'],
    ['#service', '旅に合う整備を、一緒に。'],
    ['#about', '愛車と、これからの旅へ。'],
    ['#flow', 'ご相談から、次の旅まで。'],
    ['.consultation-step:nth-child(1)', 'まずは写真で、ご相談を。'],
    ['.consultation-step:nth-child(2)', '愛車の状態を、一つずつ。'],
    ['.consultation-step:nth-child(3)', '内容と費用は、作業の前に。'],
    ['.consultation-step:nth-child(4)', '整えて、また旅に出よう。'],
    ['#faq', '気になる疑問、お答えします。'],
    ['#store-info', '千葉・君津で、お待ちしています。'],
    ['#contact', 'まずはLINEで、気軽に相談。'],
  ];
  const scenes = messages.flatMap(([selector, text]) => {
    const element = document.querySelector(selector);
    return element ? [{ element, text }] : [];
  });
  const departureScene = document.querySelector('#contact');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let scheduled = false;
  let transition;
  let departed = false;
  let drive;

  function updateDeparture() {
    if (!departureScene) return;
    const reachedBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
    const next = reachedBottom || departureScene.getBoundingClientRect().top <= window.innerHeight * 0.6;
    if (next === departed) return;
    departed = next;
    camper.classList.toggle('is-departed', departed);
    drive?.cancel();
    if (reducedMotion.matches || !camper.animate) return;
    // Facing left: leave forward to the left, come back forward from the right.
    drive = departed
      ? camper.animate(
        [{ transform: 'translateX(0)' }, { transform: 'translateX(calc(-100vw - 100%))' }],
        { duration: 1600, easing: 'cubic-bezier(.5,0,.85,.45)', fill: 'forwards' },
      )
      : camper.animate(
        [{ transform: 'translateX(calc(100% + 30px))' }, { transform: 'translateX(0)' }],
        { duration: 900, easing: 'cubic-bezier(.2,.7,.3,1)' },
      );
  }

  function updateMessage() {
    scheduled = false;
    updateDeparture();
    // Read fresh positions so image loading and accordion changes stay in sync.
    const readingLine = window.innerHeight * 0.42;
    let active = scenes[0];
    for (const scene of scenes) {
      if (scene.element.getBoundingClientRect().top <= readingLine) active = scene;
    }
    if (!active || bubble.textContent === active.text) return;
    bubble.textContent = active.text;
    transition?.cancel();
    if (!reducedMotion.matches && bubble.animate) {
      transition = bubble.animate(
        [{ opacity: 0.6, transform: 'translateY(3px)' }, { opacity: 1, transform: 'translateY(0)' }],
        { duration: 220, easing: 'ease-out' },
      );
    }
  }

  function scheduleUpdate() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(updateMessage);
  }

  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', scheduleUpdate);
  window.addEventListener('pageshow', scheduleUpdate);
  document.addEventListener('toggle', scheduleUpdate, true);
  document.addEventListener('load', scheduleUpdate, true);
  reducedMotion.addEventListener('change', () => {
    transition?.cancel();
    if (reducedMotion.matches) drive?.cancel();
  });
  updateMessage();
})();
