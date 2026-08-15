import os
import shutil
from scripts.rdp.ops.project import reset_project_scaffolding


def test_reset_project_scaffolding_empties_status_md(tmp_path):
    """
    Memverifikasi bahwa reset_project_scaffolding mengosongkan berkas STATUS.md
    serta berkas cadangan Status.md jika ada.
    """
    proj_name = "test-project"
    proj_desc = "Test Description"

    # Setup file-file palsu yang akan di-reset
    status_file = tmp_path / "STATUS.md"
    status_file.write_text("Some active development status...", encoding="utf-8")

    status_file_alt = tmp_path / "Status.md"
    status_file_alt.write_text("Another status...", encoding="utf-8")

    readme_file = tmp_path / "README.md"
    readme_file.write_text("Old readme", encoding="utf-8")

    changelog_file = tmp_path / "CHANGELOG.md"
    changelog_file.write_text("Old changelog", encoding="utf-8")

    # Jalankan reset
    reset_project_scaffolding(str(tmp_path), proj_name, proj_desc)

    # Verifikasi berkas STATUS.md kosong
    assert status_file.exists()
    assert status_file.read_text(encoding="utf-8") == ""

    # Verifikasi berkas Status.md kosong
    assert status_file_alt.exists()
    assert status_file_alt.read_text(encoding="utf-8") == ""

    # Verifikasi README.md dan CHANGELOG.md ikut ter-reset dan tidak mengandung literal "\n"
    assert readme_file.exists()
    readme_content = readme_file.read_text(encoding="utf-8")
    assert "# test-project" in readme_content
    assert "\\n" not in readme_content

    assert changelog_file.exists()
    changelog_content = changelog_file.read_text(encoding="utf-8")
    assert "# Changelog" in changelog_content
    assert "\\n" not in changelog_content


def test_cleanup_optional_features_removes_templates(tmp_path):
    """
    Memverifikasi bahwa cleanup_optional_features menghapus templates/apps/inventory,
    templates/apps/test_app, dan templates/inventory jika has_demo_pages=False.
    """
    from scripts.rdp.ops.project import cleanup_optional_features

    # Setup struktur direktori palsu
    apps_dir = tmp_path / "apps"
    apps_dir.mkdir()
    (apps_dir / "inventory").mkdir()
    (apps_dir / "test_app").mkdir()

    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    apps_tmpl_dir = templates_dir / "apps"
    apps_tmpl_dir.mkdir()
    (apps_tmpl_dir / "inventory").mkdir()
    (apps_tmpl_dir / "test_app").mkdir()

    (templates_dir / "inventory").mkdir()
    (templates_dir / "inventory" / "partials").mkdir()

    # Jalankan cleanup dengan has_demo_pages=False
    cleanup_optional_features(
        target_dir=str(tmp_path),
        has_landing=True,
        has_auth=True,
        has_dashboard=True,
        has_demo_pages=False
    )

    # Verifikasi folder apps dihapus
    assert not (apps_dir / "inventory").exists()
    assert not (apps_dir / "test_app").exists()

    # Verifikasi folder templates dihapus
    assert not (apps_tmpl_dir / "inventory").exists()
    assert not (apps_tmpl_dir / "test_app").exists()
    assert not (templates_dir / "inventory").exists()
