"""
View Handler untuk Observability Dashboard (/dev/telemetry/) & Health Check Probe (/healthz/).
US: US-014 — Telemetry & Observability
"""

import shutil
import time

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.db import connection, models
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views import View

from apps.core.models.trace_log import ExecutionTraceLog


class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin otorisasi ketat: Hanya mengizinkan superuser atau staff.
    """

    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_superuser or self.request.user.is_staff
        )

    def handle_no_permission(self):
        if self.request.headers.get("HX-Request"):
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Akses khusus Superuser/Staff.</p>"
            )
        return render(self.request, "errors/403.html", status=403)


class TelemetryDashboardView(SuperuserRequiredMixin, View):
    """
    Dashboard Telemetri Runtime di /dev/telemetry/ (Superuser/Staff Only).
    """

    def get(self, request, *args, **kwargs):
        trace_logs = ExecutionTraceLog.objects.all()[:100]

        # Metric Summaries
        total_traces = ExecutionTraceLog.objects.count()
        avg_exec_time = (
            ExecutionTraceLog.objects.aggregate(avg=models.Avg("execution_time_ms"))["avg"] or 0.0
        )
        avg_db_queries = (
            ExecutionTraceLog.objects.aggregate(avg=models.Avg("db_query_count"))["avg"] or 0.0
        )
        total_units = (
            ExecutionTraceLog.objects.aggregate(sum=models.Sum("service_units_consumed"))["sum"]
            or 0.0
        )

        # Slow endpoints (exec_time > 200ms)
        slow_endpoints = ExecutionTraceLog.objects.filter(execution_time_ms__gt=200.0)[:10]

        # High DB Queries (N+1 query suspects: db_query_count > 10)
        high_db_queries = ExecutionTraceLog.objects.filter(db_query_count__gt=10)[:10]

        context = {
            "trace_logs": trace_logs,
            "total_traces": total_traces,
            "avg_exec_time": round(avg_exec_time, 2),
            "avg_db_queries": round(avg_db_queries, 1),
            "total_units": round(total_units, 2),
            "slow_endpoints": slow_endpoints,
            "high_db_queries": high_db_queries,
        }

        if request.headers.get("HX-Request"):
            return render(request, "core/partials/telemetry_content.html", context)

        return render(request, "core/telemetry.html", context)


class HealthCheckView(View):
    """
    Liveness & Readiness Probe Endpoint di /healthz/ (JSON format).
    """

    def get(self, request, *args, **kwargs):
        checks = {}
        all_ok = True

        # 1. Database Check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            checks["database"] = "ok"
        except Exception as e:
            checks["database"] = f"error: {e!s}"
            all_ok = False

        # 2. Cache Check
        try:
            cache.set("health_check_key", "ok", 10)
            val = cache.get("health_check_key")
            if val == "ok":
                checks["cache"] = "ok"
            else:
                checks["cache"] = "error: read mismatch"
                all_ok = False
        except Exception as e:
            checks["cache"] = f"error: {e!s}"
            all_ok = False

        # 3. Disk Space Check
        try:
            _total, _used, free = shutil.disk_usage(settings.BASE_DIR)
            free_gb = round(free / (1024**3), 2)
            checks["storage"] = f"ok ({free_gb} GB free)"
        except Exception as e:
            checks["storage"] = f"error: {e!s}"

        status_code = 200 if all_ok else 503
        response_data = {
            "status": "ok" if all_ok else "unhealthy",
            "timestamp": int(time.time()),
            "environment": getattr(settings, "ENVIRONMENT", "development"),
            "checks": checks,
        }

        return JsonResponse(response_data, status=status_code)
