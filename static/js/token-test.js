/**
 * switchTheme — Ganti tema aktif di token test page.
 * @param {string} id — ID tema dari daftar THEMES
 */
function switchTheme(id) {
    var darkThemes = ['dark', 'midnight', 'terminal', 'nord', 'dracula'];
    var isDark = darkThemes.indexOf(id) >= 0;

    // Update <html> attributes
    document.documentElement.setAttribute('data-rdp-theme', id);
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');

    // Persist
    try { localStorage.setItem('rdp-rdp-theme', id); } catch(e) {}

    // Tidak perlu swap CSS link — semua tema sudah di-load bersamaan di <head>
    // agar Theme Gallery dapat menampilkan setiap card dengan warna yang benar.

    // Update label
    var label = document.getElementById('tt-active-theme-label');
    if (label) label.textContent = id;

    // Update card highlights
    document.querySelectorAll('.tt-theme-card').forEach(function(card) {
        card.classList.toggle('active-theme', card.dataset.themeId === id);
    });

    // Update nav buttons
    document.querySelectorAll('[id^="nav-"]').forEach(function(btn) {
        var btnId = btn.id.replace('nav-', '');
        btn.style.color = btnId === id ? 'var(--rdp-primary)' : '';
        btn.style.fontWeight = btnId === id ? '700' : '';
    });
}

/**
 * updateHeaderHeight — Ukur tinggi header dan set CSS variable --tt-header-h.
 * Dijalankan saat load dan resize agar sidebar sticky selalu di posisi yang benar.
 */
function updateHeaderHeight() {
    var header = document.querySelector('.tt-header');
    if (header) {
        document.documentElement.style.setProperty('--tt-header-h', header.offsetHeight + 'px');
    }
}

// Init — highlight current theme card on load
document.addEventListener('DOMContentLoaded', function() {
    updateHeaderHeight();
    var current = document.documentElement.getAttribute('data-rdp-theme') || 'default';
    switchTheme(current);
});

// Update header height saat resize window
window.addEventListener('resize', updateHeaderHeight);

window.switchTheme = switchTheme;
