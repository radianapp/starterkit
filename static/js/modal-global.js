/* ==========================================================================
   Global Modal Handler (US-028)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('global-modal');
    const contentContainer = document.getElementById('global-modal-content');

    if (!modal || !contentContainer) return;

    // Close modal when clicking outside (backdrop click)
    modal.addEventListener('click', (event) => {
        const rect = modal.getBoundingClientRect();
        const isInDialog = (
            rect.top <= event.clientY && event.clientY <= rect.top + rect.height &&
            rect.left <= event.clientX && event.clientX <= rect.left + rect.width
        );
        if (!isInDialog) {
            modal.close();
        }
    });

    // Listen for HTMX openModal event
    document.body.addEventListener('openModal', (e) => {
        if (e.detail && e.detail.url) {
            // Load content via HTMX ajax
            if (typeof htmx !== 'undefined') {
                htmx.ajax('GET', e.detail.url, {
                    target: '#global-modal-content',
                    swap: 'innerHTML'
                }).then(() => {
                    modal.showModal();
                });
            } else {
                // Fallback without HTMX
                fetch(e.detail.url)
                    .then(response => response.text())
                    .then(html => {
                        contentContainer.innerHTML = html;
                        modal.showModal();
                    });
            }
        }
    });

    // Support close event triggered via standard HTMX event if needed
    document.body.addEventListener('closeModal', () => {
        modal.close();
    });
});
