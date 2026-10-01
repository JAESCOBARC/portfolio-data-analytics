// Footer compartido por todas las páginas: única fuente de verdad.
// Se inyecta en el punto exacto donde está el <script> (sin defer/async).
// Estilos en estilos/base.css (.site-footer).
(function () {
  var year = new Date().getFullYear();
  document.write(
    '<footer class="site-footer">' +
      '<div class="footer-inner">' +
        '<a href="/" class="footer-logo">Jhony Escobar</a>' +
        '<div class="footer-links">' +
          '<a href="/#servicios">Servicios</a>' +
          '<a href="/portfolio/">Portfolio</a>' +
          '<a href="/portfolio/dream-resort-hotels/">Caso Dream Resort Hotels</a>' +
          '<a href="/portfolio/control-piscinas/">Caso Control Piscinas</a>' +
          '<a href="/#faq">Preguntas frecuentes</a>' +
          '<a href="/#contacto">Contacto</a>' +
        '</div>' +
        '<span class="footer-copy">© ' + year + ' · Data Analytics &amp; Business Automation · Granada</span>' +
      '</div>' +
    '</footer>'
  );
})();
