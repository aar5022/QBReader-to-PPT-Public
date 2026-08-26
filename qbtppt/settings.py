import json
from pathlib import Path

from qbtppt.models import AppSettings


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "defaults.json"


def load_settings(config_path: Path = DEFAULT_CONFIG_PATH) -> AppSettings:
    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    api = config["api"]
    generation = config["generation"]
    powerpoint = config["powerpoint"]

    return AppSettings(
        random_tossup_url=api["random_tossup_url"],
        random_bonus_url=api["random_bonus_url"],
        set_list_url=api["set_list_url"],
        num_packets_url=api["num_packets_url"],
        packet_url=api["packet_url"],
        deck_title=generation["deck_title"],
        deck_subtitle=generation["deck_subtitle"],
        default_output_path=generation["default_output_path"],
        manual_tossup_count=generation["manual_tossup_count"],
        manual_bonus_count=generation["manual_bonus_count"],
        include_bonuses_default=generation["include_bonuses_default"],
        default_source_mode=generation["default_source_mode"],
        min_year=generation["min_year"],
        max_year=generation["max_year"],
        effect_appear=powerpoint["effect_appear"],
        animate_by_first_level=powerpoint["animate_by_first_level"],
        animate_by_word=powerpoint["animate_by_word"],
        question_background_color=powerpoint["question_background_color"],
        question_text_color=powerpoint["question_text_color"],
        question_font_family=powerpoint["question_font_family"],
        question_max_font_size=powerpoint["question_max_font_size"],
        question_margin_left=powerpoint["question_margin_left"],
        question_margin_top=powerpoint["question_margin_top"],
        question_margin_right=powerpoint["question_margin_right"],
        question_margin_bottom=powerpoint["question_margin_bottom"],
        question_internal_margin=powerpoint["question_internal_margin"],
        question_paragraph_spacing_after=powerpoint["question_paragraph_spacing_after"],
        question_line_spacing=powerpoint["question_line_spacing"],
    )
