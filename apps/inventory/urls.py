# apps/inventory/urls.py

from django.urls import path

from .views import (
    ProdukCreateModalView,
    ProdukDeleteModalView,
    ProdukDetailView,
    ProdukEditModalView,
    ProdukListView,
)

app_name = "inventory"

urlpatterns = [
    path("produk/", ProdukListView.as_view(), name="produk-list"),
    path("", ProdukListView.as_view(), name="list"),
    path("produk/baru/", ProdukCreateModalView.as_view(), name="produk-create"),
    path("produk/baru/modal/", ProdukCreateModalView.as_view(), name="produk-create-modal"),
    path("produk/<int:pk>/edit/", ProdukEditModalView.as_view(), name="produk-edit"),
    path("produk/<int:pk>/edit/modal/", ProdukEditModalView.as_view(), name="produk-edit-modal"),
    path("produk/<int:pk>/hapus/", ProdukDeleteModalView.as_view(), name="produk-delete"),
    path(
        "produk/<int:pk>/hapus/modal/", ProdukDeleteModalView.as_view(), name="produk-delete-modal"
    ),
    path("produk/<int:pk>/", ProdukDetailView.as_view(), name="produk-detail"),
]
