// Grow Slow: Season tabs and episode filters.
(function () {
  var root = document.documentElement;
  root.classList.add('js');

  // Season tabs
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  var panels = Array.prototype.slice.call(document.querySelectorAll('[role="tabpanel"]'));
  if (tabs.length) {
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

    // Deep link such as #season-2
    var m = /^#season-(\d)$/.exec(location.hash || '');
    if (m) select(m[1]);
  }

  // Filter released episodes by season (All, S2, S1)
  var pills = Array.prototype.slice.call(document.querySelectorAll('.filter-pill'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('.rel-grid.all-eps .ep-card'));
  if (pills.length && cards.length) {
    pills.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var filter = btn.dataset.filter;
        pills.forEach(function (p) {
          var on = p === btn;
          p.classList.toggle('active', on);
          p.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        cards.forEach(function (c) {
          var show = filter === 'all' || c.dataset.season === filter;
          c.style.display = show ? '' : 'none';
        });
      });
    });
  }
})();
