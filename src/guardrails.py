MAX_REQUEST_LENGTH = 500


def validate_request(request: str) -> str:
    """Return cleaned input, or raise ValueError for invalid input."""
    cleaned = request.strip()

    if not cleaned:
        raise ValueError("Please describe the music you want.")

    if len(cleaned) > MAX_REQUEST_LENGTH:
        raise ValueError(
            f"Please keep your request within {MAX_REQUEST_LENGTH} characters."
        )

    return cleaned

def validate_preferences(preferences: dict) -> dict:
    """Check AI-generated preferences before using them to rank songs."""
    if not isinstance(preferences, dict):
        raise ValueError("Preferences must be a dictionary.")

    cleaned = {}

    for field in ("genre", "mood"):
        value = preferences.get(field)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Please provide a valid {field}.")

        cleaned[field] = value.strip().lower()

    energy = preferences.get("energy")

    if isinstance(energy, bool) or not isinstance(energy, (int, float)):
        raise ValueError("Energy must be a number between 0 and 1.")

    if not 0 <= energy <= 1:
        raise ValueError("Energy must be between 0 and 1.")

    cleaned["energy"] = float(energy)

    return cleaned