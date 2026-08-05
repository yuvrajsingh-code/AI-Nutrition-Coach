"""Nutritionist pipeline: chain tools into a full workflow."""
import time
from tools import (
    estimate_calories,
    log_meal,
    suggest_next_meal,
    search_calories,
    generate_food_image,
)


def run_nutritionist_pipeline(username, meal_desc, dietary_preference):
    """Run the full nutrition workflow for a single meal.

    Steps:
      1. Look up calories via web search (fallback to LLM estimation).
      2. Log the meal with a timestamp under the user's name.
      3. Suggest a follow-up meal matching the dietary preference.
      4. Generate an image of the suggested meal.

    Returns a dict with `calories`, `logged`, `next_meal_suggestion`,
    `meal_image`, and `tools_used`.
    """
    tools_used = set()

    # Step 1: Calorie estimation (web search with fallback)
    print(f"Searching calories for: {meal_desc}")
    calories = search_calories(meal_desc)
    tools_used.add("Web Search")

    if calories == 0:
        print("Web search returned no result, falling back to LLM estimation...")
        time.sleep(1)  # gentle throttle between API calls
        calories = estimate_calories(meal_desc)
        tools_used.add("Calorie Estimation")

    print(f"Estimated calories: {calories}")

    # Step 2: Log the meal
    print(f"Logging meal for {username}...")
    time.sleep(1)
    log_response = log_meal(username, meal_desc, calories)
    tools_used.add("Meal Logging")

    # Step 3: Suggest next meal
    print("Generating next meal suggestion...")
    time.sleep(1)
    suggestion = suggest_next_meal(calories, dietary_preference)
    tools_used.add("Next Meal Suggestion")

    # Step 4: Generate image of the suggested meal
    print("Generating image for suggested meal...")
    time.sleep(1)
    meal_image = generate_food_image(suggestion)
    tools_used.add("Image Generation")

    return {
        "calories": calories,
        "logged": log_response,
        "next_meal_suggestion": suggestion,
        "meal_image": meal_image,
        "tools_used": sorted(tools_used),
    }
