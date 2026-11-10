// Grow Slow release-plan site: season tabs, calendar links and the live release status. Everything works without JS (all seasons stack).
(function () {
  var root = document.documentElement;
  root.classList.add('js');

  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  var panels = Array.prototype.slice.call(document.querySelectorAll('[role="tabpanel"]'));
  if (!tabs.length) return;

  function select(n, moveFocus) {
    n = String(n);
    tabs.forEach(function (t) {
      var on = t.dataset.season === n;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      if (on && moveFocus) t.focus();
    });
    panels.forEach(function (p) {
      p.classList.toggle('active', p.dataset.season === n);
    });
  }

  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t.dataset.season); });
    t.addEventListener('keydown', function (ev) {
      var next = null;
      if (ev.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
      if (ev.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
      if (ev.key === 'Home') next = tabs[0];
      if (ev.key === 'End') next = tabs[tabs.length - 1];
      if (next) { ev.preventDefault(); select(next.dataset.season, true); }
    });
  });

  // Calendar tiles jump to their season.
  Array.prototype.slice.call(document.querySelectorAll('[data-goto-season]')).forEach(function (a) {
    a.addEventListener('click', function () { select(a.dataset.gotoSeason); });
  });

  // Deep link such as #season-3.
  var m = /^#season-(\d)$/.exec(location.hash || '');
  select(m ? m[1] : 1);
})();

