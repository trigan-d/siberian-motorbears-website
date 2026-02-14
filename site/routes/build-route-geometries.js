/**
 * Однократно запрашивает геометрию всех маршрутов у OSRM и сохраняет в route-geometries.js.
 * Запуск: node build-route-geometries.js
 * Требует: доступ в интернет (используется встроенный https, без fetch).
 */
const fs = require('fs');
const path = require('path');
const https = require('https');

const OSRM_HOST = 'router.project-osrm.org';

const TRACKS = {
  suzun: [[55.0084, 82.9357], [54.6355, 82.83], [54.2286, 81.7094], [53.786, 82.314], [54.344, 84.211], [54.6445, 83.9268], [54.646, 83.819], [54.768, 83.853], [54.959, 83.991], [55.0084, 82.9357]],
  lakes: [[55.0084, 82.9357], [55.0455, 80.3541], [55.28, 76.82], [55.336, 76.943], [54.227, 77.978], [53.7333, 78.0333], [55.0084, 82.9357]],
  yarovoye: [[55.0084, 82.9357], [54.3588, 81.8859], [53.9828, 79.2375], [53.7333, 78.0333], [53.2167, 78.9833], [52.9978, 78.6447], [52.9253, 78.5869], [52.9978, 78.6447], [53.2167, 78.9833], [53.7333, 78.0333], [53.9828, 79.2375], [54.3588, 81.8859], [55.0084, 82.9357]],
  altai5: [[55.0084, 82.9357], [52.51, 85.15], [52.00, 85.92], [51.98, 85.87], [51.41, 86.00], [51.123, 86.165], [51.82, 85.77], [52.51, 85.15], [55.0084, 82.9357]],
  altai7: [[55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00], [50.75, 86.13], [50.30, 87.60], [50.63, 87.95], [50.91, 88.22], [50.30, 87.60], [50.75, 86.13], [51.98, 85.87], [52.51, 85.15], [55.0084, 82.9357]],
  altai10: [[55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00], [50.75, 86.13], [50.30, 87.60], [50.0, 88.66], [51.41, 86.00], [52.51, 85.15], [53.36, 83.75], [55.0084, 82.9357]],
  multa: [[55.0084, 82.9357], [52.51, 85.15], [51.96, 85.92], [50.98, 84.99], [50.27, 85.615], [50.17, 85.95], [50.15, 86.3], [50.27, 85.615], [50.98, 84.99], [51.96, 85.92], [52.51, 85.15], [55.0084, 82.9357]],
  barnaul_loop: [[55.0084, 82.9357], [53.36, 83.75], [52.5, 82.783], [51.983, 81.833], [51.594, 82.291], [51.683, 83.25], [51.65, 84.317], [51.3975, 84.6761], [51.995, 84.98], [52.51, 85.15], [55.0084, 82.9357]],
  teletskoye: [[55.0084, 82.9357], [52.51, 85.15], [51.96, 85.92], [51.7911, 87.2558], [52.25, 87.12], [52.51, 85.15], [55.0084, 82.9357]],
  parabel_kargasok: [[55.0084, 82.9357], [56.49, 84.95], [58.31, 82.9], [58.71, 81.50], [59.06, 80.87], [56.26, 83.98], [55.746, 83.365], [55.3, 82.733], [55.0084, 82.9357]],
  tanay: [[55.0084, 82.9357], [54.7953, 84.9988], [55.6664, 85.6278], [52.9533, 87.9556], [55.0084, 82.9357]],
  krasnoyarsk_ergaki: [[55.0084, 82.9357], [56.015, 92.893], [53.72, 91.43], [52.81, 93.29], [53.72, 91.43], [56.015, 92.893], [55.0084, 82.9357]],
  baikal: [[55.0084, 82.9357], [55.35, 86.09], [56.015, 92.893], [55.94, 98.00], [52.28, 104.28], [51.857, 104.862], [52.28, 104.28], [56.015, 92.893], [55.0084, 82.9357]],
  crimea: [[55.0084, 82.9357], [54.99, 73.37], [55.16, 61.40], [54.73, 55.97], [53.20, 50.15], [48.71, 44.52], [47.23, 39.70], [45.02, 38.97], [45.36, 36.47], [44.95, 34.10], [45.36, 36.47], [45.02, 38.97], [47.23, 39.70], [51.67, 39.20], [55.75, 37.62], [56.13, 40.41], [55.79, 49.12], [56.84, 60.61], [57.15, 65.53], [54.99, 73.37], [55.0084, 82.9357]],
  // vladivostok: больше промежуточных точек, чтобы OSRM мог построить сегменты (Чита–Хабаровск, север Байкала, БАМ)
  vladivostok: [
    [55.0084, 82.9357], [55.35, 86.09], [56.015, 92.893], [52.28, 104.28], [51.83, 107.58], [52.03, 113.50],
    [50.29, 127.53], [48.48, 135.07], [50.55, 137.01], [48.48, 135.07], [43.8, 131.95], [43.12, 131.87], [42.82, 132.87],
    [43.12, 131.87], [43.8, 131.95], [48.48, 135.07], [50.29, 127.53], [52.03, 113.50], [51.83, 107.58],
    [54.0, 108.3], [55.65, 109.32], [56.8, 105.72], [56.13, 101.61], [55.95, 98.0], [56.015, 92.893], [55.0084, 82.9357]
  ]
};

