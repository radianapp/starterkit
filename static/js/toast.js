/* ==========================================================================
   Toast Notification Handler (US-028)
   ========================================================================== */

function showGlobalToast(message, type = 'info', position = '') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    // Reset dan tambahkan class posisi jika diberikan
    container.className = 'rdp-toast-container';
    if (position) {
        container.classList.add(`toast-${position}`);
    }

    const toast = document.createElement('div');
    toast.className = `rdp-toast rdp-toast--${type}`;
    
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';

    toast.innerHTML = `
        <span class="rdp-toast__icon">${icon}</span>
        <span class="rdp-toast__message">${message}</span>
        <button class="rdp-toast__close" aria-label="Tutup">&times;</button>
    `;

    toast.querySelector('.rdp-toast__close').addEventListener('click', () => {
        toast.remove();
    });

    container.appendChild(toast);

    // Auto dismiss after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 3700);
}

// Bind event listener for HTMX showToast trigger
document.body.addEventListener('showToast', (e) => {
    if (e.detail) {
        const message = e.detail.message || e.detail;
        const type = e.detail.type || 'info';
        const position = e.detail.position || '';
        showGlobalToast(message, type, position);
    }
});
