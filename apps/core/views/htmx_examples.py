"""
Views untuk mendemonstrasikan 10 HTMX patterns.
US: US-036 — 10 HTMX patterns — contoh hidup + resep cookbook
"""

from django import forms
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.core.mixins.htmx import HtmxFormMixin

# Data in-memory sederhana untuk simulasi database CRUD & search
DUMMY_CONTACTS = [
    {"id": 1, "name": "Budi Santoso", "email": "budi@radian.web.id", "phone": "081234567890"},
    {"id": 2, "name": "Rahadi Putra", "email": "rahadi@radian.web.id", "phone": "081298765432"},
    {"id": 3, "name": "Ani Wijaya", "email": "ani@radian.web.id", "phone": "081345671234"},
    {
        "id": 4,
        "name": "Bambang Pamungkas",
        "email": "bambang@radian.web.id",
        "phone": "081122334455",
    },
    {"id": 5, "name": "Citra Lestari", "email": "citra@radian.web.id", "phone": "081566778899"},
]


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Nama Lengkap",
        widget=forms.TextInput(attrs={"placeholder": "Masukkan nama lengkap..."}),
    )
    email = forms.EmailField(
        label="Surel (Email)",
        widget=forms.EmailInput(attrs={"placeholder": "Masukkan alamat email..."}),
    )
    phone = forms.CharField(
        max_length=20,
        label="Nomor Telepon",
        widget=forms.TextInput(attrs={"placeholder": "Contoh: 0812345..."}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Contoh validasi kustom: dilarang menggunakan domain spam.test
        if email and email.endswith("spam.test"):
            raise forms.ValidationError("Domain email spam.test dilarang.")
        return email


class HtmxExamplesIndexView(TemplateView):
    """Halaman indeks yang merangkum semua contoh 10 pola HTMX."""

    template_name = "htmx_examples/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contacts"] = DUMMY_CONTACTS
        return context


# Pattern 1 & 2: CRUD List + Form & Modal Form
class ContactCreateView(HtmxFormMixin, FormView):
    """
    US: US-029 & US-036 — Membuat kontak baru.
    Mendukung flow form HTMX: status 422 jika error, HX-Redirect jika sukses.
    """

    form_class = ContactForm
    template_name = "htmx_examples/partials/contact_form.html"
    htmx_template_name = "htmx_examples/partials/contact_form.html"
    success_url = reverse_lazy("htmx-examples")

    def form_valid(self, form):
        # Simulasi simpan ke database
        new_id = max([c["id"] for c in DUMMY_CONTACTS], default=0) + 1
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        phone = form.cleaned_data["phone"]
        DUMMY_CONTACTS.append({"id": new_id, "name": name, "email": email, "phone": phone})

        # Kirim sinyal sukses via trigger toast dan redirect
        if self.request.headers.get("HX-Request") == "true":
            response = HttpResponse("")
            import json

            # Set header HX-Trigger untuk memicu toast notification di frontend
            response["HX-Trigger"] = json.dumps(
                {"showToast": {"message": "Kontak berhasil ditambahkan!", "type": "success"}}
            )
            response["HX-Redirect"] = self.get_success_url()
            return response
        return super().form_valid(form)


# Pattern 3: Delete Confirmation
class ContactDeleteView(View):
    """
    US: US-036 — Hapus kontak dengan konfirmasi.
    Merespons request DELETE via HTMX.
    """

    def delete(self, request, pk, *args, **kwargs):
        global DUMMY_CONTACTS
        # Cari dan hapus dari list dummy
        DUMMY_CONTACTS = [c for c in DUMMY_CONTACTS if c["id"] != pk]

        # Kirim response kosong dengan memicu toast sukses
        response = HttpResponse("")
        import json

        response["HX-Trigger"] = json.dumps(
            {"showToast": {"message": "Kontak berhasil dihapus!", "type": "success"}}
        )
        return response


# Pattern 4: Live Validation Field
class LiveValidationView(View):
    """
    US: US-036 — Validasi field secara langsung sewaktu user mengetik (keyup/blur).
    """

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email", "")
        error_msg = None

        if not email:
            error_msg = "Email tidak boleh kosong."
        elif "@" not in email:
            error_msg = "Format email tidak valid (harus mengandung '@')."
        elif email.endswith("spam.test"):
            error_msg = "Domain email spam.test dilarang."
        elif any(c["email"] == email for c in DUMMY_CONTACTS):
            error_msg = "Email ini sudah terdaftar."

        if error_msg:
            # Kembalikan fragmen input dengan status error (status code tetap 200 agar di-swap normal oleh HTMX, atau class error dipicu)
            return render(
                request,
                "htmx_examples/partials/email_input.html",
                {"email_value": email, "error_msg": error_msg},
            )

        return render(
            request,
            "htmx_examples/partials/email_input.html",
            {"email_value": email, "success_msg": "Email tersedia!"},
        )


# Pattern 5: Inline Edit
class ContactInlineEditView(View):
    """
    US: US-036 — Ubah baris data secara langsung di tempat (inline edit).
    """

    def get(self, request, pk, *args, **kwargs):
        contact = next((c for c in DUMMY_CONTACTS if c["id"] == pk), None)
        if not contact:
            raise Http404()
        return render(request, "htmx_examples/partials/contact_row_edit.html", {"contact": contact})

    def post(self, request, pk, *args, **kwargs):
        contact = next((c for c in DUMMY_CONTACTS if c["id"] == pk), None)
        if not contact:
            raise Http404()

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Validasi sederhana
        if not name or not email:
            return HttpResponse("Nama & Email wajib diisi.", status=400)

        contact["name"] = name
        contact["email"] = email
        contact["phone"] = phone

        response = render(
            request, "htmx_examples/partials/contact_row_view.html", {"contact": contact}
        )
        import json

        response["HX-Trigger"] = json.dumps(
            {"showToast": {"message": f"Kontak {name} diperbarui!", "type": "info"}}
        )
        return response


# Pattern 6: Search dengan Debounce
class ContactSearchView(View):
    """
    US: US-036 — Live search dengan input debounce 300ms.
    """

    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "").lower()
        if q:
            results = [
                c for c in DUMMY_CONTACTS if q in c["name"].lower() or q in c["email"].lower()
            ]
        else:
            results = DUMMY_CONTACTS

        return render(
            request, "htmx_examples/partials/contact_list_body.html", {"contacts": results}
        )


