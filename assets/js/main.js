/* Progressive enhancement: every page and all content work without JavaScript. */
(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#primary-nav');
  const narrow = window.matchMedia('(max-width: 900px)');
  function syncMenu() {
    menu.hidden = !narrow.matches;
    menu.setAttribute('aria-expanded', 'false');
    nav.hidden = narrow.matches;
  }
  syncMenu();
  narrow.addEventListener('change', syncMenu);
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.hidden = !open;
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && narrow.matches && !nav.hidden) {
      nav.hidden = true;
      menu.setAttribute('aria-expanded', 'false');
      menu.focus();
    }
  });

  // The provider is contacted only after configuration and only on the public site.
  const visitorMap = document.querySelector('.visitor-map');
  if (visitorMap && visitorMap.dataset.widgetId && visitorMap.dataset.siteUrl) {
    try {
      const site = new URL(visitorMap.dataset.siteUrl);
      const basePath = site.pathname.endsWith('/') ? site.pathname : `${site.pathname}/`;
      const isPublicSite = location.protocol === 'https:' && location.origin === site.origin
        && (location.pathname === site.pathname || location.pathname.startsWith(basePath));
      const key = visitorMap.dataset.widgetId;
      if (isPublicSite && /^[A-Za-z0-9_-]+$/.test(key)) {
        const target = document.querySelector('#visitor-map-widget');
        const placeholder = visitorMap.querySelector('.visitor-map-placeholder');
        const status = visitorMap.querySelector('.visitor-map-status');
        status.textContent = 'Loading visitor map…';
        const script = document.createElement('script');
        script.id = 'mapmyvisitors';
        script.src = `https://mapmyvisitors.com/map.js?d=${encodeURIComponent(key)}&cl=f5f6f7&w=a`;
        script.async = true;
        const observer = new MutationObserver(() => {
          if (target.querySelector('img, canvas, svg, iframe')) {
            placeholder.hidden = true;
            status.textContent = 'Approximate visitor locations based on IP geolocation · MapMyVisitors';
            observer.disconnect();
          }
        });
        observer.observe(target, { childList: true, subtree: true });
        script.onerror = () => {
          status.textContent = 'The visitor map is temporarily unavailable.';
          observer.disconnect();
        };
        target.appendChild(script);
        setTimeout(() => {
          if (!placeholder.hidden) {
            status.textContent = 'The visitor map is temporarily unavailable.';
            observer.disconnect();
          }
        }, 15000);
      }
    } catch (_) {
      // Keep the honest inactive state when a public URL has not been configured.
    }
  }
})();
