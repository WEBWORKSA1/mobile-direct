/* Plan match questionnaire: the lead-generation engine. */
(function () {
  'use strict';
  var MD = window.MD, $ = MD.$, $$ = MD.$$;

  function guessCountry() {
    var l = (navigator.language || 'en-US').toUpperCase();
    if (/-CA$/.test(l)) return 'CA';
    if (/-GB$/.test(l)) return 'UK';
    if (/-IN$/.test(l) || /^HI/.test(l)) return 'IN';
    if (/-AU$/.test(l)) return 'AU';
    if (/-US$/.test(l)) return 'US';
    return 'US';
  }

  /* Home hero: first question inline; the answer carries into the full questionnaire. */
  var hero = $('#hero-quiz');
  if (hero) {
    $$('[data-lines]', hero).forEach(function (b) {
      b.addEventListener('click', function () {
        location.href = MD.root + 'get-matched.html?lines=' + b.getAttribute('data-lines') + '&country=' + guessCountry() + '#quiz';
      });
    });
  }

  var app = $('#matcher');
  if (!app) return;

  var steps = [
    { key: 'country', q: 'Where will you use the plan?', opts: [['US', 'United States'], ['CA', 'Canada'], ['UK', 'United Kingdom'], ['IN', 'India'], ['AU', 'Australia'], ['OTHER', 'Somewhere else']] },
    { key: 'lines', q: 'How many lines do you need?', opts: [['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5 or more']] },
    { key: 'data', q: 'How much data does each person use a month?', help: 'Not sure? Most people use 5–15 GB. The data calculator on the Tools page gives an exact figure.', opts: [['light', 'Under 5 GB'], ['medium', '5–20 GB'], ['heavy', '20–50 GB'], ['unlimited', 'More than 50 GB']] },
    { key: 'priority', q: 'What matters most to you?', opts: [['price', 'Lowest price'], ['coverage', 'Best coverage'], ['travel', 'Using it abroad'], ['5g', 'Fastest 5G'], ['premium', 'Perks and priority data']] },
    { key: 'phone', q: 'What about the phone?', opts: [['byod', 'Keep my current phone'], ['flagship', 'New flagship'], ['budget', 'New, under $400'], ['refurb', 'Refurbished'], ['help', 'Help me choose']] },
    { key: 'bill', q: 'What do you pay now in total each month?', type: 'number' }
  ];
  var qs = new URLSearchParams(location.search);
  var ans = { country: qs.get('country') || guessCountry(), lines: qs.get('lines') || '', data: '', priority: '', phone: '', bill: '' };
  var i = ans.lines ? 2 : 0;
  var carriers = null, phones = null;
  Promise.all([MD.json('data/carriers.json'), MD.json('data/phones.json')]).then(function (r) { carriers = r[0]; phones = r[1].phones; }).catch(function () {});

  var stepBox = $('#quiz-step'), bar = $('#quiz-progress span'), back = $('#quiz-back'), count = $('#quiz-count');
  function draw() {
    var s = steps[i];
    bar.style.width = Math.round(i / steps.length * 100) + '%';
    count.textContent = 'Question ' + (i + 1) + ' of ' + steps.length;
    back.hidden = i === 0;
    var html = '<p class="quiz-q" id="q-label">' + s.q + '</p>';
    if (s.help) html += '<p class="small">' + s.help + '</p>';
    if (s.type === 'number') {
      var cur = (carriers && carriers.countries[ans.country]) ? carriers.countries[ans.country].currency : 'USD';
      html += '<div class="field"><label for="q-bill">Monthly total in ' + cur + '</label><input id="q-bill" type="number" min="0" step="1" inputmode="numeric" value="' + MD.esc(ans.bill) + '" placeholder="e.g. 85"></div>' +
        '<div class="seg"><button type="button" class="btn" id="q-next">See my match</button><button type="button" class="btn btn-ghost" id="q-skip">Skip this question</button></div>';
    } else {
      html += '<div class="seg" role="group" aria-labelledby="q-label">' + s.opts.map(function (o) {
        return '<button type="button" data-v="' + o[0] + '" aria-pressed="' + (ans[s.key] === o[0]) + '">' + o[1] + '</button>';
      }).join('') + '</div>';
    }
    stepBox.innerHTML = html;
    var first = $('button, input', stepBox); if (first && i > 0) first.focus();
    $$('[data-v]', stepBox).forEach(function (b) {
      b.addEventListener('click', function () { ans[s.key] = b.getAttribute('data-v'); next(); });
    });
    var nx = $('#q-next');
    if (nx) {
      nx.addEventListener('click', function () { ans.bill = $('#q-bill').value; finish(); });
      $('#q-skip').addEventListener('click', function () { ans.bill = ''; finish(); });
      $('#q-bill').addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); nx.click(); } });
    }
  }
  function next() { i++; if (i >= steps.length) { finish(); return; } draw(); }
  var done = false;
  back.addEventListener('click', function () { if (done) { done = false; $('#lead-form').hidden = true; var w = $('#lead-why'); if (w) w.hidden = false; draw(); return; } if (i > 0) { i--; draw(); } });

  function finish() {
    done = true;
    bar.style.width = '100%';
    count.textContent = 'Your match is ready';
    back.hidden = false;
    var c = carriers && carriers.countries[ans.country];
    var lines = parseInt(ans.lines, 10) || 1;
    var labels = {
      price: 'a budget sub-brand or MVNO that rides a major network',
      coverage: 'the strongest network in your area, or its own budget sub-brand',
      travel: 'a plan with roaming built in, or a cheap home plan plus travel eSIMs',
      '5g': 'the network with the widest mid-band 5G where you live',
      premium: 'a network-owned unlimited plan with priority data and perks'
    };
    var archetype = labels[ans.priority] || labels.price;
    var html = '<div class="reco"><h2>Your best-fit plan type</h2><p>For ' + lines + (lines === 1 ? ' line' : ' lines') + ' using ' +
      ({ light: 'under 5 GB', medium: '5–20 GB', heavy: '20–50 GB', unlimited: '50 GB+' }[ans.data] || 'moderate data') + ' each, go with <strong>' + archetype + '</strong>.</p>';
    var est = null;
    if (c) {
      var band = ans.priority === 'premium' ? c.bands.premium : c.bands[ans.data || 'medium'];
      var per = (band[0] + band[1]) / 2;
      var mult = lines === 1 ? 1 : lines === 2 ? .9 : lines <= 4 ? .8 : .75;
      est = per * lines * mult;
      html += '<p>Typical cost for this setup in ' + c.name + ': <strong>' + MD.money(band[0] * lines * mult, c.currency) + '–' + MD.money(band[1] * lines * mult, c.currency) + ' a month</strong> in total.</p>';
      var bill = parseFloat(ans.bill);
      if (bill > 0) {
        var save = (bill - est) * 12;
        html += save > 0 ? '<p class="big-out">' + MD.money(save, c.currency) + '</p><p>Estimated saving a year versus your current ' + MD.money(bill, c.currency) + ' a month.</p>'
          : '<p>Your current bill is already at or below the typical range. Switching only makes sense for better coverage or perks.</p>';
      }
      var pick = c.carriers.filter(function (x) { return x.bestFor.indexOf(ans.priority) > -1; });
      if (pick.length < 3) pick = pick.concat(c.carriers.filter(function (x) { return pick.indexOf(x) < 0; })).slice(0, 4);
      html += '<p><strong>Compare these first:</strong></p><ul class="carrier-pills">' + pick.slice(0, 5).map(function (x) {
        return '<li><a href="' + x.url + '" rel="nofollow noopener" target="_blank">' + MD.esc(x.name) + '</a></li>';
      }).join('') + '</ul><p class="small">' + pick.slice(0, 5).map(function (x) { return MD.esc(x.name) + ': ' + x.type + (x.type !== 'Network' ? ' on ' + MD.esc(x.network) : ''); }).join('; ') + '.</p>';
    } else {
      html += '<p>Compare the local operators against travel eSIM plans. Our eSIM planner and band checker show what works where you are.</p>';
    }
    var phoneTip = {
      byod: 'Keeping your phone keeps the bill lowest. Check it is unlocked and supports local bands before you switch.',
      flagship: 'Compare carrier financing against buying unlocked with the total cost calculator; promotions often lock you in for 24–36 months.',
      refurb: 'A refurbished phone graded Excellent typically saves 30–50%. Ask for battery health of 85% or more.',
      help: 'The phone finder ranks current models by what you care about.'
    }[ans.phone];
    if (ans.phone === 'budget' && phones) {
      var cheap = phones.filter(function (p) { return p.price <= 400; }).sort(function (a, b) { return a.price - b.price; }).slice(0, 3);
      phoneTip = 'Good-value picks under $400: ' + cheap.map(function (p) { return (p.model.indexOf(p.brand) === 0 ? p.model : p.brand + ' ' + p.model) + ' (' + MD.money(p.price) + ')'; }).join(', ') + '.';
    }
    if (phoneTip) html += '<p><strong>Phone:</strong> ' + MD.esc(phoneTip) + '</p>';
    html += '</div>';
    stepBox.innerHTML = html;
    var form = $('#lead-form');
    form.hidden = false;
    var why = $('#lead-why'); if (why) why.hidden = true;
    $('#lead-summary').value = 'Country ' + ans.country + '; lines ' + lines + '; data ' + ans.data + '; priority ' + ans.priority + '; phone ' + ans.phone + '; current bill ' + (ans.bill || 'n/a') + (est ? '; est. new total ' + Math.round(est) : '');
    $('#lead-form h2').focus();
  }
  draw();
})();
