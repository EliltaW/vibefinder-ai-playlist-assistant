# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Streaming platforms can use listening history, patterns from people with similar tastes,
and song features to recommend music. My simulator will use content-based filtering
to compare songs with the listener’s stated preferences.

- **Song** — Uses `genre`, `mood`, and `energy` for scoring. The `title` identifies
  the song in the results.
- **UserProfile** stores the listener’s preferred `genre` and `mood`, and their target `energy`.
- **Recommender** — A matching genre earns 2 points, and a matching mood earns
  1 point. To calculate energy points, subtract the absolute difference between
  the song’s energy and the listener’s target energy from 1. Add the three
  point values to get the song’s total score.
- **Recommendations** — The recommender sorts songs from highest to lowest
  total score and returns the top results.

**Data flow:** The program reads songs from `data/songs.csv`, scores each song
against the listener’s preferences, and shows the five highest-scoring songs
when the listener requests five recommendations.
**Potential bias:** A song outside the listener’s favorite genre can earn at
most 2 points, even with a perfect mood and energy match. This can make it
harder to discover songs from other genres that fit the listener’s mood.

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

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

````
## Sample Recommendation Output

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
````

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
