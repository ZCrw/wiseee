// Menú lateral (en móvil se abre/cierra; en escritorio se oculta/muestra)
document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("toggle-nav");
  if (!btn) return;
  btn.addEventListener("click", function () {
    var mobile = window.matchMedia("(max-width: 900px)").matches;
    document.body.classList.toggle(mobile ? "nav-open" : "nav-hidden");
  });
});
