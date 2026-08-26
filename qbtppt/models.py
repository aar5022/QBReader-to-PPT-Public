from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AppSettings:
    random_tossup_url: str
    random_bonus_url: str
    set_list_url: str
    num_packets_url: str
    packet_url: str
    deck_title: str
    deck_subtitle: str
    default_output_path: str
    manual_tossup_count: int
    manual_bonus_count: int
    include_bonuses_default: bool
    default_source_mode: str
    min_year: int
    max_year: int
    effect_appear: int
    animate_by_first_level: int
    animate_by_word: int
    question_background_color: str
    question_text_color: str
    question_font_family: str
    question_max_font_size: int
    question_margin_left: float
    question_margin_top: float
    question_margin_right: float
    question_margin_bottom: float
    question_internal_margin: float
    question_paragraph_spacing_after: int
    question_line_spacing: float


@dataclass(frozen=True)
class TossupData:
    question_sanitized: str
    answer_sanitized: str
    category: str | None = None
    subcategory: str | None = None

    @classmethod
    def from_api_json(cls, data: dict[str, Any]) -> "TossupData":
        return cls(
            question_sanitized=data["question_sanitized"],
            answer_sanitized=data["answer_sanitized"],
            category=data.get("category"),
            subcategory=data.get("subcategory"),
        )


@dataclass(frozen=True)
class BonusData:
    leadin_sanitized: str
    parts_sanitized: tuple[str, ...]
    answers_sanitized: tuple[str, ...]
    values: tuple[int, ...] | None = None
    category: str | None = None
    subcategory: str | None = None

    @classmethod
    def from_api_json(cls, data: dict[str, Any]) -> "BonusData":
        return cls(
            leadin_sanitized=data["leadin_sanitized"],
            parts_sanitized=tuple(data["parts_sanitized"]),
            answers_sanitized=tuple(data["answers_sanitized"]),
            values=tuple(data["values"]) if data.get("values") else None,
            category=data.get("category"),
            subcategory=data.get("subcategory"),
        )


@dataclass(frozen=True)
class SelectionOptions:
    source_mode: str
    difficulties: list[int]
    min_year: int
    max_year: int
    distribution: str
    categories: list[Any]
    tossup_count: int
    include_bonuses: bool
    bonus_count: int
    set_name: str | None = None
    packet_number: int | None = None


@dataclass(frozen=True)
class PacketSelection:
    set_name: str
    packet_number: int
