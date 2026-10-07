// Tracking compartido por todas las páginas: única fuente de verdad.
// 1. Pega tu ID de Google Tag Manager en GTM_ID para activar el contenedor.
// 2. Los clics de contacto se envían a dataLayer como evento "contact_click"
//    con contact_method = whatsapp | email | linkedin, listos para usar en GTM/GA4.
(function () {
  var GTM_ID = 'GTM-N9XLDFCS';

  window.dataLayer = window.dataLayer || [];

  if (GTM_ID) {
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
    document.head.appendChild(s);
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    var method =
      href.indexOf('wa.me/') !== -1 ? 'whatsapp' :
      href.indexOf('mailto:') === 0 ? 'email' :
      href.indexOf('linkedin.com') !== -1 ? 'linkedin' : null;
    if (method) {
      window.dataLayer.push({ event: 'contact_click', contact_method: method, page_path: location.pathname });
    }
  });
})();
