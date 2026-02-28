import pytest
import foo_bar_baz as fbb


def _expected_token(i: int) -> str:
    if i % 15 == 0:
        return "Baz"
    if i % 3 == 0:
        return "Foo"
    if i % 5 == 0:
        return "Bar"
    return str(i)


def _expected_str(n: int) -> str:
    if n < 1:
        return ""
    return " ".join(_expected_token(i) for i in range(1, n + 1))


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, "1"),
        (2, "1 2"),
        (3, "1 2 Foo"),
        (5, "1 2 Foo 4 Bar"),
        (15, "1 2 Foo 4 Bar Foo 7 8 Foo Bar 11 Foo 13 14 Baz"),
    ],
)
def test_known_examples(n, expected):
    assert fbb.foo_bar_baz(n) == expected


@pytest.mark.parametrize("n", [0, -1, -10])
def test_zero_and_negative_returns_empty_string(n):
    assert fbb.foo_bar_baz(n) == ""


@pytest.mark.parametrize("n", [1, 3, 5, 6, 10, 15, 16, 30, 50])
def test_matches_reference_implementation(n):
    assert fbb.foo_bar_baz(n) == _expected_str(n)


def test_output_format_is_space_delimited_for_positive_n():
    n = 20
    out = fbb.foo_bar_baz(n)

    assert isinstance(out, str)
    assert out == out.strip()
    assert "  " not in out

    tokens = out.split(" ")
    assert len(tokens) == n

    for idx, tok in enumerate(tokens, start=1):
        assert tok in {"Foo", "Bar", "Baz"} or tok.isdigit()
        assert tok == _expected_token(idx)