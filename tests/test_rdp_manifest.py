"""
Unit test untuk deteksi manifest signature proyek RDP dan kompatibilitas multi-versi.
US: US-024 — CLI rdp new & project detection
"""

import json

from scripts.rdp.utils import get_project_manifest, is_rdp_project


def test_manifest_detection_from_rdp_json(tmp_path):
    """Memverifikasi deteksi dari berkas rdp.json."""
    manifest_data = {
        "project_type": "rdp-starter-kit",
        "schema_version": 1,
        "framework_version": "0.4.7",
        "config": {
            "apps_dir": "custom_apps",
            "settings_file": "config/settings/custom.py",
        },
    }
    manifest_file = tmp_path / "rdp.json"
    manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")

    result = get_project_manifest(str(tmp_path))
    assert result is not None
    assert result["project_type"] == "rdp-starter-kit"
    assert result["_source"] == "rdp.json"
    assert result["config"]["apps_dir"] == "custom_apps"
    assert is_rdp_project(str(tmp_path)) is True


def test_manifest_detection_from_pyproject_toml(tmp_path):
    """Memverifikasi deteksi dari section [tool.rdp] di pyproject.toml jika rdp.json tidak ada."""
    pyproject_content = """
[project]
name = "my-custom-rdp-app"
version = "1.0.0"

[tool.rdp]
project_type = "rdp-starter-kit"
schema_version = 1
framework_version = "0.4.7"
apps_dir = "my_apps"
settings_file = "config/settings/base.py"
"""
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(pyproject_content, encoding="utf-8")

    result = get_project_manifest(str(tmp_path))
    assert result is not None
    assert result["_source"] == "pyproject.toml"
    assert result["config"]["apps_dir"] == "my_apps"
    assert is_rdp_project(str(tmp_path)) is True


def test_manifest_legacy_fallback(tmp_path):
    """Memverifikasi fallback heuristik untuk proyek versi lama (v0.1 - v0.4)."""
    (tmp_path / "apps").mkdir()
    (tmp_path / "config").mkdir()
    version_file = tmp_path / "config" / "version.json"
    version_file.write_text(json.dumps({"version": "0.3.2"}), encoding="utf-8")

    result = get_project_manifest(str(tmp_path))
    assert result is not None
    assert result["_source"] == "legacy_heuristics"
    assert result["framework_version"] == "0.3.2"
    assert is_rdp_project(str(tmp_path)) is True


def test_non_rdp_project(tmp_path):
    """Memverifikasi bahwa folder kosong / proyek non-RDP tidak terdeteksi sebagai proyek RDP."""
    result = get_project_manifest(str(tmp_path))
    assert result is None
    assert is_rdp_project(str(tmp_path)) is False
