import logging
from celery import shared_task
from django.conf import settings

from apps.accounts.services.user_service import process_bulk_users

logger = logging.getLogger(__name__)

@shared_task
def process_bulk_users_task(rows: list, request_info: dict = None):
    """
    TUJUAN: Proses bulk user secara background dengan Celery jika data besar.
    """
    logger.info(f"Mulai memproses bulk user sebanyak {len(rows)} baris.")
    
    # request_info bisa berisi base_url atau parameter lain jika dibutuhkan
    # tapi karena send_verification_email sudah support fallback request=None,
    # kita biarkan None di sini, atau kita mock sedikit behavior-nya.
    
    results = process_bulk_users(rows, request=None)
    
    logger.info(f"Selesai proses bulk user. Sukses: {results['success']}, Gagal: {results['failed']}")
    
    # Notifikasi ke superadmin (bisa lewat email atau web socket)
    # Untuk sementara, cukup log saja atau kirim notifikasi dasar jika diimplementasikan.
    return results
