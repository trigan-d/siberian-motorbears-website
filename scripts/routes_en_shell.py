"""Замены для оболочки страницы маршрутов (мета, герой, легенда карты, JS ROUTE_INFO)."""

ROUTES_SHELL_PAIRS: list[tuple[str, str]] = [
    (
        "<title>Маршруты на автодоме из Новосибирска — куда поехать: Алтай, Байкал, Сибирь | Siberian motorbears</title>",
        "<title>Motorhome routes from Novosibirsk — Altai, Baikal, Siberia | Siberian motorbears</title>",
    ),
    (
        'content="Маршруты на автодоме из Новосибирска — куда поехать на автодоме: от 3 до 35 дней. Сузун (3 дня), Карачи и Чаны (3), Яровое (3–4), Танай и Шерегеш (5), Алтай — Чемал, Кату-Ярык, Кош-Агач (5–10), Телецкое (5–6), Барнаул и Денисова пещера (5–6), Мульты (7), Парабель и Каргасок (7–8), Красноярск и Ергаки (8–10), Байкал (14), Тобольск — Салехард (10–14), Карелия и Териберка (18–24), Крым (21–28), Владивосток (25–35). Расписание и стоянки."',
        'content="Motorhome routes from Novosibirsk — trip ideas from 3 to 35 days: Suzun (3 d), Karachi & Chany lakes (3), Yarovoye (3–4), Tanay & Sheregesh (5), Altai — Chemal, Katu-Yaryk, Kosh-Agach (5–10), Lake Teletskoye (5–6), Barnaul & Denisova Cave (5–6), Multa (7), Parabel & Kargasok (7–8), Krasnoyarsk & Ergaki (8–10), Baikal (14), Tobolsk — Salekhard (10–14), Karelia & Teriberka (18–24), Crimea (21–28), Vladivostok (25–35). Sample itineraries and stops."',
    ),
    (
        'content="маршруты автодом, куда поехать из Новосибирска, автодом Алтай, кемпер Байкал, стоянки автодом, Siberian motorbears"',
        'content="motorhome routes, trip ideas from Novosibirsk, Altai motorhome, Baikal camper, motorhome stops, Siberian motorbears"',
    ),
    (
        '<meta property="og:title" content="Идеи маршрутов на прокатном автодоме из Новосибирска | Siberian motorbears">',
        '<meta property="og:title" content="Trip ideas with a rental motorhome from Novosibirsk | Siberian motorbears">',
    ),
    (
        '<meta property="og:description" content="Наши медведи исколесили немало дорог и могут подсказать идеи маршрутов на прокатном автодоме из Новосибирска: от 3 до 14 дней. Сузун, Алтай, Байкал, Ергаки — расписание и стоянки.">',
        '<meta property="og:description" content="Our motorbears have covered plenty of roads — here are rental motorhome ideas from Novosibirsk, about 3–14 days at a glance. Suzun, Altai, Baikal, Ergaki — sample schedules and stops.">',
    ),
    (
        '<meta name="twitter:title" content="Идеи маршрутов на прокатном автодоме из Новосибирска | Siberian motorbears">',
        '<meta name="twitter:title" content="Trip ideas with a rental motorhome from Novosibirsk | Siberian motorbears">',
    ),
    (
        '<meta name="twitter:description" content="Наши медведи исколесили немало дорог и могут подсказать идеи маршрутов на прокатном автодоме из Новосибирска: от 3 до 14 дней. Сузун, Алтай, Байкал, Ергаки — расписание и стоянки.">',
        '<meta name="twitter:description" content="Our motorbears have covered plenty of roads — rental motorhome ideas from Novosibirsk, about 3–14 days. Suzun, Altai, Baikal, Ergaki — schedules and stops.">',
    ),
    (
        '<div class="hero__img"><img src="../../assets/img/routes-hero.png" alt="Прокатный автодом из Новосибирска в пути — маршруты по Сибири, Алтаю и горам" width="800" height="533"></div>',
        '<div class="hero__img"><img src="../../assets/img/routes-hero.png" alt="Rental motorhome from Novosibirsk on the road — Siberia, Altai, and mountains" width="800" height="533"></div>',
    ),
    (
        '<h1 style="font-size: 1.35rem;">Маршруты на автодоме из Новосибирска</h1>',
        '<h1 style="font-size: 1.35rem;">Motorhome routes from Novosibirsk</h1>',
    ),
    (
        '<p class="text-muted">Наши моторизированные медведи исколесили немало сибирских (и не только) дорог. Они повидали всякого и могут кое-что подсказать и коренному сибиряку, и гостю издалека: куда податься на пару дней, а куда — на две недели.</p>',
        '<p class="text-muted">Our motorbears have roamed plenty of Siberian (and not only Siberian) roads. They have seen a lot and can suggest something useful whether you live here or arrive from far away — where to go for a weekend and where for two weeks.</p>',
    ),
    (
        '<p class="text-muted">Ниже мы собрали несколько идей о том, куда можно поехать на арендованном автодоме из Новосибирска: от коротких вылазок до больших экспедиций. Расписание и стоянки ориентировочные — подстраивайте этапы под себя и уточняйте маршрут перед выездом.</p>',
        '<p class="text-muted">Below are ideas for trips from Novosibirsk in a rental motorhome — from short breaks to long expeditions. Schedules and stops are indicative: adapt stages to your pace and double-check roads before you leave.</p>',
    ),
    (
        '<section class="section overview-routes-section" id="overview-routes" aria-label="Общая карта маршрутов">',
        '<section class="section overview-routes-section" id="overview-routes" aria-label="Overview map of routes">',
    ),
    (
        '<nav class="overview-routes-legend-wrap" aria-label="Оглавление маршрутов">',
        '<nav class="overview-routes-legend-wrap" aria-label="Route list">',
    ),
    (
        '<div class="container"><a href="../">Home</a> → <a href="../rent/">Rental</a> → <span>Маршруты</span></div>',
        '<div class="container"><a href="../">Home</a> → <a href="../rent/">Rental</a> → <span>Trip ideas</span></div>',
    ),
    (
        """            <ul class="overview-routes-legend" id="overview-routes-legend">
              <li><a href="#route-3-suzun" data-route="suzun"><span class="legend-swatch" style="background:#2e7d32"></span><span class="legend-name">Сузун, Бердские скалы</span><span class="legend-days">3 дня</span></a></li>
              <li><a href="#route-3-lakes" data-route="lakes"><span class="legend-swatch" style="background:#1565c0"></span><span class="legend-name">Озёра Карачи, Чаны</span><span class="legend-days">3 дня</span></a></li>
              <li><a href="#route-4-yarovoye" data-route="yarovoye"><span class="legend-swatch" style="background:#c62828"></span><span class="legend-name">Яровое, Гальбштадт</span><span class="legend-days">3–4 дня</span></a></li>
              <li><a href="#route-5-tanay" data-route="tanay"><span class="legend-swatch" style="background:#6a1b9a"></span><span class="legend-name">Танай, Шерегеш</span><span class="legend-days">5 дней</span></a></li>
              <li><a href="#route-5-altai" data-route="altai5"><span class="legend-swatch" style="background:#00838f"></span><span class="legend-name">Алтай (Чемал)</span><span class="legend-days">5 дней</span></a></li>
              <li><a href="#route-7-altai" data-route="altai7"><span class="legend-swatch" style="background:#ef6c00"></span><span class="legend-name">Алтай (Кату-Ярык)</span><span class="legend-days">7 дней</span></a></li>
              <li><a href="#route-10-altai-loop" data-route="altai10"><span class="legend-swatch" style="background:#558b2f"></span><span class="legend-name">Алтай (Кош-Агач)</span><span class="legend-days">10 дней</span></a></li>
              <li><a href="#route-6-barnaul-loop" data-route="barnaul_loop"><span class="legend-swatch" style="background:#7b1fa2"></span><span class="legend-name">Барнаул, Денисова пещера</span><span class="legend-days">5–6 дней</span></a></li>
              <li><a href="#route-6-teletskoye" data-route="teletskoye"><span class="legend-swatch" style="background:#0277bd"></span><span class="legend-name">Телецкое озеро</span><span class="legend-days">5–6 дней</span></a></li>
              <li><a href="#route-7-multa" data-route="multa"><span class="legend-swatch" style="background:#bf360c"></span><span class="legend-name">Мульты, Тюнгур</span><span class="legend-days">7 дней</span></a></li>
              <li><a href="#route-8-parabel" data-route="parabel_kargasok"><span class="legend-swatch" style="background:#00695c"></span><span class="legend-name">Парабель, Каргасок</span><span class="legend-days">7–8 дней</span></a></li>
              <li><a href="#route-10-krasnoyarsk-ergaki" data-route="krasnoyarsk_ergaki"><span class="legend-swatch" style="background:#283593"></span><span class="legend-name">Красноярск, Ергаки</span><span class="legend-days">8–10 дней</span></a></li>
              <li><a href="#route-10-tobolsk-salekhard" data-route="tobolsk_salekhard"><span class="legend-swatch" style="background:#37474f"></span><span class="legend-name">Тобольск — Салехард</span><span class="legend-days">10–14 дней</span></a></li>
              <li><a href="#route-14-baikal" data-route="baikal"><span class="legend-swatch" style="background:#4e342e"></span><span class="legend-name">Байкал</span><span class="legend-days">14 дней</span></a></li>
              <li><a href="#route-18-karelia-teriberka" data-route="karelia_teriberka"><span class="legend-swatch" style="background:#795548"></span><span class="legend-name">Карелия, Териберка</span><span class="legend-days">18–24 дня</span></a></li>
              <li><a href="#route-21-crimea" data-route="crimea"><span class="legend-swatch" style="background:#455a64"></span><span class="legend-name">Крым</span><span class="legend-days">21–28 дней</span></a></li>
              <li><a href="#route-25-vladivostok" data-route="vladivostok"><span class="legend-swatch" style="background:#e65100"></span><span class="legend-name">Владивосток</span><span class="legend-days">25–35 дней</span></a></li>
              <li><a href="#route-10-ski-ring" data-route="ski_ring"><span class="legend-swatch" style="background:#006064"></span><span class="legend-name">Горнолыжное кольцо Сибири</span><span class="legend-days">8 дней</span></a></li>
            </ul>""",
        """            <ul class="overview-routes-legend" id="overview-routes-legend">
              <li><a href="#route-3-suzun" data-route="suzun"><span class="legend-swatch" style="background:#2e7d32"></span><span class="legend-name">Suzun, Berd Rocks</span><span class="legend-days">3 days</span></a></li>
              <li><a href="#route-3-lakes" data-route="lakes"><span class="legend-swatch" style="background:#1565c0"></span><span class="legend-name">Karachi & Chany lakes</span><span class="legend-days">3 days</span></a></li>
              <li><a href="#route-4-yarovoye" data-route="yarovoye"><span class="legend-swatch" style="background:#c62828"></span><span class="legend-name">Yarovoye, Halbstadt</span><span class="legend-days">3–4 days</span></a></li>
              <li><a href="#route-5-tanay" data-route="tanay"><span class="legend-swatch" style="background:#6a1b9a"></span><span class="legend-name">Tanay, Sheregesh</span><span class="legend-days">5 days</span></a></li>
              <li><a href="#route-5-altai" data-route="altai5"><span class="legend-swatch" style="background:#00838f"></span><span class="legend-name">Altai (Chemal)</span><span class="legend-days">5 days</span></a></li>
              <li><a href="#route-7-altai" data-route="altai7"><span class="legend-swatch" style="background:#ef6c00"></span><span class="legend-name">Altai (Katu-Yaryk)</span><span class="legend-days">7 days</span></a></li>
              <li><a href="#route-10-altai-loop" data-route="altai10"><span class="legend-swatch" style="background:#558b2f"></span><span class="legend-name">Altai (Kosh-Agach)</span><span class="legend-days">10 days</span></a></li>
              <li><a href="#route-6-barnaul-loop" data-route="barnaul_loop"><span class="legend-swatch" style="background:#7b1fa2"></span><span class="legend-name">Barnaul, Denisova Cave</span><span class="legend-days">5–6 days</span></a></li>
              <li><a href="#route-6-teletskoye" data-route="teletskoye"><span class="legend-swatch" style="background:#0277bd"></span><span class="legend-name">Lake Teletskoye</span><span class="legend-days">5–6 days</span></a></li>
              <li><a href="#route-7-multa" data-route="multa"><span class="legend-swatch" style="background:#bf360c"></span><span class="legend-name">Multa, Tyungur</span><span class="legend-days">7 days</span></a></li>
              <li><a href="#route-8-parabel" data-route="parabel_kargasok"><span class="legend-swatch" style="background:#00695c"></span><span class="legend-name">Parabel, Kargasok</span><span class="legend-days">7–8 days</span></a></li>
              <li><a href="#route-10-krasnoyarsk-ergaki" data-route="krasnoyarsk_ergaki"><span class="legend-swatch" style="background:#283593"></span><span class="legend-name">Krasnoyarsk, Ergaki</span><span class="legend-days">8–10 days</span></a></li>
              <li><a href="#route-10-tobolsk-salekhard" data-route="tobolsk_salekhard"><span class="legend-swatch" style="background:#37474f"></span><span class="legend-name">Tobolsk — Salekhard</span><span class="legend-days">10–14 days</span></a></li>
              <li><a href="#route-14-baikal" data-route="baikal"><span class="legend-swatch" style="background:#4e342e"></span><span class="legend-name">Baikal</span><span class="legend-days">14 days</span></a></li>
              <li><a href="#route-18-karelia-teriberka" data-route="karelia_teriberka"><span class="legend-swatch" style="background:#795548"></span><span class="legend-name">Karelia, Teriberka</span><span class="legend-days">18–24 days</span></a></li>
              <li><a href="#route-21-crimea" data-route="crimea"><span class="legend-swatch" style="background:#455a64"></span><span class="legend-name">Crimea</span><span class="legend-days">21–28 days</span></a></li>
              <li><a href="#route-25-vladivostok" data-route="vladivostok"><span class="legend-swatch" style="background:#e65100"></span><span class="legend-name">Vladivostok</span><span class="legend-days">25–35 days</span></a></li>
              <li><a href="#route-10-ski-ring" data-route="ski_ring"><span class="legend-swatch" style="background:#006064"></span><span class="legend-name">Siberia ski circuit</span><span class="legend-days">8 days</span></a></li>
            </ul>""",
    ),
    (
        '<a href="#overview-routes" id="back-to-routes-list" class="back-to-routes-list" title="К списку маршрутов" aria-label="К списку маршрутов">↑</a>',
        '<a href="#overview-routes" id="back-to-routes-list" class="back-to-routes-list" title="Back to route list" aria-label="Back to route list">↑</a>',
    ),
    (
        """        <p class="text-muted" style="margin-top: 2rem;">
          Хотите обсудить маршрут или <a href="../rent/" class="link--inline">взять автодом в аренду</a>? Напишите нам: <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a>, <a href="tel:+79134602050" class="link--contact">+7 (913) 460-20-50</a>, <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a>.
        </p>""",
        """        <p class="text-muted" style="margin-top: 2rem;">
          Want to discuss a route or <a href="../rent/" class="link--inline">rent a motorhome</a>? Write to us: <a href="mailto:siberian.motorbears@gmail.com" class="link--contact">siberian.motorbears@gmail.com</a>, <a href="tel:+79134602050" class="link--contact">+7 (913) 460-20-50</a>, <a href="https://t.me/trigansda" target="_blank" rel="noopener" class="link--contact">t.me/trigansda</a>.
        </p>""",
    ),
    (
        """      var ROUTE_INFO = {
        suzun: { name: 'Сузун, Бердские скалы', days: '3 дня', sectionId: 'route-3-suzun' },
        lakes: { name: 'Озёра Карачи, Чаны', days: '3 дня', sectionId: 'route-3-lakes' },
        yarovoye: { name: 'Яровое, Гальбштадт', days: '3–4 дня', sectionId: 'route-4-yarovoye' },
        tanay: { name: 'Танай, Шерегеш', days: '5 дней', sectionId: 'route-5-tanay' },
        altai5: { name: 'Алтай (Чемал)', days: '5 дней', sectionId: 'route-5-altai' },
        altai7: { name: 'Алтай (Кату-Ярык)', days: '7 дней', sectionId: 'route-7-altai' },
        altai10: { name: 'Алтай (Кош-Агач)', days: '10 дней', sectionId: 'route-10-altai-loop' },
        barnaul_loop: { name: 'Барнаул, Денисова пещера', days: '5–6 дней', sectionId: 'route-6-barnaul-loop' },
        teletskoye: { name: 'Телецкое озеро', days: '5–6 дней', sectionId: 'route-6-teletskoye' },
        multa: { name: 'Мульты, Тюнгур', days: '7 дней', sectionId: 'route-7-multa' },
        parabel_kargasok: { name: 'Парабель, Каргасок', days: '7–8 дней', sectionId: 'route-8-parabel' },
        krasnoyarsk_ergaki: { name: 'Красноярск, Ергаки', days: '8–10 дней', sectionId: 'route-10-krasnoyarsk-ergaki' },
        tobolsk_salekhard: { name: 'Тобольск — Салехард', days: '10–14 дней', sectionId: 'route-10-tobolsk-salekhard' },
        baikal: { name: 'Байкал', days: '14 дней', sectionId: 'route-14-baikal' },
        karelia_teriberka: { name: 'Карелия, Териберка', days: '18–24 дня', sectionId: 'route-18-karelia-teriberka' },
        crimea: { name: 'Крым', days: '21–28 дней', sectionId: 'route-21-crimea' },
        vladivostok: { name: 'Владивосток', days: '25–35 дней', sectionId: 'route-25-vladivostok' },
        ski_ring: { name: 'Горнолыжное кольцо Сибири', days: '8 дней', sectionId: 'route-10-ski-ring' }
      };""",
        """      var ROUTE_INFO = {
        suzun: { name: 'Suzun, Berd Rocks', days: '3 days', sectionId: 'route-3-suzun' },
        lakes: { name: 'Karachi & Chany lakes', days: '3 days', sectionId: 'route-3-lakes' },
        yarovoye: { name: 'Yarovoye, Halbstadt', days: '3–4 days', sectionId: 'route-4-yarovoye' },
        tanay: { name: 'Tanay, Sheregesh', days: '5 days', sectionId: 'route-5-tanay' },
        altai5: { name: 'Altai (Chemal)', days: '5 days', sectionId: 'route-5-altai' },
        altai7: { name: 'Altai (Katu-Yaryk)', days: '7 days', sectionId: 'route-7-altai' },
        altai10: { name: 'Altai (Kosh-Agach)', days: '10 days', sectionId: 'route-10-altai-loop' },
        barnaul_loop: { name: 'Barnaul, Denisova Cave', days: '5–6 days', sectionId: 'route-6-barnaul-loop' },
        teletskoye: { name: 'Lake Teletskoye', days: '5–6 days', sectionId: 'route-6-teletskoye' },
        multa: { name: 'Multa, Tyungur', days: '7 days', sectionId: 'route-7-multa' },
        parabel_kargasok: { name: 'Parabel, Kargasok', days: '7–8 days', sectionId: 'route-8-parabel' },
        krasnoyarsk_ergaki: { name: 'Krasnoyarsk, Ergaki', days: '8–10 days', sectionId: 'route-10-krasnoyarsk-ergaki' },
        tobolsk_salekhard: { name: 'Tobolsk — Salekhard', days: '10–14 days', sectionId: 'route-10-tobolsk-salekhard' },
        baikal: { name: 'Baikal', days: '14 days', sectionId: 'route-14-baikal' },
        karelia_teriberka: { name: 'Karelia, Teriberka', days: '18–24 days', sectionId: 'route-18-karelia-teriberka' },
        crimea: { name: 'Crimea', days: '21–28 days', sectionId: 'route-21-crimea' },
        vladivostok: { name: 'Vladivostok', days: '25–35 days', sectionId: 'route-25-vladivostok' },
        ski_ring: { name: 'Siberia ski circuit', days: '8 days', sectionId: 'route-10-ski-ring' }
      };""",
    ),
    (
        "      // Порядок маршрутов: по длительности (короткие → длинные). ski_ring всегда последний, не участвует в сортировке (см. README-ROUTES.md).",
        "      // Route order: by duration (short → long). ski_ring is always last (see README-ROUTES.md).",
    ),
    # Section markers (<!-- ... -->) copied from site/routes/index.html
    (
        "        <!-- ========== 3 дня: Караканский бор — Бердские скалы — Салаирский кряж ========== -->",
        "        <!-- ========== 3 days: Karakan forest — Berd Rocks — Salair ridge ========== -->",
    ),
    (
        "        <!-- ========== 3 дня: Озёра ========== -->",
        "        <!-- ========== 3 days: Lakes ========== -->",
    ),
    (
        "        <!-- ========== 3–4 дня: Большое Яровое озеро ========== -->",
        "        <!-- ========== 3–4 days: Lake Yarovoye ========== -->",
    ),
    (
        "        <!-- ========== 5 дней: Танай, Томская писаница, Шерегеш ========== -->",
        "        <!-- ========== 5 days: Tanay, Tomskaya Pisanitsa, Sheregesh ========== -->",
    ),
    (
        "        <!-- ========== 5 дней: Алтай начало ========== -->",
        "        <!-- ========== 5 days: Altai — introduction ========== -->",
    ),
    (
        "        <!-- ========== 5–6 дней: Кольцо Барнаул — Алейск — Солонешное — Белокуриха — Бийск ========== -->",
        "        <!-- ========== 5–6 days: Barnaul — Aleysk — Soloneshnoye — Belokurikha — Biysk loop ========== -->",
    ),
    (
        "        <!-- ========== 5–6 дней: Телецкое озеро кольцом через Турочак ========== -->",
        "        <!-- ========== 5–6 days: Lake Teletskoye loop via Turochak ========== -->",
    ),
    (
        "        <!-- ========== 7 дней: Алтай глубже ========== -->",
        "        <!-- ========== 7 days: Altai — deeper ========== -->",
    ),
    (
        "        <!-- ========== 7 дней: Мульта и Мультинские озёра ========== -->",
        "        <!-- ========== 7 days: Multa and Multinskoye lakes ========== -->",
    ),
    (
        "        <!-- ========== 7–8 дней: Парабель, Каргасок ========== -->",
        "        <!-- ========== 7–8 days: Parabel, Kargasok ========== -->",
    ),
    (
        "        <!-- ========== 8–10 дней: Красноярск, Абакан, Ергаки ========== -->",
        "        <!-- ========== 8–10 days: Krasnoyarsk, Abakan, Ergaki ========== -->",
    ),
    (
        "        <!-- ========== 10 дней: Алтай до Кош-Агача + Барнаул ========== -->",
        "        <!-- ========== 10 days: Altai to Kosh-Agach + Barnaul ========== -->",
    ),
    (
        "        <!-- ========== 10–14 дней: Тобольск — Ханты-Мансийск — Сургут — Салехард ========== -->",
        "        <!-- ========== 10–14 days: Tobolsk — Khanty-Mansiysk — Surgut — Salekhard ========== -->",
    ),
    (
        "        <!-- ========== 14 дней: Байкал ========== -->",
        "        <!-- ========== 14 days: Baikal ========== -->",
    ),
    (
        "        <!-- ========== 18–24 дня: Карелия и Териберка ========== -->",
        "        <!-- ========== 18–24 days: Karelia and Teriberka ========== -->",
    ),
    (
        "        <!-- ========== 21–28 дней: Новосибирск — Крым и обратно ========== -->",
        "        <!-- ========== 21–28 days: Novosibirsk — Crimea and back ========== -->",
    ),
    (
        "        <!-- ========== 25–35 дней: Новосибирск — Владивосток и Находка — обратно ========== -->",
        "        <!-- ========== 25–35 days: Novosibirsk — Vladivostok and Nakhodka — return ========== -->",
    ),
    (
        "        <!-- ========== 8 дней: Горнолыжное кольцо Сибири (зимний маршрут) ========== -->",
        "        <!-- ========== 8 days: Siberia ski circuit (winter route) ========== -->",
    ),
]
