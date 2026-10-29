from typing import Self

from pydantic import Field, model_validator

from workout_api.models.base import CamelModel
from workout_api.models.muscle_group import MuscleGroup


class Exercise(CamelModel):
    id: str
    name: str = Field(min_length=1)
    description: str = ""
    primary_muscle: MuscleGroup
    secondary_muscles: list[MuscleGroup] = []
    image_url: str | None = None
    video_url: str | None = None
    target_sets_min: int = Field(ge=1)
    target_sets_max: int = Field(ge=1)
    target_reps_min: int = Field(ge=1)
    target_reps_max: int = Field(ge=1)
    is_timed: bool = False
    rest_seconds: int = Field(ge=0)
    target_rpe: float | None = Field(default=None, ge=1, le=10)
    uses_external_weight: bool = True
    tracks_negative_tempo: bool = False

    @model_validator(mode="after")
    def check_set_ranges(self) -> Self:
        if self.target_sets_min > self.target_sets_max:
            raise ValueError("target_sets_min must be <= target_sets_max")
        return self

    @model_validator(mode="after")
    def check_reps_ranges(self) -> Self:
        if self.target_reps_min > self.target_reps_max:
            raise ValueError("target_reps_min must be <= target_reps_max")
        return self
