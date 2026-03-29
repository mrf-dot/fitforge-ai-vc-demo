# FitForge AI — Local AI-Powered Workout Planner

A lightweight, local-first AI-powered workout planner that generates personalized training plans based on user goals, fitness level, and available equipment. It runs on your machine with a clean web interface and an extensible backend designed for rapid demos and integration planning with wellness platforms.

## Features

- AI-generated workouts with warmups, cooldowns, and coaching notes; deterministic fallback if AI is unavailable
- Personalization across goals (General Fitness, Weight Loss, Muscle Gain, Endurance, Flexibility, Strength), fitness levels, and equipment
- Local deployment on port 8080; REST API for integration and automation
- Extensible: Docker-ready, CI-friendly, and plugin architecture for future mobile apps or integrations
- Privacy-first: data and plans can remain on-device; OpenRouter is optional via OPENROUTER_API_KEY

## How It Works
1) User inputs goals, level, and equipment via a simple UI.
2) Server generates a plan with warmup, 5–7 exercises (name, sets, reps, rest, notes), cooldown, and tips.
3) Optional AI path uses OpenRouter to tailor content on the fly; otherwise a deterministic fallback keeps the flow reliable.
4) Result is returned as JSON and rendered in the UI for quick demonstration.

## Getting Started (Local Dev)

1) Install dependencies: pip install -r requirements.txt
2) Copy example env and configure API key:
   - cp .example_env .env
   - Edit .env to set OPENROUTER_API_KEY="your-real-api-key"
3) Run: python app.py
4) Open: http://localhost:8080

## API

### `POST /api/workout`

Request:
```json
{
  "goals": "muscle gain",
  "level": "intermediate",
  "equipment": "dumbbells"
}
```

Response:
```json
{
  "plan_name": "Muscle Gain Plan",
  "description": "An intermediate-level workout targeting muscle gain.",
  "duration": "45-55 minutes",
  "warmup": "5 min light cardio + dynamic stretches",
  "exercises": [
    {
      "name": "Dumbbell Rows",
      "muscle_group": "Back",
      "sets": 3,
      "reps": "10-12",
      "rest": "60s",
      "notes": "Squeeze shoulder blade at top"
    }
  ],
  "cooldown": "5 min walking + static stretches",
  "tips": ["Stay hydrated", "Focus on form over speed"]
}
```

### `GET /health`

Returns server status and AI configuration.

## Local Development Notes
- The app runs on port 8080 by default. Change via environment if needed.
- The OpenRouter integration is optional; a deterministic fallback is used when API key is absent.
- Secrets (like OPENROUTER_API_KEY) should never be committed.

## License

MIT

## Contact

If you have questions or want to discuss features, reach out via the public repo issues or your preferred contact method.