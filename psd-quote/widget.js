/**
 * PSD Quote Widget — embeddable floating "Get a Quote" launcher.
 * Drop onto any page:
 *   <script src="https://psdepot.com/quote/widget.js" data-api="https://psdepot.com/quote"></script>
 * Opens the external quote widget in a modal (or links to the full page if no API).
 */
(function () {
  var s = document.currentScript;
  var api = (s && s.getAttribute('data-api')) || '';

  var btn = document.createElement('button');
  btn.textContent = 'Get a Quote';
  btn.setAttribute('aria-label', 'Get a free POS quote');
  btn.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:99999;background:#1a56db;color:#fff;' +
    'border:none;border-radius:24px;padding:13px 20px;font-size:15px;font-weight:600;cursor:pointer;' +
    'box-shadow:0 4px 16px rgba(0,0,0,.25);font-family:-apple-system,Segoe UI,Roboto,sans-serif;';
  btn.addEventListener('click', function () {
    if (api) {
      var f = document.createElement('iframe');
      f.src = api + '/widget';
      f.style.cssText = 'position:fixed;top:0;right:0;bottom:0;width:420px;max-width:100vw;height:100%;' +
        'border:none;z-index:100000;background:#fff;box-shadow:-4px 0 20px rgba(0,0,0,.2);';
      f.id = 'psd-quote-frame';
      var close = document.createElement('button');
      close.textContent = '✕';
      close.style.cssText = 'position:fixed;top:10px;right:10px;z-index:100001;background:#fff;border:1px solid #ddd;' +
        'border-radius:50%;width:32px;height:32px;cursor:pointer;font-size:15px;';
      close.onclick = function () { f.remove(); close.remove(); };
      document.body.appendChild(f);
      document.body.appendChild(close);
    } else {
      window.location.href = '/widget';
    }
  });
  document.body.appendChild(btn);
})();
