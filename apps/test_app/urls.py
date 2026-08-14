from django.urls import path

from .views import (
    BarangCreateModalView,
    BarangDeleteModalView,
    BarangDetailView,
    BarangEditModalView,
    BarangListView,
)

app_name = "test_app"

urlpatterns = [
    path("barang/", BarangListView.as_view(), name="barang-list"),
    path("", BarangListView.as_view(), name="list"),
    path("barang/baru/", BarangCreateModalView.as_view(), name="barang-create"),
    path("barang/baru/modal/", BarangCreateModalView.as_view(), name="barang-create-modal"),
    path("barang/<int:pk>/edit/", BarangEditModalView.as_view(), name="barang-edit"),
    path("barang/<int:pk>/edit/modal/", BarangEditModalView.as_view(), name="barang-edit-modal"),
    path("barang/<int:pk>/hapus/", BarangDeleteModalView.as_view(), name="barang-delete"),
    path(
        "barang/<int:pk>/hapus/modal/", BarangDeleteModalView.as_view(), name="barang-delete-modal"
    ),
    path("barang/<int:pk>/", BarangDetailView.as_view(), name="barang-detail"),
    # path('', views.index, name='index'),
]
