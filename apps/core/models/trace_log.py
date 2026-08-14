"""
Model ExecutionTraceLog untuk mencatat historis tracing eksekusi user.
US: US-014 — Telemetry & Logging Terstruktur
Ref: docs/architecture/code-map-tracing.md
"""

from django.conf import settings
from django.db import models


class ExecutionTraceLog(models.Model):
    """
    Menyimpan trace historis eksekusi user untuk kebutuhan Reverse Engineering & Debugging.
    """

    trace_id = models.CharField(max_length=64, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="trace_logs",
    )
    feature_name = models.CharField(max_length=100, db_index=True)
    endpoint = models.CharField(max_length=255, blank=True, default="")
    class_function_path = models.CharField(max_length=255)
    execution_time_ms = models.FloatField(default=0.0)
    db_query_count = models.IntegerField(default=0)
    service_units_consumed = models.FloatField(default=0.0)
    status_code = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Execution Trace Log"
        verbose_name_plural = "Execution Trace Logs"

    def __str__(self):
        return f"Trace [{self.trace_id[:8]}] {self.feature_name} ({self.execution_time_ms:.2f}ms)"
