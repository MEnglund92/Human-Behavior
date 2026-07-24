const CACHE = 'human-behavior-study-v6';
const FILES = ['index.html','data.js','manifest.json','icons/icon-180.png','icons/icon-192.png','icons/icon-512.png'];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)));
});

self.addEventListener('activate', e => {
  self.clients.claim();
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
});

self.addEventListener('fetch', e => {
  const isHTML = e.request.mode === 'navigate' || e.request.headers.get('accept')?.includes('text/html');
  if (isHTML) {
    e.respondWith(
      fetch(e.request).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      }).catch(() => caches.match('index.html'))
    );
    return;
  }
  e.respondWith(
    caches.match(e.request).then(res => {
      if (res) return res;
      return fetch(e.request).then(response => {
        const ct = response.headers.get('content-type') || '';
        if (ct.startsWith('text/') || ct.startsWith('application/') || ct.startsWith('image/')) {
          const clone = response.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return response;
      }).catch(() => caches.match('index.html'));
    })
  );
});
