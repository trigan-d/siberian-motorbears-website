(function () {
  function normalizePath(pathname) {
    var p = pathname || '/';
    p = p.replace(/\/index\.html$/i, '/');
    if (p.length > 1 && p.slice(-1) === '/') p = p.slice(0, -1);
    return p || '/';
  }

  function siblingRuFromEn(enPath) {
    if (enPath.indexOf('/en') !== 0) return '/';
    var tail = enPath.slice(3);
    if (!tail || tail === '/') return '/';
    return tail.indexOf('/') === 0 ? tail : '/' + tail;
  }

  /** Каталоговый URL на /en/.../ одним завершающим слэшем, без // */
  function enFromRu(ruPath) {
    if (ruPath === '/') return '/en';
    return '/en' + ruPath;
  }

  /** Каталоги — со слэшем в конце; явные .html (страницы записей блога) — без лишнего слэша */
  function canonicalHref(path) {
    if (path === '/') return '/';
    if (path === '/en') return '/en/';
    if (/\.html$/i.test(path)) return path;
    return path.slice(-1) === '/' ? path : path + '/';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var container = document.querySelector('.site-header .container');
    var logo = document.querySelector('.site-header .logo');
    if (!container || !logo || container.querySelector('.site-header__brand')) return;

    var path = normalizePath(location.pathname);
    var isEn = path === '/en' || path.indexOf('/en/') === 0;
    var ruPath = isEn ? siblingRuFromEn(path) : path;
    var enPath = isEn ? path : enFromRu(ruPath);

    var ruHref = canonicalHref(ruPath);
    var enHref = canonicalHref(enPath);

    var wrap = document.createElement('div');
    wrap.className = 'lang-switch';
    wrap.setAttribute('aria-label', 'Language');

    function markChoice(lang) {
      try {
        localStorage.setItem('smb_lang', lang);
      } catch (e) {}
    }

    var inner = document.createElement('div');
    inner.className = 'lang-switch__inner';

    function link(lang, href, label, flag, isCurrent) {
      var a = document.createElement('a');
      a.href = href;
      a.setAttribute('lang', lang);
      a.hreflang = lang;
      a.className = 'lang-switch__link' + (isCurrent ? ' lang-switch__link--current' : '');
      var f = document.createElement('span');
      f.className = 'lang-switch__flag';
      f.setAttribute('aria-hidden', 'true');
      f.textContent = flag;
      var t = document.createElement('span');
      t.className = 'lang-switch__code';
      t.textContent = label;
      a.appendChild(f);
      a.appendChild(document.createTextNode('\u00a0'));
      a.appendChild(t);
      return a;
    }

    var aRu = link('ru', ruHref, 'RU', '\uD83C\uDDF7\uD83C\uDDFA', !isEn);
    aRu.addEventListener('click', function () {
      markChoice('ru');
    });

    var sep = document.createElement('span');
    sep.className = 'lang-switch__sep';
    sep.setAttribute('aria-hidden', 'true');
    sep.textContent = '\u00a0|\u00a0';

    var aEn = link('en', enHref, 'EN', '\uD83C\uDDEC\uD83C\uDDE7', isEn);
    aEn.addEventListener('click', function () {
      markChoice('en');
    });

    inner.appendChild(aRu);
    inner.appendChild(sep);
    inner.appendChild(aEn);
    wrap.appendChild(inner);

    var brand = document.createElement('div');
    brand.className = 'site-header__brand';
    logo.parentNode.insertBefore(brand, logo);
    brand.appendChild(logo);
    brand.appendChild(wrap);
  });
})();
