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
