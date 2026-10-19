import tomllib

from brand.cli import main
from brand.sync import TOML


def test_sync_then_check_round_trip(tmp_path, capsys):
    path = tmp_path / "config.toml"
    path.write_text(f"{TOML.start}\n{TOML.end}\n\n[server]\nheadless = true\n")

    assert main(["sync", "streamlit", str(path), "--check"]) == 1
    assert main(["sync", "streamlit", str(path)]) == 0
    assert main(["sync", "streamlit", str(path), "--check"]) == 0

    config = tomllib.loads(path.read_text())
    assert config["server"]["headless"] is True
    assert "primaryColor" in config["theme"]
    assert "up to date" in capsys.readouterr().out


def test_unmarked_file_exits_2(tmp_path, capsys):
    path = tmp_path / "styles.css"
    path.write_text("body {}\n")

    assert main(["sync", "css", str(path)]) == 2
    assert "no brand markers" in capsys.readouterr().err


def test_contrast_passes(capsys):
    assert main(["contrast"]) == 0
    assert "0 violation(s)" in capsys.readouterr().out
