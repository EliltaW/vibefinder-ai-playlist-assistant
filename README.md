# VibeFinder — AI Playlist Assistant

## Project Summary

VibeFinder turns a listener's plain-language music request into song
recommendations from a small local catalog. It uses Gemini to interpret
preferences, Python to retrieve and rank matching songs, and Gemini again
to explain the results using the retrieved song data.

The goal is to make recommendations understandable while handling invalid
requests, missing matches, and explanation failures gracefully.

## Original Project

This project extends my Module 3 **Music Recommender Simulation
(VibeFinder 1.0)**:

https://github.com/EliltaW/ai110-module3show-musicrecommendersimulation-starter

The original application ranked a 16-song catalog using predefined listener
profiles with genre, mood, and energy preferences. It displayed the top
songs with numerical scores and rule-based explanations, allowing me to
explore how scoring weights affected recommendations.

The final project adds natural-language input, Gemini integration,
retrieval filtering, generated explanations, validation, logging,
and fallback behavior.

## How the AI Works

1. The listener describes the music they want.
2. Python rejects blank requests and requests longer than 500 characters.
3. Gemini extracts genre, mood, and target energy as JSON.
4. Python validates the extracted values.
5. The retriever selects songs matching at least the genre or mood.
6. The existing scoring function ranks those candidates.
7. Gemini receives the retrieved song attributes and scoring reasons,
   then generates an explanation for each song.
8. Python checks that the explanations contain exactly the retrieved
   song IDs and nonempty text before displaying them.

This is a retrieval-augmented generation (RAG) workflow: retrieved catalog
data supplies the context for generated explanations. Retrieval uses
attribute filtering and weighted ranking, rather than vector embeddings.

### Ranking

- Genre match: 1 point.
- Mood match: 1 point.
- Energy similarity: `2 × (1 − abs(song energy − target energy))`.

The system returns up to five qualifying songs. Scores measure agreement
with the scoring rule; they are not probabilities or confidence estimates.

### Guardrails and Fallbacks

- Invalid input or invalid extracted preferences stop the workflow.
- No matching songs produce a helpful message without an explanation call.
- Missing or extra song IDs and empty explanations are rejected.
- If explanation generation fails in a handled way, the application
  displays its rule-based scoring reasons.
- Logs report retrieval counts, validation failures, and fallback use.

Song-ID checks verify which songs the explanations reference. They do not
prove that every sentence is accurate or that the listener will enjoy
the recommendations.

## Architecture Overview

The system separates input validation, AI calls, retrieval/ranking, and
application orchestration into Python modules:

| File                 | Responsibility                                               |
| -------------------- | ------------------------------------------------------------ |
| `src/main.py`        | Runs the interactive workflow and handles errors             |
| `src/ai_client.py`   | Extracts preferences and generates grounded explanations     |
| `src/guardrails.py`  | Validates requests and extracted preferences                 |
| `src/recommender.py` | Loads, filters, scores, and ranks catalog songs              |
| `data/songs.csv`     | Stores the song catalog                                      |
| `tests/`             | Checks ranking, validation, retrieval, and fallback behavior |

Architecture diagram source: [diagrams/architecture.mmd](diagrams/architecture.mmd).

Automated tests check defined behaviors. Human review checks whether
the generated explanations accurately describe matches and mismatches.

---

## Getting Started

### Prerequisites

- Python 3.10 or newer. Development was tested with Python 3.13.
- A Gemini API key and access to the configured model.
- Internet access for Gemini calls.

### 1. Clone the repository

```bash
git clone https://github.com/EliltaW/vibefinder-ai-playlist-assistant.git
cd vibefinder-ai-playlist-assistant
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Gemini

Create an API key in [Google AI Studio](https://aistudio.google.com/apikey).

Copy `.env.example` to a new file named `.env` in the project root.
Replace the placeholder key in `.env` with your own key:

```dotenv
GEMINI_API_KEY=your_actual_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Keep `.env` private. It is excluded from Git through `.gitignore`.

