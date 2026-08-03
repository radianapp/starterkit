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
  /* Restore state dari localStorage secara sinkron untuk menghindari flicker/glitch UI */
  const savedSidebar = localStorage.getItem('sidebarOpen');
  const initialSidebarOpen = savedSidebar !== null ? JSON.parse(savedSidebar) : window.innerWidth >= 768;

  const savedCollapsed = localStorage.getItem('sidebarCollapsed');
  const initialSidebarCollapsed = savedCollapsed !== null ? JSON.parse(savedCollapsed) : false;

  return {
    sidebarOpen: initialSidebarOpen,
    sidebarCollapsed: initialSidebarCollapsed,
    darkMode: false,

    init() {

      /* Watch state changes untuk disimpan ke localStorage */
      this.$watch('sidebarOpen', (value) => {
        localStorage.setItem('sidebarOpen', JSON.stringify(value));
      });
      this.$watch('sidebarCollapsed', (value) => {
        localStorage.setItem('sidebarCollapsed', JSON.stringify(value));
      });

      /* Sync darkMode dari DOM attribute (yang sudah diset oleh script inline base.html/theme.js) */
      this.darkMode = document.documentElement.getAttribute('data-theme') === 'dark';
      
      /* Listen event rdp-theme-changed dari theme.js untuk meng-update state secara reaktif */
      window.addEventListener('rdp-theme-changed', (e) => {
          const darkThemes = ['dark','midnight','terminal','nord','dracula'];
          this.darkMode = darkThemes.includes(e.detail.theme);
      });

      /* Listen untuk resize events — auto open sidebar saat desktop, jangan force close di mobile */
      window.addEventListener('resize', () => {
        if (window.innerWidth >= 768 && !this.sidebarOpen) {
          this.sidebarOpen = true;
        }
      });
    },

    closeSidebar() {
      /* Close sidebar hanya di mobile (window < 768px) */
      if (window.innerWidth < 768) {
        this.sidebarOpen = false;
      }
    },


  };
}