// Live release status. The plan's slots (planned time in IST) are compared with the visitor's clock, so
// "out now", "today" and "coming up" stay current without rebuilding the page. Preview any moment with
// ?now=2026-11-14T20:00:00%2B05:30 on the page address.
(function () {
  var host = document.getElementById('live-app');
  var raw = document.getElementById('slots-data');
  if (!host || !raw) return;
  var slots;
  try { slots = JSON.parse(raw.textContent); } catch (e) { return; }
  document.documentElement.classList.add('js');

  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var IST = 330 * 60000, DAY = 86400000, HOUR = 3600000;
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var WD = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var LAUNCH = '2026-11-10', TOTAL_DAYS = 48;
  slots.forEach(function (s) { s.ms = Date.parse(s.t); s.day = s.t.slice(0, 10); });
  slots.sort(function (a, b) { return a.ms - b.ms; });

  var startReal = Date.now(), fake = NaN, q = /[?&]now=([^&]+)/.exec(location.search);
  if (q) fake = Date.parse(decodeURIComponent(q[1]).replace(' ', '+'));
  function now() { return isNaN(fake) ? Date.now() : fake + (Date.now() - startReal); }

  function esc(v) { return String(v).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function ist(ms) {
    var d = new Date(ms + IST);
    return { key: d.toISOString().slice(0, 10), y: d.getUTCFullYear(), m: d.getUTCMonth(), d: d.getUTCDate(), wd: d.getUTCDay(), h: d.getUTCHours(), mi: d.getUTCMinutes(), s: d.getUTCSeconds() };
  }
  function clock12(p, secs) {
    var h = p.h % 12 || 12;
    return h + ':' + pad(p.mi) + (secs ? ':' + pad(p.s) : '') + ' ' + (p.h < 12 ? 'AM' : 'PM');
  }
  function dayLabel(key) { var d = new Date(key + 'T00:00:00Z'); return WD[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MON[d.getUTCMonth()]; }
  function dayDiff(a, b) { return Math.round((Date.parse(a + 'T00:00:00Z') - Date.parse(b + 'T00:00:00Z')) / DAY); }
  var localIST = new Date().getTimezoneOffset() === -330;
  function localLabel(ms) {
    if (localIST) return '';
    try { return new Date(ms).toLocaleString(undefined, { weekday: 'short', hour: 'numeric', minute: '2-digit' }); } catch (e) { return ''; }
  }
  function rel(key, today) {
    var n = dayDiff(key, today);
    if (n === 0) return 'Today';
    if (n === 1) return 'Tomorrow';
    if (n === -1) return 'Yesterday';
    return n > 0 ? 'In ' + n + ' days' : Math.abs(n) + ' days ago';
  }

  var CHECK = '<span class="check" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7"/></svg></span>';
  function chips(s) {
    return '<span class="langs">' + s.l.map(function (l) {
      return '<span class="lg ' + l + '"' + (l === 'hi' ? ' lang="hi"' : '') + '>' + (l === 'hi' ? 'Hindi' : 'English') + '</span>';
    }).join('') + '</span>';
  }
  function kindLabel(s) { return s.k === 'short' ? s.c : (s.k === 'film' ? 'FILM' : 'COUNTDOWN'); }
  // Films are on YouTube only. A Short or countdown gets YouTube and Instagram buttons for each language that is out.
  function watch(s) {
    if (s.k === 'film' || !s.g) {
      return '<div class="links">' + s.l.map(function (l) {
        return '<a href="' + esc(s.u[l]) + '" target="_blank" rel="noopener">Watch the film</a>';
      }).join('') + '</div>';
    }
    return '<div class="links by-lang">' + s.l.map(function (l) {
      var hi = l === 'hi', name = hi ? 'Hindi' : 'English';
      return '<div class="lk-row"><span class="lk-l"' + (hi ? ' lang="hi"' : '') + '>' + (hi ? 'हिंदी' : 'English') + '</span>' +
        '<a href="' + esc(s.u[l]) + '" target="_blank" rel="noopener" aria-label="Watch ' + esc(s.c) + ' in ' + name + ' on YouTube">YouTube</a>' +
        '<a href="' + esc(s.g[l]) + '" target="_blank" rel="noopener" aria-label="Watch ' + esc(s.c) + ' in ' + name + ' on Instagram">Instagram</a></div>';
    }).join('') + '</div>';
  }

  function card(s, i, state, today, n) {
    var fresh = state === 'out' && n - s.ms < 3 * HOUR;
    var label = state === 'out' ? (fresh ? 'Just out' : 'Out now') : state === 'next' ? 'Next up' : state === 'held' ? esc(s.d || 'Coming soon') : state === 'later' ? 'Today' : 'Upcoming';
    var local = localLabel(s.ms);
    return '<article class="rel st-' + state + (fresh ? ' fresh' : '') + '" style="--i:' + i + '">' +
      '<div class="pic"><img src="' + esc(s.i) + '" alt="" loading="lazy" width="720" height="405"><span class="kind">' + esc(kindLabel(s)) + '</span>' + (state === 'out' ? CHECK : '') + '</div>' +
      '<div class="rb"><div class="top"><span class="st">' + label + '</span>' + chips(s) + '</div>' +
      '<h4>' + esc(s.n) + '</h4>' +
      '<p class="when">' + dayLabel(s.day) + ' · ' + clock12(ist(s.ms)) + ' IST' + (local ? '<small>Your time: ' + esc(local) + '</small>' : '') + '</p>' +
      (s.x ? '<p class="when">' + esc(s.x) + '</p>' : '') +
      (state === 'out' ? watch(s) : '') + '</div></article>';
  }

  function lane(title, sub, cards, empty, cls) {
    return '<section class="lane ' + cls + '"><header><h3>' + title + '</h3><span>' + sub + '</span></header>' +
      (cards.length ? '<div class="stack">' + cards.join('') + '</div>' : '<p class="empty">' + empty + '</p>') + '</section>';
  }

  // Hindi and English uploads of one episode that are both out become one card with both watch buttons.
  function mergeOut(list) {
    var byCode = {}, order = [];
    list.slice().reverse().forEach(function (s) {
      var g = byCode[s.c];
      if (!g) { g = byCode[s.c] = {}; for (var p in s) g[p] = s[p]; g.l = s.l.slice(); order.push(g); }
      else s.l.forEach(function (l) { if (g.l.indexOf(l) < 0) g.l.push(l); });
    });
    order.forEach(function (g) { g.l.sort(function (a) { return a === 'hi' ? -1 : 1; }); });
    return order;
  }

  var key = '', cd = null;

  function compute(n) {
    var today = ist(n).key, out = [], todays = [], up = [], next = null;
    slots.forEach(function (s) {
      var held = !!s.d, done = !held && s.ms <= n;
      s.state = done ? 'out' : (held ? 'held' : 'later');
      if (done) out.push(s);
      if (!done && !held && !next) next = s;
      if (s.day === today) todays.push(s);
      else if (!done && (s.day > today || (held && s.day < today))) up.push(s);
    });
    if (next) next.state = 'next';
    return { today: today, out: out, todays: todays, up: up, next: next };
  }

  function render(n, v) {
    var i = 0, today = v.today;
    var groups = mergeOut(v.out);  // newest first, one card per episode or film
    var recent = groups.slice(0, 6);
    var firstMs = slots[0].ms;

    // Next release with a live countdown.
    var nextHtml;
    if (v.next) {
      var s = v.next, local = localLabel(s.ms);
      var kicker = n < firstMs ? 'Series premiere' : (s.day === today ? 'Today at ' + clock12(ist(s.ms)) + ' IST' : dayLabel(s.day) + ' · ' + clock12(ist(s.ms)) + ' IST');
      nextHtml = '<div class="next-card" style="--i:0"><div class="pic"><img src="' + esc(s.i) + '" alt=""><span class="badge"><i class="live-dot"></i>Next release</span></div>' +
        '<div class="nb"><span class="kicker">' + esc(kicker) + '</span><h3>' + esc(s.n) + '</h3>' +
        '<p class="sub">' + esc(s.k === 'short' ? s.c : (s.x || '')) + '</p><div class="langs-row">' + chips(s) + '</div>' +
        '<div class="cd" role="timer" aria-live="off" aria-label="Time until the next release"><div class="u"><b data-u="d">00</b><small>days</small></div><div class="u"><b data-u="h">00</b><small>hours</small></div><div class="u"><b data-u="m">00</b><small>min</small></div><div class="u"><b data-u="s">00</b><small>sec</small></div></div>' +
        (local ? '<p class="local">Your time: ' + esc(local) + '</p>' : '') + '</div></div>';
    } else {
      nextHtml = '<div class="next-card done" style="--i:0"><div class="nb"><span class="kicker">The series is complete</span><h3>Thank you for growing slow</h3><p class="sub">All 48 stories, six season films and the complete film are out. Start again from Season 1 any time.</p></div></div>';
    }

    // Journey: day counter, progress bar and season pills.
    var dayNo = dayDiff(today, LAUNCH) + 1;
    var dayText = dayNo < 1 ? 'Starts ' + dayLabel(LAUNCH) : dayNo > TOTAL_DAYS ? 'All ' + TOTAL_DAYS + ' days complete' : 'Day ' + dayNo + ' of ' + TOTAL_DAYS;
    var pct = Math.round(v.out.length / slots.length * 100);
    var pills = [1, 2, 3, 4, 5, 6, 0].map(function (sn) {
      var mine = slots.filter(function (x) { return x.s === sn; });
      var all = mine.every(function (x) { return x.state === 'out'; });
      var active = !all && v.next && v.next.s === sn;
      return '<li class="pill ' + (all ? 'st-done' : active ? 'st-active' : '') + '">' + (all ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7"/></svg>' : '') + (sn ? 'S' + sn : 'Finale') + '</li>';
    }).join('');
    var journey = '<div class="journey" style="--i:1"><span class="eyebrow">The journey</span><div class="day-no">' + esc(dayText) + '</div>' +
      '<div class="track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '" aria-label="Releases out so far"><div class="fill" style="--pct:' + pct + '%"></div></div>' +
      '<p class="meta-line"><b>' + v.out.length + '</b> of ' + slots.length + ' releases out · <b>' + (slots.length - v.out.length) + '</b> to go</p>' +
      '<ul class="pills" aria-label="Seasons">' + pills + '</ul></div>';

    // Lanes.
    var todayCards = v.todays.map(function (s) { return card(s, i++, s.state, today, n); });
    var upCards = v.up.slice(0, 6).map(function (s) { return card(s, i++, s.state === 'held' ? 'held' : 'upcoming', today, n); });
    var upSub = v.up.length > 6 ? '+' + (v.up.length - 6) + ' more in the calendar' : (v.up.length ? 'Next ' + v.up.length : '');
    var nextDay = v.next && v.next.day !== today ? dayLabel(v.next.day) : '';
    var todayEmpty = nextDay ? 'Nothing goes out today. The next release is ' + nextDay + '.' : 'Nothing goes out today.';
    var lanes = '<div class="lanes">' +
      lane('Out now', groups.length ? (groups.length === 1 ? '1 release' : groups.length + ' releases') : '', recent.map(function (s) { return card(s, i++, 'out', today, n); }), 'Nothing is out yet. The first story goes live ' + (v.next ? (v.next.day === today ? 'today at ' + clock12(ist(v.next.ms)) + ' IST' : dayLabel(v.next.day)) : 'soon') + '.', 'l-out') +
      lane('Today', dayLabel(today), todayCards, todayEmpty, 'l-today') +
      lane('Coming up', upSub, upCards, 'The plan is complete.', 'l-up') + '</div>';

    var bar = '<div class="live-bar"><span class="pulse" aria-hidden="true"></span><b>Live schedule</b><span class="live-clock" id="live-clock"></span></div>';
    host.innerHTML = bar + '<div class="live-top">' + nextHtml + journey + '</div>' + lanes;
    cd = {
      d: host.querySelector('[data-u="d"]'), h: host.querySelector('[data-u="h"]'),
      m: host.querySelector('[data-u="m"]'), s: host.querySelector('[data-u="s"]')
    };
    cd.last = {};
    mark(n, v);
  }

  // Calendar days and season-episode chips follow the same clock.
  function mark(n, v) {
    Array.prototype.forEach.call(document.querySelectorAll('.day[data-date]'), function (d) {
      var k = d.getAttribute('data-date');
      d.classList.toggle('is-past', k < v.today);
      d.classList.toggle('is-today', k === v.today);
    });
    Array.prototype.forEach.call(document.querySelectorAll('.ep[data-code]'), function (e) {
      var code = e.getAttribute('data-code');
      var mine = slots.filter(function (x) { return x.c === code; });
      if (!mine.length) return;
      var done = mine.filter(function (x) { return x.state === 'out'; }).length, cls, text;
      if (done === mine.length) { cls = 'out'; text = 'Out now'; }
      else if (done > 0) { cls = 'part'; text = 'Partly out'; }
      else if (mine.some(function (x) { return x.day === v.today; })) { cls = 'today'; text = 'Today'; }
      else { cls = 'soon'; text = 'Upcoming'; }
      var chip = e.querySelector('.state');
      if (!chip) { chip = document.createElement('span'); e.appendChild(chip); }
      chip.className = 'state ' + cls;
      chip.textContent = text;
    });
  }

  function setUnit(node, value, name) {
    var text = pad(value);
    if (cd.last[name] === text) return;
    cd.last[name] = text;
    node.textContent = text;
    if (!reduce) { node.classList.remove('tick'); void node.offsetWidth; node.classList.add('tick'); }
  }

  function tick() {
    var n = now(), v = compute(n);
    var k = v.today + '|' + v.out.length + '|' + (v.next ? v.next.t + v.next.c + (v.next.l || []).join('') : '-');
    if (k !== key) { key = k; render(n, v); }
    var p = ist(n), c = document.getElementById('live-clock');
    if (c) c.textContent = WD[p.wd] + ' ' + p.d + ' ' + MON[p.m] + ' ' + p.y + ' · ' + clock12(p, true) + ' IST';
    if (v.next && cd && cd.d) {
      var diff = Math.max(0, v.next.ms - n);
      setUnit(cd.d, Math.floor(diff / DAY), 'd');
      setUnit(cd.h, Math.floor(diff % DAY / HOUR), 'h');
      setUnit(cd.m, Math.floor(diff % HOUR / 60000), 'm');
      setUnit(cd.s, Math.floor(diff % 60000 / 1000), 's');
    }
  }

  tick();
  setInterval(tick, 1000);

  // Reveal with a staggered entrance the first time the section scrolls into view.
  function reveal() { host.classList.remove('pre'); host.classList.add('in'); }
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { reveal(); io.disconnect(); }
    }, { threshold: 0 });  // any part in view: the section is tall, so a ratio threshold could leave cards hidden
    io.observe(host);
    // Safety net for contexts that throttle observers: if the section is already on screen, reveal it anyway.
    setTimeout(function () {
      var r = host.getBoundingClientRect();
      if (host.classList.contains('pre') && r.top < window.innerHeight && r.bottom > 0) { reveal(); io.disconnect(); }
    }, 1200);
  } else {
    reveal();
  }
})();
