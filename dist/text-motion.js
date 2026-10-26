(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduced.matches || !('IntersectionObserver' in window)) return;
  const root = document.documentElement;
  const headings = [...document.querySelectorAll([
    '.poster-heading h1', '.story-worries h2', '.worry-copy h3',
    '.story-center-sticky h2', '.story-service-title h3',
    '.story-consult h3', '.camp-intro h2', '.camp-reasons-lead',
    '.camp-reason-panel h3', '.consultation-lead',
    '.camp-faq-copy h2', '.story-access h2', '.story-contact h2'
  ].join(','))];
  let observer;
  let arrowObserver;
  try {
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-text-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -16px 0px' });
    headings.forEach(heading => {
      const vertical = heading.matches('.story-center-sticky h2, .camp-intro h2');
      heading.setAttribute('data-text-reveal', vertical ? 'vertical' : '');
      if (vertical) {
        // Reveal the right-hand column first, preserving vertical Japanese text.
        [...heading.children].forEach((column, index) => {
          column.style.setProperty('--vertical-delay', `${index * 240}ms`);
        });
        observer.observe(heading);
        return;
      }
      const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
      const nodes = [];
      while (walker.nextNode()) {
        if (walker.currentNode.textContent.trim()) nodes.push(walker.currentNode);
      }
      // Inline spans preserve Japanese wrapping, line breaks and vertical type.
      nodes.forEach((node, index) => {
        const unit = document.createElement('span');
        unit.className = 'text-reveal-unit';
        unit.style.setProperty('--text-delay', `${Math.min(index, 4) * 85}ms`);
        node.replaceWith(unit);
        unit.appendChild(node);
      });
      observer.observe(heading);
    });
    arrowObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        entry.target.classList.toggle('is-motion-active', entry.isIntersecting);
      });
    }, { threshold: 0.1 });
    document.querySelectorAll('.story-down').forEach(arrow => arrowObserver.observe(arrow));
    root.classList.add('text-motion-ready');
    reduced.addEventListener?.('change', event => {
      if (!event.matches) return;
      observer.disconnect();
      arrowObserver.disconnect();
      root.classList.remove('text-motion-ready');
    });
  } catch {
    observer?.disconnect();
    arrowObserver?.disconnect();
    root.classList.remove('text-motion-ready');
  }
})();