# Pattern 8: Infinite Scroll
class InfiniteScrollView(TemplateView):
    """
    US: US-036 — Memuat baris data tambahan di bagian akhir secara tak terbatas saat scroll.
    """

    template_name = "htmx_examples/infinite_scroll.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Halaman 1 langsung dirender di awal (tidak usah lazy load)
        per_page = 10
        rows = [
            {
                "id": i,
                "title": f"Log Sistem Item #{i}",
                "status": "Sukses" if i % 2 == 0 else "Peringatan",
            }
            for i in range(1, per_page + 1)
        ]
        context["initial_rows"] = rows
        context["next_page"] = 2
        return context


class InfiniteScrollRowsView(View):
    """
    US: US-036 — Memuat baris data dengan lazy load.
    Menggunakan OOB swap untuk memperbarui sentinel scroll sekaligus menambahkan baris.
    """

    def get(self, request, *args, **kwargs):
        import time
        page = int(request.GET.get("page", 1))

        if page > 1:
            time.sleep(1.5)  # Simulasi proses loading lambat 1.5 detik

        per_page = 10
        start = (page - 1) * per_page + 1
        end = start + per_page
        rows = [
            {
                "id": i,
                "title": f"Log Sistem Item #{i}",
                "status": "Sukses" if i % 2 == 0 else "Peringatan",
            }
            for i in range(start, end)
        ]

        # Limit total 50 baris (5 halaman @10 baris per load)
        next_page = page + 1 if page < 5 else None

        return render(
            request,
            "htmx_examples/partials/log_rows.html",
            {"rows": rows, "next_page": next_page},
        )



# Pattern 9: Polling Status
class JobStatusPollingView(View):
    """
    US: US-036 — Polling background job status otomatis via HTMX trigger.
    """

    # Menyimpan status simulasi job (in-memory)
    job_progress = 0

    def get(self, request, *args, **kwargs):
        # Memicu reset progress
        if request.GET.get("action") == "start":
            JobStatusPollingView.job_progress = 10
            return render(request, "htmx_examples/partials/job_status.html", {"progress": 10})

        progress = JobStatusPollingView.job_progress
        if 0 < progress < 100:
            # Tingkatkan progress setiap request
            JobStatusPollingView.job_progress = min(progress + 30, 100)
            progress = JobStatusPollingView.job_progress

        return render(request, "htmx_examples/partials/job_status.html", {"progress": progress})


# Pattern 10: Server-Triggered Toast
class ToastDemoView(View):
    """
    US: US-036 — Memicu toast notification hanya dari response header (HX-Trigger).
    """

    def post(self, request, *args, **kwargs):
        response = HttpResponse("")
        import json

        # Ambil tipe toast dari request (default success)
        toast_type = request.POST.get("type", "success")
        message = request.POST.get("message", "Aksi berhasil dieksekusi!")
        position = request.POST.get("position", "bottom-right") # default di layout css

        response["HX-Trigger"] = json.dumps(
            {"showToast": {"message": message, "type": toast_type, "position": position}}
        )
        return response
