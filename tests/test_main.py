from unittest.mock import patch

from src.main import main


def test_explanation_failure_uses_rule_based_fallback(capsys):
    preferences = {"genre": "lofi", "mood": "chill", "energy": 0.2}
    song = {
        "id": "1",
        "title": "Test Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.2,
    }
    reasons = (
        "genre match (+1.0); mood match (+1.0); "
        "energy similarity (+2.00)"
    )

    with (
        patch("builtins.input", return_value="Calm lofi music"),
        patch("src.main.parse_preferences", return_value=preferences),
        patch("src.main.load_songs", return_value=[song]),
        patch(
            "src.main.explain_recommendations",
            side_effect=ValueError("Invalid AI explanation"),
        ),
    ):
        main()

    output = capsys.readouterr().out

    assert "AI explanations unavailable; showing scoring reasons." in output
    assert "Test Lofi" in output
    assert f"Rule-based explanation: {reasons}" in output