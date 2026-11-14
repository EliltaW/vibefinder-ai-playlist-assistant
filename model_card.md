# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a listener’s preferred
genre, mood, and target energy. It assumes the listener can provide one value
for each preference. It is designed for classroom exploration of scoring,
ranking, and recommendation bias. It should not be used to make claims about
a person’s personality or to guarantee which songs they will enjoy.

---

## 3. How the Model Works

The model reads songs from a CSV file and scores each against the listener’s preferences. A matching genre earns 1 point, and a matching mood earns 1 point. Energy earns up to 2 points using twice the energy similarity: `2 × (1 − abs(song energy − target energy))`. An exact energy match earns 2 points. The recommender adds these points, ranks songs from highest to lowest, and explains each recommendation’s score.

## 4. Data

The catalog contains 16 songs: 10 starter songs and 6 fictional songs added
with Copilot’s help. The additions introduced classical, hip-hop, country,
reggae, metal, and blues, along with new moods.

Each song has an ID, title, artist, genre, mood, energy, tempo, valence,
danceability, and acousticness. The recommender scores genre, mood, and
energy. The small catalog offers limited variety and contains no listener
ratings or listening history to show whether people actually enjoy the songs.

---

## 5. Strengths

The recommender gives readable reasons for each score, making its rankings
easy to check. With the original weights, Happy Pop, Chill Lofi, and Intense
Rock each ranked a song matching the requested genre and mood first.
After increasing the energy weight, Iron Bloom ranked first for Aggressive
Classical, matching my expectation for an aggressive, high-energy song.

---

## 6. Limitations and Bias

The catalog contains only 16 songs, so it offers limited choices for each
listener. With the experimental weights, energy can contribute up to 2 points,
while genre and mood contribute 1 point each, allowing a close energy match
to outrank a preferred-genre match. The scoring ignores available attributes
such as tempo, valence, danceability, and acousticness. The system has no
diversity or repeat penalty, so the same profile and catalog produce the
same recommendations each time. Repeated exposure to similar recommendations
could create a filter bubble by limiting the variety of music a listener sees.

---

## 7. Evaluation

I tested Happy Pop, Chill Lofi, Intense Rock, and Aggressive Classical.
For each profile, I examined the top five songs, their scores, and their
explanations. I checked sample scores by hand. The two starter tests passed
before the weight experiment.
After completing the class methods, all three tests passed with the final
weights. The added regression test checks that a better match ranks first
even when supplied second and that its explanation shows the correct points.

With the original weights, I compared every pair of profiles:

- Happy Pop and Chill Lofi had no songs in common in their top five.
  Their preferred genres, moods, and energy levels were different.
- Happy Pop and Intense Rock shared three songs: Sunrise City, Gym Hero,
  and Side Street. Their first choices differed: Sunrise City for Happy Pop
  and Storm Runner for Intense Rock.
- Happy Pop and Aggressive Classical shared Sunrise City and Gym Hero.
  Their high energy targets helped these songs appear in both lists,
  while the genre match put Paper Moon first for Aggressive Classical.
- Chill Lofi and Intense Rock had no top-five songs in common.
  The profiles favored different genres, moods, and energy levels.
- Chill Lofi and Aggressive Classical had no top-five songs in common.
  Chill Lofi favored calm songs, while Aggressive Classical combined
  a classical genre preference with a high energy target.
- Intense Rock and Aggressive Classical shared four songs: Gym Hero,
  Iron Bloom, Storm Runner, and Sunrise City. Their similar energy targets
  favored many of the same songs, but their different genre and mood
  preferences changed the order.

I then reduced the genre weight from 2 to 1 and increased the energy
weight from 1 to 2. For Aggressive Classical, Iron Bloom moved from second
at 2.00 to first at 3.00, while Paper Moon dropped from first at 2.37
to fourth at 1.74. This better matched my expectation for that profile,
so I kept the new weights. Broader listener feedback would be needed
to determine whether this improves recommendations for other people.

---

## 8. Future Work

- Let listeners choose multiple genres and moods and adjust how much each
  preference matters.
- Expand the catalog with more songs per genre and use features such as
  acousticness and danceability in scoring.
- Add a diversity rule to include a wider range of artists or genres
  among the top recommendations.

---

## 9. Personal Reflection

My biggest learning moment was seeing how changing the weights changed
the top recommendation. Paper Moon originally ranked first for Aggressive
Classical. After reducing the genre weight and increasing the energy weight,
Iron Bloom moved to first place. This helped me understand how the importance
we assign to each feature shapes the results.

Copilot helped me implement the functions and suggest profiles to test.
During our review, we caught its incorrect prediction that Iron Bloom would
score 1.00 with the original weights. Checking the mood and energy points
showed that the correct score was 2.00. I learned to verify AI suggestions
with calculations and actual program output. Next, I would try letting
listeners adjust the weights to reflect their own preferences.
