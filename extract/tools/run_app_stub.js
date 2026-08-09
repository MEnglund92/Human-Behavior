// run_app_stub.js — executes the app's inline script in a node vm with DOM stubs.
// Catches init errors that browser-less checks (node --check, HTTP smoke) miss.
// Usage: node run_app_stub.js [workdir]
// Verifies: clean parse, DOMContentLoaded init without error, and all 11 tabs
// render without throwing (incl. cloze Easy/Hard paths and exam start).
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = process.argv[2] || process.cwd();

function mkEl() {
  const target = function () {};
  return new Proxy(target, {
    get: (o, p) => {
      if (p === 'then') return undefined;
      if (p === Symbol.toPrimitive) return () => '';
      if (p === 'length') return 0;
      return mkEl();
    },
    set: () => true,
    apply: () => mkEl(),
  });
}

const store = {};
let domReadyCb = null;
let initError = null;
const errors = [];

const ctx = {
  console: {
    log: () => {},
    warn: (...a) => { if (String(a[0]).includes('Init error')) initError = a[1]; },
    error: (...a) => { errors.push(a.join(' ')); },
  },
  setInterval: () => 0, clearInterval: () => {},
  setTimeout: () => 0, clearTimeout: () => {},
  requestAnimationFrame: () => 0,
  confirm: () => true, alert: () => {},
  Math, JSON, Date, parseInt, parseFloat, isNaN,
  encodeURIComponent, decodeURIComponent, escape, unescape,
  String, Number, Boolean, Array, Object, RegExp, Promise, Map, Set, Error,
  Infinity, NaN, undefined,
};
ctx.localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; },
  clear: () => { for (const k in store) delete store[k]; },
};
ctx.navigator = { userAgent: 'stub', onLine: true, language: 'en-US', mediaDevices: {}, serviceWorker: {} };
ctx.document = {
  body: mkEl(), head: mkEl(),
  getElementById: () => mkEl(),
  querySelector: () => mkEl(),
  querySelectorAll: () => [],
  createElement: () => mkEl(),
  addEventListener: (ev, cb) => { if (ev === 'DOMContentLoaded') domReadyCb = cb; },
  documentElement: mkEl(),
};
ctx.window = ctx; ctx.self = ctx; ctx.globalThis = ctx;
ctx.getComputedStyle = () => ({ getPropertyValue: () => '' });
ctx.location = { href: 'http://localhost:8765/', reload: () => {}, protocol: 'http:' };
ctx.Audio = function () {};
ctx.speechSynthesis = { speak: () => {}, cancel: () => {}, getVoices: () => [] };
ctx.SpeechSynthesisUtterance = function () {};
vm.createContext(ctx);

let fails = 0;
const run = (f) => {
  try { vm.runInContext(fs.readFileSync(f, 'utf8'), ctx, { filename: f }); }
  catch (e) { fails++; console.log('FAIL ' + f + ': ' + e.message); }
};

const topics = fs.readdirSync(path.join(root, 'data/topics')).filter(f => f.endsWith('.js')).sort();
topics.forEach(f => run(path.join(root, 'data/topics', f)));
['data/deep-dives.js', 'data/resources.js', 'data.js'].forEach(f => run(path.join(root, f)));
const assets = fs.readdirSync(path.join(root, 'assets')).filter(f => f.startsWith('assetlib')).sort();
assets.forEach(f => run(path.join(root, 'assets', f)));
run(path.join(root, 'assets.js'));

