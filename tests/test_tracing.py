"""
Test suite untuk Code Map & Debug Tracing Engine.
US: US-014 — Telemetry & Logging Terstruktur
"""

from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from apps.core.middleware import TraceMiddleware, get_current_trace_id, set_current_trace_id
from apps.core.models import ExecutionTraceLog
from apps.core.utils import code_map_trace


class TracingEngineTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_trace_middleware_injects_header(self):
        """Uji TraceMiddleware menambahkan X-Trace-ID di request dan response header."""
        request = self.factory.get("/")

        def get_response(req):
            return HttpResponse("OK")

        middleware = TraceMiddleware(get_response)
        response = middleware(request)

        self.assertTrue(hasattr(request, "trace_id"))
        self.assertIsNotNone(request.trace_id)
        self.assertEqual(response["X-Trace-ID"], request.trace_id)
        self.assertEqual(get_current_trace_id(), request.trace_id)

    def test_trace_middleware_preserves_existing_header(self):
        """Uji TraceMiddleware menjaga X-Trace-ID jika sudah dikirim oleh client/upstream."""
        custom_trace_id = "custom-trace-12345"
        request = self.factory.get("/", HTTP_X_TRACE_ID=custom_trace_id)

        def get_response(req):
            return HttpResponse("OK")

        middleware = TraceMiddleware(get_response)
        response = middleware(request)

        self.assertEqual(request.trace_id, custom_trace_id)
        self.assertEqual(response["X-Trace-ID"], custom_trace_id)

    def test_code_map_trace_decorator(self):
        """Uji decorator @code_map_trace dapat melacak fungsi tanpa merusak return value."""
        set_current_trace_id("test-decorator-trace")

        @code_map_trace(feature_name="TEST_CALCULATION", service_unit_cost=2.5)
        def sample_business_logic(a, b):
            return a + b

        result = sample_business_logic(10, 20)
        self.assertEqual(result, 30)

    def test_execution_trace_log_model(self):
        """Uji pembuatan dan querying model ExecutionTraceLog."""
        log = ExecutionTraceLog.objects.create(
            trace_id="tr-unique-99",
            feature_name="PRODUCT_EXECUTION",
            endpoint="/services/execute/",
            class_function_path="apps.services.views.ExecuteServiceView",
            execution_time_ms=142.5,
            db_query_count=3,
            service_units_consumed=5.0,
            status_code=200,
        )

        self.assertEqual(log.trace_id, "tr-unique-99")
        self.assertEqual(ExecutionTraceLog.objects.count(), 1)
        fetched = ExecutionTraceLog.objects.first()
        self.assertEqual(fetched.trace_id, "tr-unique-99")
        self.assertEqual(fetched.service_units_consumed, 5.0)
        self.assertIn("PRODUCT_EXECUTION", str(fetched))
