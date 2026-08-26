from typing import Any

from qbreader import Category

from qbtppt.trivia.categories import POP_CULTURE_CATEGORY


NO_DISTRIBUTION = "None"
NAQT_DISTRIBUTION = "NAQT-distro"
ACF_DISTRIBUTION = "ACF-distro"
JUST_TRASH = "Just trash"
RANDOM_SOURCE_MODE = "Random questions"
PACKET_SOURCE_MODE = "Select existing packet"
SOURCE_MODES = [RANDOM_SOURCE_MODE, PACKET_SOURCE_MODE]
DISTRIBUTIONS = [NAQT_DISTRIBUTION, ACF_DISTRIBUTION, JUST_TRASH, NO_DISTRIBUTION]

DistributionBucket = tuple[int, list[Any]]


def get_distribution_buckets(distribution: str, manual_tossup_count: int) -> tuple[int, list[DistributionBucket] | None]:
    common_final_bucket = [
        Category.GEOGRAPHY,
        Category.CURRENT_EVENTS,
        Category.OTHER_ACADEMIC,
        POP_CULTURE_CATEGORY,
    ]

    if distribution == NAQT_DISTRIBUTION:
        return 24, [
            (4, [Category.LITERATURE]),
            (5, [Category.HISTORY]),
            (4, [Category.SCIENCE]),
            (3, [Category.FINE_ARTS]),
            (1, [Category.RELIGION, Category.MYTHOLOGY]),
            (2, [Category.SOCIAL_SCIENCE, Category.PHILOSOPHY]),
            (5, common_final_bucket),
        ]

    if distribution == ACF_DISTRIBUTION:
        return 20, [
            (4, [Category.LITERATURE]),
            (4, [Category.HISTORY]),
            (4, [Category.SCIENCE]),
            (3, [Category.FINE_ARTS]),
            (2, [Category.RELIGION, Category.MYTHOLOGY]),
            (2, [Category.SOCIAL_SCIENCE, Category.PHILOSOPHY]),
            (1, common_final_bucket),
        ]

    if distribution == JUST_TRASH:
        return 20, [
            (20, [POP_CULTURE_CATEGORY])
        ]

    return manual_tossup_count, None
