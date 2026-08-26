from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from admirable.domain.exceptions import ValidationError

_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class Slug:
    value: str

    def __post_init__(self) -> None:
        if not _SLUG_PATTERN.match(self.value):
            raise ValidationError(f"Invalid slug: {self.value!r}")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_text(cls, text: str) -> Slug:
        """ASCII-fold + kebab-case, equivalent to Laravel's `Str::slug`.

        Only used for newly created records — existing rows keep their
        original slug verbatim on migration, so any divergence from
        `Str::slug` never touches already-published URLs.
        """
        # Đ/đ is a stroke letter, not a combining diacritic — NFKD does not
        # decompose it, so it must be mapped explicitly or it gets dropped.
        text = text.replace("Đ", "D").replace("đ", "d")
        normalized = unicodedata.normalize("NFKD", text)
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
        slug = _NON_ALNUM.sub("-", ascii_text).strip("-")
        return cls(slug or "n-a")
