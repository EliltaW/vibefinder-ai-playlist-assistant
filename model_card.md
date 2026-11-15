# Model Card: VibeFinder — AI Playlist Assistant

## 1. System Overview

VibeFinder 2.0 extends my Module 3 Music Recommender Simulation.
It combines Gemini language-model calls with Python retrieval,
weighted ranking, validation, and fallback explanations.

The configured model used during development was
`gemini-3.5-flash-lite`. I did not train or fine-tune it.

## 2. Intended Use

The system helps a listener explore a small music catalog by describing
their preferred genre, mood, and energy in plain language.

It is a classroom and portfolio application. It does not stream music,
guarantee enjoyment, infer personality, or provide music therapy.

## 3. Data

The catalog contains 16 songs: 10 starter songs and six fictional songs
added with Copilot's help during the original project. Those additions
introduced classical, hip-hop, country, reggae, metal, and blues.

Each record includes an ID, title, artist, genre, mood, energy, tempo,
valence, danceability, and acousticness. The ranking uses only genre,
mood, and energy.

The catalog contains no listener ratings or listening history that
could establish whether people actually enjoy the recommendations.

## 4. How the System Works

1. Python validates the listener's request.
2. Gemini extracts genre, mood, and energy as JSON.
3. Python validates and normalizes those preferences.
4. Retrieval selects songs matching at least the genre or mood.
5. Python ranks those songs using the original scoring function.
6. Gemini generates explanations using retrieved song attributes
   and scoring reasons.
7. Python checks explanation IDs and nonempty text before display.

The scoring rule awards one point for genre, one for mood, and up to
two for energy similarity:

`score = genre_match + mood_match + 2 × (1 − abs(song_energy − target_energy))`

Scores are preference-match scores, not probabilities of enjoyment.

The explanation stage uses retrieval-augmented generation (RAG).
Retrieval uses attribute filtering and weighted ranking, not embeddings.

## 5. Guardrails and Reliability Measures

- Blank requests and requests longer than 500 characters are rejected
  before calling Gemini.
- Genre and mood must be nonempty strings.
- Energy must be a valid number between zero and one.
- Requests with invalid extracted preferences stop before retrieval.
- No matching songs produce a helpful message and skip explanation
  generation.
- Generated explanations must contain exactly the retrieved song IDs
  and nonempty text.
- Handled explanation failures trigger rule-based scoring explanations.
- Logs report retrieval counts, validation failures, and fallback use.
- The API key is stored locally in `.env`, which Git ignores.

These checks do not prove that Gemini correctly interpreted the request
or that every explanation is factually supported.

## 6. Limitations and Biases

The small catalog does not represent the full variety of music,
cultures, genres, or listener preferences. Its genre and mood labels
simplify subjective qualities.

Energy contributes up to twice as many points as either genre or mood.
This design can prioritize energy similarity over another preference.

The system accepts only one genre, one mood, and one energy target.
It does not fully support exclusions, multiple preferences, or strict
requests such as "only lofi." A song can qualify by matching either
genre or mood.

Gemini may misinterpret vague language, miss contradictions, or return
unsupported explanations. Valid JSON and valid song IDs do not establish
semantic correctness.

Ranking is deterministic for identical validated preferences and catalog
data, but Gemini's interpretations and wording can vary between runs.

There is no diversity or repeat penalty. Repeatedly recommending similar
songs could narrow what a listener discovers and create a filter bubble.

The test suite covers selected behaviors, not every network, API,
catalog, or malformed-response failure.

## 7. Possible Misuse and Prevention

Someone could present the recommendations as guaranteed indicators of
a person's taste, personality, or emotional needs. To reduce this risk,
the documentation limits the system to catalog exploration, and the
explanation prompt prohibits invented health benefits.

Someone could submit instructions intended to make Gemini invent facts
or ignore its task. The prompts tell Gemini to treat supplied content
as data, and Python validates preferences and explanation IDs.
These measures reduce some risks but do not guarantee resistance to
prompt injection or unsupported claims.

An exposed API key could allow unauthorized API usage. I keep the key
in an ignored `.env` file and provide only a placeholder in
`.env.example`.

Requests are sent to an external AI provider. Users should describe
music preferences without including sensitive personal information.

## 8. Reliability Testing and Results

The automated test command was:

`python -m pytest -q`

Observed result:

`28 passed in 0.72s`

The tests cover original ranking behavior, input and preference
validation, retrieval filtering, and a simulated explanation failure.
They do not make live Gemini calls.

| Scenario                                 | Expected behavior                               | Observed result                                                            | Method                                |
| ---------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------- |
| Calm lofi for studying, low energy       | Extract preferences and explain retrieved songs | Pass — four songs returned with explanations acknowledging partial matches | Live run and manual review            |
| Empty request                            | Reject before an AI call                        | Pass — helpful message and graceful exit                                   | Live application run                  |
| Zydeco, triumphant, energy 0.6           | Report no catalog matches                       | Pass — zero results and no explanation call                                | Live application run                  |
| Capital of France question               | Avoid unrelated recommendations                 | Pass — extracted preferences rejected                                      | Live application run                  |
| Explanation generation raises ValueError | Display scoring reasons                         | Pass — fallback output verified                                            | Automated test with simulated failure |

The unrelated-input message could be clearer: it asks for a valid genre
rather than explaining that the application needs a music request.

These results show success on the tested cases, not an overall accuracy
rate. More diverse requests, repeated runs, and additional human reviewers
would be needed for broader conclusions.

Reproducible commands and live outputs are included in README.md.

## 9. What Surprised Me During Testing

A useful discovery was that the original top-five ranking included
Paper Moon for the calm-lofi request even though it matched neither
genre nor mood. It appeared because energy contributed points and the
function returned the five highest-scoring songs.

Adding a retrieval rule requiring at least a genre or mood match removed
Paper Moon and returned four songs instead. This showed me that a ranking
function can calculate scores correctly while still producing results
that need a better selection rule.

## 10. Collaboration With AI

I used ChatGPT to help plan the architecture, draft implementation code,
suggest tests, debug errors, and organize documentation. I added the code
in VS Code, ran tests and live requests, and reviewed the outputs.

### Suggestion I Accepted

I accepted the suggestion to show rule-based scoring explanations when
AI explanation generation fails. The songs have already been retrieved
and ranked by Python, so the application can still provide useful results
without Gemini's explanation.

I verified this behavior with an automated test that simulated an
explanation failure and checked that the scoring reasons appeared.

### Suggestion I Revised

The AI suggested a parameterized test using `request` as a parameter
name. Running the test revealed that pytest reserves this name.

I changed it to `user_input` and reran the tests successfully. This
showed me why AI-generated code needs to be executed and checked
rather than accepted solely because it looks correct.

## 11. Future Improvements

- Ask clearer follow-up questions when preferences are missing.
- Support multiple genres, exclusions, and strict preference constraints.
- Expand the catalog and evaluate recommendations with multiple listeners.
- Add diversity controls and listener-adjustable scoring weights.
- Test more API failures and malformed AI responses.
- Evaluate explanation accuracy across more requests and repeated runs.
