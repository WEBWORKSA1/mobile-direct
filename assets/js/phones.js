/* Phone finder: filters, personal match score, compare up to 3. */
(function () {
  'use strict';
  var MD = window.MD, $ = MD.$, $$ = MD.$$;
  var root = $('#phone-app');
  var homeList = $('#home-phones');
  if (!root && !homeList) return;

  var chipTier = {
    'A19 Pro': 10, 'Snapdragon 8 Elite Gen 5': 10, 'Snapdragon 8 Elite Gen 5 for Galaxy': 10,
    'A19': 9.5, 'Snapdragon 8 Elite': 9.4, 'Snapdragon 8 Elite for Galaxy': 9.5,
    'A18': 8.8, 'Snapdragon 8 Gen 3': 8.5, 'Snapdragon 8s Gen 4': 8.3, 'Tensor G5': 8.2, 'Exynos 2500': 8.2, 'Exynos 2400': 8.0,
    'Tensor G4': 7.5, 'Exynos 1580': 6.4, 'Dimensity 7400X': 6.3, 'Snapdragon 7s Gen 3': 6.2, 'Dimensity 6300': 4.8
  };
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function score(p) {
    var perf = chipTier[p.chipset] || 6;
    var cams = p.cameras || [];
    var camera = 5 + Math.min(2, (cams.length - 1)) * 1.1 + (p.tele ? 1.4 : 0) + (cams[0] >= 200 ? .7 : cams[0] >= 48 ? .5 : 0) + (perf >= 9 ? .4 : 0);
    var battery = 4 + ((p.battery || 4000) - 3000) / 700 + (p.os === 'iOS' ? 1.2 : 0) + ((p.charging || 25) >= 60 ? .5 : 0);
    var display = 5 + (p.refresh >= 120 ? 2 : p.refresh >= 90 ? 1 : 0) + (p.refresh > 120 ? .5 : 0) + clamp((p.display - 6.0) * 1.6, 0, 2.2);
    var avg = (perf + clamp(camera, 0, 10) + clamp(battery, 0, 10) + clamp(display, 0, 10)) / 4;
    var value = 2 + 8 * (avg / 10) * Math.sqrt(700 / Math.max(150, p.price));
    return { perf: clamp(perf, 0, 10), camera: clamp(camera, 0, 10), battery: clamp(battery, 0, 10), display: clamp(display, 0, 10), value: clamp(value, 0, 10) };
  }
  function match(s, w) {
    var t = 0, sum = 0;
    Object.keys(w).forEach(function (k) { t += s[k] * w[k]; sum += w[k]; });
    return sum ? t / sum : 0;
  }
  function specLine(p) {
    return p.display + '" ' + p.refresh + 'Hz, ' + p.chipset + ', ' + p.ram + ' GB RAM, ' +
      (p.battery ? (p.batteryApprox ? '~' : '') + p.battery + ' mAh' : 'battery n/a') + ', ' + p.cameras.join(' + ') + ' MP';
  }
  function bars(v) { return MD.bars(v / 2.5); }
  function pname(p) { return p.model.toLowerCase().indexOf(p.brand.toLowerCase()) === 0 ? p.model : p.brand + ' ' + p.model; }

  MD.json('data/phones.json').then(function (d) {
    var phones = d.phones.map(function (p) { p.s = score(p); return p; });

    if (homeList) {
      var latest = phones.slice().sort(function (a, b) { return b.released.localeCompare(a.released); }).slice(0, 6);
      homeList.innerHTML = latest.map(function (p) {
        var m = match(p.s, { perf: 1, camera: 1, battery: 1, display: 1, value: 1 });
        return '<tr><td><strong>' + MD.esc(pname(p)) + '</strong><br><span class="small">' + MD.esc(p.released) + '</span></td>' +
          '<td class="num">' + MD.money(p.price) + '</td><td>' + p.display + '"</td><td>' + MD.esc(p.chipset) + '</td>' +
          '<td>' + bars(m) + ' ' + m.toFixed(1) + '</td></tr>';
      }).join('');
      return;
    }

    var brands = Array.from(new Set(phones.map(function (p) { return p.brand; }))).sort();
    $('#f-brand').innerHTML = '<option value="">All brands</option>' + brands.map(function (b) { return '<option>' + b + '</option>'; }).join('');
    var selected = [];
    var hash = new URLSearchParams(location.hash.slice(1));
    if (hash.get('compare')) selected = hash.get('compare').split(',').filter(function (id) { return phones.some(function (p) { return p.id === id; }); }).slice(0, 3);

    function weights() {
      var w = {};
      $$('#weights input[type=range]').forEach(function (r) { w[r.name] = +r.value; var o = r.parentNode.querySelector('output'); if (o) o.textContent = r.value; });
      return w;
    }
    function render() {
      var q = $('#f-q').value.trim().toLowerCase(), brand = $('#f-brand').value, max = +$('#f-price').value || 99999;
      var size = $('#f-size').value, sort = $('#f-sort').value, w = weights();
      var list = phones.filter(function (p) {
        if (brand && p.brand !== brand) return false;
        if (p.price > max) return false;
        if (q && (p.brand + ' ' + p.model + ' ' + p.chipset).toLowerCase().indexOf(q) < 0) return false;
        if (size === 'compact' && p.display > 6.3) return false;
        if (size === 'large' && p.display < 6.6) return false;
        if (size === 'fold' && !p.foldable) return false;
        return true;
      }).map(function (p) { p.m = match(p.s, w); return p; });
      var sorters = {
        match: function (a, b) { return b.m - a.m; },
        price: function (a, b) { return a.price - b.price; },
        newest: function (a, b) { return b.released.localeCompare(a.released); },
        battery: function (a, b) { return (b.battery || 0) - (a.battery || 0); }
      };
      list.sort(sorters[sort] || sorters.match);
      $('#phone-count').textContent = list.length + (list.length === 1 ? ' phone' : ' phones');
      $('#phone-list').innerHTML = list.length ? list.map(function (p, i) {
        var on = selected.indexOf(p.id) > -1;
        return '<li class="phone-row">' +
          '<span class="rank">' + (i + 1) + '</span>' +
          '<div><h3>' + MD.esc(pname(p)) + '</h3><span class="small">Released ' + MD.esc(p.released) + '. eSIM: ' + MD.esc(p.esim) + '</span></div>' +
          '<div class="specs">' + MD.esc(specLine(p)) + (p.ip ? ', ' + p.ip : '') + '</div>' +
          '<div><div class="score">' + bars(p.m) + ' ' + p.m.toFixed(1) + '</div><span class="small">' + MD.money(p.price) + (p.priceNote ? ' (' + MD.esc(p.priceNote) + ')' : '') + '</span></div>' +
          '<div class="acts"><button type="button" class="btn btn-sm ' + (on ? '' : 'btn-ghost') + '" data-compare="' + p.id + '" aria-pressed="' + on + '">' + (on ? 'Added to compare' : 'Compare') + '</button>' +
          '<button type="button" class="btn btn-sm btn-ghost" data-open-dialog="alert-dialog" data-item="' + MD.esc(pname(p)) + '">Price alert</button></div>' +
          '</li>';
      }).join('') : '<li class="phone-row"><span></span><div><h3>No phones match</h3><p class="small">Raise the price limit or clear the brand filter.</p></div></li>';
      updateBar();
    }
    function updateBar() {
      var bar = $('#compare-bar');
      bar.classList.toggle('show', selected.length > 0);
      $('#compare-names').textContent = selected.map(function (id) { var p = phones.filter(function (x) { return x.id === id; })[0]; return p.model; }).join(', ');
      $('#compare-go').disabled = selected.length < 2;
    }
    function showCompare() {
      var ps = selected.map(function (id) { return phones.filter(function (x) { return x.id === id; })[0]; });
      if (ps.length < 2) return;
      var w = weights();
      ps.forEach(function (p) { p.m = match(p.s, w); });
      var rows = [
        ['Match score', function (p) { return p.m; }, 'max', function (p) { return p.m.toFixed(1); }],
        ['Launch price', function (p) { return p.price; }, 'min', function (p) { return MD.money(p.price); }],
        ['Released', function (p) { return p.released; }, 'max', function (p) { return p.released; }],
        ['Screen', function (p) { return p.display; }, null, function (p) { return p.display + '"'; }],
        ['Refresh rate', function (p) { return p.refresh; }, 'max', function (p) { return p.refresh + ' Hz'; }],
        ['Chipset', function (p) { return p.s.perf; }, 'max', function (p) { return p.chipset; }],
        ['RAM', function (p) { return p.ram; }, 'max', function (p) { return p.ram + ' GB'; }],
        ['Base storage', function (p) { return p.storage; }, 'max', function (p) { return p.storage + ' GB'; }],
        ['Battery', function (p) { return p.battery || 0; }, 'max', function (p) { return p.battery ? (p.batteryApprox ? '~' : '') + p.battery + ' mAh' : 'n/a'; }],
        ['Wired charging', function (p) { return p.charging || 0; }, 'max', function (p) { return p.charging ? p.charging + ' W' : 'n/a'; }],
        ['Rear cameras', function (p) { return p.s.camera; }, 'max', function (p) { return p.cameras.join(' + ') + ' MP' + (p.tele ? ' (telephoto)' : ''); }],
        ['Water resistance', null, null, function (p) { return p.ip || 'n/a'; }],
        ['eSIM', null, null, function (p) { return p.esim; }]
      ];
      var html = '<table class="compare-table"><thead><tr><th scope="col">Spec</th>' + ps.map(function (p) { return '<th scope="col">' + MD.esc(pname(p)) + '</th>'; }).join('') + '</tr></thead><tbody>';
      rows.forEach(function (r) {
        var best = null;
        if (r[1] && r[2]) {
          var vals = ps.map(r[1]);
          best = r[2] === 'max' ? vals.reduce(function (a, b) { return a > b ? a : b; }) : vals.reduce(function (a, b) { return a < b ? a : b; });
          if (vals.every(function (v) { return v === best; })) best = null;
        }
        html += '<tr><th scope="row">' + r[0] + '</th>' + ps.map(function (p) {
          var win = best !== null && r[1](p) === best;
          return '<td' + (win ? ' class="win"' : '') + '>' + MD.esc(r[3](p)) + '</td>';
        }).join('') + '</tr>';
      });
      html += '</tbody></table>';
      $('#compare-table').innerHTML = html;
      $('#compare-section').hidden = false;
      history.replaceState(null, '', '#compare=' + selected.join(','));
      $('#compare-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    root.addEventListener('click', function (e) {
      var b = e.target.closest('[data-compare]');
      if (!b) return;
      var id = b.getAttribute('data-compare'), i = selected.indexOf(id);
      if (i > -1) selected.splice(i, 1);
      else { if (selected.length >= 3) selected.shift(); selected.push(id); }
      render();
    });
    $('#compare-go').addEventListener('click', showCompare);
    $('#compare-clear').addEventListener('click', function () { selected = []; $('#compare-section').hidden = true; history.replaceState(null, '', location.pathname + location.search); render(); });
    $$('#phone-filters input, #phone-filters select, #weights input').forEach(function (el) { el.addEventListener('input', render); el.addEventListener('change', render); });
    var pr = $('#f-price'), po = $('#f-price-out');
    var updPrice = function () { po.textContent = +pr.value >= 2000 ? 'Any' : MD.money(+pr.value); };
    pr.addEventListener('input', updPrice); updPrice();
    render();
    if (selected.length >= 2) showCompare();
  }).catch(function () {
    var target = $('#phone-list') || homeList;
    if (target) target.innerHTML = '<li>Phone data could not load. Refresh the page to try again.</li>';
  });
})();
