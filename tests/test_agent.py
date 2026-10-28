
import pytest

from agent import validate_topic, build_prompt


def test_valid_topic():
    assert validate_topic("Artificial Intelligence") == (
        "Artificial Intelligence"
    )


def test_empty_topic():
    with pytest.raises(ValueError):
        validate_topic("   ")


def test_topic_too_long():
    with pytest.raises(ValueError):
        validate_topic("A" * 201)


def test_prompt_contains_topic_and_results():
    messages = build_prompt(
        "Climate Change",
        "Search result about climate research",
    )
    combined = " ".join(str(message.content) for message in messages)

    assert "Climate Change" in combined
    assert "Search result about climate research" in combined
    assert "three bullet points" in combined
