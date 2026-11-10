// Grow Slow release-plan site: season tabs and calendar links. Everything works without JS (all seasons stack).
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
