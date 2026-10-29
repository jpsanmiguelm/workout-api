import json
from pathlib import Path

from pydantic import ValidationError

from workout_api.models import Exercise, Routine, WorkoutSession

SAMPLE_SESSION = """
{
  "id": "s-1",
  "routineId": "empuje-a",
  "date": "2026-10-26T07:30:00.000",
  "exerciseLogs": [
    {
      "exerciseId": "press-plano-mancuernas",
      "sets": [
        {"setNumber": 1, "reps": 10, "weightKg": 22.5, "rpe": 7.5, "negativeSeconds": null, "completedAt": "2026-10-26T07:35:10.000"},
        {"setNumber": 2, "reps": 9, "weightKg": 22.5, "rpe": 8.5, "negativeSeconds": null, "completedAt": "2026-10-26T07:38:02.000"},
        {"setNumber": 3, "reps": 8, "weightKg": 20, "rpe": null, "negativeSeconds": null, "completedAt": "2026-10-26T07:41:00.000"}
      ]
    }
  ],
  "durationSeconds": 3120,
  "completed": true
}
"""


def main() -> None:
    raw_exercises = json.loads(Path("data/exercises.json").read_text(encoding="utf-8"))
    exercises = [Exercise.model_validate(item) for item in raw_exercises]
    print(len(exercises), exercises[0].name, exercises[0].primary_muscle)

    raw_routines = json.loads(Path("data/routines.json").read_text(encoding="utf-8"))
    routines = [Routine.model_validate(item) for item in raw_routines]
    print(
        len(routines),
        [f"{r.letter}:{r.display_title}" for r in routines if not r.archived],
    )

    session = WorkoutSession.model_validate_json(SAMPLE_SESSION)
    log = session.exercise_logs[0]
    print(session.date.weekday(), log.average_rpe, log.max_weight_kg)
    print(session.model_dump_json(by_alias=True)[:60])

    try:
        Exercise.model_validate(
            {**raw_exercises[0], "targetSetsMin": 5, "targetSetsMax": 3}
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
