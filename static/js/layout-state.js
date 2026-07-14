/* US-010: Alpine.js layout state — Sidebar toggle management */
/* TUJUAN: Manage sidebar open/close state dengan localStorage persistence */
/*
ALUR:
  1. Initialize sidebarOpen berdasarkan window width (desktop=true, mobile=false)
  2. Restore state dari localStorage jika ada
  3. Listen untuk window resize events
  4. Persist state ke localStorage saat berubah
  5. Close sidebar saat user click outside di mobile

DIPANGGIL DARI: templates/cotton/layouts/base.html via x-data="layoutState()"
DEPENDENSI: Alpine.js 3.x
*/

function layoutState() {
  return {
    sidebarOpen: window.innerWidth >= 768,
    sidebarCollapsed: false,
    darkMode: false,

    init() {
      /* Restore sidebar state dari localStorage */
      const savedSidebar = localStorage.getItem('sidebarOpen');
      if (savedSidebar !== null) {
        this.sidebarOpen = JSON.parse(savedSidebar);
      }

      /* Restore dark mode dari localStorage — default light */
      const savedTheme = localStorage.getItem('rdp-theme');
      this.darkMode = savedTheme === 'dark';
      this.applyTheme();

      /* Listen untuk resize events — auto open sidebar saat desktop, jangan force close di mobile */
      window.addEventListener('resize', () => {
        if (window.innerWidth >= 768 && !this.sidebarOpen) {
          this.sidebarOpen = true;
        }
      });
    },

    watch_sidebarOpen(value) {
      /* Persist state ke localStorage */
      localStorage.setItem('sidebarOpen', JSON.stringify(value));
    },

    closeSidebar() {
      /* Close sidebar hanya di mobile (window < 768px) */
      if (window.innerWidth < 768) {
        this.sidebarOpen = false;
      }
    },

    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      localStorage.setItem('rdp-theme', this.darkMode ? 'dark' : 'light');
      this.applyTheme();
    },

    applyTheme() {
      /* Update pico theme attribute */
      document.documentElement.setAttribute('data-theme', this.darkMode ? 'dark' : 'light');
      
      /* Update RDP specific theme attribute and CSS */
      let currentRdpTheme = document.documentElement.getAttribute('data-rdp-theme') || 'default';
      const darkThemes = ['dark','midnight','terminal','nord','dracula'];
      
      if (this.darkMode && !darkThemes.includes(currentRdpTheme)) {
        currentRdpTheme = 'dark';
      } else if (!this.darkMode && darkThemes.includes(currentRdpTheme)) {
        currentRdpTheme = 'default';
      }
      
      document.documentElement.setAttribute('data-rdp-theme', currentRdpTheme);
      localStorage.setItem('rdp-rdp-theme', currentRdpTheme);
      
      const themeLink = document.getElementById('rdp-theme-css');
      if (themeLink) {
        const currentHref = themeLink.getAttribute('href');
        const newHref = currentHref.replace(/\/[^\/]+\.css$/, '/' + currentRdpTheme + '.css');
        themeLink.setAttribute('href', newHref);
      }
    }
  };
}

