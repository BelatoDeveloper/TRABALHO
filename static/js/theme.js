(function() {
  const currentTheme = localStorage.getItem('beatbooks_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme);

  document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (!toggleBtn) return;

    function updateIcon(theme) {
      toggleBtn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
      toggleBtn.setAttribute('title', theme === 'dark' ? 'Mudar para Modo Claro' : 'Mudar para Modo Escuro');
    }

    updateIcon(document.documentElement.getAttribute('data-theme') || 'dark');

    toggleBtn.addEventListener('click', function() {
      const activeTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', activeTheme);
      localStorage.setItem('beatbooks_theme', activeTheme);
      updateIcon(activeTheme);
    });
  });
})();

