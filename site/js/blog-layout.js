/**
 * Blog feed: высоту текстового блока всегда ограничиваем высотой соседнего
 * медиа-блока (карусель/видео). Работает и на десктопе (две колонки), и на
 * мобильном (одна колонка — медиа сверху, текст снизу со скроллом).
 * Записи без медиа — без ограничений.
 */
(function () {
  'use strict';

  var observers = new WeakMap();

  function apply(entry) {
    var media = entry.querySelector('.product-block__media');
    var info = entry.querySelector('.product-block__info');
    if (!media || !info) return;

    var noMedia =
      entry.classList.contains('blog-entry--no-media') ||
      !media.children.length ||
      (window.getComputedStyle(media).display === 'none');

    if (noMedia) {
      info.style.maxHeight = '';
      info.style.overflowY = '';
      return;
    }

    var h = media.getBoundingClientRect().height;
    if (!h) return;
    info.style.maxHeight = h + 'px';
    info.style.overflowY = 'auto';
  }

  function watch(entry) {
    if (observers.has(entry)) {
      apply(entry);
      return;
    }
    var media = entry.querySelector('.product-block__media');
    if (!media) return;
    if (typeof ResizeObserver === 'undefined') {
      apply(entry);
      return;
    }
    var ro = new ResizeObserver(function () { apply(entry); });
    ro.observe(media);
    observers.set(entry, ro);
    apply(entry);
  }

  function initAll() {
    document.querySelectorAll('.blog-entry').forEach(watch);
  }

  window.addEventListener('resize', function () {
    document.querySelectorAll('.blog-entry').forEach(apply);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  window.initBlogLayout = initAll;
})();
