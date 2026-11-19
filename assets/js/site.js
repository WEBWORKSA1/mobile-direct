/* Mobile.Direct shared behaviour: theme, nav, forms, donations, ads, notices. */
(function () {
  'use strict';
  var D = document;
  var root = D.documentElement.getAttribute('data-root') || '';
  function $(s, c) { return (c || D).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || D).querySelectorAll(s)); }
  var MD = window.MD = window.MD || {};
  MD.root = root; MD.$ = $; MD.$$ = $$;
  MD.store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  MD.session = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };
  var cache = {};
  MD.json = function (path) {
    if (!cache[path]) {
      cache[path] = fetch(root + path, { cache: 'no-cache' }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      });
    }
    return cache[path];
  };
  MD.money = function (n, cur) {
    try { return new Intl.NumberFormat(undefined, { style: 'currency', currency: cur || 'USD', maximumFractionDigits: 0 }).format(n); }
    catch (e) { return '$' + Math.round(n); }
  };
  MD.esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  };
  MD.bars = function (n, weak) {
    n = Math.max(0, Math.min(4, Math.round(n)));
    return '<span class="bars b' + n + (weak ? ' weak' : '') + '" aria-hidden="true"><i></i><i></i><i></i><i></i></span>';
  };

  /* Private inbox: assembled at runtime, never written in the page. */
  var K = ['=', 'tyb3diZXc', 'W1nQDFhc2', 'bW9jLmxpY'];
  MD.inbox = function () { return atob(K.slice().reverse().join('')).split('').reverse().join(''); };

  /* Theme */
  var themeBtn = $('#theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var cur = D.documentElement.getAttribute('data-theme');
      if (!cur) cur = window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      var next = cur === 'dark' ? 'light' : 'dark';
      D.documentElement.setAttribute('data-theme', next);
      MD.store.set('md-theme', next);
      themeBtn.setAttribute('aria-label', next === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    });
  }

  /* Mobile nav */
  var menuBtn = $('#menu-toggle'), nav = $('#site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    D.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.focus(); }
    });
  }

  /* Forms: every form with data-md-form posts to the private inbox through the form relay. */
  MD.send = function (form, extra) {
    var status = $('.form-status', form);
    if (!status) { status = D.createElement('p'); status.className = 'form-status'; status.setAttribute('role', 'status'); form.appendChild(status); }
    if (!form.checkValidity()) { form.reportValidity(); return Promise.resolve(false); }
    var fd = new FormData(form);
    if (fd.get('_honey')) { status.textContent = 'Thanks, received.'; status.className = 'form-status ok'; return Promise.resolve(true); }
    var data = {};
    fd.forEach(function (v, k) {
      if (k === '_honey') return;
      data[k] = data[k] ? data[k] + ', ' + v : v;
    });
    if (extra) Object.keys(extra).forEach(function (k) { data[k] = extra[k]; });
    data._subject = 'Mobile.Direct: ' + (form.getAttribute('data-md-form') || 'Form') + (data.name ? ' from ' + data.name : '');
    data._template = 'table';
    data._captcha = 'false';
    data['Form'] = form.getAttribute('data-md-form') || 'Form';
    data['Page'] = location.href;
    data['Submitted'] = new Date().toISOString();
    var btn = $('button[type=submit]', form);
    if (btn) btn.disabled = true;
    status.className = 'form-status';
    status.textContent = 'Sending…';
    return fetch('https://formsubmit.co/ajax/' + MD.inbox(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok || String(j.success) === 'false') throw new Error(j.message || 'Not accepted');
        return j;
      });
    }).then(function () {
      status.className = 'form-status ok';
      status.textContent = form.getAttribute('data-success') || 'Thanks, we have it. You will hear back within two business days.';
      form.reset();
      form.dispatchEvent(new CustomEvent('md:sent', { bubbles: true }));
      return true;
    }).catch(function () {
      status.className = 'form-status err';
      status.textContent = 'That did not go through. Check your connection and press the button again.';
      return false;
    }).then(function (ok) { if (btn) btn.disabled = false; return ok; });
  };
  D.addEventListener('submit', function (e) {
    var f = e.target;
    if (f && f.matches && f.matches('form[data-md-form]') && !f.hasAttribute('data-custom-submit')) {
      e.preventDefault();
      MD.send(f);
    }
  });

  /* Donations through PayPal; the recipient is added only when the visitor clicks. */
  $$('[data-donate-form]').forEach(function (form) {
    var amountInput = $('input[name=amount]', form);
    $$('[data-amount]', form).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('[data-amount]', form).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        amountInput.value = b.getAttribute('data-amount');
      });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var amt = parseFloat(amountInput.value);
      if (!(amt >= 1)) { amountInput.focus(); amountInput.setCustomValidity('Enter an amount of 1 or more'); amountInput.reportValidity(); amountInput.setCustomValidity(''); return; }
      var purpose = ($('select[name=purpose]', form) || {}).value || 'General support';
      var url = 'https://www.paypal.com/donate/?business=' + encodeURIComponent(MD.inbox()) +
        '&amount=' + encodeURIComponent(amt.toFixed(2)) + '&currency_code=USD&no_recurring=0' +
        '&item_name=' + encodeURIComponent('Mobile.Direct support: ' + purpose);
      window.open(url, '_blank', 'noopener');
    });
  });

  /* Optional manual ad units (auto ads work without this). */
  if ($('.ad-slot[data-slot]')) {
    MD.json('data/config.json').then(function (cfg) {
      $$('.ad-slot[data-slot]').forEach(function (el) {
        var id = cfg.adSlots && cfg.adSlots[el.getAttribute('data-slot')];
        if (!id) return;
        el.classList.add('on');
        el.innerHTML = '<ins class="adsbygoogle" style="display:block" data-ad-client="' + cfg.adClient + '" data-ad-slot="' + id + '" data-ad-format="auto" data-full-width-responsive="true"></ins>';
        try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
      });
    }).catch(function () {});
  }

  /* Last updated stamp */
  var stamps = $$('[data-last-updated]');
  if (stamps.length) {
    MD.json('data/meta.json').then(function (m) {
      var d = new Date(m.lastUpdated);
      var txt = d.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
      stamps.forEach(function (s) { s.textContent = txt; s.setAttribute('datetime', m.lastUpdated); });
    }).catch(function () {});
  }

  /* Tip of the day (rotates daily) */
  var tips = [
    'Dial *#06# on any phone. If an EID appears, the phone supports eSIM.',
    'Before switching carriers, ask for your port-out or transfer PIN so your number moves with you.',
    'Check the total cost of a contract, including yearly price rises, not just the first month.',
    'Most people use 5–15 GB a month. Unlimited only pays off above roughly 25 GB.',
    'A carrier sub-brand often runs on the same towers as the parent network for half the price.',
    'Turn on Wi-Fi calling to fix weak indoor signal without changing plans.',
    'Remove your account lock (Find My, Google account) before you sell or trade in a phone.',
    'Refurbished phones graded "Excellent" usually look new and cost 30–50% less.',
    'Travel eSIMs are almost always cheaper than a carrier day pass for trips longer than three days.',
    'If your phone was bought on a payment plan, it may stay carrier-locked until it is paid off.',
    'Check signal at home and work with a crowdsourced map, not just the carrier\'s own map.',
    'Family plans get cheaper per line, but only if everyone actually needs the same network.'
  ];
  var tipEl = $$('[data-tip]');
  if (tipEl.length) {
    var start = new Date(new Date().getFullYear(), 0, 0);
    var day = Math.floor((new Date() - start) / 864e5);
    tipEl.forEach(function (t) { t.textContent = tips[day % tips.length]; });
  }
  $$('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); });

  /* Lightweight YouTube embeds: load the player only on click. */
  D.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button[data-yt]');
    if (!b) return;
    var id = b.getAttribute('data-yt'), list = b.getAttribute('data-list');
    var src = list ? 'https://www.youtube-nocookie.com/embed/videoseries?list=' + encodeURIComponent(list) + '&autoplay=1'
                   : 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1';
    var f = D.createElement('iframe');
    f.src = src; f.title = b.getAttribute('aria-label') || 'Video';
    f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen = true;
    b.replaceWith(f);
  });

  /* Cookie notice */
  var cookie = $('#cookie');
  if (cookie && !MD.store.get('md-cookie')) {
    cookie.hidden = false;
    $$('[data-cookie-ok]', cookie).forEach(function (b) {
      b.addEventListener('click', function () { MD.store.set('md-cookie', b.getAttribute('data-cookie-ok')); cookie.hidden = true; });
    });
  }

  /* One-time slide-in that points to the plan match, after real engagement. */
  var slide = $('#slidein');
  if (slide && !D.body.hasAttribute('data-no-slidein') && !MD.session.get('md-slide')) {
    var armed = false, timerDone = false;
    var show = function () {
      if (armed || !timerDone) return;
      var depth = (window.scrollY + window.innerHeight) / D.documentElement.scrollHeight;
      if (depth < 0.45) return;
      armed = true; slide.classList.add('show'); MD.session.set('md-slide', '1');
    };
    setTimeout(function () { timerDone = true; show(); }, 45000);
    window.addEventListener('scroll', show, { passive: true });
    $('.close', slide).addEventListener('click', function () { slide.classList.remove('show'); });
  }

  /* Share */
  $$('[data-share]').forEach(function (b) {
    b.addEventListener('click', function () {
      var data = { title: D.title, url: location.href };
      if (navigator.share) { navigator.share(data).catch(function () {}); return; }
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { b.textContent = 'Link copied'; });
    });
  });

  /* Price-drop / generic dialogs */
  D.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-open-dialog]');
    if (b) {
      var dlg = D.getElementById(b.getAttribute('data-open-dialog'));
      if (!dlg) return;
      var target = $('[name=item]', dlg);
      if (target && b.getAttribute('data-item')) target.value = b.getAttribute('data-item');
      var label = $('[data-item-label]', dlg);
      if (label) label.textContent = b.getAttribute('data-item') || '';
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
      return;
    }
    var c = e.target.closest && e.target.closest('dialog [data-close]');
    if (c) c.closest('dialog').close();
  });
})();
