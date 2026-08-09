const CACHE = 'human-behavior-study-v25';
const FILES = [
  'index.html','data.js','manifest.json','icons/icon-180.png','icons/icon-192.png','icons/icon-512.png',
  'data/topics/topic-intro-behavior.js','data/topics/topic-behavioral-psych.js','data/topics/topic-social-psych.js',
  'data/topics/topic-body-language.js','data/topics/topic-cognitive-biases.js','data/topics/topic-personality.js',
  'data/topics/topic-nonverbal-codes.js','data/topics/topic-deception-detection.js','data/topics/topic-emotion-expression.js',
  'data/topics/topic-impression-mgmt.js','data/topics/topic-interpersonal-dynamics.js','data/topics/topic-reading-people.js',
  'data/topics/topic-moral-psychology.js','data/topics/topic-evolutionary-psych.js','data/topics/topic-biological-bases.js',
  'data/topics/topic-attachment-relationships.js','data/topics/topic-existential-humanistic.js','data/topics/topic-body-language-extracted.js',
  'data/deep-dives.js','data/resources.js',
  'assets/assetlib-apa_nonverbal.js','assets/assetlib-attached_workbook.js','assets/assetlib-behave.js',
  'assets/assetlib-bowden_truth_lies.js','assets/assetlib-definitive_body_language.js','assets/assetlib-dictionary_body_language.js',
  'assets/assetlib-emotions_revealed.js','assets/assetlib-glass_liars.js','assets/assetlib-influence.js',
  'assets/assetlib-laws_human_nature.js','assets/assetlib-mans_search_meaning.js','assets/assetlib-mistakes.js',
  'assets/assetlib-moral_animal.js','assets/assetlib-predictably_irrational.js','assets/assetlib-reiman_power_body_language.js',
  'assets/assetlib-research_methods.js','assets/assetlib-righteous_mind.js','assets/assetlib-social_animal.js',
  'assets/assetlib-social_intelligence.js','assets/assetlib-telling_lies.js','assets/assetlib-what_every_body.js',
  'assets.js'
];

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
