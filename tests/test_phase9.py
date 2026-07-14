"""
Unit tests untuk Phase 9 - CLI & DX.
US: US-024, US-025, US-037, US-038
"""

import os
import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from apps.dashboard.models.activity import Activity
from scripts import lint_templates

User = get_user_model()


@pytest.mark.django_db
class TestPhase9CLIAndDX:
    """Test Suite untuk memverifikasi fungsionalitas Phase 9."""

    def test_loaddemodata_command(self):
        """Verify loaddemodata command creates users and demo data and is idempotent."""
        # 1. Run loaddemodata
        call_command("loaddemodata")

        # Verify superuser exists
        admin_user = User.objects.get(email="admin@rdp.test")
        assert admin_user.is_superuser
        assert admin_user.is_staff

        # Verify regular users exist
        user1 = User.objects.get(email="user1@rdp.test")
        user2 = User.objects.get(email="user2@rdp.test")
        assert not user1.is_superuser
        assert not user2.is_superuser

        # Verify activities are created
        total_activities = Activity.objects.count()
        assert total_activities >= 15

        # 2. Run again to test idempotency (should not raise integrity error or duplicate records)
        call_command("loaddemodata")
        assert Activity.objects.count() == total_activities

    def test_lint_templates_checks(self):
        """Verify lint_templates logic detects inline style and script attributes correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file with style violation
            style_file = os.path.join(tmpdir, "test_style.html")
            with open(style_file, "w", encoding="utf-8") as f:
                f.write('<html><body><div style="color: red;">Hello</div></body></html>')

            violations = lint_templates.check_html_file(style_file)
            assert len(violations) == 1
            assert "Inline style attribute found" in violations[0][1]

            # Create a file with script violation
            script_file = os.path.join(tmpdir, "test_script.html")
            with open(script_file, "w", encoding="utf-8") as f:
                f.write("<html><body><script>console.log('test');</script></body></html>")

            violations = lint_templates.check_html_file(script_file)
            assert len(violations) == 1
            assert "Inline script tag found" in violations[0][1]

            # Create a clean file
            clean_file = os.path.join(tmpdir, "test_clean.html")
            with open(clean_file, "w", encoding="utf-8") as f:
                f.write(
                    '<html><body><script src="/static/js/theme.js"></script><script type="application/ld+json">{}</script></body></html>'
                )

            violations = lint_templates.check_html_file(clean_file)
            assert len(violations) == 0

    def test_lint_css_checks(self):
        """Verify lint_templates logic detects hex colors in CSS but allows var fallbacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create CSS file with hardcoded hex color
            bad_css = os.path.join(tmpdir, "bad.css")
            with open(bad_css, "w", encoding="utf-8") as f:
                f.write(".my-class {\n  color: #ff0000;\n}")

            violations = lint_templates.check_css_file(bad_css)
            assert len(violations) == 1
            assert "Hardcoded hex color found" in violations[0][1]

            # Create clean CSS file with variables and var fallbacks
            clean_css = os.path.join(tmpdir, "clean.css")
            with open(clean_css, "w", encoding="utf-8") as f:
                f.write(
                    ".my-class {\n  color: var(--primary, #3b6797);\n  background-color: var(--color-bg);\n}"
                )

            violations = lint_templates.check_css_file(clean_css)
            assert len(violations) == 0
