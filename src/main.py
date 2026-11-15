"""Run VibeFinder's AI playlist assistant."""

import logging
from pathlib import Path

from google.genai import errors

from .ai_client import parse_preferences, explain_recommendations
from .recommender import load_songs, retrieve_songs


PROJECT_ROOT = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    print("VibeFinder — AI Playlist Assistant")
    request = input("Describe the music you want: ")

    try:
        preferences = parse_preferences(request)
    except ValueError as error:
        logger.warning("Request or preference validation failed.")
        print(f"Please check your request or setup: {error}")
        return
    except (errors.APIError, ConnectionError, TimeoutError):
        logger.warning("Preference generation failed.")
        print("The AI service is unavailable. Please try again later.")
        return

    print("\nInterpreted preferences:", preferences)

    try:
        songs = load_songs(str(PROJECT_ROOT / "data" / "songs.csv"))
        recommendations = retrieve_songs(preferences, songs)
    except (OSError, ValueError, KeyError):
        logger.error("Song catalog could not be loaded or processed.")
        print("Unable to read the song catalog. Please check data/songs.csv.")
        return

    logger.info("Retrieved %d matching songs.", len(recommendations))

    if not recommendations:
        print("No songs match your genre or mood. Try different preferences.")
        return

    try:
        explanations = explain_recommendations(
            preferences, recommendations
        )
        explanation_label = "AI explanation"
        logger.info("AI explanations passed song-ID and text checks.")
    except (
        ValueError,
        errors.APIError,
        ConnectionError,
        TimeoutError,
    ):
        logger.warning("Using rule-based explanations as a fallback.")
        explanations = {
            str(song["id"]): reasons
            for song, _, reasons in recommendations
        }
        explanation_label = "Rule-based explanation"
        print("\nAI explanations unavailable; showing scoring reasons.")

    for song, score, _ in recommendations:
        print(f"\n{song['title']} — Score: {score:.2f}")
        print(
            f"{explanation_label}: "
            f"{explanations[str(song['id'])]}"
        )


if __name__ == "__main__":
    main()