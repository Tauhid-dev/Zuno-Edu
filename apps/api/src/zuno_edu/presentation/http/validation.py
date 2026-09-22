"""Opt-in dependencies used by owning feature routers; no authorization is inferred."""

import re

from fastapi import Request

from .errors import ApiError


def require_json(request: Request) -> None:
    if (
        request.headers.get("content-type", "").partition(";")[0].strip().lower()
        != "application/json"
    ):
        raise ApiError("VALIDATION_ERROR")


def expected_version(if_match: str | None) -> int:
    if if_match is None or not re.fullmatch(r'[1-9][0-9]{0,17}|"[1-9][0-9]{0,17}"', if_match):
        raise ApiError("VALIDATION_ERROR")
    return int(if_match.strip('"'))


def first_write_version(if_match: str | None, if_none_match: str | None) -> int | None:
    if if_none_match == "*" and if_match is None:
        return None
    if if_none_match is None and if_match is not None:
        return expected_version(if_match)
    raise ApiError("VALIDATION_ERROR")
