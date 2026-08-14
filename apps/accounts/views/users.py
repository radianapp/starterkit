import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.accounts.decorators import role_required
from apps.accounts.forms.user_management import UserManagementForm

User = get_user_model()


def _get_grouped_permissions():
    """Kelompokkan Permission berdasarkan app_label ContentType."""
    permissions = Permission.objects.select_related("content_type").order_by(
        "content_type__app_label", "content_type__model", "codename"
    )
    groups = {}
    for perm in permissions:
        app_label = perm.content_type.app_label.replace("_", " ").title()
        groups.setdefault(app_label, []).append(perm)
    return groups


@role_required("SuperAdmin")
def user_list(request):
    """
    Menampilkan daftar user beserta role-nya.
    """
    users = User.objects.all().prefetch_related("groups").order_by("-date_joined")

    return render(
        request,
        "accounts/users/list.html",
        {
            "users": users,
            "title": "Manajemen Pengguna",
        },
    )


@role_required("SuperAdmin")
def user_add(request):
    """
    Slide-over untuk menambah pengguna baru.
    """
    if request.method == "POST":
        form = UserManagementForm(request.POST)
        if form.is_valid():
            user = form.save()

            password = form.cleaned_data.get("new_password")
            if password:
                user.set_password(password)
            else:
                # Set default password (sebaiknya ada notifikasi untuk ganti)
                user.set_password("Rdp12345!")

            user.save()

            response = HttpResponse("")
            response["HX-Trigger"] = json.dumps(
                {
                    "showToast": {
                        "message": f"Pengguna {user.username} berhasil dibuat.",
                        "tags": "success",
                    },
                    "refreshUserList": True,
                }
            )
            return response
        else:
            return render(
                request,
                "accounts/users/partials/form_drawer.html",
                {
                    "form": form,
                    "is_new": True,
                },
                status=422,
            )

    else:
        form = UserManagementForm()

    return render(
        request,
        "accounts/users/partials/form_drawer.html",
        {
            "form": form,
            "is_new": True,
            "grouped_permissions": _get_grouped_permissions(),
        },
    )


@role_required("SuperAdmin")
def user_edit(request, user_id):
    """
    Slide-over untuk mengedit pengguna.
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = UserManagementForm(request.POST, instance=user)
        if form.is_valid():
            # Cek keamanan agar SuperAdmin tidak menghilangkan status SuperAdmin dirinya sendiri
            new_role = form.cleaned_data.get("role")
            if user == request.user and (not new_role or new_role.name != "SuperAdmin"):
                response = render(
                    request,
                    "accounts/users/partials/form_drawer.html",
                    {
                        "u": user,
                        "form": form,
                    },
                    status=422,
                )
                response["HX-Trigger"] = json.dumps(
                    {
                        "showToast": {
                            "message": "Anda tidak dapat menghapus role SuperAdmin dari akun Anda sendiri.",
                            "tags": "error",
                        }
                    }
                )
                return response

            user = form.save()

            password = form.cleaned_data.get("new_password")
            if password:
                user.set_password(password)
                user.save()

            # Kembalikan response yang menutup drawer dan memicu refresh list
            response = HttpResponse("")
            response["HX-Trigger"] = json.dumps(
                {
                    "showToast": {
                        "message": f"Pengguna {user.username} berhasil diperbarui.",
                        "tags": "success",
                    },
                    "refreshUserList": True,
                }
            )
            return response
        else:
            return render(
                request,
                "accounts/users/partials/form_drawer.html",
                {
                    "u": user,
                    "form": form,
                },
                status=422,
            )

    else:
        form = UserManagementForm(instance=user)

    selected_perms = set(str(p.pk) for p in user.user_permissions.all())
    return render(
        request,
        "accounts/users/partials/form_drawer.html",
        {
            "u": user,
            "form": form,
            "grouped_permissions": _get_grouped_permissions(),
            "selected_perms": selected_perms,
        },
    )


@role_required("SuperAdmin")
def user_list_partial(request):
    """
    Mengembalikan sebagian baris tabel pengguna untuk di-refresh oleh HTMX.
    """
    users = User.objects.all().prefetch_related("groups").order_by("-date_joined")
    return render(
        request,
        "accounts/users/partials/list_table.html",
        {
            "users": users,
        },
    )


@role_required("SuperAdmin")
def user_bulk_upload(request):
    """
    Menangani upload file CSV untuk Bulk User Upload.
    Jika baris > 1000, kirim ke Celery task.
    """
    import csv
    import io

    from apps.accounts.forms.bulk_upload import BulkUploadForm
    from apps.accounts.services.user_service import process_bulk_users
    from apps.accounts.tasks import process_bulk_users_task

    if request.method == "POST":
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]

            try:
                # Membaca isi file CSV
                file_data = csv_file.read().decode("utf-8-sig")
                reader = csv.DictReader(io.StringIO(file_data))
                rows = list(reader)

                if len(rows) > 1000:
                    # Lempar ke Celery
                    process_bulk_users_task.delay(rows)
                    message = f"File sedang diproses di background karena mengandung lebih dari 1000 baris ({len(rows)} baris)."
                    tags = "info"
                else:
                    # Proses langsung (sinkron)
                    results = process_bulk_users(rows, request=request)
                    if results["failed"] == 0:
                        message = f"Berhasil menambah {results['success']} pengguna dari CSV."
                        tags = "success"
                    else:
                        message = f"Berhasil: {results['success']}, Gagal: {results['failed']}. Cek log untuk detail."
                        tags = "warning"

                response = HttpResponse("")
                response["HX-Trigger"] = json.dumps(
                    {
                        "showToast": {"message": message, "tags": tags},
                        "refreshUserList": True,
                        "closeModal": True,
                    }
                )
                return response

            except Exception as e:
                return render(
                    request,
                    "accounts/users/partials/bulk_upload_modal.html",
                    {"form": form, "error": f"Gagal membaca file: {e!s}"},
                    status=422,
                )
        else:
            return render(
                request,
                "accounts/users/partials/bulk_upload_modal.html",
                {"form": form},
                status=422,
            )

    # GET request
    form = BulkUploadForm()
    return render(
        request,
        "accounts/users/partials/bulk_upload_modal.html",
        {"form": form},
    )


@role_required("SuperAdmin")
def resend_invite_email(request, user_id):
    """
    Mengirim ulang email invite/verifikasi kepada pengguna.
    Hanya via method POST (HTMX).
    """
    if request.method == "POST":
        from apps.accounts.services.email_service import send_verification_email

        target_user = get_object_or_404(User, id=user_id)

        # Kirim email
        success = send_verification_email(target_user, request)

        response = HttpResponse("")
        if success:
            message = f"Email invite berhasil dikirim ulang ke {target_user.email}."
            tags = "success"
        else:
            message = f"Gagal mengirim ulang email invite ke {target_user.email}."
            tags = "error"

        response["HX-Trigger"] = json.dumps({"showToast": {"message": message, "tags": tags}})
        return response

    return HttpResponse("Method not allowed", status=405)
