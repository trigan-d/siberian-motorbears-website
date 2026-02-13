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
        [54.6445, 83.9268],           // Гора Зверобой (Бердские скалы)
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [54.6355, 82.83], title: 'Бурмистрово — Караканский бор, берег водохранилища', type: 'stop' },
        { coords: [54.6355, 82.83], title: 'Караканский бор — сосновый лес, ООПТ', type: 'sight' },
        { coords: [54.2286, 81.7094], title: 'Абрашинский карьер (мраморное озеро) — стоянка, дайвинг', type: 'stop' },
        { coords: [54.2286, 81.7094], title: 'Абрашинский карьер — бывший мраморный карьер, прозрачное озеро', type: 'sight' },
        { coords: [53.786, 82.314], title: 'Сузун — стоянка, турбазы', type: 'stop' },
        { coords: [53.786, 82.314], title: 'Музей «Сузун-завод. Монетный двор»', type: 'sight' },
        { coords: [54.6445, 83.9268], title: 'Гора Зверобой (Бердские скалы) — памятник природы, смотровая', type: 'sight' }
      ]
    },
    lakes: {
      center: [54.8, 79.5],
      zoom: 7,
      track: [
        [55.0084, 82.9357], [55.05, 80.35], [55.25, 76.75], [55.336, 76.943],
        [54.35, 76.85], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [55.25, 76.75], title: 'Озеро Чаны — стоянки, базы «Бухта Лазурная», «Белый лебедь»', type: 'stop' },
        { coords: [55.25, 76.75], title: 'Озеро Чаны (крупнейшее в Западной Сибири)', type: 'sight' },
        { coords: [55.336, 76.943], title: 'Озеро Карачи — санаторий, окрестности', type: 'stop' },
        { coords: [55.336, 76.943], title: 'Озеро Карачи (лечебные грязи, рапа)', type: 'sight' },
        { coords: [54.35, 76.85], title: 'Озеро Горькое — зоны отдыха (Купинский/Баганский р-н)', type: 'stop' },
        { coords: [54.35, 76.85], title: 'Озеро Горькое (минеральные источники)', type: 'sight' }
      ]
    },
    altai5: {
      center: [51.8, 84.5],
      zoom: 7,
      track: [
        [55.0084, 82.9357], [52.51, 85.15], [52.00, 85.92], [51.98, 85.87],
        [51.41, 86.00], [51.82, 85.77], [52.51, 85.15], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [52.00, 85.92], title: 'Сростки — музей Шукшина', type: 'sight' },
        { coords: [51.98, 85.87], title: 'Майма / Горно-Алтайск — стоянки, кемпинги', type: 'stop' },
        { coords: [51.41, 86.00], title: 'Чемал — кемпинги «Млечный путь», «Долина Катуни»', type: 'stop' },
        { coords: [51.41, 86.00], title: 'Чемальская ГЭС, остров Патмос, Козья тропа', type: 'sight' },
        { coords: [51.82, 85.77], title: 'Манжерок — туркомплекс, кемпинг у озера', type: 'stop' },
        { coords: [51.82, 85.77], title: 'Манжерокское озеро, канатная дорога на Синюху', type: 'sight' }
      ]
    },
    altai7: {
      center: [51.2, 85.2],
      zoom: 6,
      track: [
        [55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00],
        [50.75, 86.13], [50.30, 87.60], [50.75, 86.13], [51.98, 85.87],
        [52.51, 85.15], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [51.98, 85.87], title: 'Майма — стоянка', type: 'stop' },
        { coords: [51.41, 86.00], title: 'Чемал — стоянка', type: 'stop' },
        { coords: [50.75, 86.13], title: 'Онгудай — кемпинги вдоль тракта', type: 'stop' },
        { coords: [50.30, 87.60], title: 'Акташ / Курай — стоянки у трассы', type: 'stop' },
        { coords: [50.30, 87.60], title: 'Курайская степь, Гейзерное озеро', type: 'sight' },
        { coords: [50.25, 86.75], title: 'Перевал Чике-Таман', type: 'sight' },
        { coords: [50.92, 85.90], title: 'Перевал Семинский', type: 'sight' },
        { coords: [50.47, 86.98], title: 'Петроглифы Калбак-Таш', type: 'sight' }
      ]
    },
    altai10: {
      center: [52.5, 84.0],
      zoom: 6,
      track: [
        [55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00],
        [50.75, 86.13], [50.30, 87.60], [51.41, 86.00], [52.51, 85.15],
        [53.36, 83.75], [55.0084, 82.9357]
      ],
      waypoints: [
        { coords: [51.41, 86.00], title: 'Чемал — стоянка', type: 'stop' },
        { coords: [51.82, 85.77], title: 'Манжерок — стоянка', type: 'stop' },
        { coords: [50.75, 86.13], title: 'Онгудай — стоянка', type: 'stop' },
        { coords: [50.30, 87.60], title: 'Акташ — стоянка', type: 'stop' },
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
        [50.08, 85.63],              // Усть-Кокса
        [50.17, 85.95],              // Мульта
        [50.08, 85.63],              // Усть-Кокса (обратно)
        [50.98, 84.99],              // Усть-Кан
        [51.96, 85.92],              // Горно-Алтайск
        [52.51, 85.15],              // Бийск
        [55.0084, 82.9357]           // Новосибирск
      ],
      waypoints: [
        { coords: [50.98, 84.99], title: 'Усть-Кан — стоянка, ночёвка в пути', type: 'stop' },
        { coords: [50.98, 84.99], title: 'Усть-Канская пещера (Белый Камень), Канская степь', type: 'sight' },
        { coords: [50.08, 85.63], title: 'Усть-Кокса — стоянки, турбазы, центр района', type: 'stop' },
        { coords: [50.08, 85.63], title: 'Усть-Кокса: слияние Коксы и Катуни, музеи Рериха и старообрядцев, перевал Громотуха', type: 'sight' },
        { coords: [50.17, 85.95], title: 'Мульта — стоянки, базы, старт тропы к озёрам', type: 'stop' },
        { coords: [49.98, 85.83], title: 'Мультинские озёра — Нижнее, Среднее, водопад Шумы, Катунский заповедник', type: 'sight' }
      ]
    },
    barnaul_loop: {
      center: [52.8, 84.0],
      zoom: 7,
      track: [
        [55.0084, 82.9357],           // Новосибирск
        [53.36, 83.75],               // Барнаул
        [52.5, 82.783],               // Алейск
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
        [56.49, 84.95],               // Томск
        [58.31, 82.9],                // Колпашево
        [58.71, 81.50],               // Парабель
        [59.06, 80.87],               // Каргасок
        [56.49, 84.95],               // Томск (обратно)
        [55.0084, 82.9357]            // Новосибирск
      ],
      waypoints: [
        { coords: [56.49, 84.95], title: 'Томск — стоянка, деревянное зодчество, музеи', type: 'stop' },
        { coords: [56.49, 84.95], title: 'Томск — исторический центр, набережная Томи', type: 'sight' },
        { coords: [58.2, 82.75], title: 'Чажемто — база «Источник», сероводородный источник (по дороге)', type: 'sight' },
        { coords: [58.31, 82.9], title: 'Колпашево — транзит, краеведческий музей', type: 'stop' },
        { coords: [58.71, 81.50], title: 'Парабель — стоянка, краеведческий музей (мамонт, Нарымский край)', type: 'stop' },
        { coords: [58.71, 81.50], title: 'Парабель — музей, Нарым (ссылка), долина Оби и Парабели', type: 'sight' },
        { coords: [59.06, 80.87], title: 'Каргасок — стоянка, Музей искусства народов Севера', type: 'stop' },
        { coords: [59.06, 80.87], title: 'Каргасок — Обь, Васюган, Коларовские угодья, муралы', type: 'sight' }
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
