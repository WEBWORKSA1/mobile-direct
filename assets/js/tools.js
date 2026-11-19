/* Mobile.Direct calculators. Each tool runs only if its container is on the page. */
(function () {
  'use strict';
  var MD = window.MD, $ = MD.$, $$ = MD.$$;
  function num(el) { var v = parseFloat(el && el.value); return isNaN(v) ? 0 : v; }
  function bindRanges(scope, fn) {
    $$('input, select', scope).forEach(function (i) { i.addEventListener('input', fn); i.addEventListener('change', fn); });
    $$('.range-row', scope).forEach(function (r) {
      var inp = $('input[type=range]', r), out = $('output', r);
      if (!inp || !out) return;
      var unit = out.getAttribute('data-unit') || '';
      var upd = function () { out.textContent = inp.value + unit; };
      inp.addEventListener('input', upd); upd();
    });
    fn();
  }

  /* 1. Data usage calculator */
  var dataTool = $('#tool-data');
  if (dataTool) {
    bindRanges(dataTool, function () {
      var daily = 0;
      $$('input[data-rate]', dataTool).forEach(function (i) { daily += num(i) * parseFloat(i.getAttribute('data-rate')); });
      var wifi = num($('#data-wifi')) / 100;
      var monthly = daily * 30.4 * (1 - wifi);
      $('#data-out').textContent = monthly < 10 ? monthly.toFixed(1) + ' GB' : Math.round(monthly) + ' GB';
      var rec, bars;
      if (monthly < 3) { rec = 'Light user. A 3–5 GB plan covers you with room to spare.'; bars = 1; }
      else if (monthly < 12) { rec = 'Moderate user. Pick a 15 GB plan so streaming weeks do not push you over.'; bars = 2; }
      else if (monthly < 30) { rec = 'Heavy user. Look at 40–50 GB plans or entry-level unlimited.'; bars = 3; }
      else { rec = 'Very heavy user. Choose unlimited, ideally with priority data and a hotspot allowance.'; bars = 4; }
      $('#data-rec').textContent = rec;
      $('#data-bars').innerHTML = MD.bars(bars).replace('class="bars', 'class="bars lg');
      var hidden = $('#data-summary'); if (hidden) hidden.value = $('#data-out').textContent;
    });
  }

  /* 2. Total cost of ownership: option A vs option B */
  var tco = $('#tool-tco');
  if (tco) {
    var calc = function (p) {
      var g = function (n) { return num($('[name=' + p + n + ']', tco)); };
      var months = Math.max(1, g('months'));
      var rise = g('rise') / 100, plan = g('plan'), total = g('device') - g('trade');
      for (var m = 0; m < months; m++) total += plan * Math.pow(1 + rise, Math.floor(m / 12)) + g('extras');
      return { total: total, monthly: total / months, months: months };
    };
    bindRanges(tco, function () {
      var a = calc('a'), b = calc('b');
      $('#tco-a').textContent = MD.money(a.total);
      $('#tco-b').textContent = MD.money(b.total);
      $('#tco-a-m').textContent = MD.money(a.monthly) + ' a month over ' + a.months + ' months';
      $('#tco-b-m').textContent = MD.money(b.monthly) + ' a month over ' + b.months + ' months';
      var diff = Math.abs(a.total - b.total);
      var who = a.total < b.total ? 'Option A' : 'Option B';
      $('#tco-verdict').textContent = diff < 1 ? 'Both options cost the same.' : who + ' is cheaper by ' + MD.money(diff) + ' over the period.';
    });
  }

  /* 3. Refurbished vs new */
  var ref = $('#tool-refurb');
  if (ref) {
    bindRanges(ref, function () {
      var price = num($('#rf-new')), disc = num($('#rf-disc')) / 100;
      var batt = $('#rf-batt').checked ? num($('#rf-batt-cost')) : 0;
      var refurb = price * (1 - disc) + batt;
      var save = price - refurb;
      $('#rf-out').textContent = MD.money(save);
      $('#rf-detail').innerHTML = '<li><span>New</span><strong>' + MD.money(price) + '</strong></li>' +
        '<li><span>Refurbished, all-in</span><strong>' + MD.money(refurb) + '</strong></li>' +
        '<li><span>You keep</span><strong>' + Math.round(price ? save / price * 100 : 0) + '%</strong></li>';
    });
  }

  /* 4. Trade-in value estimator */
  var tin = $('#tool-tradein');
  if (tin) {
    var curves = { Apple: [1, .62, .48, .36, .26, .18], Samsung: [1, .50, .33, .22, .15, .1], Google: [1, .45, .30, .20, .13, .09], other: [1, .40, .25, .15, .1, .07] };
    var cond = { flawless: 1, good: .85, fair: .65, cracked: .35 };
    var phones = [];
    var sel = $('#ti-phone');
    var setFromPhone = function () {
      var p = phones.filter(function (x) { return x.id === sel.value; })[0];
      if (!p) return;
      $('#ti-price').value = p.price;
      var rel = new Date(p.released + '-15'), now = new Date();
      var months = Math.max(0, (now.getFullYear() - rel.getFullYear()) * 12 + now.getMonth() - rel.getMonth());
      $('#ti-age').value = Math.min(72, months);
      tin.setAttribute('data-brand', p.brand);
    };
    var run = function () {
      var brand = tin.getAttribute('data-brand') || 'other';
      var c = curves[brand] || curves.other;
      var years = num($('#ti-age')) / 12, i = Math.floor(years), f = years - i;
      var a = c[Math.min(i, c.length - 1)], b = c[Math.min(i + 1, c.length - 1)];
      var ret = a + (b - a) * f;
      var v = num($('#ti-price')) * ret * (cond[$('#ti-cond').value] || 1) * num($('#ti-storage'));
      if ($('#ti-locked').checked) v *= .85;
      var lo = Math.max(0, v * .88), hi = v * 1.12;
      $('#ti-out').textContent = MD.money(lo) + ' – ' + MD.money(hi);
      $('#ti-note').textContent = 'Retains about ' + Math.round(ret * 100) + '% of launch price at this age before condition adjustments.';
      var hidden = $('#ti-summary'); if (hidden) hidden.value = ($('#ti-phone').selectedOptions[0] || {}).textContent + ', est. ' + $('#ti-out').textContent;
    };
    MD.json('data/phones.json').then(function (d) {
      phones = d.phones.slice().sort(function (a, b) { return a.brand.localeCompare(b.brand) || b.released.localeCompare(a.released); });
      sel.innerHTML = phones.map(function (p) { return '<option value="' + p.id + '">' + MD.esc(p.model.indexOf(p.brand) === 0 ? p.model : p.brand + ' ' + p.model) + '</option>'; }).join('') + '<option value="other">Another phone (enter price)</option>';
      sel.value = 'iphone-16';
      setFromPhone();
      sel.addEventListener('change', function () { if (sel.value === 'other') tin.setAttribute('data-brand', 'other'); else setFromPhone(); run(); });
      bindRanges(tin, run);
    }).catch(function () { bindRanges(tin, run); });
  }

  /* 5. eSIM compatibility checker */
  var es = $('#tool-esim');
  if (es) {
    var models = {
      Apple: [
        ['iPhone 14 or newer bought in the US', 'yes', 'Supports eSIM and has no physical SIM tray. eSIM is the only option.'],
        ['iPhone XR, XS or newer (outside the US)', 'yes', 'Supports eSIM alongside the physical SIM. Most models bought in mainland China use two physical SIMs instead.'],
        ['iPhone X, 8 or older', 'no', 'No eSIM. Use a physical travel SIM or roaming.']
      ],
      Samsung: [
        ['Galaxy S20 series or newer', 'yes', 'Supported in most regions. Some early US carrier models needed a software update.'],
        ['Galaxy Z Fold or Z Flip (any)', 'yes', 'Supported in most regions.'],
        ['Galaxy A5x / A3x (2023 or newer)', 'check', 'Supported in many regions but not all. Run the EID test below.'],
        ['Galaxy A1x / A2x', 'check', 'Often missing eSIM. Run the EID test below.']
      ],
      Google: [
        ['Pixel 4 or newer', 'yes', 'Supported. Pixel 10 models sold in the US are eSIM-only.'],
        ['Pixel 3 / 3a', 'check', 'Supported except some models sold in Australia, Taiwan, Japan and by certain carriers.'],
        ['Pixel 2 or older', 'no', 'No general eSIM support.']
      ],
      Motorola: [
        ['Razr (2019 or newer)', 'yes', 'Supported.'],
        ['Edge (2022 or newer)', 'yes', 'Supported in most regions.'],
        ['Moto G series', 'check', 'Varies by model and carrier. Run the EID test below.']
      ],
      OnePlus: [
        ['OnePlus 11, 12, 13, 15 (US/EU models)', 'yes', 'Supported on US and European models.'],
        ['OnePlus Nord series', 'check', 'Varies by region.']
      ],
      Other: [
        ['Fairphone 4 or newer', 'yes', 'Supported.'],
        ['Nothing Phone (3)', 'yes', 'Supported.'],
        ['Xiaomi, Oppo, Vivo, Honor and others', 'check', 'Depends on the regional model. Run the EID test below.']
      ]
    };
    var brandSel = $('#es-brand'), modelSel = $('#es-model');
    var fill = function () {
      modelSel.innerHTML = models[brandSel.value].map(function (m, i) { return '<option value="' + i + '">' + MD.esc(m[0]) + '</option>'; }).join('');
      show();
    };
    var show = function () {
      var m = models[brandSel.value][modelSel.value];
      var map = { yes: ['status-good', 'Supports eSIM', 4], check: ['status-mid', 'Check your exact model', 2], no: ['status-bad', 'No eSIM', 0] };
      var s = map[m[1]];
      $('#es-out').innerHTML = MD.bars(s[2], m[1] === 'no').replace('class="bars', 'class="bars lg') + ' <span class="' + s[0] + '">' + s[1] + '</span>';
      $('#es-note').textContent = m[2];
    };
    brandSel.innerHTML = Object.keys(models).map(function (b) { return '<option>' + b + '</option>'; }).join('');
    brandSel.addEventListener('change', fill);
    modelSel.addEventListener('change', show);
    fill();
  }

  /* 6. Will my phone work abroad (band match) */
  var bt = $('#tool-bands');
  if (bt) {
    MD.json('data/bands.json').then(function (d) {
      var csel = $('#bd-country'), psel = $('#bd-preset');
      var keys = Object.keys(d.countries).sort(function (a, b) { return d.countries[a].name.localeCompare(d.countries[b].name); });
      csel.innerHTML = keys.map(function (k) { return '<option value="' + k + '">' + MD.esc(d.countries[k].name) + '</option>'; }).join('');
      var qs = new URLSearchParams(location.search);
      csel.value = qs.get('country') && d.countries[qs.get('country')] ? qs.get('country') : 'JP';
      psel.innerHTML = Object.keys(d.presets).map(function (k) { return '<option value="' + k + '">' + MD.esc(d.presets[k].label) + '</option>'; }).join('') + '<option value="custom">Enter my phone\'s bands</option>';
      var parse = function (txt) {
        var lte = [], nr = [];
        String(txt).split(/[\s,;\/]+/).forEach(function (t) {
          t = t.trim().toLowerCase(); if (!t) return;
          var m = t.match(/^n(\d+)$/); if (m) { nr.push(+m[1]); return; }
          m = t.match(/^b?(\d+)$/); if (m) lte.push(+m[1]);
        });
        return { lte: lte, nr: nr };
      };
      var run = function () {
        var c = d.countries[csel.value];
        $('#bd-custom-wrap').hidden = psel.value !== 'custom';
        var phone = psel.value === 'custom' ? parse($('#bd-custom').value) : d.presets[psel.value];
        var hitL = c.lte.filter(function (b) { return phone.lte.indexOf(b) > -1; });
        var hitN = c.nr.filter(function (b) { return phone.nr.indexOf(b) > -1; });
        var cov = c.lte.length ? hitL.length / c.lte.length : 0;
        var verdict, cls, bars;
        if (cov >= .75) { verdict = 'Works well on 4G'; cls = 'status-good'; bars = 4; }
        else if (cov >= .45) { verdict = 'Works, with some coverage gaps'; cls = 'status-mid'; bars = 3; }
        else if (cov > 0) { verdict = 'Limited 4G coverage'; cls = 'status-mid'; bars = 1; }
        else { verdict = 'Unlikely to work on 4G'; cls = 'status-bad'; bars = 0; }
        $('#bd-out').innerHTML = MD.bars(bars, bars < 2).replace('class="bars', 'class="bars lg') + ' <span class="' + cls + '">' + verdict + '</span>';
        var missL = c.lte.filter(function (b) { return hitL.indexOf(b) < 0; });
        $('#bd-detail').innerHTML =
          '<li><span>4G bands matched</span><strong>' + hitL.length + ' of ' + c.lte.length + '</strong></li>' +
          '<li><span>Missing 4G bands</span><strong>' + (missL.length ? missL.map(function (b) { return 'B' + b; }).join(', ') : 'None') + '</strong></li>' +
          '<li><span>5G bands matched</span><strong>' + (c.nr.length ? hitN.length + ' of ' + c.nr.length : 'No 5G data') + '</strong></li>';
      };
      [csel, psel].forEach(function (s) { s.addEventListener('change', run); });
      $('#bd-custom').addEventListener('input', run);
      run();
    });
  }

  /* 7. IMEI validator (Luhn) — runs locally, nothing is sent. */
  var im = $('#tool-imei');
  if (im) {
    var inp = $('#imei-in');
    var check = function () {
      var v = inp.value.replace(/\D/g, '');
      var out = $('#imei-out'), note = $('#imei-note');
      if (!v.length) { out.textContent = 'Enter 15 digits'; out.className = ''; note.textContent = ''; return; }
      if (v.length !== 15) { out.textContent = v.length + ' of 15 digits'; out.className = 'status-mid'; note.textContent = 'An IMEI has exactly 15 digits. Dial *#06# to see yours.'; return; }
      var sum = 0;
      for (var i = 0; i < 14; i++) { var n = +v[i]; if (i % 2 === 1) { n *= 2; if (n > 9) n -= 9; } sum += n; }
      var cd = (10 - (sum % 10)) % 10;
      if (cd === +v[14]) {
        out.textContent = 'Valid IMEI format'; out.className = 'status-good';
        note.textContent = 'Type Allocation Code (model identifier): ' + v.slice(0, 8) + '. A valid format does not prove the phone is clean; check the official blocklists below.';
      } else {
        out.textContent = 'Invalid IMEI'; out.className = 'status-bad';
        note.textContent = 'The check digit should be ' + cd + '. A mistyped or altered IMEI is a red flag when buying used.';
      }
    };
    inp.addEventListener('input', check); check();
  }

  /* 8. Roaming vs travel eSIM */
  var ro = $('#tool-roam');
  if (ro) {
    bindRanges(ro, function () {
      var days = Math.max(1, num($('#ro-days'))), gb = num($('#ro-gb')) * days;
      var pass = num($('#ro-pass')) * days;
      var fixed = gb * num($('#ro-pergb'));
      var unl = num($('#ro-unl')) * days;
      var opts = [['Carrier day pass', pass], ['Travel eSIM, fixed data', fixed], ['Travel eSIM, unlimited', unl]];
      opts.sort(function (a, b) { return a[1] - b[1]; });
      $('#ro-out').textContent = MD.money(opts[0][1]);
      $('#ro-best').textContent = opts[0][0] + ' is cheapest for ' + days + ' days and about ' + gb.toFixed(1) + ' GB.';
      $('#ro-detail').innerHTML = opts.map(function (o) { return '<li><span>' + o[0] + '</span><strong>' + MD.money(o[1]) + '</strong></li>'; }).join('');
    });
  }

  /* 9. Family bill splitter */
  var sp = $('#tool-split');
  if (sp) {
    var rows = $('#sp-rows');
    var addRow = function (name, gb) {
      var li = document.createElement('div');
      li.className = 'grid-2';
      li.innerHTML = '<div class="field"><label>Person</label><input type="text" value="' + MD.esc(name) + '" class="sp-name"></div>' +
        '<div class="field"><label>Data used (GB a month)</label><input type="number" min="0" step="0.5" value="' + gb + '" class="sp-gb"></div>';
      rows.appendChild(li);
      $$('input', li).forEach(function (i) { i.addEventListener('input', run); });
    };
    var run = function () {
      var total = num($('#sp-total')), share = num($('#sp-share')) / 100;
      var names = $$('.sp-name', sp), gbs = $$('.sp-gb', sp).map(num);
      var sumGb = gbs.reduce(function (a, b) { return a + b; }, 0) || 1;
      var base = total * (1 - share) / names.length;
      $('#sp-detail').innerHTML = names.map(function (n, i) {
        var amt = base + total * share * (gbs[i] / sumGb);
        return '<li><span>' + MD.esc(n.value || 'Line ' + (i + 1)) + '</span><strong>' + MD.money(amt) + '</strong></li>';
      }).join('');
    };
    [['Alex', 20], ['Sam', 6], ['Jordan', 2]].forEach(function (r) { addRow(r[0], r[1]); });
    $('#sp-add').addEventListener('click', function () { addRow('Line ' + ($$('.sp-name', sp).length + 1), 5); run(); });
    bindRanges(sp, run);
  }

  /* 10. Signal strength interpreter */
  var sg = $('#tool-signal');
  if (sg) {
    var rate = function (v, t) { return v >= t[0] ? 4 : v >= t[1] ? 3 : v >= t[2] ? 2 : v >= t[3] ? 1 : 0; };
    var words = ['Very poor', 'Poor', 'Fair', 'Good', 'Excellent'];
    bindRanges(sg, function () {
      var r = rate(num($('#sg-rsrp')), [-80, -90, -100, -110]);
      var q = rate(num($('#sg-rsrq')), [-10, -12, -15, -20]);
      var s = rate(num($('#sg-sinr')), [20, 13, 5, 0]);
      var overall = Math.min(r, Math.round((r + q + s) / 3));
      $('#sg-out').innerHTML = MD.bars(overall, overall < 2).replace('class="bars', 'class="bars lg') + ' <span class="' + (overall >= 3 ? 'status-good' : overall === 2 ? 'status-mid' : 'status-bad') + '">' + words[overall] + '</span>';
      $('#sg-detail').innerHTML =
        '<li><span>Signal power (RSRP)</span><strong>' + words[r] + '</strong></li>' +
        '<li><span>Signal quality (RSRQ)</span><strong>' + words[q] + '</strong></li>' +
        '<li><span>Noise ratio (SINR)</span><strong>' + words[s] + '</strong></li>';
      var advice = overall >= 3 ? 'Your connection is healthy. Slow speeds are more likely network congestion than signal.'
        : overall === 2 ? 'Usable but marginal indoors. Wi-Fi calling or moving near a window helps.'
        : 'Weak. Try Wi-Fi calling, a carrier on a different network, or a signal booster approved for your carrier.';
      $('#sg-advice').textContent = advice;
    });
  }
})();
