# apps/inventory/forms/produk_forms.py
# US-CRUD-01: Form tambah/edit produk

from django import forms

from apps.inventory.models.produk import Produk


class ProdukForm(forms.ModelForm):
    """
    TUJUAN: Validasi input tambah/edit produk dari modal HTMX.

    DIPANGGIL DARI: views/produk.py (TambahProdukView, EditProdukView)
    DEPENDENSI: Produk model
    """

    class Meta:
        model = Produk
        fields = ["nama", "sku", "kategori", "harga", "stok", "pemasok", "deskripsi"]

    def clean_nama(self):
        nama = self.cleaned_data.get("nama", "").strip()
        qs = Produk.objects.filter(nama__iexact=nama)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Produk dengan nama ini sudah ada.")
        return nama

    def clean_harga(self):
        harga = self.cleaned_data.get("harga")
        if harga is not None and harga < 0:
            raise forms.ValidationError("Harga tidak boleh negatif.")
        return harga
