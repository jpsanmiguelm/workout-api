from pydantic import Field

from workout_api.models.base import CamelModel


class RoutineExercise(CamelModel):
    exercise_id: str
    order: int = Field(ge=1)
    sets_override: int | None = None
    reps_min_override: int | None = None
    reps_max_override: int | None = None
    rest_seconds_override: int | None = None
    superset_with_next: bool = False
    note: str | None = None


class Routine(CamelModel):
    id: str
    name: str
    focus: str | None = None
    order: int = Field(ge=1)
    scheduled_weekday: int | None = Field(default=None, ge=1, le=7)
    archived: bool = False
    exercises: list[RoutineExercise]

    @property
    def letter(self) -> str:
        return chr(64 + min(max(self.order, 1), 26))

    @property
    def display_title(self) -> str:
        return self.focus if self.focus is not None else self.name
