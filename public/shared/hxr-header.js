class HxrHeader extends HTMLElement {
  connectedCallback() {
    const current = (this.getAttribute('current') || '').toLowerCase();
    const mode = (this.getAttribute('mode') || '').toLowerCase(); // "overlay" | ""
    const homeHref = this.getAttribute('home-href') || 'index.html';
    const mappingHref = this.getAttribute('mapping-href') || 'gallery.html';
    const labelHome = this.getAttribute('label-home') || 'Home';
    const labelMapping = this.getAttribute('label-mapping') || 'Mapping';

    // If used as an overlay header, expose a safe top offset for other UI on the page.
    if (mode === 'overlay') {
      // 22px top padding + ~72px bar height + ~10px breathing room
      document.documentElement.style.setProperty('--hxr-header-safe-top', '104px');
    }

    const shadow = this.attachShadow({ mode: 'open' });

    const isHome = current === 'home';
    const isMapping = current === 'mapping';

    const pos = mode === 'overlay'
      ? 'position: fixed; inset: 0 0 auto 0; z-index: 2000;'
      : 'position: relative;';

    shadow.innerHTML = `
      <style>
        :host { display: block; ${pos} }
        *, *::before, *::after { box-sizing: border-box; }

        .topbar { padding: 22px 20px 0; }
        .nav {
          max-width: 1280px;
          margin: 0 auto;
          height: 72px;
          padding: 12px 30px;
          border-radius: 16px;
          background: linear-gradient(90deg, rgba(255,255,255,0.16), rgba(255,255,255,0.10));
          box-shadow:
            0 0 0 2px rgba(255,255,255,0.22) inset,
            0px 10px 30px rgba(0,0,0,0.25);
          backdrop-filter: blur(14px);
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 16px;
        }

        a {
          color: rgba(255,255,255,0.92);
          text-decoration: none;
          font-family: "Satoshi", Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
          font-weight: 800;
          letter-spacing: 0.01em;
          font-size: clamp(18px, 2.2vw, 28px);
          padding: 10px 12px;
          border-radius: 12px;
          transition: background 140ms ease, color 140ms ease;
        }

        a:hover { color: rgba(255,255,255,1); background: rgba(0,0,0,0.10); }
        a[aria-current="page"] { background: rgba(0,0,0,0.14); }
        a:focus-visible { outline: 2px solid rgba(255,255,255,0.65); outline-offset: 3px; }

        @media (max-width: 640px) {
          .topbar { padding-top: 16px; }
          .nav { height: 62px; padding: 10px 14px; }
        }
      </style>

      <header class="topbar" aria-label="Header">
        <nav class="nav" aria-label="Primary">
          <a href="${homeHref}" ${isHome ? 'aria-current="page"' : ''}>${labelHome}</a>
          <a href="${mappingHref}" ${isMapping ? 'aria-current="page"' : ''}>${labelMapping}</a>
        </nav>
      </header>
    `;
  }
}

if (!customElements.get('hxr-header')) {
  customElements.define('hxr-header', HxrHeader);
}

