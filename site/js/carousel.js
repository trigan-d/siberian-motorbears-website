/**
 * Carousel: Swiper, fullscreen on click
 */
(function () {
  'use strict';

  function initCarousels() {
    var carousels = document.querySelectorAll('.carousel');
    if (!carousels.length) return;

    if (typeof Swiper === 'undefined') {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css';
      document.head.appendChild(link);
      var script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js';
      script.onload = function () { runSwipers(); };
      document.head.appendChild(script);
    } else {
      runSwipers();
    }
  }

  function runSwipers() {
    var carousels = document.querySelectorAll('.carousel');
    carousels.forEach(function (carousel) {
      var track = carousel.querySelector('.carousel-slides');
      if (!track || track.classList.contains('swiper-initialized')) return;
      track.classList.add('swiper-wrapper');
      [].forEach.call(track.children, function (el) { el.classList.add('swiper-slide'); });
      var swiperEl = document.createElement('div');
      swiperEl.className = 'swiper';
      carousel.insertBefore(swiperEl, track);
      swiperEl.appendChild(track);
      var prev = document.createElement('div');
      prev.className = 'swiper-button-prev';
      var next = document.createElement('div');
      next.className = 'swiper-button-next';
      var pag = document.createElement('div');
      pag.className = 'swiper-pagination';
      swiperEl.appendChild(prev);
      swiperEl.appendChild(next);
      swiperEl.appendChild(pag);

      var swiper = new Swiper(swiperEl, {
        loop: true,
        pagination: { el: pag, clickable: true },
        navigation: { nextEl: next, prevEl: prev },
        keyboard: true,
        grabCursor: true
      });

      track.classList.add('swiper-initialized');
      var slides = track.querySelectorAll('.swiper-slide');
      var srcs = [].map.call(slides, function (s) {
        var img = s.querySelector('img');
        return img ? (img.src || img.getAttribute('data-src')) : null;
      }).filter(Boolean);
      carousel._gallerySrcs = srcs;
      carousel._swiper = swiper;
      [].forEach.call(slides, function (slide, idx) {
        slide.addEventListener('click', function (e) {
          e.preventDefault();
          openFullscreen(carousel, idx);
        });
      });
    });
  }

  function openFullscreen(carousel, startIndex) {
    var srcs = carousel._gallerySrcs;
    if (!srcs || !srcs.length) return;

    var wrap = document.getElementById('fullscreen-gallery');
    if (!wrap) {
      wrap = document.createElement('div');
      wrap.id = 'fullscreen-gallery';
      wrap.className = 'fullscreen-gallery';
      wrap.innerHTML = '<button type="button" class="fullscreen-gallery__close" aria-label="Закрыть">&times;</button>' +
        '<button type="button" class="fullscreen-gallery__prev" aria-label="Назад">&lsaquo;</button>' +
        '<div class="fullscreen-gallery__inner"><img src="" alt=""></div>' +
        '<button type="button" class="fullscreen-gallery__next" aria-label="Вперёд">&rsaquo;</button>' +
        '<span class="fullscreen-gallery__counter"></span>';
      document.body.appendChild(wrap);

      wrap.querySelector('.fullscreen-gallery__close').addEventListener('click', closeFullscreen);
      wrap.querySelector('.fullscreen-gallery__prev').addEventListener('click', function () { moveFullscreen(-1); });
      wrap.querySelector('.fullscreen-gallery__next').addEventListener('click', function () { moveFullscreen(1); });
      wrap.addEventListener('click', function (e) { if (e.target === wrap) closeFullscreen(); });
      document.addEventListener('keydown', fullscreenKeydown);
      fullscreenSwipe(wrap);
    }

    wrap._srcs = srcs;
    wrap._index = startIndex % srcs.length;
    wrap.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    showFullscreenImage(wrap);
  }

  function showFullscreenImage(wrap) {
    var srcs = wrap._srcs;
    var idx = wrap._index;
    var img = wrap.querySelector('.fullscreen-gallery__inner img');
    var counter = wrap.querySelector('.fullscreen-gallery__counter');
    img.src = srcs[idx];
    counter.textContent = (idx + 1) + ' / ' + srcs.length;
  }

  function moveFullscreen(delta) {
    var wrap = document.getElementById('fullscreen-gallery');
    if (!wrap || !wrap.classList.contains('is-open')) return;
    var srcs = wrap._srcs;
    wrap._index = (wrap._index + delta + srcs.length) % srcs.length;
    showFullscreenImage(wrap);
  }

  function closeFullscreen() {
    var wrap = document.getElementById('fullscreen-gallery');
    if (wrap) {
      wrap.classList.remove('is-open');
      document.body.style.overflow = '';
    }
  }

  function fullscreenKeydown(e) {
    var wrap = document.getElementById('fullscreen-gallery');
    if (!wrap || !wrap.classList.contains('is-open')) return;
    if (e.key === 'Escape') closeFullscreen();
    if (e.key === 'ArrowLeft') moveFullscreen(-1);
    if (e.key === 'ArrowRight') moveFullscreen(1);
  }

  function fullscreenSwipe(wrap) {
    var startX = 0;
    var minSwipe = 50;
    wrap.addEventListener('touchstart', function (e) {
      if (e.touches.length === 1) startX = e.touches[0].clientX;
    }, { passive: true });
    wrap.addEventListener('touchend', function (e) {
      if (e.changedTouches.length !== 1) return;
      var delta = e.changedTouches[0].clientX - startX;
      if (delta > minSwipe) moveFullscreen(-1);
      else if (delta < -minSwipe) moveFullscreen(1);
    }, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCarousels);
  } else {
    initCarousels();
  }

  window.initCarousels = initCarousels;
})();
