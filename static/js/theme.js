/* ==========================================================================
   Persistent Theme & Accent Helper (US-028, Extras)
   ========================================================================== */

// RDP-UI theme switcher — dipakai oleh navbar theme picker dropdown
window.setRdpTheme = function(theme) {
    var darkThemes = ['dark', 'midnight', 'terminal', 'nord', 'dracula'];
    document.documentElement.setAttribute('data-rdp-theme', theme);
    document.documentElement.setAttribute('data-theme', darkThemes.indexOf(theme) >= 0 ? 'dark' : 'light');
    localStorage.setItem('rdp-rdp-theme', theme);
    // Swap theme CSS
    var link = document.getElementById('rdp-theme-css');
    if (link) {
        var base = link.href.replace(/[^/]+\.css$/, '');
        link.href = base + theme + '.css';
    }
    window.dispatchEvent(new CustomEvent('rdp-theme-changed', { detail: { theme: theme } }));
};

// Dark mode toggle — dipakai navbar user dropdown
window.toggleRdpDarkMode = function() {
    var current = document.documentElement.getAttribute('data-rdp-theme') || 'default';
    var darkThemes = ['dark', 'midnight', 'terminal', 'nord', 'dracula'];
    var isDark = darkThemes.indexOf(current) >= 0;
    window.setRdpTheme(isDark ? 'default' : 'dark');
};

(function() {
    window.ThemeHelper = {
        getTheme() {
            return localStorage.getItem('rdp-theme') || 'light';
        },
        setTheme(theme) {
            localStorage.setItem('rdp-theme', theme);
            document.documentElement.setAttribute('data-theme', theme);
            // Dispatch event for reactive components (like theme picker)
            window.dispatchEvent(new CustomEvent('rdp-theme-changed', { detail: { theme } }));
        },
        toggle() {
            const current = this.getTheme();
            const next = current === 'dark' ? 'light' : 'dark';
            this.setTheme(next);
            return next;
        },
        getAccent() {
            return localStorage.getItem('rdp-accent') || document.documentElement.getAttribute('data-accent') || 'navy';
        },
        setAccent(accent) {
            localStorage.setItem('rdp-accent', accent);
            document.documentElement.setAttribute('data-accent', accent);
            window.dispatchEvent(new CustomEvent('rdp-accent-changed', { detail: { accent } }));
        }
    };
})();

