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
  suzun: [[55.0084, 82.9357], [54.6355, 82.83], [54.2286, 81.7094], [53.786, 82.314], [54.6445, 83.9268], [55.0084, 82.9357]],
  lakes: [[55.0084, 82.9357], [55.05, 80.35], [55.25, 76.75], [55.336, 76.943], [54.35, 76.85], [55.0084, 82.9357]],
  yarovoye: [[55.0084, 82.9357], [54.3588, 81.8859], [53.9828, 79.2375], [53.7333, 78.0333], [53.2167, 78.9833], [52.9978, 78.6447], [52.9253, 78.5869], [52.9978, 78.6447], [53.2167, 78.9833], [53.7333, 78.0333], [53.9828, 79.2375], [54.3588, 81.8859], [55.0084, 82.9357]],
  altai5: [[55.0084, 82.9357], [52.51, 85.15], [52.00, 85.92], [51.98, 85.87], [51.41, 86.00], [51.82, 85.77], [52.51, 85.15], [55.0084, 82.9357]],
  altai7: [[55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00], [50.75, 86.13], [50.30, 87.60], [50.75, 86.13], [51.98, 85.87], [52.51, 85.15], [55.0084, 82.9357]],
  altai10: [[55.0084, 82.9357], [52.51, 85.15], [51.98, 85.87], [51.41, 86.00], [50.75, 86.13], [50.30, 87.60], [51.41, 86.00], [52.51, 85.15], [53.36, 83.75], [55.0084, 82.9357]],
  multa: [[55.0084, 82.9357], [52.51, 85.15], [51.96, 85.92], [50.98, 84.99], [50.08, 85.63], [50.17, 85.95], [50.08, 85.63], [50.98, 84.99], [51.96, 85.92], [52.51, 85.15], [55.0084, 82.9357]],
  barnaul_loop: [[55.0084, 82.9357], [53.36, 83.75], [52.5, 82.783], [51.65, 84.317], [51.3975, 84.6761], [51.995, 84.98], [52.51, 85.15], [55.0084, 82.9357]],
  teletskoye: [[55.0084, 82.9357], [52.51, 85.15], [51.96, 85.92], [51.7911, 87.2558], [52.25, 87.12], [52.51, 85.15], [55.0084, 82.9357]],
  parabel_kargasok: [[55.0084, 82.9357], [56.49, 84.95], [58.31, 82.9], [58.71, 81.50], [59.06, 80.87], [56.49, 84.95], [55.0084, 82.9357]],
  tanay: [[55.0084, 82.9357], [54.7953, 84.9988], [55.6664, 85.6278], [52.9533, 87.9556], [55.0084, 82.9357]],
  krasnoyarsk_ergaki: [[55.0084, 82.9357], [56.015, 92.893], [53.72, 91.43], [52.81, 93.29], [53.72, 91.43], [56.015, 92.893], [55.0084, 82.9357]],
  baikal: [[55.0084, 82.9357], [55.35, 86.09], [56.015, 92.893], [55.94, 98.00], [52.28, 104.28], [51.857, 104.862], [52.28, 104.28], [56.015, 92.893], [55.0084, 82.9357]]
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
  const segments = [];
  for (let i = 0; i < points.length - 1; i++) {
    segments.push(fetchRouteGeometry([points[i], points[i + 1]]));
  }
  const results = await Promise.all(segments);
  let all = [];
  for (let j = 0; j < results.length; j++) {
    if (!results[j] || results[j].length === 0) return null;
    if (j > 0 && all.length > 0 && results[j][0][0] === all[all.length - 1][0] && results[j][0][1] === all[all.length - 1][1]) {
      all = all.concat(results[j].slice(1));
    } else {
      all = all.concat(results[j]);
    }
  }
  return all;
}

async function getGeometry(key, points) {
  let coords = await fetchRouteGeometry(points);
  if (!coords || coords.length < 2) {
    coords = await fetchRouteGeometrySegmented(points);
  }
  return coords;
}

async function main() {
  const out = {};
  const keys = Object.keys(TRACKS);
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
