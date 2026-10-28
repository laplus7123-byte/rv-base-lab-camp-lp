(() => {
  const details = document.getElementById('lithium-details');
  if (!details) return;

  const openFromHash = () => {
    if (window.location.hash === '#lithium-details') details.open = true;
  };

  document.querySelectorAll('a[href="#lithium-details"]').forEach(link => {
    link.addEventListener('click', () => { details.open = true; });
  });
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
})();
