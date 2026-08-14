"""
Utility tracing dan decorator @code_map_trace untuk Code Map Engine.
US: US-014 — Telemetry & Logging Terstruktur
Ref: docs/architecture/code-map-tracing.md
"""

import functools
import logging
import time

from django.db import connection

from apps.core.middleware import get_current_trace_id

logger = logging.getLogger("code_map.tracer")


def code_map_trace(feature_name: str, service_unit_cost: float = 0.0):
    """
    Decorator untuk melacak eksekusi fungsi/class method dalam Code Map.
    Mencatat: trace_id, execution_time_ms, db_query_count, dan service_unit_cost.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            trace_id = get_current_trace_id() or "LOCAL_DEBUG"
            start_time = time.perf_counter()
            initial_queries = len(connection.queries)

            exception_raised = None
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                exception_raised = e
                raise
            finally:
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                queries_count = len(connection.queries) - initial_queries

                module_name = func.__module__
                func_name = func.__qualname__
                full_path = f"{module_name}.{func_name}"

                logger.info(
                    f"[CODE_MAP_TRACE] | TraceID: {trace_id} | Feature: {feature_name} | "
                    f"Path: {full_path} | ExecutionTime: {elapsed_ms:.2f}ms | "
                    f"DBQueries: {queries_count} | ServiceUnits: {service_unit_cost} | "
                    f"Status: {'ERROR' if exception_raised else 'SUCCESS'}"
                )

        return wrapper

    return decorator
