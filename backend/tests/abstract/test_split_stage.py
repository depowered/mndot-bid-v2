import pytest

from src.abstract.stages.split.split_abstracts import (
    SplitError,
    Subtable,
    _split_abstract_into_subtables,
)


def test_split_fail() -> None:
    content = "table one\n\ntable two"
    with pytest.raises(SplitError):
        _split_abstract_into_subtables(content=content)


def test_split_succeed() -> None:
    content = "table one\n\ntable two\n\ntable three"
    subtables = _split_abstract_into_subtables(content=content)

    assert subtables == [
        Subtable("contract", "table one"),
        Subtable("bid", "table two"),
        Subtable("bidder", "table three"),
    ]
