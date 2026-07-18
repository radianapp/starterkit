from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.dashboard.models import SystemUpdate


class SystemUpdateListView(LoginRequiredMixin, ListView):
    """
    View untuk menampilkan daftar log pembaruan sistem (Changelog / Deploy Log).

    TUJUAN: Memberikan transparansi kepada pengguna tentang pembaruan yang telah diterapkan.
    TEMPLATE: dashboard/changelog.html
    URL NAME: dashboard:changelog
    DIPANGGIL DARI: /changelog/
    """

    model = SystemUpdate
    template_name = "dashboard/changelog.html"
    context_object_name = "updates"
    paginate_by = 10
