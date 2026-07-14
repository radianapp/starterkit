/* ==========================================================================
   Persistent Theme & Accent Helper (US-028, Extras)
   ========================================================================== */

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

