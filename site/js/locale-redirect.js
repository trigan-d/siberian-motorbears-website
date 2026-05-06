(function () {
  try {
    if (typeof sessionStorage === 'undefined') return;
    var path = location.pathname || '/';
    if (/^\/en(\/|$)/.test(path)) return;
    if (sessionStorage.getItem('smb_locale_redirect_done')) return;
    if (localStorage.getItem('smb_lang') === 'ru' || localStorage.getItem('smb_lang') === 'en') return;

    var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    var primary = langs[0] || '';
    var prefersRu = /^ru\b/i.test(primary);
    var prefersEn = /^en\b/i.test(primary);
    if (!prefersEn || prefersRu) return;

    var norm = path.replace(/\/index\.html$/i, '/');
    if (norm.length > 1 && norm.slice(-1) === '/') norm = norm.slice(0, -1);
    var target = '/en' + (norm === '/' || norm === '' ? '/' : norm + '/');
    if (target === path || target + 'index.html' === path) return;

    sessionStorage.setItem('smb_locale_redirect_done', '1');
    location.replace(target);
  } catch (e) {}
})();
