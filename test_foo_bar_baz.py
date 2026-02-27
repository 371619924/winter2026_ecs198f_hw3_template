import pytest
from foo_bar_baz import foo_bar_baz


import importlib

_fbb_mod = importlib.import_module("foo_bar_baz")


def foo_bar_baz(n):
    
    return _fbb_mod.foo_bar_baz(n)


def expected_foo_bar_baz(n: int) -> str:
    if n <= 0:
        return ""
    parts = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            parts.append("Baz")
        elif i % 3 == 0:
            parts.append("Foo")
        elif i % 5 == 0:
            parts.append("Bar")
        else:
            parts.append(str(i))
    return " ".join(parts)


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 10, 14, 15, 16, 30])
def test_exact_output_matches_expected(n):
    assert foo_bar_baz(n) == expected_foo_bar_baz(n)


@pytest.mark.parametrize("n", [0, -1, -10])
def test_edge_cases_non_positive_n(n):
    assert foo_bar_baz(n) == ""


@pytest.mark.parametrize("n", [1, 2, 3, 5, 15, 25])
def test_format_space_delimited_and_no_extra_spaces(n):
    out = foo_bar_baz(n)
    assert isinstance(out, str)
    assert out == out.strip()   # no leading/trailing spaces
    assert "  " not in out      # no double spaces

    if n == 1:
        assert out.count(" ") == 0
        assert len(out.split(" ")) == 1
    else:
        assert out.count(" ") == n - 1
        assert len(out.split(" ")) == n


def test_rules_hold_for_many_values():
    for n in range(1, 101):
        out = foo_bar_baz(n)
        tokens = out.split(" ")
        assert len(tokens) == n

        for i, tok in enumerate(tokens, start=1):
            if i % 15 == 0:
                assert tok == "Baz"
            elif i % 3 == 0:
                assert tok == "Foo"
            elif i % 5 == 0:
                assert tok == "Bar"
            else:
                assert tok == str(i)


def test_large_n_not_truncated_and_tail_correct():
    n = 300
    out = foo_bar_baz(n)

    assert out.count(" ") == n - 1
    tokens = out.split(" ")
    assert len(tokens) == n

    expected_tokens = expected_foo_bar_baz(n).split(" ")
    assert tokens[-1] == expected_tokens[-1]
    assert tokens[-2] == expected_tokens[-2]
    assert tokens[-3] == expected_tokens[-3]


@pytest.mark.parametrize("bad_n", ["10", 10.0, 3.5, None])
def test_invalid_input_types_raise_type_error(bad_n):
    with pytest.raises(TypeError):
        foo_bar_baz(bad_n)