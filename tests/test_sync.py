import pytest

from brand.sync import CSS, TOML, SyncError, sync


def _config(tmp_path, middle="old = 1"):
    path = tmp_path / "config.toml"
    path.write_text(
        f'[server]\nheadless = true\n\n{TOML.start}\n{middle}\n{TOML.end}\n\n[client]\nx = "y"\n'
    )
    return path


def test_replaces_only_the_managed_block(tmp_path):
    path = _config(tmp_path)

    sync(path, "new = 2", TOML, check=False)

    text = path.read_text()
    assert "new = 2" in text
    assert "old = 1" not in text
    assert text.startswith("[server]\nheadless = true\n")
    assert text.endswith('[client]\nx = "y"\n')


def test_second_sync_is_a_no_op(tmp_path):
    path = _config(tmp_path)
    sync(path, "new = 2", TOML, check=False)

    assert sync(path, "new = 2", TOML, check=False) is None


def test_check_reports_drift_without_writing(tmp_path):
    path = _config(tmp_path)
    before = path.read_text()

    diff = sync(path, "new = 2", TOML, check=True)

    assert "-old = 1" in diff
    assert "+new = 2" in diff
    assert path.read_text() == before


def test_refuses_a_file_without_markers(tmp_path):
    path = tmp_path / "styles.css"
    path.write_text(":root { --x: red; }\n")

    with pytest.raises(SyncError, match="no brand markers"):
        sync(path, ":root {}", CSS, check=False)


def test_refuses_duplicated_markers(tmp_path):
    path = _config(tmp_path, middle=f"{TOML.end}\n{TOML.start}")

    with pytest.raises(SyncError, match="exactly one"):
        sync(path, "new = 2", TOML, check=False)


def test_missing_file_is_an_error(tmp_path):
    with pytest.raises(SyncError, match="not found"):
        sync(tmp_path / "nope.toml", "", TOML, check=False)
