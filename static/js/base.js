/* US-010: Base layout utilities — CSRF token setup untuk HTMX */
/* TUJUAN: Setup CSRF token di HTMX request headers secara otomatis */
/*
ALUR:
  1. Wait untuk htmx:configRequest event
  2. Extract CSRF token dari meta tag
  3. Add ke request headers sebelum dikirim
  4. Ini berlaku otomatis untuk semua HTMX requests
*/

document.addEventListener('htmx:configRequest', function(event) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]');
  if (csrfToken) {
    event.detail.headers['X-CSRFToken'] = csrfToken.content;
  }
});

// Izinkan HTMX swap response 422 (form validation errors)
// Tanpa ini, HTMX buang response 4xx dan user tidak melihat error
document.addEventListener('htmx:beforeSwap', function(event) {
  if (event.detail.xhr.status === 422) {
    event.detail.shouldSwap = true;
    event.detail.isError = false;
  }
});

// --- 1. NPROGRESS & ERROR HANDLING ---
document.addEventListener('htmx:beforeRequest', function(e) {
  if(typeof NProgress !== 'undefined') NProgress.start();
});

document.addEventListener('htmx:afterRequest', function(e) {
  if(typeof NProgress !== 'undefined') NProgress.done();
});

// Handle HTTP Errors gracefully
document.addEventListener('htmx:responseError', function(e) {
  const status = e.detail.xhr.status;
  if (status >= 500) {
    Swal.fire({
      icon: 'error',
      title: 'Server Error',
      text: 'Terjadi kesalahan pada server. Silakan coba lagi.'
    });
  }
});

document.addEventListener('htmx:sendError', function(e) {
  Swal.fire({
    icon: 'error',
    title: 'Koneksi Terputus',
    text: 'Gagal menghubungi server. Periksa koneksi internet Anda.'
  });
});

// --- 2. OFFLINE DETECTION ---
window.addEventListener('offline', function() {
  if (typeof rdpShowToast === 'function') {
    rdpShowToast('error', 'Koneksi internet terputus. Aplikasi mungkin tidak berfungsi dengan baik.');
  } else {
    Swal.fire({ icon: 'warning', title: 'Offline', text: 'Koneksi internet terputus.', toast: true, position: 'top-end', showConfirmButton: false, timer: 3000 });
  }
});
window.addEventListener('online', function() {
  if (typeof rdpShowToast === 'function') {
    rdpShowToast('success', 'Kembali online!');
  }
});

// --- 3. HTMX CUSTOM CONFIRM INTERCEPTOR ---
document.addEventListener('htmx:confirm', function(e) {
  e.preventDefault(); // Stop standard confirm
  
  // Jika elemen tidak memiliki teks konfirmasi, langsung jalankan request
  const confirmMsg = e.detail.question;
  if (!confirmMsg) {
    e.detail.issueRequest(true);
    return;
  }

  // Tampilkan SweetAlert2
  Swal.fire({
    title: 'Konfirmasi',
    text: confirmMsg,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: 'var(--pico-primary)',
    cancelButtonColor: 'var(--pico-secondary)',
    confirmButtonText: 'Ya, lanjutkan!',
    cancelButtonText: 'Batal'
  }).then((result) => {
    if (result.isConfirmed) {
      e.detail.issueRequest(true);
    }
  });
});
