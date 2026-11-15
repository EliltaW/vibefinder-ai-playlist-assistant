import pytest

from src.guardrails import validate_request, validate_preferences

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

def test_preferences_are_normalized():
    result = validate_preferences(
        {"genre": " Lofi ", "mood": "Chill", "energy": 0.3}
    )

    assert result == {"genre": "lofi", "mood": "chill", "energy": 0.3}


@pytest.mark.parametrize("energy", [0, 1])
def test_energy_boundaries_are_accepted(energy):
    result = validate_preferences(
        {"genre": "pop", "mood": "happy", "energy": energy}
    )

    assert result["energy"] == float(energy)


@pytest.mark.parametrize(
    "energy",
    [-0.1, 1.1, "high", None, True, float("nan"), float("inf")],
)
def test_invalid_energy_is_rejected(energy):
    with pytest.raises(ValueError):
        validate_preferences(
            {"genre": "pop", "mood": "happy", "energy": energy}
        )


@pytest.mark.parametrize(
    "preferences",
    [
        None,
        [],
        {},
        {"genre": "pop", "energy": 0.5},
        {"genre": " ", "mood": "happy", "energy": 0.5},
        {"genre": "pop", "mood": 123, "energy": 0.5},
    ],
)
def test_invalid_preferences_are_rejected(preferences):
    with pytest.raises(ValueError):
        validate_preferences(preferences)