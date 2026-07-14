"""
Views untuk dashboard app.
US: US-032 — Halaman dashboard default dengan demo data
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render

from apps.dashboard.models.activity import Activity

User = get_user_model()


@login_required
def dashboard_index(request):
    """
    TUJUAN: Render halaman dashboard utama.
    US: US-032 — Dashboard default dengan demo data

    ALUR:
      1. Ambil KPI dari DB:
         - Total Users
         - Total Activities
         - Total Revenue (Sum of amount where status=completed)
         - Pending Activities
      2. Ambil data Activity terpaginasi (10 baris per halaman)
      3. Jika request HTMX: render fragment table saja
      4. Jika non-HTMX: render full page dashboard/index.html
    """
    # Hitung metrik KPI secara dinamis
    total_users = User.objects.count()
    total_activities = Activity.objects.count()

    total_revenue_dict = Activity.objects.filter(status="completed").aggregate(total=Sum("amount"))
    total_revenue = total_revenue_dict["total"] or 0

    pending_activities = Activity.objects.filter(status="pending").count()

    # Query activities dengan pagination
    activities_list = Activity.objects.select_related("user").all()
    paginator = Paginator(activities_list, 10)  # 10 baris per halaman

    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)

    context = {
        "total_users": total_users,
        "total_activities": total_activities,
        "total_revenue": total_revenue,
        "pending_activities": pending_activities,
        "page_obj": page_obj,
    }

    # Jika request dari HTMX, kirim fragment tabel saja
    if request.headers.get("HX-Request") == "true":
        return render(request, "dashboard/partials/activity_table.html", context)

    return render(request, "dashboard/index.html", context)
