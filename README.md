# 🍽️ AI Nutrition Coach

An AI-powered nutrition coach. Log a meal, get a calorie estimate from a live web search, receive a healthy follow-up suggestion, and view an AI-generated image of the recommended dish — all through a simple Gradio interface.

**Runs entirely on free APIs. No credit card required.**

---

## ✨ Features

- **Web-search calorie lookup** — Uses live web grounding to fetch accurate calorie counts.
- **LLM fallback** — Falls back to a chat-based estimate if web search is unavailable.
- **Meal logger** — Records each meal with a timestamp under the user's name.
- **Next-meal suggester** — Recommends a follow-up meal matching the user's dietary preference (vegetarian, vegan, non-vegetarian, gluten-free), with a short recipe.
- **Image generation** — Renders an appetizing image of the suggested meal.
- **Gradio UI** — Clean web frontend, no framework knowledge required.

---

## 📁 Project Structure

```
ai-nutrition-coach/
├── generated_images/           # Saved meal images (gitignored)
│   └── .gitkeep
├── tools/
│   ├── __init__.py             # Package exports
│   ├── configs.py              # AI client init and setup
│   ├── image_gen.py            # Image generation via Pollinations.ai
│   ├── next.py                 # Fallback estimator, logger, next-meal suggester
│   └── web_search.py           # Web-search-grounded calorie lookup
├── agent.py                    # Main pipeline chaining all tools
├── app.py                      # Gradio UI (entry point)
├── requirements.txt            # Python dependencies
├── .env.example                # Template for env vars
├── .gitignore
├── LICENSE                     # MIT
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python **3.10+** (tested on 3.10, 3.11, 3.12)
- A **free** Google AI Studio API key. Sign in at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) with any Google account and click **Create API key**. No credit card, no billing setup required for the free tier.
- Image generation uses [Pollinations.ai](https://pollinations.ai) — no signup or key needed.

### 2. Clone the repo

```bash
git clone https://github.com/yuvrajsingh-code/ai-nutrition-coach.git
cd ai-nutrition-coach
```

### 3. Create a virtual environment

**Using `venv`:**

```bash
python -m venv .venv
source .venv/bin/activate         # macOS / Linux
# .venv\Scripts\activate          # Windows PowerShell
```

**Using `conda`:**

```bash
conda create -n nutrition-coach python=3.11 -y
conda activate nutrition-coach
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add your API key

```bash
cp .env.example .env
```

Then edit `.env` and set:

```
AI_API_KEY=your_actual_key_here
```

### 6. Run the app

```bash
python app.py
```

Open the URL Gradio prints (usually `http://127.0.0.1:7860`) in your browser.

---

## 🧠 How It Works

The pipeline in `agent.py` runs these steps for every meal:

1. **Calorie lookup** — `search_calories()` uses Gemini with Google Search grounding to fetch the meal's calorie count from the live web. If that returns nothing, the pipeline falls back to `estimate_calories()`, which uses a plain chat completion.
2. **Meal logging** — `log_meal()` sends the user, meal, calories, and timestamp to a lightweight chat model that returns a natural-language confirmation.
3. **Next-meal suggestion** — `suggest_next_meal()` prompts the model to recommend a follow-up meal matching the dietary preference, with a short recipe.
4. **Image generation** — `generate_food_image()` sends the suggestion as a prompt to Pollinations.ai, downloads the returned image, and saves it under `generated_images/`.

Each step's outputs feed the next, and the whole result (calories, log confirmation, suggestion text, image path, tools used) is returned to the Gradio UI as a single dict.

---

## 🔧 Configuration

You can tweak these in `tools/configs.py`:

- `DEFAULT_MODEL` — Model for tasks that benefit from stronger reasoning (default: `gemini-2.5-flash`).
- `FAST_MODEL` — Model for fallback/high-volume tasks with higher rate limits (default: `gemini-2.5-flash-lite`).

Both are available on the free tier at time of writing. If Google changes free-tier eligibility, swap the model IDs here.

---

## 🐛 Troubleshooting

**`AI_API_KEY is not set`** — You skipped step 5. Make sure `.env` exists in the project root and contains a valid key.

**`ModuleNotFoundError: No module named 'google'`** — Activate your virtualenv and rerun `pip install -r requirements.txt`.

**`429 RESOURCE_EXHAUSTED`** — You've hit Gemini's free-tier rate limit (roughly 10 requests/minute for Flash). Wait a minute and try again, or switch to `gemini-2.5-flash-lite` everywhere for higher limits.

**Image doesn't appear** — Pollinations.ai occasionally times out or returns a small placeholder. Check the terminal output. The rest of the response (calories, suggestion) will still render.

**Image is slow** — Pollinations generates on-demand; first generation for a new prompt can take 15–30 seconds. Subsequent identical prompts are usually cached and faster.

**`400 INVALID_ARGUMENT` on web search** — Google Search grounding may not be enabled for your key/project. The pipeline automatically falls back to LLM-only estimation, so this still works.

---

## 📚 Extending the Project

Some ideas if you want to build on this:

- **Persistent meal log** — Replace the LLM-based logger with a SQLite database.
- **Daily calorie budget** — Track cumulative calories per user per day and warn when the budget is exceeded.
- **Photo input** — Add an image-upload field and use Gemini's vision to identify meals from photos.
- **Structured nutrition database** — Wrap a nutrition API (USDA FoodData, Nutritionix) as a tool for more reliable numbers.
- **Multi-user history** — Store meal logs per user and show trends over time.

---

## 📄 License

MIT — see [LICENSE](LICENSE).
