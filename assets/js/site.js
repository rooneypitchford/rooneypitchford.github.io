function toggleEmbed(el) {
  const panel = el.querySelector('.embed-panel');
  if (!panel) return;
  const isOpen = panel.classList.contains('open');
  document.querySelectorAll('.embed-panel.open').forEach(p => p.classList.remove('open'));
  if (!isOpen) panel.classList.add('open');
}
