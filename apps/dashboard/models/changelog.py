from django.db import models


class SystemUpdate(models.Model):
    """
    Model untuk menyimpan log pembaruan sistem (Changelog / Deploy Log).

    TUJUAN: Mencatat setiap perubahan signifikan pada halaman atau fungsi core,
            sehingga pengguna dapat melihat riwayat pembaruan melalui halaman Changelog.

    DIKELOLA OLEH: Admin via Django Admin Panel (Jazzmin).
    DIPANGGIL DARI: apps/dashboard/views/changelog.py (SystemUpdateListView)
    """

    UPDATE_TYPES = [
        ("core", "Core Update"),
        ("page", "Page Update"),
        ("bugfix", "Bugfix"),
        ("feature", "New Feature"),
    ]

    version = models.CharField(max_length=50, help_text="Contoh: v1.1.0")
    title = models.CharField(max_length=255)
    description = models.TextField()
    update_type = models.CharField(max_length=20, choices=UPDATE_TYPES, default="feature")
    release_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-release_date"]
        verbose_name = "System Update"
        verbose_name_plural = "System Updates"

    def __str__(self):
        return f"{self.version} - {self.title}"
