import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict, dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dicts = [asdict(song) for song in self.songs]
        songs_by_dict_id = {
            id(song_dict): song
            for song_dict, song in zip(song_dicts, self.songs)
        }
        recommendations = recommend_songs(user_prefs, song_dicts, k)
        return [
            songs_by_dict_id[id(song_dict)]
            for song_dict, _, _ in recommendations
        ]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        _, reasons = score_song(user_prefs, asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Returns song dictionaries loaded from a CSV file."""
    with open(csv_path, newline="") as csv_file:
        songs = list(csv.DictReader(csv_file))

    for song in songs:
        for field in ("energy", "valence", "danceability", "acousticness"):
            song[field] = float(song[field])
        song["tempo_bpm"] = int(song["tempo_bpm"])

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Returns a song's preference score and a list of scoring reasons."""
    score = 0.0
    reasons = []

    genre_points = 1.0 if song["genre"] == user_prefs["genre"] else 0.0
    score += genre_points
    genre_result = "match" if genre_points else "mismatch"
    reasons.append(f"genre {genre_result} (+{genre_points:.1f})")

    mood_points = 1.0 if song["mood"] == user_prefs["mood"] else 0.0
    score += mood_points
    mood_result = "match" if mood_points else "mismatch"
    reasons.append(f"mood {mood_result} (+{mood_points:.1f})")

    energy_points = 2.0 * (1.0 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top k songs as song, score, and explanation tuples."""
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_songs.append((song, score, explanation))

    return sorted(scored_songs, key=lambda result: result[1], reverse=True)[:k]

def retrieve_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, str]]:
    """Rank songs matching at least the requested genre or mood."""
    candidates = [
        song
        for song in songs
        if song["genre"] == user_prefs["genre"]
        or song["mood"] == user_prefs["mood"]
    ]

    return recommend_songs(user_prefs, candidates, k)

