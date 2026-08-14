import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def sync_stock():
    """Tugas background Celery untuk sync_stock."""
    try:
        logger.info("Memulai task sync_stock")
        # Implementasi task di sini
        pass
    except Exception as e:
        logger.error(f"Error di task sync_stock: {e}")
        raise
