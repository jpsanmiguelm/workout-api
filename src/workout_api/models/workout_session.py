from datetime import datetime

from pydantic import Field

from workout_api.models.base import CamelModel


class SetLog(CamelModel):
    set_number: int = Field(ge=1)
    reps: int = Field(ge=0)
    weight_kg: float | None = Field(default=None, ge=0)
    rpe: float | None = Field(default=None, ge=1, le=10)
    negative_seconds: int | None = Field(default=None, ge=0)
    completed_at: datetime


class ExerciseLog(CamelModel):
    exercise_id: str
    sets: list[SetLog] = []

    @property
    def average_rpe(self) -> float | None:
        rpes = [s.rpe for s in self.sets if s.rpe is not None]
        if len(rpes) == 0:
            return None
        return sum(rpes) / len(rpes)

    @property
    def max_weight_kg(self) -> float | None:
        return max(
            (log.weight_kg for log in self.sets if log.weight_kg is not None),
            default=None,
        )


class WorkoutSession(CamelModel):
    id: str
    routine_id: str
    date: datetime
    exercise_logs: list[ExerciseLog] = []
    duration_seconds: int | None = Field(default=None, ge=0)
    completed: bool = False