const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.log('FAIL: inline script not found'); process.exit(1); }
// Inject the exposed app object at the TOP of the DOMContentLoaded callback body,
// where all function declarations are hoisted (functions are NOT in scope at top level).
const expose = 'document.addEventListener(\'DOMContentLoaded\',function(){window.__app={switchTab:switchTab,initMatch:initMatch,initCloze:initCloze,setDifficulty:setDifficulty,initQuiz:initQuiz,initFlash:initFlash,initSequence:initSequence,initLabConfig:initLabConfig,initReview:initReview,renderDeepDives:renderDeepDives,renderResources:renderResources,renderDashboard:renderDashboard,getEntries:getEntries,renderBrowse:renderBrowse,initSRS:initSRS,labModes:labModes,labSessionStart:labSessionStart,labGrade:labGrade,labInsights:labInsights,renderLab:renderLab,get labQ(){return labQ},get labIdx(){return labIdx},set labIdx(v){labIdx=v}};';
let inline = m[1].replace('document.addEventListener(\'DOMContentLoaded\',function(){', expose);
try { vm.runInContext(inline, ctx, { filename: 'index.html:inline' }); }
catch (e) { fails++; console.log('FAIL inline parse/top-level: ' + String(e)); }

if (!domReadyCb) { console.log('FAIL: DOMContentLoaded callback not registered'); process.exit(1); }
domReadyCb();
if (initError) { fails++; console.log('FAIL init: ' + initError.stack.split('\n').slice(0, 8).join('\n')); }

// Exercise every tab through switchTab + re-init paths.
const tabs = ['browse', 'flash', 'quiz', 'match', 'cloze', 'sequence', 'exam', 'lab', 'review', 'deep', 'resources', 'dashboard'];
tabs.forEach(t => {
  try { vm.runInContext("__app.switchTab('" + t + "')", ctx); }
  catch (e) { fails++; console.log('FAIL switchTab(' + t + '): ' + e.message); }
});
// Cloze easy/hard difficulty paths (initCloze throws for these when t is shadowed).
['easy', 'hard'].forEach(d => {
  try { vm.runInContext("__app.setDifficulty('cloze','" + d + "');__app.initCloze()", ctx); }
  catch (e) { fails++; console.log('FAIL initCloze(' + d + '): ' + e.message); }
});
// Match restart + browse re-render paths.
try { vm.runInContext('__app.initMatch()', ctx); } catch (e) { fails++; console.log('FAIL initMatch rerun: ' + e.message); }
try { vm.runInContext('__app.renderBrowse()', ctx); } catch (e) { fails++; console.log('FAIL renderBrowse rerun: ' + e.message); }

// Scenario Lab: run a session per mode (incl. derived modes) with 3 fixed
// questions, answer the first card, render the rest, and finish the session.
const labModes = vm.runInContext('__app.labModes()', ctx);
labModes.forEach(mode => {
  try {
    vm.runInContext("__app.labSessionStart('" + mode + "',3); if(__app.labQ.length){__app.labGrade(__app.labQ[__app.labIdx],true,__app.labInsights(__app.labQ[__app.labIdx]));__app.renderLab();} while(__app.labIdx+1<__app.labQ.length){__app.labIdx++;__app.renderLab();}", ctx);
  } catch (e) { fails++; console.log('FAIL labSessionStart(' + mode + '): ' + e.message); }
});

// Data assertion: every entry must be playable - a concept plus a scenario
// (or a definition fallback for it). Guards against blank match/quiz prompts.
try {
  const bad = vm.runInContext("__app.getEntries().filter(e=>!(e.concept&&String(e.concept).trim())||(!(e.real_world_scenario&&String(e.real_world_scenario).trim())&&!(e.definition&&String(e.definition).trim()))).length", ctx);
  if (bad > 0) { fails++; console.log('FAIL data: ' + bad + ' entries missing concept or both scenario+definition'); }
} catch (e) { fails++; console.log('FAIL data assertion: ' + e.message); }

console.log('tabs exercised: ' + tabs.length + ' | topics=' + (() => { try { return vm.runInContext('topics.length', ctx); } catch (e) { return 'ERR'; } })() + ' | ASSET_LIBS=' + (() => { try { return vm.runInContext('ASSET_LIBS.length', ctx); } catch (e) { return 'ERR'; } })());
console.log(fails === 0 ? 'ALL OK' : fails + ' FAILURES');
process.exit(fails === 0 ? 0 : 1);