The model above was used during development. Model availability and
free-tier limits can change; check your project's Google AI Studio dashboard.

### 5. Run the application

From the project root:

```bash
python -m src.main
```

At the prompt, enter a request such as:

```text
I want calm lofi music for studying, with low energy.
```

A successful recommendation run normally makes two Gemini generation
calls: one to extract preferences and one to explain retrieved songs.
Blank input is rejected before any API call. A request with no catalog
matches skips the explanation call.

### Running Tests

```bash
python -m pytest -q
```

Observed result during development:

```text
28 passed in 0.72s
```

The automated tests cover the original ranking behavior, input and
preference validation, retrieval filtering, and fallback explanations.

These tests do not make live Gemini calls. The fallback test simulates
an explanation failure while exercising the real application workflow.
Live execution examples are documented separately below.

---

## Sample Interactions and Execution Evidence

These examples were observed while running:

```bash
python -m src.main
```

SDK HTTP logs are omitted for readability. AI wording and interpreted
energy values may vary between runs.

### Example 1: Successful Recommendation

```text
VibeFinder — AI Playlist Assistant
Describe the music you want: I want calm lofi music for studying, with low energy.

Interpreted preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.2}
INFO: Retrieved 4 matching songs.
INFO: AI explanations passed song-ID and text checks.

Library Rain — Score: 3.70
AI explanation: This song matches the preferred lofi genre and chill mood, with anenergy level close to your preference.

Midnight Coding — Score: 3.56
AI explanation: It aligns with the lofi genre and chill mood, though the energy level is slightly higher than requested.

Spacewalk Thoughts — Score: 2.84
AI explanation: While it features a chill mood and a similar energy level, there is a genre mismatch since it is ambient instead of lofi.

Focus Flow — Score: 2.60
AI explanation: This track fits the lofi genre and has a close energy level, but there is a mood mismatch as it is focused rather than chill.
```

This run demonstrates the complete RAG workflow: preference extraction,
catalog retrieval and ranking, and explanations generated from retrieved
attributes and scoring reasons.

### Example 2: Empty Input

The user pressed Enter without entering a request.

```text
VibeFinder — AI Playlist Assistant
Describe the music you want:
WARNING: Request or preference validation failed.
Please check your request or setup: Please describe the music you want.
```

The request was rejected before calling Gemini.

### Example 3: No Catalog Matches

```text
VibeFinder — AI Playlist Assistant
Describe the music you want: I want zydeco music with a triumphant mood and energyof 0.6.

Interpreted preferences: {'genre': 'zydeco', 'mood': 'triumphant', 'energy': 0.6}
INFO: Retrieved 0 matching songs.
No songs match your genre or mood. Try different preferences.
```

Gemini preserved the requested preferences. Retrieval returned no matches,
and the application skipped explanation generation.

### Example 4: Unrelated Request

```text
VibeFinder — AI Playlist Assistant
Describe the music you want: What is the capital of France?
WARNING: Request or preference validation failed.
Please check your request or setup: Please provide a valid genre.
```

The returned preferences failed validation, so the application did not
recommend songs. The message could be improved to explain more clearly
that the request must describe music preferences.

## Testing and Evaluation

### Automated Tests

Command:

```bash
python -m pytest -q
```

Observed output:

```text
28 passed in 0.72s
```

Tests cover:

- Original recommendation ranking and scoring explanations.
- Whitespace cleanup and rejection of blank or overlong requests.
- Preference normalization and rejection of missing or invalid values.
- Energy boundaries, including rejection of booleans, NaN, and infinity.
- Retrieval that requires a genre or mood match.
- Empty retrieval results when neither preference matches.
- Rule-based fallback when explanation generation raises a simulated error.

The automated suite runs without live Gemini calls. It does not establish
the accuracy of Gemini's interpretation or generated explanations.

### Structured Evaluation Results

