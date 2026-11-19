/* eSIM trip planner + news filter + client fallback renders. */
(function () {
  'use strict';
  var MD = window.MD, $ = MD.$, $$ = MD.$$;

  var trip = $('#tool-trip');
  if (trip) {
    MD.json('data/bands.json').then(function (d) {
      var sel = $('#tr-country');
      var keys = Object.keys(d.countries).sort(function (a, b) { return d.countries[a].name.localeCompare(d.countries[b].name); });
      sel.innerHTML = keys.map(function (k) { return '<option value="' + k + '">' + MD.esc(d.countries[k].name) + '</option>'; }).join('');
      sel.value = 'FR';
      var run = function () {
        var days = Math.max(1, parseFloat($('#tr-days').value) || 1);
        var per = parseFloat($('#tr-use').value);
        var total = days * per * 1.2;
        var c = d.countries[sel.value];
        $('#tr-out').textContent = (total < 10 ? total.toFixed(1) : Math.round(total)) + ' GB';
        var type = per >= 1.5 ? 'an unlimited plan (check the daily fair-use limit)' : total <= 3 ? 'a small fixed plan (1–3 GB)' : 'a fixed plan of about ' + Math.ceil(total / 5) * 5 + ' GB';
        $('#tr-rec').textContent = 'For ' + days + ' days in ' + c.name + ', buy ' + type + ', valid for at least ' + (days <= 7 ? 7 : days <= 15 ? 15 : 30) + ' days.';
        $('#tr-bands').innerHTML = '<li><span>4G bands in use</span><strong>' + c.lte.map(function (b) { return 'B' + b; }).join(', ') + '</strong></li>' +
          '<li><span>5G bands in use</span><strong>' + (c.nr.length ? c.nr.map(function (b) { return 'n' + b; }).join(', ') : 'Limited or none') + '</strong></li>';
        $('#tr-bandlink').href = MD.root + 'tools.html?country=' + sel.value + '#bands';
        var h = $('#tr-summary'); if (h) h.value = c.name + ', ' + days + ' days, ~' + $('#tr-out').textContent;
      };
      $$('input, select', trip).forEach(function (el) { el.addEventListener('input', run); el.addEventListener('change', run); });
      run();
    });
  }

  /* News filter by tag */
  var news = $('#news-app');
  if (news) {
    var list = $('#news-list');
    var renderFromJson = function () {
      return MD.json('data/news.json').then(function (d) {
        if (!d.items || !d.items.length) return;
        list.innerHTML = d.items.map(function (n) {
          var dt = new Date(n.date);
          return '<li data-tags="' + MD.esc((n.tags || []).join(' ')) + '"><time datetime="' + MD.esc(n.date) + '">' + dt.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) + '</time><div><a href="' + MD.esc(n.link) + '" rel="nofollow noopener" target="_blank">' + MD.esc(n.title) + '</a><span class="src">' + MD.esc(n.source) + '</span></div></li>';
        }).join('');
      }).catch(function () {});
    };
    var ready = list.children.length && !list.querySelector('[data-empty]') ? Promise.resolve() : renderFromJson();
    ready.then(function () {
      $$('[data-tag]', news).forEach(function (b) {
        b.addEventListener('click', function () {
          var t = b.getAttribute('data-tag');
          $$('[data-tag]', news).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          $$('li[data-tags]', list).forEach(function (li) { li.hidden = t !== 'all' && (' ' + li.getAttribute('data-tags') + ' ').indexOf(' ' + t + ' ') < 0; });
        });
      });
    });
  }
})();
