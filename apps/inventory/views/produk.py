# apps/inventory/views/produk.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.template.loader import render_to_string

from ..models import Produk
from ..forms import ProdukForm


class ProdukListView(LoginRequiredMixin, ListView):
    """
    TUJUAN: Tampilkan daftar semua Produk.

    DIPANGGIL DARI: urls.py → name="produk-list"
    DEPENDENSI: Produk model, templates/apps/inventory/produk_list.html
    """

    model = Produk
    template_name = "apps/inventory/produk_list.html"
    context_object_name = "items"
    paginate_by = 20

    def get_paginate_by(self, queryset):
        """Ambil jumlah baris per halaman dari URL parameter atau pengaturan akun."""
        # 1. Cek parameter URL (misal sedang diubah via dropdown HTMX)
        paginate_by = self.request.GET.get("paginate_by")
        if paginate_by and paginate_by.isdigit():
            return int(paginate_by)
            
        # 2. Cek preferensi pengguna yang tersimpan di UserProfile
        if self.request.user.is_authenticated:
            from apps.accounts.services.settings_service import get_user_preference
            user_pref = get_user_preference(self.request.user, "rows_per_page")
            if user_pref:
                try:
                    return int(user_pref)
                except ValueError:
                    pass
                    
        # 3. Fallback default
        return self.paginate_by

    def get_queryset(self):
        """Filter queryset berdasarkan parameter q (pencarian)."""
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(nama__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        """Tambahkan current_paginate_by ke context agar dropdown sinkron."""
        context = super().get_context_data(**kwargs)
        context["current_paginate_by"] = self.get_paginate_by(self.get_queryset())
        return context


class ProdukCreateModalView(LoginRequiredMixin, CreateView):
    """
    TUJUAN: Tampilkan modal form tambah Produk (HTMX partial).

    DIPANGGIL DARI: urls.py → name="produk-create-modal" (GET)
                    urls.py → name="produk-create" (POST)
    """

    model = Produk
    form_class = ProdukForm
    template_name = "apps/inventory/produk_create_modal.html"

    def get(self, request, *args, **kwargs):
        """Tampilkan modal create — response partial HTML."""
        form = self.form_class()
        html = render_to_string(self.template_name, {"form": form}, request=request)
        return HttpResponse(html)

    def form_valid(self, form):
        """Simpan data, trigger reload halaman via HX-Refresh."""
        self.object = form.save()
        response = HttpResponse("")
        response["HX-Refresh"] = "true"
        return response

    def form_invalid(self, form):
        """Kembalikan modal dengan error — HTTP 422 agar HTMX tahu ini error."""
        html = render_to_string(self.template_name, {"form": form}, request=self.request)
        return HttpResponse(html, status=422)


class ProdukEditModalView(LoginRequiredMixin, UpdateView):
    """
    TUJUAN: Tampilkan modal form edit Produk (HTMX partial).

    DIPANGGIL DARI: urls.py → name="produk-edit-modal" (GET)
                    urls.py → name="produk-edit" (POST)
    """

    model = Produk
    form_class = ProdukForm
    template_name = "apps/inventory/produk_edit_modal.html"

    def get(self, request, *args, **kwargs):
        """Tampilkan modal edit dengan data yang ada — response partial HTML."""
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        html = render_to_string(self.template_name, {"form": form, "object": self.object}, request=request)
        return HttpResponse(html)

    def form_valid(self, form):
        """Simpan perubahan, trigger reload halaman."""
        self.object = form.save()
        response = HttpResponse("")
        response["HX-Refresh"] = "true"
        return response

    def form_invalid(self, form):
        """Kembalikan modal dengan error — HTTP 422."""
        html = render_to_string(self.template_name, {"form": form, "object": self.object}, request=self.request)
        return HttpResponse(html, status=422)


class ProdukDeleteModalView(LoginRequiredMixin, DeleteView):
    """
    TUJUAN: Tampilkan modal konfirmasi hapus (GET) dan proses hapus (DELETE/POST).

    DIPANGGIL DARI: urls.py → name="produk-delete-modal" (GET)
                    urls.py → name="produk-delete" (DELETE/POST)
    """

    model = Produk
    template_name = "apps/inventory/produk_delete_modal.html"
    success_url = reverse_lazy("inventory:produk-list")

    def get(self, request, *args, **kwargs):
        """Tampilkan modal konfirmasi hapus — response partial HTML."""
        self.object = self.get_object()
        html = render_to_string(self.template_name, {"object": self.object}, request=request)
        return HttpResponse(html)

    def delete(self, request, *args, **kwargs):
        """Hapus object, tutup modal + refresh halaman."""
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse("")
        response["HX-Refresh"] = "true"
        return response

    # Alias untuk POST (karena HTMX form pakai hx-delete → method override)
    post = delete


class ProdukDetailView(LoginRequiredMixin, DetailView):
    """
    TUJUAN: Tampilkan detail satu Produk.

    DIPANGGIL DARI: urls.py → name="produk-detail"
    """

    model = Produk
    template_name = "apps/inventory/produk_detail.html"