| Test input or scenario                   | Evaluation criteria                                                                      | Observed result                                                                | Method                                |
| ---------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------- |
| Calm lofi for studying, low energy       | Extract suitable preferences, retrieve catalog songs, and explain matches and mismatches | Pass — four songs returned; explanations acknowledged genre or mood mismatches | Live run and manual review            |
| Empty input                              | Reject gracefully before calling Gemini                                                  | Pass — validation message, no generation call                                  | Live application run                  |
| Zydeco, triumphant, energy 0.6           | Preserve preferences and report no matches without inventing songs                       | Pass — zero matches; explanation call skipped                                  | Live run and manual review            |
| Capital of France question               | Avoid producing music recommendations for unrelated input                                | Pass — preferences rejected; message could be clearer                          | Live application run                  |
| Explanation generation raises ValueError | Display rule-based reasons instead of failing                                            | Pass — fallback output verified                                                | Automated test with simulated failure |

These are a small set of examples, not a measured overall accuracy rate.
More varied requests and repeated live runs would be needed to assess
general reliability.

### What Testing Revealed

The original top-five ranking included Paper Moon for the calm-lofi request
even though it matched neither genre nor mood. Adding a retrieval filter
removed that result and returned four qualifying songs instead.

The initial AI-generated test used `request` as a pytest parameter name.
Pytest rejected it because that name is reserved. Renaming it to
`user_input` fixed test collection. A separate indentation error introduced
while adding tests was also corrected.

## Design Decisions and Trade-offs

- **Reuse the original scoring logic:** Python calculates scores, keeping
  ranking inspectable and testable.
- **Retrieve before generating explanations:** Gemini receives only the
  retrieved song attributes and scoring reasons as context for its
  explanations.
- **Require a genre or mood match:** This avoids filling the list with
  energy-only matches, but may exclude songs a listener could enjoy.
- **Allow partial matches:** A song can qualify through either genre or mood.
  This offers variety, but does not enforce requests such as "only lofi."
- **Separate interpretation from explanation:** Two AI calls keep their
  responsibilities clear, at the cost of additional latency and quota use.
- **Validate generated output:** Python checks preference values and
  explanation IDs, but these checks cannot prove semantic accuracy.
- **Provide a fallback:** Handled explanation failures use scoring reasons.
  Preference-extraction failures stop the workflow because valid
  preferences are needed for ranking.

## Limitations and Future Improvements

- The catalog contains only 16 songs and includes fictional entries.
  The application recommends catalog records; it does not stream music.
- The system supports one genre, one mood, and one energy target.
  Complex requests, exclusions, and multiple preferences are not fully supported.
- Energy can contribute twice as many points as either genre or mood.
- Genre and mood matching depends on labels and normalization.
- A matching genre or mood does not guarantee a suitable overall result.
- AI explanations may contain unsupported claims despite prompting and
  song-ID checks.
- Low temperature does not guarantee identical responses.
- The automated suite does not yet cover every API, network, or malformed
  response failure.
- The application has no diversity or repeat penalty and does not learn
  from listener feedback.

Future work could improve clarification messages, expand failure-case
tests, support explicit exclusions, and evaluate a larger catalog with
feedback from multiple listeners.

## Reflection

This project showed how a rule-based recommender can become an applied AI
system by combining language interpretation, retrieval, generation, and
verification. Testing the complete workflow helped reveal behavior that
individual component checks did not show, such as weak songs appearing
simply to fill a top-five list.

For responsible-AI reflections, limitations, misuse considerations, and
accepted or revised AI suggestions, see [model_card.md](model_card.md).

## Portfolio

Code: https://github.com/EliltaW/vibefinder-ai-playlist-assistant

This project demonstrates my ability to extend an existing Python
application with an AI workflow while keeping core ranking logic
inspectable. I integrated Gemini, added validation and fallback behavior,
and checked results through automated tests and live examples. It also
shows how I verify AI-assisted work and document the limits of what my
tests establish.
