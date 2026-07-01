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

    init() {
      /* Restore sidebar state dari localStorage */
      const saved = localStorage.getItem('sidebarOpen');
      if (saved !== null) {
        this.sidebarOpen = JSON.parse(saved);
      }

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
    }
  };
}
