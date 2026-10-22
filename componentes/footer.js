// Footer compartido por todas las páginas: única fuente de verdad.
// Se inyecta en el punto exacto donde está el <script> (sin defer/async).
// Bilingüe: usa <html lang="en"> para decidir qué versión mostrar.
// Dos filas: primaria (marca + navegación + LinkedIn + idioma) y
// secundaria (copyright + enlaces legales).
// Estilos en estilos/base.css (.site-footer).
(function () {
  var year = new Date().getFullYear();
  var isEN = document.documentElement.lang === 'en';

  var html = isEN
    ? (
      '<footer class="site-footer">' +
        '<div class="footer-primary">' +
          '<a href="/en/" class="footer-logo">Jhony Escobar</a>' +
          '<div class="footer-links">' +
            '<a href="/servicios/">Services</a>' +
            '<a href="/en/portfolio/">Portfolio</a>' +
            '<a href="/en/portfolio/dream-resort-hotels/">Dream Resort Hotels case</a>' +
            '<a href="/en/portfolio/control-piscinas/">Control Piscinas case</a>' +
            '<a href="/en/#faq">FAQ</a>' +
            '<a href="/en/#contacto">Contact</a>' +
            '<a href="https://www.linkedin.com/in/jaescobarc" target="_blank" rel="noopener">LinkedIn</a>' +
            '<a href="/" class="lang-switch">ES</a>' +
          '</div>' +
        '</div>' +
        '<div class="footer-secondary">' +
          '<span class="footer-copy">© ' + year + ' · Data Analytics &amp; Business Automation · Granada, Spain · jhonyescobar.com</span>' +
          '<div class="footer-legal">' +
            '<a href="/en/legal-notice/">Legal Notice</a>' +
            '<a href="/en/privacy-policy/">Privacy Policy</a>' +
          '</div>' +
        '</div>' +
      '</footer>'
    )
    : (
      '<footer class="site-footer">' +
        '<div class="footer-primary">' +
          '<a href="/" class="footer-logo">Jhony Escobar</a>' +
          '<div class="footer-links">' +
            '<a href="/servicios/">Servicios</a>' +
            '<a href="/portfolio/">Portfolio</a>' +
            '<a href="/portfolio/dream-resort-hotels/">Caso Dream Resort Hotels</a>' +
            '<a href="/portfolio/control-piscinas/">Caso Control Piscinas</a>' +
            '<a href="/#faq">Preguntas frecuentes</a>' +
            '<a href="/#contacto">Contacto</a>' +
            '<a href="https://www.linkedin.com/in/jaescobarc" target="_blank" rel="noopener">LinkedIn</a>' +
            '<a href="/en/" class="lang-switch">EN</a>' +
          '</div>' +
        '</div>' +
        '<div class="footer-secondary">' +
          '<span class="footer-copy">© ' + year + ' · Data Analytics &amp; Business Automation · Granada · jhonyescobar.com</span>' +
          '<div class="footer-legal">' +
            '<a href="/aviso-legal/">Aviso Legal</a>' +
            '<a href="/privacidad/">Privacidad</a>' +
          '</div>' +
        '</div>' +
      '</footer>'
    );

  document.write(html);
})();
