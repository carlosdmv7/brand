from brand import contrast, tokens


def test_palette_has_no_aa_violations():
    assert contrast.violations() == []


def test_ratio_matches_known_values():
    assert round(contrast.ratio("#000000", "#FFFFFF"), 2) == 21.0
    assert round(contrast.ratio(tokens.WHITE, tokens.RUST_500), 2) == 3.42


def test_text_safe_colours_clear_aa_on_surface():
    for colour in tokens.TEXT_SAFE_ON_SURFACE:
        assert contrast.ratio(colour, tokens.SURFACE) >= contrast.TEXT, colour


def test_white_label_fills_clear_aa():
    for fill in tokens.WHITE_LABEL_FILLS:
        assert contrast.ratio(tokens.WHITE, fill) >= contrast.TEXT, fill


def test_forbidden_pairs_really_fail():
    # A forbidden pair that passes is a rule nobody needs any more: drop it.
    for pair in contrast.PAIRS:
        if pair.forbidden:
            assert contrast.measure(pair) < pair.minimum, pair


def test_every_pair_names_real_tokens():
    for pair in contrast.PAIRS:
        assert pair.fg in tokens.COLORS
        assert pair.bg in tokens.COLORS
