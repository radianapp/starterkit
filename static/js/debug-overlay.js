/* AlpineJS component for Layout Debug Overlay */
function debugState(layoutName) {
  return {
    open: false,
    layout: layoutName || 'unknown',
    breakpoint: 'Desktop',
    width: window.innerWidth,
    darkMode: false,

    init() {
      // Monitor dark mode state from layoutState
      this.updateDarkMode();
      
      // Watch for manual changes via click or storage
      window.addEventListener('storage', () => this.updateDarkMode());
      
      // Polling or intercepting local toggle
      setInterval(() => {
        this.updateDarkMode();
      }, 500);

      // Listen resize
      this.updateBreakpoint();
      window.addEventListener('resize', () => {
        this.width = window.innerWidth;
        this.updateBreakpoint();
      });
    },

    updateDarkMode() {
      this.darkMode = document.documentElement.getAttribute('data-theme') === 'dark';
    },

    updateBreakpoint() {
      const w = window.innerWidth;
      if (w < 480) {
        this.breakpoint = 'Mobile (Small)';
      } else if (w < 768) {
        this.breakpoint = 'Mobile';
      } else if (w <= 1024) {
        this.breakpoint = 'Tablet';
      } else {
        this.breakpoint = 'Desktop';
      }
    }
  };
}
