# apps/inventory/views/produk.py
# US-CRUD-01: Views CRUD Produk — demo dashboard CRUD

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from apps.inventory.forms import ProdukForm
from apps.inventory.models import Kategori, Pemasok, Produk


def _shared_ctx():
    """Konteks dropdown yang dipakai modal tambah dan edit."""
    return {
        "kategori_list": Kategori.objects.all(),
        "pemasok_list": Pemasok.objects.all(),
    }


def _produk_list_qs(request):
    """
    TUJUAN: Bangun queryset produk dengan filter q dan kategori_filter.

    ALUR:
      1. Ambil semua produk dengan select_related
      2. Filter berdasarkan q (nama/SKU) dan kategori_filter
      3. Return queryset + page_obj

    DIPANGGIL DARI: ProdukListView, TabelProdukView
    """
    qs = Produk.objects.select_related("kategori", "pemasok").order_by("-updated_at")

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(nama__icontains=q) | Q(sku__icontains=q))

    kategori_filter = request.GET.get("kategori_filter", "").strip()
    if kategori_filter:
        qs = qs.filter(kategori_id=kategori_filter)

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return qs, page_obj


class ProdukListView(LoginRequiredMixin, View):
    """
    TUJUAN: Halaman list produk (full page).
    US: US-CRUD-01 — CRUD Produk Dashboard
    """

    def get(self, request):
        from django.shortcuts import render

        _, page_obj = _produk_list_qs(request)
        return render(request, "apps/produk/list.html", {
            **_shared_ctx(),
            "produk_list": page_obj.object_list,
            "page_obj": page_obj,
        })


class TabelProdukView(LoginRequiredMixin, View):
    """
    TUJUAN: HTMX partial — swap #produk-table-area saat filter/search berubah.
    US: US-CRUD-01
    """

    def get(self, request):
        from django.shortcuts import render

        _, page_obj = _produk_list_qs(request)
        return render(request, "apps/produk/partials/table_body.html", {
            "produk_list": page_obj.object_list,
            "page_obj": page_obj,
        })


class DetailPanelView(LoginRequiredMixin, View):
    """
    TUJUAN: HTMX partial — isi #detail-panel-container saat baris diklik.
    US: US-CRUD-01
    """

    def get(self, request, pk):
        from django.shortcuts import render

        produk = get_object_or_404(Produk.objects.select_related("kategori", "pemasok"), pk=pk)
        return render(request, "apps/produk/partials/detail_panel.html", {"produk": produk})


class TambahModalView(LoginRequiredMixin, View):
    """
    TUJUAN: HTMX partial — render modal tambah produk.
    US: US-CRUD-01
    """

    def get(self, request):
        from django.shortcuts import render

        return render(request, "apps/produk/partials/modal_tambah.html", {
            "form": ProdukForm(),
            **_shared_ctx(),
        })


class TambahProdukView(LoginRequiredMixin, View):
    """
    TUJUAN: Handle POST tambah produk, return table partial atau modal dengan error.
    US: US-CRUD-01
    """

    def post(self, request):
        from django.shortcuts import render

        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            _, page_obj = _produk_list_qs(request)
            response = render(request, "apps/produk/partials/table_body.html", {
                "produk_list": page_obj.object_list,
                "page_obj": page_obj,
            })
            # KEPUTUSAN TEKNIS: HX-Trigger untuk toast sukses via JS global
            response["HX-Trigger"] = '{"showToast": {"message": "Produk ditambahkan", "type": "success"}}'
            return response

        return render(request, "apps/produk/partials/modal_tambah.html", {
            "form": form,
            **_shared_ctx(),
        }, status=422)


class EditModalView(LoginRequiredMixin, View):
    """
    TUJUAN: HTMX partial — render modal edit produk dengan data pre-fill.
    US: US-CRUD-01
    """

    def get(self, request, pk):
        from django.shortcuts import render

        produk = get_object_or_404(Produk, pk=pk)
        return render(request, "apps/produk/partials/modal_edit.html", {
            "form": ProdukForm(instance=produk),
            "produk": produk,
            **_shared_ctx(),
        })


class EditProdukView(LoginRequiredMixin, View):
    """
    TUJUAN: Handle POST edit produk, return table partial atau modal dengan error.
    US: US-CRUD-01
    """

    def post(self, request, pk):
        from django.shortcuts import render

        produk = get_object_or_404(Produk, pk=pk)
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            _, page_obj = _produk_list_qs(request)
            response = render(request, "apps/produk/partials/table_body.html", {
                "produk_list": page_obj.object_list,
                "page_obj": page_obj,
            })
            response["HX-Trigger"] = '{"showToast": {"message": "Produk diperbarui", "type": "success"}}'
            return response

        return render(request, "apps/produk/partials/modal_edit.html", {
            "form": form,
            "produk": produk,
            **_shared_ctx(),
        }, status=422)


class HapusKonfirmasiView(LoginRequiredMixin, View):
    """
    TUJUAN: HTMX partial — render dialog konfirmasi hapus.
    US: US-CRUD-01
    """

    def get(self, request, pk):
        from django.shortcuts import render

        produk = get_object_or_404(Produk.objects.select_related("kategori"), pk=pk)
        return render(request, "apps/produk/partials/confirm_hapus.html", {"produk": produk})


class HapusProdukView(LoginRequiredMixin, View):
    """
    TUJUAN: Handle POST hapus produk, return table partial yang diperbarui.
    US: US-CRUD-01
    """

    def post(self, request, pk):
        from django.shortcuts import render

        produk = get_object_or_404(Produk, pk=pk)
        nama = produk.nama
        produk.delete()
        _, page_obj = _produk_list_qs(request)
        response = render(request, "apps/produk/partials/table_body.html", {
            "produk_list": page_obj.object_list,
            "page_obj": page_obj,
        })
        response["HX-Trigger"] = f'{{"showToast": {{"message": "\\"{nama}\\" dihapus", "type": "success"}}}}'
        return response
