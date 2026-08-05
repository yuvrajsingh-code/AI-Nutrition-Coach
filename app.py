"""Gradio web interface for the AI Nutrition Coach."""
import os
import re
import gradio as gr
from agent import run_nutritionist_pipeline


def process_meal(username, meal_desc, dietary_preference):
    """Gradio callback: run the pipeline and format its output for the UI."""
    if not username.strip() or not meal_desc.strip():
        return "⚠️ Please enter both a username and a meal description.", None

    result = run_nutritionist_pipeline(username, meal_desc, dietary_preference)

    # Prefer the calories value returned directly by the pipeline; fall back
    # to parsing the log confirmation string.
    calories = result.get("calories", 0)
    if not calories and result.get("logged"):
        match = re.search(r"(\d+)\s*calories", result["logged"], re.IGNORECASE)
        if match:
            calories = match.group(1)

    output = f"""# 🍽️ Meal Analysis Results

## Meal Details
- **User:** {username}
- **Meal Description:** {meal_desc}
- **Dietary Preference:** {dietary_preference}
- **Estimated Calories:** {calories}

## Log Confirmation
{result['logged']}

## Next Meal Suggestion
{result['next_meal_suggestion']}
"""

    image_path = result["meal_image"]
    is_valid_image = (
        isinstance(image_path, str)
        and image_path.endswith(".png")
        and os.path.exists(image_path)
    )
    return output, (image_path if is_valid_image else None)


with gr.Blocks(theme=gr.themes.Soft(), title="AI Nutrition Coach") as demo:
    gr.Markdown(
        """
        # 🍽️ AI Nutrition Coach
        Log a meal, get a calorie estimate, receive a healthy follow-up
        suggestion, and see a generated image of it.
        """
    )

    with gr.Row():
        with gr.Column():
            username = gr.Textbox(label="Username", placeholder="Enter your name")
            meal_desc = gr.Textbox(
                label="Meal Description",
                placeholder="e.g., Chicken salad with olive oil dressing",
                lines=2,
            )
            dietary_preference = gr.Dropdown(
                choices=["vegetarian", "vegan", "non-vegetarian", "gluten-free"],
                label="Dietary Preference",
                value="non-vegetarian",
            )
            submit_btn = gr.Button("Process Meal", variant="primary")

        with gr.Column():
            output = gr.Markdown(label="Results")
            image_output = gr.Image(label="Suggested Meal", type="filepath")

    submit_btn.click(
        fn=process_meal,
        inputs=[username, meal_desc, dietary_preference],
        outputs=[output, image_output],
    )


if __name__ == "__main__":
    demo.launch()
