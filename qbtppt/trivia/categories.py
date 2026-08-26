from typing import Any

from qbreader import Category


POP_CULTURE_CATEGORY = "Pop Culture"


def category_value(category: Any) -> str:
    return category.value if hasattr(category, "value") else str(category)


def selectable_categories() -> list[Any]:
    categories = [category for category in Category if category != Category.TRASH]
    categories.append(POP_CULTURE_CATEGORY)
    return categories
