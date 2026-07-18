function toggleEmbed(el) {
  var panel = el.querySelector('.embed-panel');
  if (!panel) return;
  var isOpen = panel.classList.contains('open');
  document.querySelectorAll('.embed-panel.open').forEach(function (p) {
    p.classList.remove('open');
  });
  if (!isOpen) panel.classList.add('open');
}
