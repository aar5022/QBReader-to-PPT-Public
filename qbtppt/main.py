import random

from qbtppt.api.qbreader import num_packets, packet_questions, random_bonuses, random_tossups, set_list
from qbtppt.gui.selectors import collect_selection_options, select_existing_packet, select_source_mode
from qbtppt.models import AppSettings, BonusData, SelectionOptions, TossupData
from qbtppt.ppt.generator import add_reveal_animations, build_powerpoint
from qbtppt.settings import load_settings
from qbtppt.trivia.distributions import PACKET_SOURCE_MODE, get_distribution_buckets


def fetch_tossups(settings: AppSettings, options: SelectionOptions) -> list[TossupData]:
    _, distribution_buckets = get_distribution_buckets(options.distribution, settings.manual_tossup_count)
    if not distribution_buckets:
        return list(
            random_tossups(
                random_tossup_url=settings.random_tossup_url,
                difficulties=options.difficulties,
                categories=options.categories,
                number=options.tossup_count,
                min_year=options.min_year,
                max_year=options.max_year,
            )
        )

    tossups = []
    for bucket_size, bucket_categories in distribution_buckets:
        tossups.extend(
            random_tossups(
                random_tossup_url=settings.random_tossup_url,
                difficulties=options.difficulties,
                categories=bucket_categories,
                number=bucket_size,
                min_year=options.min_year,
                max_year=options.max_year,
            )
        )
    random.shuffle(tossups)
    return tossups


def fetch_bonuses(settings: AppSettings, options: SelectionOptions) -> list[BonusData]:
    if not options.include_bonuses:
        return []

    _, distribution_buckets = get_distribution_buckets(options.distribution, settings.manual_bonus_count)
    if not distribution_buckets:
        return list(
            random_bonuses(
                random_bonus_url=settings.random_bonus_url,
                difficulties=options.difficulties,
                categories=options.categories,
                number=options.bonus_count,
                min_year=options.min_year,
                max_year=options.max_year,
            )
        )

    bonuses = []
    for bucket_size, bucket_categories in distribution_buckets:
        bonuses.extend(
            random_bonuses(
                random_bonus_url=settings.random_bonus_url,
                difficulties=options.difficulties,
                categories=bucket_categories,
                number=bucket_size,
                min_year=options.min_year,
                max_year=options.max_year,
            )
        )
    random.shuffle(bonuses)
    return bonuses


def load_existing_packet(settings: AppSettings) -> tuple[list[TossupData], list[BonusData], SelectionOptions]:
    available_sets = set_list(set_list_url=settings.set_list_url)
    packet_selection = select_existing_packet(
        available_sets,
        lambda set_name: num_packets(num_packets_url=settings.num_packets_url, set_name=set_name),
    )
    tossups, bonuses = packet_questions(
        packet_url=settings.packet_url,
        set_name=packet_selection.set_name,
        packet_number=packet_selection.packet_number,
    )
    options = SelectionOptions(
        source_mode=PACKET_SOURCE_MODE,
        difficulties=[],
        min_year=0,
        max_year=0,
        distribution="Existing packet",
        categories=[],
        tossup_count=len(tossups),
        include_bonuses=True,
        bonus_count=len(bonuses),
        set_name=packet_selection.set_name,
        packet_number=packet_selection.packet_number,
    )
    return tossups, bonuses, options


def main() -> None:
    settings = load_settings()
    source_mode = select_source_mode(settings.default_source_mode)
    if source_mode == PACKET_SOURCE_MODE:
        tossups, bonuses, options = load_existing_packet(settings)
    else:
        options = collect_selection_options(settings)
        tossups = fetch_tossups(settings, options)
        bonuses = fetch_bonuses(settings, options)
    output_path = build_powerpoint(tossups, bonuses, options, settings)

    try:
        add_reveal_animations(output_path, settings)
        print(f"File saved to {output_path} with reveal animations")
    except Exception as exc:
        print(f"File saved to {output_path}, but reveal animations could not be added: {exc}")
