# apps/inventory/urls.py
# US-CRUD-01: URL routing CRUD Produk

from django.urls import path

from apps.inventory.views import (
    DetailPanelView,
    EditModalView,
    EditProdukView,
    HapusKonfirmasiView,
    HapusProdukView,
    ProdukListView,
    TabelProdukView,
    TambahModalView,
    TambahProdukView,
)

# KEPUTUSAN TEKNIS: app_name='produk' agar template {% url 'produk:...' %} jalan
# ALASAN: Template sudah pakai namespace 'produk'; inventory adalah nama internal app
app_name = "produk"

urlpatterns = [
    path("produk/", ProdukListView.as_view(), name="produk-list"),
    # Full page
    path("", ProdukListView.as_view(), name="list"),
    # HTMX partials — table
    path("tabel/", TabelProdukView.as_view(), name="tabel"),
    # HTMX partials — detail panel
    path("<int:pk>/detail/", DetailPanelView.as_view(), name="detail_panel"),
    # HTMX partials — modal tambah
    path("tambah/modal/", TambahModalView.as_view(), name="tambah_modal"),
    path("tambah/", TambahProdukView.as_view(), name="tambah"),
    # HTMX partials — modal edit
    path("<int:pk>/edit/modal/", EditModalView.as_view(), name="edit_modal"),
    path("<int:pk>/edit/", EditProdukView.as_view(), name="edit"),
    # HTMX partials — konfirmasi hapus
    path("<int:pk>/hapus/konfirmasi/", HapusKonfirmasiView.as_view(), name="hapus_konfirmasi"),
    path("<int:pk>/hapus/", HapusProdukView.as_view(), name="hapus"),
]
