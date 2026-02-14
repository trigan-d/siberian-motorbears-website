/**
 * Карты маршрутов (Leaflet + OpenStreetMap).
 * Маршруты прокладываются по дорогам через OSRM (Open Source Routing Machine).
 */
(function () {
  'use strict';

  var OSRM_BASE = 'https://router.project-osrm.org/route/v1/driving';

  var ROUTES = {
    suzun: {
      center: [54.35, 82.4],
      zoom: 8,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [54.6355, 82.83],             // Бурмистрово (Караканский бор)
        [54.2286, 81.7094],           // Абрашинский карьер
        [53.786, 82.314],             // Сузун
        [54.344, 84.211],             // Маслянино (проезд Сузун → Зверобой)
        [54.6445, 83.9268],           // Гора Зверобой (Бердские скалы)
        [54.646, 83.819],             // Легостаево (обратно в Нск)
        [54.768, 83.853],             // Мосты
        [54.959, 83.991],             // Владимировка (Тогучинский р-н)
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [54.6355, 82.83], title: 'Караканский бор — Бурмистрово, сосновый лес у водохранилища, ООПТ', type: 'sight' },
        { coords: [54.2286, 81.7094], title: 'Абрашинский карьер — мраморное озеро, стоянка, дайвинг', type: 'stop' },
        { coords: [54.2286, 81.7094], title: 'Абрашинский карьер — бывший мраморный карьер, прозрачная вода', type: 'sight' },
        { coords: [53.786, 82.314], title: 'Сузун — музей «Монетный двор», стоянка, турбазы', type: 'stop' },
        { coords: [53.786, 82.314], title: 'Сузун — история медеплавильного завода, сибирская монета', type: 'sight' },
        { coords: [54.344, 84.211], title: 'Маслянинский район — Маслянино, долина Берди', type: 'stop' },
        { coords: [54.6445, 83.9268], title: 'Бердские скалы — гора Зверобой, памятник природы, смотровые', type: 'sight' },
        { coords: [54.646, 83.819], title: 'Салаирский кряж — Легостаево, отроги, заказник', type: 'sight' },
        { coords: [54.768, 83.853], title: 'Мосты — транзит в Нск (Искитимский р-н)', type: 'stop' },
        { coords: [54.959, 83.991], title: 'Владимировка — транзит в Нск (Тогучинский р-н)', type: 'stop' }
      ]
    },
    lakes: {
      center: [54.8, 79.5],
      zoom: 7,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [55.0455, 80.3541],           // Каргат (трасса Р-254)
        [55.28, 76.82],               // Озеро Чаны — база «Бухта Лазурная»
        [55.336, 76.943],             // Озеро Карачи
        [54.227, 77.978],             // Озеро Горькое (у с. Новоключи)
        [53.7333, 78.0333],           // Карасук
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [55.0455, 80.3541], title: 'Каргат — транзит по Р-254 «Иртыш», заправки', type: 'stop' },
        { coords: [55.28, 76.82], title: 'Озеро Чаны — база «Бухта Лазурная», стоянка у воды', type: 'stop' },
        { coords: [55.28, 76.82], title: 'Озеро Чаны (крупнейшее в Западной Сибири) — птицы, закаты, пляж', type: 'sight' },
        { coords: [55.336, 76.943], title: 'Озеро Карачи — санаторий, окрестности', type: 'stop' },
        { coords: [55.336, 76.943], title: 'Озеро Карачи (лечебные грязи, рапа)', type: 'sight' },
        { coords: [54.227, 77.978], title: 'Озеро Горькое — у с. Новоключи, зоны отдыха (Купинский/Баганский р-н)', type: 'stop' },
        { coords: [54.227, 77.978], title: 'Озеро Горькое (лечебные грязи, рапа, «сибирское Мёртвое море»)', type: 'sight' },
        { coords: [53.7333, 78.0333], title: 'Карасук — город на юго-западе НСО, трасса Р-380, заправки', type: 'stop' }
      ]
    },
    yarovoye: {
      center: [53.7, 80.2],
      zoom: 6,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [54.3588, 81.8859],           // Ордынское
        [53.9828, 79.2375],           // Краснозёрское (трасса Р-380)
        [53.7333, 78.0333],           // Карасук
        [53.2167, 78.9833],           // Гальбштадт (Немецкий национальный район)
        [52.9978, 78.6447],           // Славгород
        [52.9253, 78.5869],           // Яровое
        [52.9978, 78.6447],           // Славгород (обратно)
        [53.2167, 78.9833],           // Гальбштадт
        [53.7333, 78.0333],           // Карасук
        [53.9828, 79.2375],           // Краснозёрское
        [54.3588, 81.8859],           // Ордынское
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [54.3588, 81.8859], title: 'Ордынское — берег Обского водохранилища, транзит по Р-380', type: 'stop' },
        { coords: [53.9828, 79.2375], title: 'Краснозёрское — транзит по трассе на Карасук', type: 'stop' },
        { coords: [53.7333, 78.0333], title: 'Карасук — город на юго-западе НСО, заправки, магазины', type: 'stop' },
        { coords: [53.2167, 78.9833], title: 'Гальбштадт — Немецкий национальный район, музей, центр немецкой культуры', type: 'stop' },
        { coords: [53.2167, 78.9833], title: 'Гальбштадт — немецкая планировка, история меннонитов, пивоварни в сёлах района', type: 'sight' },
        { coords: [52.9978, 78.6447], title: 'Славгород — город в Кулундинской степи, рядом с Яровым', type: 'stop' },
        { coords: [52.9253, 78.5869], title: 'Яровое — кемпинги, базы у озера, парковки', type: 'stop' },
        { coords: [52.9253, 78.5869], title: 'Большое Яровое озеро — солёная вода, лечебные грязи, купание', type: 'sight' },
        { coords: [52.9253, 78.5869], title: 'Аквапарк «Лава», пляжи «Причал 22» и «Причал 42», дельфинарий', type: 'sight' }
      ]
    },
    altai5: {
      center: [51.8, 84.5],
      zoom: 7,
      track: [
        [55.0084, 82.9357], [52.51, 85.15], [52.00, 85.92], [51.98, 85.87],
        [51.41, 86.00], [51.123, 86.165], [51.82, 85.77], [52.51, 85.15], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [52.00, 85.92], title: 'Сростки — музей Шукшина', type: 'sight' },
        { coords: [51.98, 85.87], title: 'Майма / Горно-Алтайск — стоянки, кемпинги', type: 'stop' },
        { coords: [51.41, 86.00], title: 'Чемал — кемпинги «Млечный путь», «Долина Катуни»', type: 'stop' },
        { coords: [51.41, 86.00], title: 'Чемальская ГЭС, остров Патмос, Козья тропа', type: 'sight' },
        { coords: [51.123, 86.165], title: 'Ороктойский мост — висячий мост через Катунь (77 км Чемальского тракта)', type: 'sight' },
        { coords: [51.82, 85.77], title: 'Манжерок — туркомплекс, кемпинг у озера', type: 'stop' },
        { coords: [51.82, 85.77], title: 'Манжерокское озеро, канатная дорога на Синюху', type: 'sight' }
      ]
    },
    altai7: {
      center: [51.2, 85.2],
      zoom: 6,
      track: [
        [55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00],
        [50.75, 86.13], [50.30, 87.60], [50.63, 87.95], [50.91, 88.22],  // Акташ → Улаган → Кату-Ярык (до перевала на автодоме)
        [50.30, 87.60], [50.75, 86.13], [51.98, 85.87], [52.51, 85.15], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [51.98, 85.87], title: 'Майма — стоянка', type: 'stop' },
        { coords: [51.41, 86.00], title: 'Чемал — стоянка', type: 'stop' },
        { coords: [50.75, 86.13], title: 'Онгудай — кемпинги вдоль тракта', type: 'stop' },
        { coords: [50.30, 87.60], title: 'Акташ / Курай — стоянки у трассы', type: 'stop' },
        { coords: [50.63, 87.95], title: 'Улаган — по Улаганскому тракту, стоянка', type: 'stop' },
        { coords: [50.91, 88.22], title: 'Перевал Кату-Ярык — смотровая (на автодоме можно); спуск и Чулышман — на джипе', type: 'sight' },
        { coords: [50.30, 87.60], title: 'Курайская степь, Гейзерное озеро', type: 'sight' },
        { coords: [50.645, 86.312], title: 'Перевал Чике-Таман (659 км Чуйского тракта, 1295 м)', type: 'sight' },
        { coords: [51.045, 85.604], title: 'Перевал Семинский (583 км Чуйского тракта, 1717 м)', type: 'sight' },
        { coords: [50.47, 86.98], title: 'Петроглифы Калбак-Таш', type: 'sight' }
      ]
    },
    altai10: {
      center: [52.5, 84.0],
      zoom: 6,
      track: [
        [55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00],
        [50.75, 86.13], [50.30, 87.60], [50.0, 88.66],             // Акташ → Кош-Агач (Чуйский тракт)
        [51.41, 86.00], [52.51, 85.15], [53.36, 83.75], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [51.41, 86.00], title: 'Чемал — стоянка', type: 'stop' },
        { coords: [51.82, 85.77], title: 'Манжерок — стоянка', type: 'stop' },
        { coords: [50.75, 86.13], title: 'Онгудай — стоянка', type: 'stop' },
        { coords: [50.30, 87.60], title: 'Акташ / Курай — стоянка', type: 'stop' },
        { coords: [50.0, 88.66], title: 'Кош-Агач — край Чуйского тракта, стоянка', type: 'stop' },
        { coords: [50.0, 88.66], title: 'Кош-Агач — Кош-Агачский район, стык границ, степь', type: 'sight' },
        { coords: [53.36, 83.75], title: 'Барнаул — ночёвка, музей, набережная Оби', type: 'stop' },
        { coords: [53.36, 83.75], title: 'Барнаул — исторический центр, Демидовская площадь', type: 'sight' }
      ]
    },
    multa: {
      center: [52.2, 85.2],
      zoom: 6,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [52.51, 85.15],              // Бийск
        [51.96, 85.92],              // Горно-Алтайск / Майма
        [50.98, 84.99],              // Усть-Кан
        [50.27, 85.615],             // Усть-Кокса (слияние Коксы и Катуни)
        [50.17, 85.95],              // Мульта
        [50.15, 86.3],               // Тюнгур (~65 км от Усть-Коксы вверх по Катуни)
        [50.27, 85.615],             // Усть-Кокса (обратно)
        [50.98, 84.99],              // Усть-Кан
        [51.96, 85.92],              // Горно-Алтайск
        [52.51, 85.15],              // Бийск
        [55.0084, 82.9357]           // Новосибирск
      ],
      waypoints: [
        { coords: [50.98, 84.99], title: 'Усть-Кан — стоянка, ночёвка в пути', type: 'stop' },
        { coords: [50.98, 84.99], title: 'Усть-Канская пещера (Белый Камень), Канская степь', type: 'sight' },
        { coords: [50.27, 85.615], title: 'Усть-Кокса — стоянки, турбазы, центр района', type: 'stop' },
        { coords: [50.27, 85.615], title: 'Усть-Кокса: слияние Коксы и Катуни, музеи Рериха и старообрядцев, перевал Громотуха', type: 'sight' },
        { coords: [50.17, 85.95], title: 'Мульта — стоянки, базы, старт тропы к озёрам', type: 'stop' },
        { coords: [49.98, 85.83], title: 'Мультинские озёра — Нижнее, Среднее, водопад Шумы, Катунский заповедник', type: 'sight' },
        { coords: [50.15, 86.3], title: 'Тюнгур — село на Катуни, старт маршрутов к Белухе, турбазы, сплавы', type: 'stop' }
      ]
    },
    barnaul_loop: {
      center: [52.8, 84.0],
      zoom: 7,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [53.36, 83.75],               // Барнаул
        [52.5, 82.783],               // Алейск
        [51.983, 81.833],             // Поспелиха
        [51.594, 82.291],             // Курья (музей Калашникова)
        [51.683, 83.25],              // Новошипуново (Краснощёковский р-н)
        [51.65, 84.317],              // Солонешное
        [51.3975, 84.6761],           // Денисова пещера (у Чёрного Ануя)
        [51.995, 84.98],              // Белокуриха
        [52.51, 85.15],               // Бийск
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [53.36, 83.75], title: 'Барнаул — стоянка, музей, набережная Оби', type: 'stop' },
        { coords: [53.36, 83.75], title: 'Барнаул — исторический центр, Демидовская площадь', type: 'sight' },
        { coords: [52.5, 82.783], title: 'Алейск — транзит, заправки', type: 'stop' },
        { coords: [51.983, 81.833], title: 'Поспелиха — ж/д станция, храм Николая Чудотворца', type: 'stop' },
        { coords: [51.983, 81.833], title: 'Поспелиха — начало трассы Р370 на Змеиногорск', type: 'sight' },
        { coords: [51.594, 82.291], title: 'Курья — музей М. Т. Калашникова, стоянка', type: 'stop' },
        { coords: [51.594, 82.291], title: 'Курья — родина Калашникова, мемориальный музей, Знаменский храм', type: 'sight' },
        { coords: [51.683, 83.25], title: 'Новошипуново — транзит (Краснощёковский р-н)', type: 'stop' },
        { coords: [51.65, 84.317], title: 'Солонешное — стоянка, гостевые дома', type: 'stop' },
        { coords: [51.3975, 84.6761], title: 'Денисова пещера — памятник археологии, денисовский человек', type: 'sight' },
        { coords: [51.995, 84.98], title: 'Белокуриха — санатории, отели, парковки', type: 'stop' },
        { coords: [51.995, 84.98], title: 'Белокуриха — курорт, гора Церковка, минеральные источники', type: 'sight' },
        { coords: [52.51, 85.15], title: 'Бийск — транзит на обратном пути', type: 'stop' }
      ]
    },
    teletskoye: {
      center: [52.0, 86.2],
      zoom: 7,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [52.51, 85.15],               // Бийск
        [51.96, 85.92],               // Горно-Алтайск (Телецкий тракт)
        [51.7911, 87.2558],           // Артыбаш / Телецкое озеро
        [52.25, 87.12],               // Турочак (обратно)
        [52.51, 85.15],               // Бийск
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [52.51, 85.15], title: 'Бийск — транзит туда и обратно', type: 'stop' },
        { coords: [51.96, 85.92], title: 'Горно-Алтайск — выезд на Телецкий тракт', type: 'stop' },
        { coords: [51.7911, 87.2558], title: 'Артыбаш / Иогач — стоянки, базы, исток Бии', type: 'stop' },
        { coords: [51.7911, 87.2558], title: 'Телецкое озеро — водопад Корбу, Алтайский заповедник, катера', type: 'sight' },
        { coords: [52.25, 87.12], title: 'Турочак — транзит на обратном пути', type: 'stop' },
        { coords: [52.25, 87.12], title: 'Турочак — центр района, тайга, р. Лебедь', type: 'sight' }
      ]
    },
    parabel_kargasok: {
      center: [57.2, 83.2],
      zoom: 6,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [56.49, 84.95],               // Томск (туда)
        [58.31, 82.9],                // Колпашево
        [58.71, 81.50],               // Парабель
        [59.06, 80.87],               // Каргасок
        [56.26, 83.98],               // Кожевниково (обратно в Нск)
        [55.746, 83.365],             // Базой (трасса Нск—Кожевниково)
        [55.3, 82.733],               // Колывань (НСО)
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [56.49, 84.95], title: 'Томск — стоянка, деревянное зодчество (туда)', type: 'stop' },
        { coords: [56.49, 84.95], title: 'Томск — исторический центр, набережная Томи', type: 'sight' },
        { coords: [58.2, 82.75], title: 'Чажемто — база «Источник», сероводородный источник (по дороге)', type: 'sight' },
        { coords: [58.31, 82.9], title: 'Колпашево — транзит, краеведческий музей', type: 'stop' },
        { coords: [58.71, 81.50], title: 'Парабель — стоянка, краеведческий музей (мамонт, Нарымский край)', type: 'stop' },
        { coords: [58.71, 81.50], title: 'Парабель — музей, Нарым (ссылка), долина Оби и Парабели', type: 'sight' },
        { coords: [59.06, 80.87], title: 'Каргасок — стоянка, Музей искусства народов Севера', type: 'stop' },
        { coords: [59.06, 80.87], title: 'Каргасок — Обь, Васюган, Коларовские угодья, муралы', type: 'sight' },
        { coords: [56.26, 83.98], title: 'Кожевниково — обратно в Нск (трасса Нск—Кожевниково)', type: 'stop' },
        { coords: [55.746, 83.365], title: 'Базой — село на трассе Нск—Кожевниково, Базойский кедровник', type: 'stop' },
        { coords: [55.3, 82.733], title: 'Колывань — р.п. в НСО, 45 км от Нск, колокололитейный музей', type: 'sight' }
      ]
    },
    tanay: {
      center: [54.3, 85.2],
      zoom: 6,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [54.7953, 84.9988],           // Озеро Танай (Журавлево)
        [55.6664, 85.6278],           // Томская писаница (д. Писаная)
        [52.9533, 87.9556],           // Шерегеш (горнолыжный курорт)
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [54.7953, 84.9988], title: 'Озеро Танай — стоянки, базы, рыбалка', type: 'stop' },
        { coords: [54.7953, 84.9988], title: 'Озеро Танай (Танаев) — Салаирский кряж, парадром, ГЛК «Танай»', type: 'sight' },
        { coords: [55.6664, 85.6278], title: 'Томская писаница — музей-заповедник, стоянка у музея', type: 'stop' },
        { coords: [55.6664, 85.6278], title: 'Томская писаница — петроглифы, минизоопарк, экспозиции под открытым небом', type: 'sight' },
        { coords: [52.9533, 87.9556], title: 'Шерегеш — отели, кемпинги, парковки у склонов', type: 'stop' },
        { coords: [52.9533, 87.9556], title: 'Шерегеш — горнолыжный курорт, г. Зелёная, Горная Шория', type: 'sight' }
      ]
    },
    krasnoyarsk_ergaki: {
      center: [54.5, 92.0],
      zoom: 5,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [56.015, 92.893],             // Красноярск
        [53.72, 91.43],               // Абакан
        [52.81, 93.29],               // Ергаки (трасса М54, визит-центр)
        [53.72, 91.43],               // Абакан (обратно)
        [56.015, 92.893],             // Красноярск
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [56.015, 92.893], title: 'Красноярск — стоянка, набережная Енисея', type: 'stop' },
        { coords: [56.015, 92.893], title: 'Красноярск — исторический центр, Часовня Параскевы', type: 'sight' },
        { coords: [55.9537, 92.7466], title: 'Красноярские Столбы — нацпарк, скалы, тропы', type: 'sight' },
        { coords: [53.72, 91.43], title: 'Абакан — стоянка, столица Хакасии', type: 'stop' },
        { coords: [53.72, 91.43], title: 'Абакан — набережная, слияние Енисея и Абакана, музеи', type: 'sight' },
        { coords: [52.81, 93.29], title: 'Ергаки — визит-центр, стоянки, старт троп', type: 'stop' },
        { coords: [52.81, 93.29], title: 'Природный парк Ергаки — Западные Саяны, озёра, Спящий Саян', type: 'sight' }
      ]
    },
    baikal: {
      center: [53.5, 96.0],
      zoom: 4,
      track: [
        [55.0084, 82.9357], [55.35, 86.09], [56.015, 92.893], [55.94, 98.00],
        [52.28, 104.28], [51.857, 104.862], [52.28, 104.28], [56.015, 92.893],
        [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [55.35, 86.09], title: 'Кемерово — стоянка в пути', type: 'stop' },
        { coords: [56.015, 92.893], title: 'Красноярск — стоянка в пути', type: 'stop' },
        { coords: [52.28, 104.28], title: 'Иркутск — исторический центр', type: 'sight' },
        { coords: [51.857, 104.862], title: 'Листвянка — кемпинги, базы', type: 'stop' },
        { coords: [51.857, 104.862], title: 'Листвянка: Байкальский музей, нерпинарий, Шаман-камень', type: 'sight' }
      ]
    },
    crimea: {
      center: [51.0, 58.0],
      zoom: 4,
      track: [
        [55.0084, 82.9357], [54.99, 73.37], [55.16, 61.40], [54.73, 55.97],
        [53.20, 50.15], [48.71, 44.52], [47.23, 39.70], [45.02, 38.97],
        [45.36, 36.47], [44.95, 34.10],
        [45.36, 36.47], [45.02, 38.97], [47.23, 39.70], [51.67, 39.20],
        [55.75, 37.62], [56.13, 40.41], [55.79, 49.12], [56.84, 60.61],
        [57.15, 65.53], [54.99, 73.37], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [54.99, 73.37], title: 'Омск — стоянка в пути', type: 'stop' },
        { coords: [55.16, 61.40], title: 'Челябинск — транзит', type: 'stop' },
        { coords: [54.73, 55.97], title: 'Уфа — стоянка, набережная', type: 'stop' },
        { coords: [53.20, 50.15], title: 'Самара — набережная Волги, бункер Сталина', type: 'sight' },
        { coords: [48.71, 44.52], title: 'Волгоград — Мамаев курган, центр', type: 'sight' },
        { coords: [47.23, 39.70], title: 'Ростов-на-Дону — Дон, въезд на юг', type: 'stop' },
        { coords: [45.02, 38.97], title: 'Краснодар — перед Крымским мостом', type: 'stop' },
        { coords: [44.95, 34.10], title: 'Крым — Симферополь, Ялта, Севастополь', type: 'sight' },
        { coords: [51.67, 39.20], title: 'Воронеж — стоянка обратно', type: 'stop' },
        { coords: [55.75, 37.62], title: 'Москва — объезд или заезд (М4)', type: 'stop' },
        { coords: [56.13, 40.41], title: 'Владимир — Золотое кольцо', type: 'sight' },
        { coords: [55.79, 49.12], title: 'Казань — Кремль, Кул-Шариф', type: 'sight' },
        { coords: [56.84, 60.61], title: 'Екатеринбург — транзит', type: 'stop' },
        { coords: [57.15, 65.53], title: 'Тюмень — стоянка в пути', type: 'stop' }
      ]
    },
    vladivostok: {
      center: [52.0, 108.0],
      zoom: 3,
      track: [
        [55.0084, 82.9357], [55.35, 86.09], [56.015, 92.893], [52.28, 104.28],
        [51.83, 107.58], [52.03, 113.50], [48.48, 135.07], [50.55, 137.01], [48.48, 135.07],
        [43.12, 131.87], [42.82, 132.87],
        [43.12, 131.87], [48.48, 135.07], [52.03, 113.50], [51.83, 107.58],
        [55.65, 109.32], [56.13, 101.61], [56.015, 92.893], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [55.35, 86.09], title: 'Кемерово — стоянка в пути', type: 'stop' },
        { coords: [56.015, 92.893], title: 'Красноярск — стоянка (туда)', type: 'stop' },
        { coords: [52.28, 104.28], title: 'Иркутск — юг Байкала, М53/М55', type: 'sight' },
        { coords: [51.83, 107.58], title: 'Улан-Удэ — стоянка, М55', type: 'stop' },
        { coords: [52.03, 113.50], title: 'Чита — стоянка, Забайкалье', type: 'stop' },
        { coords: [48.48, 135.07], title: 'Хабаровск — стоянка, Амур', type: 'stop' },
        { coords: [50.55, 137.01], title: 'Комсомольск-на-Амуре — заезд от Хабаровска (~400 км), Амур, промышленный город', type: 'stop' },
        { coords: [50.55, 137.01], title: 'Комсомольск-на-Амуре — набережная Амура, музей, город юности', type: 'sight' },
        { coords: [43.12, 131.87], title: 'Владивосток — мосты, набережные, океан', type: 'sight' },
        { coords: [42.82, 132.87], title: 'Находка — порт, бухты, восток Приморья', type: 'sight' },
        { coords: [55.65, 109.32], title: 'Северобайкальск — север Байкала, обратно', type: 'stop' },
        { coords: [56.13, 101.61], title: 'Братск — стоянка обратно (БАМ)', type: 'stop' },
        { coords: [56.015, 92.893], title: 'Красноярск — стоянка (обратно)', type: 'stop' }
      ]
    }
  };

  /**
   * Собирает URL для запроса маршрута в OSRM.
   * Точки в формате [lat, lng], OSRM ожидает lon,lat через точку с запятой.
   */
  function buildOsrmUrl(points) {
    var coords = points.map(function (p) { return p[1] + ',' + p[0]; });
    return OSRM_BASE + '/' + coords.join(';') + '?overview=full&geometries=geojson';
  }

  var FETCH_TIMEOUT_MS = 5000;

  /**
   * Запрашивает маршрут по дорогам. Возвращает массив [lat, lng] или null при ошибке/таймауте.
   */
  function fetchRouteGeometry(points) {
    if (points.length < 2) return Promise.resolve(null);
    var url = buildOsrmUrl(points);
    var timeoutPromise = new Promise(function (_, reject) {
      setTimeout(function () { reject(new Error('timeout')); }, FETCH_TIMEOUT_MS);
    });
    return Promise.race([fetch(url), timeoutPromise])
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data && data.code === 'Ok' && data.routes && data.routes[0] && data.routes[0].geometry && data.routes[0].geometry.coordinates) {
          var coords = data.routes[0].geometry.coordinates;
          return coords.map(function (c) { return [c[1], c[0]]; });
        }
        return null;
      })
      .catch(function () { return null; });
  }

  /**
   * Для длинных маршрутов OSRM может не взять все точки за раз.
   * Разбиваем на отрезки (последовательно A→B, B→C, ...) и склеиваем геометрию.
   */
  function fetchRouteGeometrySegmented(points) {
    if (points.length < 2) return Promise.resolve(null);

    var segments = [];
    for (var i = 0; i < points.length - 1; i++) {
      segments.push(fetchRouteGeometry([points[i], points[i + 1]]));
    }

    return Promise.all(segments).then(function (results) {
      var all = [];
      for (var j = 0; j < results.length; j++) {
        if (!results[j] || results[j].length === 0) return null;
        if (j > 0 && all.length > 0 && results[j][0][0] === all[all.length - 1][0] && results[j][0][1] === all[all.length - 1][1]) {
          all = all.concat(results[j].slice(1));
        } else {
          all = all.concat(results[j]);
        }
      }
      return all;
    });
  }

  function createWaypointIcon(type) {
    var color = type === 'stop' ? '#2e7d32' : '#1565c0';
    var label = type === 'stop' ? 'С' : 'Д';
    return L.divIcon({
      className: 'route-waypoint-icon',
      html: '<span style="background:' + color + ';color:#fff;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,0.3);border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;line-height:1;">' + label + '</span>',
      iconSize: [22, 22],
      iconAnchor: [11, 11]
    });
  }

  function addWaypointMarkers(map, waypoints) {
    if (!waypoints || !waypoints.length) return;
    waypoints.forEach(function (wp) {
      var popupTitle = wp.type === 'stop' ? 'Стоянка' : 'Достопримечательность';
      var icon = createWaypointIcon(wp.type);
      L.marker(wp.coords, { icon: icon })
        .addTo(map)
        .bindPopup('<strong>' + popupTitle + '</strong><br>' + wp.title);
    });
  }

  /** Строит bounds по точкам трека и waypoints, чтобы маршрут целиком влезал в карту. */
  function getRouteBounds(data) {
    var points = data.track || [];
    var waypoints = (data.waypoints || []).map(function (w) { return w.coords; });
    var all = points.concat(waypoints);
    if (all.length === 0) return null;
    var bounds = L.latLngBounds([all[0][0], all[0][1]], [all[0][0], all[0][1]]);
    all.forEach(function (p) { bounds.extend(p); });
    return bounds.isValid() ? bounds : null;
  }

  function fitMapToRoute(map, data) {
    var bounds = getRouteBounds(data);
    if (bounds) {
      map.fitBounds(bounds, { padding: [24, 24], maxZoom: 12 });
    }
  }

  function initMap(el, key) {
    var data = ROUTES[key];
    if (!data || !el) return Promise.resolve();

    var map = L.map(el, { scrollWheelZoom: true }).setView(data.center, data.zoom);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    var points = data.track || [];
    L.marker(points[0]).addTo(map).bindPopup('Новосибирск (старт)');
    if (points.length > 1 && (points[points.length - 1][0] !== points[0][0] || points[points.length - 1][1] !== points[0][1])) {
      L.marker(points[points.length - 1]).addTo(map).bindPopup('Финиш');
    }

    addWaypointMarkers(map, data.waypoints);

    function addRoutePolyline(map, points, roadCoords) {
      var coords = (roadCoords && roadCoords.length >= 2) ? roadCoords : points;
      var opts = (roadCoords && roadCoords.length >= 2)
        ? { color: '#727c8f', weight: 4, opacity: 0.9 }
        : { color: '#727c8f', weight: 4, opacity: 0.7, dashArray: '8,8' };
      try {
        if (map._leaflet_id && coords.length >= 2) {
          map.invalidateSize();
          L.polyline(coords, opts).addTo(map);
        }
      } catch (e) {}
    }

    if (typeof ROUTE_GEOMETRIES !== 'undefined' && ROUTE_GEOMETRIES[key] && ROUTE_GEOMETRIES[key].length >= 2) {
      addRoutePolyline(map, points, ROUTE_GEOMETRIES[key]);
      fitMapToRoute(map, data);
      return Promise.resolve();
    }

    return fetchRouteGeometry(points)
      .then(function (roadCoords) {
        if (!roadCoords || roadCoords.length < 2) {
          return fetchRouteGeometrySegmented(points);
        }
        return roadCoords;
      })
      .then(function (roadCoords) {
        addRoutePolyline(map, points, roadCoords);
        fitMapToRoute(map, data);
      })
      .catch(function () {
        addRoutePolyline(map, points, null);
        fitMapToRoute(map, data);
      });
  }

  function init() {
    var maps = document.querySelectorAll('.route-map[data-route]');
    var promises = [];
    maps.forEach(function (el) {
      var key = el.getAttribute('data-route');
      if (ROUTES[key]) promises.push(initMap(el, key));
    });
    Promise.all(promises).catch(function () {});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