function buildOsrmPath(points) {
  const coords = points.map(p => p[1] + ',' + p[0]);
  return '/route/v1/driving/' + coords.join(';') + '?overview=full&geometries=geojson';
}

function httpsGet(pathname) {
  return new Promise((resolve, reject) => {
    const opts = {
      hostname: OSRM_HOST,
      path: pathname,
      method: 'GET',
      family: 4
    };
    const req = https.request(opts, (res) => {
      let body = '';
      res.on('data', chunk => { body += chunk; });
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error('HTTP ' + res.statusCode + (body ? ': ' + body.slice(0, 120) : '')));
          return;
        }
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(new Error('Invalid JSON: ' + (e.message || String(e))));
        }
      });
    });
    req.on('error', (e) => {
      reject(new Error(e.code || e.message || String(e)));
    });
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

async function fetchRouteGeometry(points) {
  if (points.length < 2) return null;
  const pathname = buildOsrmPath(points);
  const data = await httpsGet(pathname);
  if (data.code === 'Ok' && data.routes && data.routes[0] && data.routes[0].geometry && data.routes[0].geometry.coordinates) {
    return data.routes[0].geometry.coordinates.map(c => [c[1], c[0]]);
  }
  return null;
}

async function fetchRouteGeometrySegmented(points) {
  if (points.length < 2) return null;
  const results = [];
  for (let i = 0; i < points.length - 1; i++) {
    const geom = await fetchRouteGeometry([points[i], points[i + 1]]);
    if (!geom || geom.length === 0) return null;
    results.push(geom);
    if (i < points.length - 2) await new Promise(r => setTimeout(r, 1200));
  }
  let all = [];
  for (let j = 0; j < results.length; j++) {
    if (j > 0 && all.length > 0 && results[j][0][0] === all[all.length - 1][0] && results[j][0][1] === all[all.length - 1][1]) {
      all = all.concat(results[j].slice(1));
    } else {
      all = all.concat(results[j]);
    }
  }
  return all;
}

async function getGeometry(key, points) {
  let coords = null;
  try {
    coords = await fetchRouteGeometry(points);
  } catch (e) {
    // полный маршрут может не строиться (NoRoute, timeout) — пробуем по сегментам
  }
  if (!coords || coords.length < 2) {
    coords = await fetchRouteGeometrySegmented(points);
  }
  return coords;
}

function loadExistingGeometries() {
  const outPath = path.join(__dirname, 'route-geometries.js');
  if (!fs.existsSync(outPath)) return {};
  const raw = fs.readFileSync(outPath, 'utf8');
  const start = raw.indexOf('var ROUTE_GEOMETRIES = ');
  if (start === -1) return {};
  const from = raw.indexOf('{', start);
  if (from === -1) return {};
  let depth = 0;
  let i = from;
  while (i < raw.length) {
    const c = raw[i];
    if (c === '{') depth++;
    else if (c === '}') { depth--; if (depth === 0) break; }
    i++;
  }
  const json = raw.slice(from, i + 1);
  try {
    return JSON.parse(json);
  } catch (e) {
    return {};
  }
}

async function main() {
  const onlyKey = process.argv[2] || null;
  const keys = onlyKey ? [onlyKey] : Object.keys(TRACKS);
  if (onlyKey && !TRACKS[onlyKey]) {
    console.error('Unknown route key: ' + onlyKey);
    process.exit(1);
  }

  let out = {};
  if (onlyKey) {
    out = loadExistingGeometries();
  }

  for (let i = 0; i < keys.length; i++) {
    const key = keys[i];
    process.stderr.write(`[${i + 1}/${keys.length}] ${key} ... `);
    try {
      const geom = await getGeometry(key, TRACKS[key]);
      if (geom && geom.length >= 2) {
        out[key] = geom;
        process.stderr.write(`${geom.length} points\n`);
      } else {
        process.stderr.write('no geometry, skip\n');
      }
    } catch (e) {
      const msg = (e && (e.message || e.code || e.cause && e.cause.message)) || String(e);
      process.stderr.write('error: ' + msg + '\n');
    }
    await new Promise(r => setTimeout(r, 400));
  }

  const outPath = path.join(__dirname, 'route-geometries.js');
  const content = '/** Pre-built OSRM route geometries. Generated by build-route-geometries.js. Do not edit by hand. */\n\nvar ROUTE_GEOMETRIES = ' + JSON.stringify(out) + ';\n';
  fs.writeFileSync(outPath, content, 'utf8');
  console.log('Wrote ' + outPath);
}

main().catch(e => { console.error(e); process.exit(1); });
