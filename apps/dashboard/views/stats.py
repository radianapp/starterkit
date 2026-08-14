from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from apps.dashboard.models.activity import Activity

User = get_user_model()


@login_required
def dashboard_stats_htmx(request):
    import time

    time.sleep(0.5)  # Simulate heavy query for demonstration of lazy loading

    total_users = User.objects.count()
    total_activities = Activity.objects.count()
    total_revenue_dict = Activity.objects.filter(status="completed").aggregate(total=Sum("amount"))
    total_revenue = total_revenue_dict["total"] or 0
    pending_activities = Activity.objects.filter(status="pending").count()

    context = {
        "total_users": total_users,
        "total_activities": total_activities,
        "total_revenue": total_revenue,
        "pending_activities": pending_activities,
    }

    return render(request, "dashboard/partials/stats.html", context)
