"""
Run the music recommender for four listener profiles and print each profile's
top five recommendations with scores and explanations.
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        ("Happy Pop", {"genre": "pop", "mood": "happy", "energy": 0.8}),
        ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.42}),
        ("Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.91}),
        ("Aggressive Classical", {"genre": "classical", "mood": "aggressive", "energy": 0.95}),
    ]

    for profile_name, user_prefs in profiles:
        print(f"\n{profile_name} - Top recommendations:\n")
        recommendations = recommend_songs(user_prefs, songs, k=5)

        for song, score, reasons in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {reasons}")
            print()


if __name__ == "__main__":
    main()
