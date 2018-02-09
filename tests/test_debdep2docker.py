import pytest

from debdep2docker import parse_deps

def test_parse_deps():
    # empty dependencies
    assert parse_deps("") == []

    # single dependency
    assert parse_deps("foo") == ["foo"]

    # multiple dependencies
    assert parse_deps("foo, bar, baz") == ["foo", "bar", "baz"]

    # ignore whitespace
    assert parse_deps(" foo  ") == ["foo"]

    # ignore versions
    assert parse_deps("foo (>= 1.0)") == ["foo"]

    # don't choke on alternatives
    assert parse_deps("foo | bar, baz") == ["foo", "baz"]
