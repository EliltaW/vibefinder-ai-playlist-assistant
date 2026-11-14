import pytest

from src.guardrails import validate_request


def test_valid_request_removes_surrounding_spaces():
    assert validate_request("  Calm lofi for studying  ") == "Calm lofi for studying"


@pytest.mark.parametrize("user_input", ["", "   ", "\n\t"])
def test_blank_request_is_rejected(user_input):
    with pytest.raises(ValueError, match="Please describe"):
        validate_request(user_input)


def test_request_at_length_limit_is_accepted():
    assert validate_request("a" * 500) == "a" * 500


def test_request_over_length_limit_is_rejected():
    with pytest.raises(ValueError, match="500 characters"):
        validate_request("a" * 501)