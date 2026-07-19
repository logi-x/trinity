"""Static wiring guards for agent readiness and UI error-state regressions."""

from pathlib import Path


_ROOT = Path(__file__).resolve().parents[2]


def test_info_panel_keeps_unavailable_distinct_from_missing_template():
    source = (_ROOT / "src/frontend/src/components/InfoPanel.vue").read_text()
    catch_body = source.split("} catch (error) {", 1)[1].split("} finally {", 1)[0]

    assert "Template Information Unavailable" in source
    assert "templateError" in source
    assert "has_template: false" not in catch_body


def test_active_file_panel_lazy_loads_directory_children():
    source = (_ROOT / "src/frontend/src/components/FilesPanel.vue").read_text()
    manager_source = (_ROOT / "src/frontend/src/views/FileManager.vue").read_text()
    node_source = (
        _ROOT / "src/frontend/src/components/file-manager/FileTreeNode.vue"
    ).read_text()

    for active_surface in (source, manager_source):
        assert "loadDirectory" in active_surface
        assert '@expand="loadDirectory"' in active_surface
        assert "children_loaded" in active_surface
    assert "@expand" in node_source
    assert "children_loading" in node_source


def test_startup_does_not_block_ready_api_on_restart_fetch_or_package_upgrade():
    startup = (_ROOT / "docker/base-image/startup.sh").read_text()
    dockerfile = (_ROOT / "docker/base-image/Dockerfile").read_text()

    existing_repo = startup.split('if [ -d "/home/developer/.git" ]; then', 1)[1]
    existing_repo = existing_repo.split("else", 1)[0]
    dependency_section = startup.split(
        'echo "Verifying agent-server dependencies..."', 1
    )[1].split("# Start SSH", 1)[0]

    assert "fetch_origin_in_background" in existing_repo
    assert "GIT_STARTUP_FETCH_TIMEOUT_SECONDS" in startup
    assert "pip install --user --quiet --upgrade" not in dependency_section
    assert "HEALTHCHECK" in dockerfile
