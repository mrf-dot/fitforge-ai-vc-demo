"""
FitForge — AI-Powered Personal Workout Generator
Copyright 2026. All rights reserved.
"""
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import json
import requests
import random

load_dotenv()

app = Flask(__name__)

# ─── Configuration ────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
AI_MODEL = "anthropic/claude-sonnet-4"


# ─── AI Workout Engine ───────────────────────────────────
def generate_workout(goals: str, level: str, equipment: str) -> dict:
    """Generate a personalized workout plan using AI via OpenRouter."""
    if not OPENROUTER_API_KEY:
        print("[FitForge] No API key found — using fallback generator")
        return _fallback_workout(goals, level, equipment)

    system_prompt = """You are FitForge AI, an expert certified personal trainer.
Generate a complete, personalized workout plan. Return ONLY valid JSON with this exact schema:
{
  "plan_name": "string",
  "description": "string (2-3 sentences)",
  "duration": "string (estimated total time)",
  "warmup": "string (detailed warmup routine)",
  "exercises": [
    {
      "name": "string",
      "muscle_group": "string",
      "sets": number,
      "reps": "string",
      "rest": "string",
      "notes": "string (form cues and tips)"
    }
  ],
  "cooldown": "string (detailed cooldown routine)",
  "tips": ["string (3-5 actionable tips)"]
}
No markdown, no explanation — pure JSON only."""

    user_prompt = f"""Create a workout plan with these parameters:
- Primary Goal: {goals}
- Fitness Level: {level}
- Available Equipment: {equipment or 'bodyweight only'}

Requirements:
- Include 5-7 exercises appropriate for the fitness level
- Provide specific sets, reps, and rest periods
- Include detailed form cues in the notes
- Make the plan feel personalized and motivating"""

    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://fitforge.ai",
                "X-Title": "FitForge AI",
            },
            json={
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 2048,
            },
            timeout=45,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()

        # Strip markdown code fences if the model wraps them
        if content.startswith("```"):
            content = "\n".join(content.split("\n")[1:])
        if content.endswith("```"):
            content = content.rsplit("```", 1)[0]

        return json.loads(content.strip())

    except Exception as e:
        print(f"[FitForge] AI generation failed: {e}")
        return _fallback_workout(goals, level, equipment)


def _fallback_workout(goals: str, level: str, equipment: str) -> dict:
    """Deterministic fallback when the AI service is unavailable."""
    pool = [
        {"name": "Push-ups", "muscle_group": "Chest", "sets": 3, "reps": "12-15", "rest": "60s", "notes": "Keep core tight, elbows at 45°"},
        {"name": "Goblet Squats", "muscle_group": "Legs", "sets": 4, "reps": "10-12", "rest": "90s", "notes": "Drive through heels, chest up"},
        {"name": "Walking Lunges", "muscle_group": "Legs", "sets": 3, "reps": "10/leg", "rest": "60s", "notes": "Knee tracks over ankle"},
        {"name": "Plank Hold", "muscle_group": "Core", "sets": 3, "reps": "45s", "rest": "30s", "notes": "Neutral spine, squeeze glutes"},
        {"name": "Dumbbell Rows", "muscle_group": "Back", "sets": 3, "reps": "10-12", "rest": "60s", "notes": "Squeeze shoulder blade at top"},
        {"name": "Mountain Climbers", "muscle_group": "Full Body", "sets": 3, "reps": "20/side", "rest": "45s", "notes": "Maintain plank position"},
        {"name": "Burpees", "muscle_group": "Full Body", "sets": 3, "reps": "8-10", "rest": "90s", "notes": "Full extension at top"},
        {"name": "Overhead Press", "muscle_group": "Shoulders", "sets": 3, "reps": "10-12", "rest": "60s", "notes": "Core braced, no arching"},
    ]
    return {
        "plan_name": f"{goals.title()} Plan",
        "description": f"A {level}-level workout targeting {goals}. This plan uses {equipment or 'bodyweight'} exercises for maximum results.",
        "duration": "45-55 minutes",
        "warmup": "5 min light cardio (jumping jacks or jogging in place) + arm circles, leg swings, hip openers",
        "exercises": random.sample(pool, k=min(6, len(pool))),
        "cooldown": "5 min walking + hamstring stretch, quad stretch, chest opener, child's pose (30s each)",
        "tips": [
            "Stay hydrated — aim for 500ml water during the workout",
            "Focus on form over speed, especially as a " + level,
            "Rest 48 hours before training the same muscle group",
            "Track your progress — increase reps or weight each week",
        ],
    }


# ─── Routes ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/workout", methods=["POST"])
def api_workout():
    data = request.get_json(force=True) or {}
    goals = data.get("goals", "general fitness")
    level = data.get("level", "intermediate")
    equipment = data.get("equipment", "")
    plan = generate_workout(goals, level, equipment)
    return jsonify(plan)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "ai_enabled": bool(OPENROUTER_API_KEY),
    })


# ─── Entry Point ─────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    print(f"\n🏋️  FitForge AI running → http://localhost:{port}")
    print(f"   AI: {'✅ Enabled' if OPENROUTER_API_KEY else '❌ Disabled (no API key)'}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
