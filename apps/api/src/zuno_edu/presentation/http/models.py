"""Reusable validation values and the approved safe Error envelope."""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StringConstraints,
)

from zuno_edu.shared.persistence import require_instant


class TransportModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True)


def _blank_to_none(value: object) -> object:
    if isinstance(value, str):
        return value.strip() or None
    return value


BoundedText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
OptionalText = Annotated[BoundedText | None, BeforeValidator(_blank_to_none)]
Instant = Annotated[datetime, AfterValidator(require_instant)]
PositiveVersion = Annotated[int, Field(strict=True, ge=1)]


class FieldError(TransportModel):
    field: BoundedText
    code: BoundedText
    message: BoundedText


class Error(TransportModel):
    code: BoundedText
    message: BoundedText
    request_id: UUID
    # Factories preserve optional-but-not-null JSON contract semantics.
    field_errors: list[FieldError] = Field(default_factory=list)
    retry_after_seconds: Annotated[int, Field(strict=True, ge=1, le=3600)] = Field(
        default_factory=lambda: 1
    )


class PageQuery(TransportModel):
    limit: Annotated[int, Field(ge=1, le=100)] = 25
    cursor: Annotated[str, StringConstraints(min_length=1, max_length=4096)] | None = None
