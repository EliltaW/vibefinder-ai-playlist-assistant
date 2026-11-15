from src.recommender import retrieve_songs


def test_retrieval_filters_then_ranks_matches():
    preferences = {"genre": "lofi", "mood": "chill", "energy": 0.2}
    songs = [
        {"title": "Neither", "genre": "pop", "mood": "happy", "energy": 0.2},
        {"title": "Genre Only", "genre": "lofi", "mood": "focused", "energy": 0.4},
        {"title": "Mood Only", "genre": "ambient", "mood": "chill", "energy": 0.2},
        {"title": "Both", "genre": "lofi", "mood": "chill", "energy": 0.2},
    ]

    results = retrieve_songs(preferences, songs, k=5)

    assert [song["title"] for song, _, _ in results] == [
        "Both",
        "Mood Only",
        "Genre Only",
    ]


def test_retrieval_returns_empty_when_no_preferences_match():
    preferences = {"genre": "lofi", "mood": "chill", "energy": 0.2}
    songs = [
        {"title": "No Match", "genre": "rock", "mood": "intense", "energy": 0.2},
    ]

    assert retrieve_songs(preferences, songs) == []