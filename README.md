# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a classroom music recommender that ranks songs from a
16-song catalog using a listener’s preferred genre, mood, and target energy.
It explains each recommendation with the points awarded for those preferences.

---

## How The System Works

Streaming platforms can use listening history, patterns from people with similar tastes,
and song features to recommend music. My simulator will use content-based filtering
to compare songs with the listener’s stated preferences.

- **Song** — Uses `genre`, `mood`, and `energy` for scoring. The `title` identifies
  the song in the results.
- **UserProfile** stores the listener’s preferred `genre` and `mood`, and their target `energy`.
- **Recommender** — A matching genre and a matching mood each earn 1 point.
  Energy earns up to 2 points using twice the energy similarity:
  `2 × (1 − abs(song energy − target energy))`. An exact energy match earns
  2 points. Add these points to get the song’s total score.
- **Recommendations** — The recommender sorts songs from highest to lowest
  total score and returns the top results.

**Data flow:** The program reads songs from `data/songs.csv`, scores each song
against the listener’s preferences, and shows the five highest-scoring songs
when the listener requests five recommendations.
**Potential bias:** Energy can earn up to 2 points, while a genre match or mood
match earns 1 point each. As a result, a close energy match can outweigh either
a genre match or a mood match, potentially favoring songs that fit the target
energy over the listener’s preferred genre or mood.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output (Original Weights: genre 2, mood 1, energy 1)

```text
Loaded songs: 16

Top recommendations:

Sunrise City - Score: 3.98
Because: genre match (+2.0); mood match (+1.0); energy similarity (+0.98)

Gym Hero - Score: 2.87
Because: genre match (+2.0); mood mismatch (+0.0); energy similarity (+0.87)

Rooftop Lights - Score: 1.96
Because: genre mismatch (+0.0); mood match (+1.0); energy similarity (+0.96)

Side Street - Score: 0.98
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.98)

Night Drive Loop - Score: 0.95
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.95)
```

---

## Experiments You Tried

### Baseline Results for Three Listener Profiles (Original Weights: genre 2, mood 1, energy 1)

Loaded songs: 16

Happy Pop - Top recommendations:

Sunrise City - Score: 3.98
Because: genre match (+2.0); mood match (+1.0); energy similarity (+0.98)

Gym Hero - Score: 2.87
Because: genre match (+2.0); mood mismatch (+0.0); energy similarity (+0.87)

Rooftop Lights - Score: 1.96
Because: genre mismatch (+0.0); mood match (+1.0); energy similarity (+0.96)

Side Street - Score: 0.98
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.98)

Night Drive Loop - Score: 0.95
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.95)

Chill Lofi - Top recommendations:

Midnight Coding - Score: 4.00
Because: genre match (+2.0); mood match (+1.0); energy similarity (+1.00)

Library Rain - Score: 3.93
Because: genre match (+2.0); mood match (+1.0); energy similarity (+0.93)

Focus Flow - Score: 2.98
Because: genre match (+2.0); mood mismatch (+0.0); energy similarity (+0.98)

Spacewalk Thoughts - Score: 1.86
Because: genre mismatch (+0.0); mood match (+1.0); energy similarity (+0.86)

Blue Hour - Score: 0.98
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.98)

Intense Rock - Top recommendations:

Storm Runner - Score: 4.00
Because: genre match (+2.0); mood match (+1.0); energy similarity (+1.00)

Gym Hero - Score: 1.98
Because: genre mismatch (+0.0); mood match (+1.0); energy similarity (+0.98)

Iron Bloom - Score: 0.96
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.96)

Sunrise City - Score: 0.91
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.91)

Side Street - Score: 0.87
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.87)

### Edge Case — Aggressive Classical (Original Weights: genre 2, mood 1, energy 1)

This profile requests classical music with an aggressive mood and energy
of 0.95. Paper Moon ranked first with 2.37 points because its genre matched.
Iron Bloom matched both mood and energy but scored only 2.00. This shows
that the genre weight can outweigh a perfect mood and energy match.

```text
Aggressive Classical - Top recommendations:

Paper Moon - Score: 2.37
Because: genre match (+2.0); mood mismatch (+0.0); energy similarity (+0.37)

Iron Bloom - Score: 2.00
Because: genre mismatch (+0.0); mood match (+1.0); energy similarity (+1.00)

Gym Hero - Score: 0.98
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.98)

Storm Runner - Score: 0.96
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.96)

Sunrise City - Score: 0.87
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+0.87)
```

### Weight Experiment

I reduced the genre weight from 2 to 1 and doubled the energy weight.
For Aggressive Classical, Iron Bloom moved from second place at 2.00
to first place at 3.00. Paper Moon dropped from first place at 2.37
to fourth place at 1.74.

The new top result better matched my expectation because Iron Bloom
matches the requested aggressive mood and energy of 0.95. This experiment
shows how changing weights changes which preferences the system prioritizes.

```text
Aggressive Classical - Top recommendations:

Iron Bloom - Score: 3.00
Because: genre mismatch (+0.0); mood match (+1.0); energy similarity (+2.00)

Gym Hero - Score: 1.96
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+1.96)

Storm Runner - Score: 1.92
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+1.92)

Paper Moon - Score: 1.74
Because: genre match (+1.0); mood mismatch (+0.0); energy similarity (+0.74)

Sunrise City - Score: 1.74
Because: genre mismatch (+0.0); mood mismatch (+0.0); energy similarity (+1.74)

```

---

## Limitations and Risks

The 16-song catalog offers limited choices, and the scoring ignores available
attributes such as tempo, valence, danceability, and acousticness. Energy can
contribute up to 2 points, compared with 1 point each for genre and mood, so a
close energy match can outweigh a preferred genre or mood. The recommender has
no diversity or repeat penalty; repeatedly showing similar songs could limit
what listeners discover and create a filter bubble. These limitations are
explored further in the model card.

---

## Reflection

For more detail on the model’s use, evaluation, limitations, and future work, see:

[**Model Card**](model_card.md)

Changing the scoring weights changed which songs ranked highest: increasing
energy’s importance moved Iron Bloom to the top for Aggressive Classical.
Checking Copilot’s incorrect score prediction against the scoring rule showed
why it’s important to verify suggestions with the actual calculation and
program output.
