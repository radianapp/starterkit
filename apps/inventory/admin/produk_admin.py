# apps/inventory/admin/produk_admin.py
# US-CRUD-01: Admin untuk Produk, Kategori, Pemasok

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from apps.inventory.models import Kategori, Pemasok, Produk


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ["nama"]
    search_fields = ["nama"]


@admin.register(Pemasok)
class PemasokAdmin(admin.ModelAdmin):
    list_display = ["nama"]
    search_fields = ["nama"]


@admin.register(Produk)
class ProdukAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ["nama", "sku", "kategori", "harga", "stok", "status", "updated_at"]
    list_filter = ["status", "kategori"]
    search_fields = ["nama", "sku"]
    list_select_related = ["kategori", "pemasok"]
