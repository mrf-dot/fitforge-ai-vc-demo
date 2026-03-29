FitForge AI — Local AI-powered Workout Planner

Overview
FitForge AI is a lightweight, local-first AI-powered workout planner that generates personalized training plans based on user goals, fitness level, and available equipment. It runs locally with a minimal web UI and a clean, extensible backend designed for rapid demos and integration planning with wellness platforms.

Key Features
- AI-generated workouts with warmups, cooldowns, and coaching notes; deterministic fallback if AI is unavailable
- Personalization across goals (General Fitness, Weight Loss, Muscle Gain, Endurance, Flexibility, Strength), fitness levels, and equipment
- Local deployment on port 8080; REST API for integration and automation
- Extensible: Docker-ready, CI-friendly, and plugin architecture for future mobile apps or integrations
- Privacy-first: data and plans can remain on-device; OpenRouter is optional via OPENROUTER_API_KEY

How It Works
1) User inputs goals, level, and equipment via a simple UI
2) Server generates a plan with warmup, 5–7 exercises (name, sets, reps, rest, notes), cooldown, and tips
3) Optional AI path uses OpenRouter to tailor content on the fly; otherwise a deterministic fallback keeps the flow reliable
4) Result is returned as JSON and rendered in the UI for quick demonstration

Getting Started (Local Dev)
1) Install dependencies: pip install -r requirements.txt
2) Copy example env and configure API key:
   - cp .example_env .env
   - Edit .env to set OPENROUTER_API_KEY="your-real-api-key"
3) Run: python app.py
4) Open: http://localhost:8080

API
- POST /api/workout
  Request: {"goals": "muscle gain", "level": "intermediate", "equipment": "dumbbells"}
  Response: {"plan_name": "Muscle Gain Plan", "description": "...", "warmup": "...", "exercises": [...], "cooldown": "...", "tips": ["..."]}

- GET /health
  Returns server status and AI configuration

Project Structure
fitforge-ai/
├── app.py              # Flask app + AI workout engine
├── templates/
│   └── index.html      # Web UI
├── static/             # Static assets
├── requirements.txt    # Python dependencies
├── .example_env        # Example environment config
├── README.md            # This document (human-friendly, developer-focused)
├── CHANGELOG.md         # Version history
├── LICENSE.md           # Open source license
├── CONTRIBUTING.md        # Contribution guidelines
├── CODE_OF_CONDUCT.md     # Community guidelines

License
MIT
"}```  to=functions.execute  codeതമ  { 