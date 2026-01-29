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
      // 11px top padding + ~34px bar height + ~5px breathing room
      document.documentElement.style.setProperty('--hxr-header-safe-top', '50px');
    }

    const shadow = this.attachShadow({ mode: 'open' });

    const isHome = current === 'home';
    const isMapping = current === 'mapping';

    const pos = mode === 'overlay'
      ? 'position: fixed; inset: 0 0 auto 0; z-index: 2000;'
      : 'position: sticky; top: 0; z-index: 100;';

    shadow.innerHTML = `
      <style>
        :host { display: block; ${pos} }
        *, *::before, *::after { box-sizing: border-box; }

        .topbar { padding: 11px 0 0; }
        .nav {
          width: 100%;
          height: 34px;
          padding: 6px 15px;
          border: 1px solid rgba(0,0,0,0.2);
          background: linear-gradient(90deg, rgba(0,0,0,0.16), rgba(0,0,0,0.10));
          box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
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
          font-size: clamp(9px, 1.1vw, 14px);
          padding: 5px 6px;
          border: 1px solid transparent;
          transition: background 140ms ease, color 140ms ease, border-color 140ms ease;
        }

        a:hover { color: rgba(255,255,255,1); background: rgba(0,0,0,0.10); }
        a[aria-current="page"] { background: rgba(0,0,0,0.14); }
        a:focus-visible { outline: 2px solid rgba(255,255,255,0.65); outline-offset: 3px; }

        @media (max-width: 640px) {
          .topbar { padding-top: 8px; }
          .nav { height: 31px; padding: 5px 8px; }
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

