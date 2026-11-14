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