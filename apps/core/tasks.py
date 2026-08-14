from celery import shared_task


@shared_task
def example_long_running_task(iterations: int = 100):
    """
    Contoh background task sederhana menggunakan Celery.
    Fungsi ini mensimulasikan tugas berat yang memakan waktu.

    TUJUAN: Memberikan referensi bagi developer baru tentang cara membuat Celery task.
    """
    import time

    total = 0
    for i in range(iterations):
        time.sleep(0.01)
        total += i

    return f"Task selesai. Total: {total}"
