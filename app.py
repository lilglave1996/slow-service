"""slow-service — a deliberately slow Flask API for BE105 Unit 3.

Every nutrition lookup takes about one second, on purpose. It stands in for any
real service that makes you wait: a payment provider, a third-party API, a
database on another machine. Call it five times in a row and you wait five
seconds. Call it five times *concurrently* and you wait one. That gap is the
whole point of asynchronous programming.

Runs on port 5001 so it can sit next to the recipe API on 5000.
"""

import random
import time

from flask import Flask, jsonify

app = Flask(__name__)

DELAY_SECONDS = 1.0

# Fake but stable nutrition numbers per 100 g. Unknown ingredients get a
# deterministic pseudo-random entry so every lookup "succeeds".
NUTRITION = {
    "eggs": {"calories": 155, "protein_g": 13.0, "carbs_g": 1.1, "fat_g": 11.0},
    "tomatoes": {"calories": 18, "protein_g": 0.9, "carbs_g": 3.9, "fat_g": 0.2},
    "peppers": {"calories": 31, "protein_g": 1.0, "carbs_g": 6.0, "fat_g": 0.3},
    "onion": {"calories": 40, "protein_g": 1.1, "carbs_g": 9.3, "fat_g": 0.1},
    "cumin": {"calories": 375, "protein_g": 17.8, "carbs_g": 44.2, "fat_g": 22.3},
    "paprika": {"calories": 282, "protein_g": 14.1, "carbs_g": 54.0, "fat_g": 12.9},
    "rolled oats": {"calories": 389, "protein_g": 16.9, "carbs_g": 66.3, "fat_g": 6.9},
    "milk": {"calories": 42, "protein_g": 3.4, "carbs_g": 5.0, "fat_g": 1.0},
    "yogurt": {"calories": 59, "protein_g": 10.0, "carbs_g": 3.6, "fat_g": 0.4},
    "chia seeds": {"calories": 486, "protein_g": 16.5, "carbs_g": 42.1, "fat_g": 30.7},
    "honey": {"calories": 304, "protein_g": 0.3, "carbs_g": 82.4, "fat_g": 0.0},
    "habaneros": {"calories": 40, "protein_g": 1.9, "carbs_g": 8.8, "fat_g": 0.4},
    "garlic": {"calories": 149, "protein_g": 6.4, "carbs_g": 33.1, "fat_g": 0.5},
    "vinegar": {"calories": 21, "protein_g": 0.0, "carbs_g": 0.9, "fat_g": 0.0},
    "bread": {"calories": 265, "protein_g": 9.0, "carbs_g": 49.0, "fat_g": 3.2},
}


def lookup(ingredient):
    key = ingredient.strip().lower()
    if key in NUTRITION:
        return dict(NUTRITION[key])
    rng = random.Random(key)  # same fake numbers every time for the same name
    return {
        "calories": rng.randint(20, 400),
        "protein_g": round(rng.uniform(0, 20), 1),
        "carbs_g": round(rng.uniform(0, 60), 1),
        "fat_g": round(rng.uniform(0, 30), 1),
    }


@app.get("/")
def index():
    return jsonify(
        {
            "service": "slow-service",
            "delay_seconds": DELAY_SECONDS,
            "try": "/nutrition/eggs",
            "health": "/health",
        }
    )


@app.get("/health")
def health():
    # Fast on purpose: health checks must not wait.
    return jsonify({"status": "ok"})


@app.get("/nutrition/<ingredient>")
def nutrition(ingredient):
    time.sleep(DELAY_SECONDS)  # the wait every caller feels
    data = lookup(ingredient)
    data["ingredient"] = ingredient.strip().lower()
    data["per"] = "100 g"
    data["took_seconds"] = DELAY_SECONDS
    return jsonify(data)


if __name__ == "__main__":
    # threaded=True is Flask's default; each request still sleeps for a second,
    # so a caller that asks one thing at a time waits N seconds for N lookups.
    app.run(port=5001, debug=True)
